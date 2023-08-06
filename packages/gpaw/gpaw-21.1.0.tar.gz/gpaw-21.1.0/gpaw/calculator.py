"""This module defines an ASE-calculator interface to GPAW.

The central object that glues everything together.
"""

import warnings
from typing import Any, Dict, List

import numpy as np
from ase import Atoms
from ase.calculators.calculator import Calculator, kpts2ndarray
from ase.dft.bandgap import bandgap
from ase.units import Bohr, Ha
from ase.utils import plural
from ase.utils.timing import Timer

import gpaw
import gpaw.mpi as mpi
import gpaw.wavefunctions.pw as pw
from gpaw import memory_estimate_depth
from gpaw.band_descriptor import BandDescriptor
from gpaw.density import RealSpaceDensity
from gpaw.dos import DOSCalculator
from gpaw.eigensolvers import get_eigensolver
from gpaw.external import PointChargePotential
from gpaw.forces import calculate_forces
from gpaw.grid_descriptor import GridDescriptor
from gpaw.hamiltonian import RealSpaceHamiltonian
from gpaw.io import Reader, Writer
from gpaw.io.logger import GPAWLogger
from gpaw.jellium import create_background_charge
from gpaw.kohnsham_layouts import get_KohnSham_layouts
from gpaw.kpt_descriptor import KPointDescriptor
from gpaw.kpt_refine import create_kpoint_descriptor_with_refinement
from gpaw.matrix import suggest_blocking
from gpaw.occupations import ParallelLayout, create_occ_calc
from gpaw.output import (print_cell, print_parallelization_details,
                         print_positions)
from gpaw.scf import SCFLoop
from gpaw.setup import Setups
from gpaw.stress import calculate_stress
from gpaw.symmetry import Symmetry
from gpaw.utilities import check_atoms_too_close
from gpaw.utilities.gpts import get_number_of_grid_points
from gpaw.utilities.grid import GridRedistributor
from gpaw.utilities.memory import MemNode, maxrss
from gpaw.utilities.partition import AtomPartition
from gpaw.wavefunctions.mode import create_wave_function_mode
from gpaw.xc import XC
from gpaw.xc.sic import SIC


class GPAW(Calculator):
    """This is the ASE-calculator frontend for doing a GPAW calculation."""

    implemented_properties = ['energy', 'forces', 'stress', 'dipole',
                              'magmom', 'magmoms']

    default_parameters: Dict[str, Any] = {
        'mode': 'fd',
        'xc': 'LDA',
        'occupations': None,
        'poissonsolver': None,
        'h': None,  # Angstrom
        'gpts': None,
        'kpts': [(0.0, 0.0, 0.0)],
        'nbands': None,
        'charge': 0,
        'setups': {},
        'basis': {},
        'spinpol': None,
        'filter': None,
        'mixer': None,
        'eigensolver': None,
        'background_charge': None,
        'experimental': {'reuse_wfs_method': 'paw',
                         'niter_fixdensity': 0,
                         'magmoms': None,
                         'soc': None,
                         'kpt_refine': None},
        'external': None,
        'random': False,
        'hund': False,
        'maxiter': 333,
        'idiotproof': True,
        'symmetry': {'point_group': True,
                     'time_reversal': True,
                     'symmorphic': True,
                     'tolerance': 1e-7,
                     'do_not_symmetrize_the_density': None},  # deprecated
        'convergence': {'energy': 0.0005,  # eV / electron
                        'density': 1.0e-4,
                        'eigenstates': 4.0e-8,  # eV^2
                        'bands': 'occupied',
                        'forces': np.inf},  # eV / Ang
        'verbose': 0,
        'fixdensity': False,  # deprecated
        'dtype': None}  # deprecated

    default_parallel: Dict[str, Any] = {
        'kpt': None,
        'domain': gpaw.parsize_domain,
        'band': gpaw.parsize_bands,
        'order': 'kdb',
        'stridebands': False,
        'augment_grids': gpaw.augment_grids,
        'sl_auto': False,
        'sl_default': None,
        'sl_diagonalize': None,
        'sl_inverse_cholesky': None,
        'sl_lcao': None,
        'sl_lrtddft': None,
        'use_elpa': False,
        'elpasolver': '2stage',
        'buffer_size': gpaw.buffer_size}

    def __init__(self,
                 restart=None,
                 *,
                 label=None,
                 timer=None,
                 communicator=None,
                 txt='?',
                 parallel=None,
                 **kwargs):

        if txt == '?':
            txt = '-' if restart is None else None

        self.parallel = dict(self.default_parallel)
        if parallel:
            for key in parallel:
                if key not in self.default_parallel:
                    allowed = ', '.join(list(self.default_parallel.keys()))
                    raise TypeError('Unexpected keyword "{}" in "parallel" '
                                    'dictionary.  Must be one of: {}'
                                    .format(key, allowed))
            self.parallel.update(parallel)

        if timer is None:
            self.timer = Timer()
        else:
            self.timer = timer

        self.scf = None
        self.wfs = None
        self.density = None
        self.hamiltonian = None
        self.spos_ac = None  # XXX store this in some better way.

        self.observers = []  # XXX move to self.scf
        self.initialized = False

        self.world = communicator
        if self.world is None:
            self.world = mpi.world
        elif not hasattr(self.world, 'new_communicator'):
            self.world = mpi.world.new_communicator(np.asarray(self.world))

        self.log = GPAWLogger(world=self.world)
        self.log.fd = txt

        self.reader = None

        Calculator.__init__(self, restart, label=label, **kwargs)

    def fixed_density(self, *,
                      update_fermi_level: bool = False,
                      communicator=None,
                      txt='-',
                      parallel: Dict[str, Any] = None,
                      **kwargs) -> 'GPAW':
        """Create new calculator and do SCF calculation with fixed density.

        Returns a new GPAW object fully converged.

        Useful for band-structure calculations.  Given a ground-state
        calculation, ``gs_calc``, one can do::

            bs_calc = gs_calc.fixed_density(kpts=<path>,
                                            symmetry='off')
            bs = bs_calc.get_band_structure()
        """
        assert not update_fermi_level  # for now ...

        for key in kwargs:
            if key not in {'nbands', 'occupations', 'poissonsolver', 'kpts',
                           'eigensolver', 'random', 'maxiter', 'basis',
                           'symmetry', 'convergence', 'verbose'}:
                raise TypeError(f'{key:!r} is an invalid keyword argument')

        params = self.parameters.copy()
        params.update(kwargs)
        calc = GPAW(communicator=communicator,
                    txt=txt,
                    parallel=parallel,
                    **params)
        calc.initialize(self.atoms)
        calc.density.initialize_from_other_density(self.density,
                                                   calc.wfs.kptband_comm)
        calc.density.fixed = True
        calc.wfs.fermi_levels = self.wfs.fermi_levels
        if calc.hamiltonian.xc.type == 'GLLB':
            new_response = calc.hamiltonian.xc.response
            old_response = self.hamiltonian.xc.response
            new_response.initialize_from_other_response(old_response)
            new_response.fix_potential = True
        calc.calculate(system_changes=[])
        return calc

    def __del__(self):
        # Write timings and close reader if necessary.
        # If we crashed in the constructor (e.g. a bad keyword), we may not
        # have the normally expected attributes:
        if hasattr(self, 'timer') and not self.log.fd.closed:
            self.timer.write(self.log.fd)

        if hasattr(self, 'reader') and self.reader is not None:
            self.reader.close()

    def write(self, filename, mode=''):
        self.log(f'Writing to {filename} (mode={mode!r})\n')
        writer = Writer(filename, self.world)
        self._write(writer, mode)
        writer.close()
        self.world.barrier()

    def _write(self, writer, mode):
        from ase.io.trajectory import write_atoms
        writer.write(version=3, gpaw_version=gpaw.__version__,
                     ha=Ha, bohr=Bohr)

        write_atoms(writer.child('atoms'), self.atoms)
        writer.child('results').write(**self.results)
        writer.child('parameters').write(**self.todict())

        self.density.write(writer.child('density'))
        self.hamiltonian.write(writer.child('hamiltonian'))
        # self.occupations.write(writer.child('occupations'))
        self.scf.write(writer.child('scf'))
        self.wfs.write(writer.child('wave_functions'), mode == 'all')

        return writer

    def _set_atoms(self, atoms):
        check_atoms_too_close(atoms)
        self.atoms = atoms
        # GPAW works in terms of the scaled positions.  We want to
        # extract the scaled positions in only one place, and that is
        # here.  No other place may recalculate them, or we might end up
        # with rounding errors and inconsistencies.
        self.spos_ac = atoms.get_scaled_positions() % 1.0

    def read(self, filename):
        from ase.io.trajectory import read_atoms
        self.log('Reading from {}'.format(filename))

        self.reader = reader = Reader(filename)

        atoms = read_atoms(reader.atoms)
        self._set_atoms(atoms)

        res = reader.results
        self.results = dict((key, res.get(key)) for key in res.keys())
        if self.results:
            self.log('Read {}'.format(', '.join(sorted(self.results))))

        self.log('Reading input parameters:')
        # XXX param
        self.parameters = self.get_default_parameters()
        dct = {}
        for key, value in reader.parameters.asdict().items():
            if key == 'txt':
                continue  # old gpw-files may have this
            if (isinstance(value, dict) and
                isinstance(self.parameters[key], dict)):
                self.parameters[key].update(value)
            else:
                self.parameters[key] = value
            dct[key] = self.parameters[key]

        self.log.print_dict(dct)
        self.log()

        self.initialize(reading=True)

        self.density.read(reader)
        self.hamiltonian.read(reader)
        self.scf.read(reader)
        self.wfs.read(reader)

        # We need to do this in a better way:  XXX
        from gpaw.utilities.partition import AtomPartition
        atom_partition = AtomPartition(self.wfs.gd.comm,
                                       np.zeros(len(self.atoms), dtype=int))
        self.density.atom_partition = atom_partition
        self.hamiltonian.atom_partition = atom_partition
        rank_a = self.density.gd.get_ranks_from_positions(self.spos_ac)
        new_atom_partition = AtomPartition(self.density.gd.comm, rank_a)
        for obj in [self.density, self.hamiltonian]:
            obj.set_positions_without_ruining_everything(self.spos_ac,
                                                         new_atom_partition)
        if new_atom_partition != atom_partition:
            for kpt in self.wfs.kpt_u:
                kpt.projections = kpt.projections.redist(new_atom_partition)
        self.wfs.atom_partition = new_atom_partition

        self.hamiltonian.xc.read(reader)

        return reader

    def check_state(self, atoms, tol=1e-12):
        system_changes = Calculator.check_state(self, atoms, tol)
        if 'positions' not in system_changes:
            if self.hamiltonian:
                if self.hamiltonian.vext:
                    if self.hamiltonian.vext.vext_g is None:
                        # QMMM atoms have moved:
                        system_changes.append('positions')
        return system_changes

    def calculate(self, atoms=None, properties=['energy'],
                  system_changes=['cell']):
        for _ in self.icalculate(atoms, properties, system_changes):
            pass

    def icalculate(self, atoms=None, properties=['energy'],
                   system_changes=['cell']):
        """Calculate things."""

        Calculator.calculate(self, atoms)
        atoms = self.atoms

        if system_changes:
            self.log('System changes:', ', '.join(system_changes), '\n')
            if system_changes == ['positions']:
                # Only positions have changed:
                self.density.reset()
            else:
                # Drastic changes:
                self.wfs = None
                self.density = None
                self.hamiltonian = None
                self.scf = None
                self.initialize(atoms)

            self.set_positions(atoms)

        if not self.initialized:
            self.initialize(atoms)
            self.set_positions(atoms)

        if not (self.wfs.positions_set and self.hamiltonian.positions_set):
            self.set_positions(atoms)

        yield

        if not self.scf.converged:
            print_cell(self.wfs.gd, self.atoms.pbc, self.log)

            with self.timer('SCF-cycle'):
                yield from self.scf.irun(
                    self.wfs, self.hamiltonian,
                    self.density,
                    self.log, self.call_observers)

            self.log('\nConverged after {} iterations.\n'
                     .format(self.scf.niter))

            e_free = self.hamiltonian.e_total_free
            e_extrapolated = self.hamiltonian.e_total_extrapolated
            self.results['energy'] = e_extrapolated * Ha
            self.results['free_energy'] = e_free * Ha

            dipole_v = self.density.calculate_dipole_moment() * Bohr
            self.log('Dipole moment: ({:.6f}, {:.6f}, {:.6f}) |e|*Ang\n'
                     .format(*dipole_v))
            self.results['dipole'] = dipole_v

            if self.wfs.nspins == 2 or not self.density.collinear:
                totmom_v, magmom_av = self.density.estimate_magnetic_moments()
                self.log('Total magnetic moment: ({:.6f}, {:.6f}, {:.6f})'
                         .format(*totmom_v))
                self.log('Local magnetic moments:')
                symbols = self.atoms.get_chemical_symbols()
                for a, mom_v in enumerate(magmom_av):
                    self.log('{:4} {:2} ({:9.6f}, {:9.6f}, {:9.6f})'
                             .format(a, symbols[a], *mom_v))
                self.log()
                self.results['magmom'] = totmom_v[2]
                self.results['magmoms'] = magmom_av[:, 2].copy()
            else:
                self.results['magmom'] = 0.0
                self.results['magmoms'] = np.zeros(len(self.atoms))

            self.summary()

            self.call_observers(self.scf.niter, final=True)

        if 'forces' in properties:
            with self.timer('Forces'):
                F_av = calculate_forces(self.wfs, self.density,
                                        self.hamiltonian, self.log)
                self.results['forces'] = F_av * (Ha / Bohr)

        if 'stress' in properties:
            with self.timer('Stress'):
                try:
                    stress = calculate_stress(self).flat[[0, 4, 8, 5, 2, 1]]
                except NotImplementedError:
                    # Our ASE Calculator base class will raise
                    # PropertyNotImplementedError for us.
                    pass
                else:
                    self.results['stress'] = stress * (Ha / Bohr**3)

    def summary(self):
        self.hamiltonian.summary(self.wfs, self.log)
        self.density.summary(self.atoms, self.results.get('magmom', 0.0),
                             self.log)
        self.wfs.summary(self.log)
        if len(self.wfs.fermi_levels) == 1:
            try:
                bandgap(self,
                        output=self.log.fd,
                        efermi=self.wfs.fermi_level * Ha)
            except ValueError:
                pass
        self.log.fd.flush()

    def set(self, **kwargs):
        """Change parameters for calculator.

        Examples::

            calc.set(xc='PBE')
            calc.set(nbands=20, kpts=(4, 1, 1))
        """

        # Verify that keys are consistent with default ones.
        for key in kwargs:
            if key != 'txt' and key not in self.default_parameters:
                raise TypeError('Unknown GPAW parameter: {}'.format(key))

            if key in ['convergence', 'symmetry',
                       'experimental'] and isinstance(kwargs[key], dict):
                # For values that are dictionaries, verify subkeys, too.
                default_dict = self.default_parameters[key]
                for subkey in kwargs[key]:
                    if subkey not in default_dict:
                        allowed = ', '.join(list(default_dict.keys()))
                        raise TypeError('Unknown subkeyword "{}" of keyword '
                                        '"{}".  Must be one of: {}'
                                        .format(subkey, key, allowed))

        changed_parameters = Calculator.set(self, **kwargs)

        for key in ['setups', 'basis']:
            if key in changed_parameters:
                dct = changed_parameters[key]
                if isinstance(dct, dict) and None in dct:
                    dct['default'] = dct.pop(None)
                    warnings.warn('Please use {key}={dct}'
                                  .format(key=key, dct=dct))

        # We need to handle txt early in order to get logging up and running:
        if 'txt' in changed_parameters:
            self.log.fd = changed_parameters.pop('txt')

        if not changed_parameters:
            return {}

        self.initialized = False
        self.scf = None
        self.results = {}

        self.log('Input parameters:')
        self.log.print_dict(changed_parameters)
        self.log()

        for key in changed_parameters:
            if key in ['eigensolver', 'convergence'] and self.wfs:
                self.wfs.set_eigensolver(None)

            if key in ['mixer', 'verbose', 'txt', 'hund', 'random',
                       'eigensolver', 'idiotproof']:
                continue

            if key in ['convergence', 'fixdensity', 'maxiter']:
                continue

            # Check nested arguments
            if key in ['experimental']:
                changed_parameters2 = changed_parameters[key]
                for key2 in changed_parameters2:
                    if key2 in ['kpt_refine', 'magmoms', 'soc']:
                        self.wfs = None
                    elif key2 in ['reuse_wfs_method', 'niter_fixdensity']:
                        continue
                    else:
                        raise TypeError('Unknown keyword argument:', key2)
                continue

            # More drastic changes:
            if self.wfs:
                self.wfs.set_orthonormalized(False)
            if key in ['xc', 'poissonsolver']:
                self.hamiltonian = None
            elif key in ['occupations', 'width']:
                pass
            elif key in ['external', 'charge', 'background_charge']:
                self.hamiltonian = None
                self.density = None
                self.wfs = None
            elif key in ['kpts', 'nbands', 'symmetry']:
                self.wfs = None
            elif key in ['h', 'gpts', 'setups', 'spinpol', 'dtype', 'mode']:
                self.density = None
                self.hamiltonian = None
                self.wfs = None
            elif key in ['basis']:
                self.wfs = None
            else:
                raise TypeError('Unknown keyword argument: "%s"' % key)

    def initialize_positions(self, atoms=None):
        """Update the positions of the atoms."""
        self.log('Initializing position-dependent things.\n')
        if atoms is None:
            atoms = self.atoms
        else:
            atoms = atoms.copy()
            self._set_atoms(atoms)

        mpi.synchronize_atoms(atoms, self.world)

        rank_a = self.wfs.gd.get_ranks_from_positions(self.spos_ac)
        atom_partition = AtomPartition(self.wfs.gd.comm, rank_a, name='gd')
        self.wfs.set_positions(self.spos_ac, atom_partition)
        self.density.set_positions(self.spos_ac, atom_partition)
        self.hamiltonian.set_positions(self.spos_ac, atom_partition)

    def set_positions(self, atoms=None):
        """Update the positions of the atoms and initialize wave functions."""
        self.initialize_positions(atoms)

        nlcao, nrand = self.wfs.initialize(self.density, self.hamiltonian,
                                           self.spos_ac)
        if nlcao + nrand:
            self.log('Creating initial wave functions:')
            if nlcao:
                self.log(' ', plural(nlcao, 'band'), 'from LCAO basis set')
            if nrand:
                self.log(' ', plural(nrand, 'band'), 'from random numbers')
            self.log()

        self.wfs.eigensolver.reset()
        self.scf.reset()
        print_positions(self.atoms, self.log, self.density.magmom_av)

    def initialize(self, atoms=None, reading=False):
        """Inexpensive initialization."""

        self.log('Initialize ...\n')

        if atoms is None:
            atoms = self.atoms
        else:
            atoms = atoms.copy()
            self._set_atoms(atoms)

        par = self.parameters

        natoms = len(atoms)

        cell_cv = atoms.get_cell() / Bohr
        number_of_lattice_vectors = cell_cv.any(axis=1).sum()
        if number_of_lattice_vectors < 3:
            raise ValueError(
                'GPAW requires 3 lattice vectors.  Your system has {}.'
                .format(number_of_lattice_vectors))

        pbc_c = atoms.get_pbc()
        assert len(pbc_c) == 3
        magmom_a = atoms.get_initial_magnetic_moments()

        if par.experimental.get('magmoms') is not None:
            magmom_av = np.array(par.experimental['magmoms'], float)
            collinear = False
        else:
            magmom_av = np.zeros((natoms, 3))
            magmom_av[:, 2] = magmom_a
            collinear = True

        mpi.synchronize_atoms(atoms, self.world)

        # Generate new xc functional only when it is reset by set
        # XXX sounds like this should use the _changed_keywords dictionary.
        if self.hamiltonian is None or self.hamiltonian.xc is None:
            if isinstance(par.xc, (str, dict)):
                xc = XC(par.xc, collinear=collinear, atoms=atoms)
            else:
                xc = par.xc
        else:
            xc = self.hamiltonian.xc

        if par.fixdensity:
            warnings.warn(
                'The fixdensity keyword has been deprecated. '
                'Please use the GPAW.fixed_density() method instead.',
                DeprecationWarning)

        mode = par.mode
        if isinstance(mode, str):
            mode = {'name': mode}
        if isinstance(mode, dict):
            mode = create_wave_function_mode(**mode)

        if par.dtype == complex:
            warnings.warn('Use mode={}(..., force_complex_dtype=True) '
                          'instead of dtype=complex'.format(mode.name.upper()))
            mode.force_complex_dtype = True
            del par['dtype']
            par.mode = mode

        if xc.orbital_dependent and mode.name == 'lcao':
            raise ValueError('LCAO mode does not support '
                             'orbital-dependent XC functionals.')

        realspace = (mode.name != 'pw' and mode.interpolation != 'fft')

        self.create_setups(mode, xc)

        if not realspace:
            pbc_c = np.ones(3, bool)

        if par.hund:
            if natoms != 1:
                raise ValueError('hund=True arg only valid for single atoms!')
            spinpol = True
            magmom_av[0, 2] = self.setups[0].get_hunds_rule_moment(par.charge)

        if collinear:
            magnetic = magmom_av.any()

            spinpol = par.spinpol
            if spinpol is None:
                spinpol = magnetic
            elif magnetic and not spinpol:
                raise ValueError('Non-zero initial magnetic moment for a ' +
                                 'spin-paired calculation!')
            nspins = 1 + int(spinpol)

            if spinpol:
                self.log('Spin-polarized calculation.')
                self.log('Magnetic moment: {:.6f}\n'.format(magmom_av.sum()))
            else:
                self.log('Spin-paired calculation\n')
        else:
            nspins = 1
            self.log('Non-collinear calculation.')
            self.log('Magnetic moment: ({:.6f}, {:.6f}, {:.6f})\n'
                     .format(*magmom_av.sum(0)))

        self.create_symmetry(magmom_av, cell_cv, reading)

        if par.gpts is not None:
            if par.h is not None:
                raise ValueError("""You can't use both "gpts" and "h"!""")
            N_c = np.array(par.gpts)
            h = None
        else:
            h = par.h
            if h is not None:
                h /= Bohr
            if h is None and reading:
                shape = self.reader.density.proxy('density').shape[-3:]
                N_c = 1 - pbc_c + shape
            elif h is None and self.density is not None:
                N_c = self.density.gd.N_c
            else:
                N_c = get_number_of_grid_points(cell_cv, h, mode, realspace,
                                                self.symmetry, self.log)

        self.setups.set_symmetry(self.symmetry)

        if isinstance(par.background_charge, dict):
            background = create_background_charge(**par.background_charge)
        else:
            background = par.background_charge

        nao = self.setups.nao
        nvalence = self.setups.nvalence - par.charge
        if par.background_charge is not None:
            nvalence += background.charge

        M = np.linalg.norm(magmom_av.sum(0))

        nbands = par.nbands

        orbital_free = any(setup.orbital_free for setup in self.setups)
        if orbital_free:
            nbands = 1

        if isinstance(nbands, str):
            if nbands == 'nao':
                nbands = nao
            elif nbands[-1] == '%':
                basebands = (nvalence + M) / 2
                nbands = int(np.ceil(float(nbands[:-1]) / 100 * basebands))
            else:
                raise ValueError('Integer expected: Only use a string '
                                 'if giving a percentage of occupied bands')

        if nbands is None:
            # Number of bound partial waves:
            nbandsmax = sum(setup.get_default_nbands()
                            for setup in self.setups)
            nbands = int(np.ceil((1.2 * (nvalence + M) / 2))) + 4
            if nbands > nbandsmax:
                nbands = nbandsmax
            if mode.name == 'lcao' and nbands > nao:
                nbands = nao
        elif nbands <= 0:
            nbands = max(1, int(nvalence + M + 0.5) // 2 + (-nbands))

        if nbands > nao and mode.name == 'lcao':
            raise ValueError('Too many bands for LCAO calculation: '
                             '%d bands and only %d atomic orbitals!' %
                             (nbands, nao))

        if nvalence < 0:
            raise ValueError(
                'Charge %f is not possible - not enough valence electrons' %
                par.charge)

        if nvalence > 2 * nbands and not orbital_free:
            raise ValueError('Too few bands!  Electrons: %f, bands: %d'
                             % (nvalence, nbands))

        if self.scf is None:
            self.create_scf(nvalence, mode)

        if not collinear:
            nbands *= 2

        if not self.wfs:
            self.create_wave_functions(mode, realspace,
                                       nspins, collinear, nbands, nao,
                                       nvalence, self.setups,
                                       cell_cv, pbc_c, N_c)
        else:
            self.wfs.set_setups(self.setups)

        occ = self.create_occupations(cell_cv, magmom_av[:, 2].sum(),
                                      orbital_free)
        self.wfs.occupations = occ

        if not self.wfs.eigensolver:
            self.create_eigensolver(xc, nbands, mode)

        if self.density is None and not reading:
            assert not par.fixdensity, 'No density to fix!'

        olddens = None
        if (self.density is not None and
            (self.density.gd.parsize_c != self.wfs.gd.parsize_c).any()):
            # Domain decomposition has changed, so we need to
            # reinitialize density and hamiltonian:
            if par.fixdensity:
                olddens = self.density

            self.density = None
            self.hamiltonian = None

        if self.density is None:
            self.create_density(realspace, mode, background, h)

        # XXXXXXXXXX if setups change, then setups.core_charge may change.
        # But that parameter was supplied in Density constructor!
        # This surely is a bug!
        self.density.initialize(self.setups, self.timer,
                                magmom_av, par.hund)
        self.density.set_mixer(par.mixer)
        if self.density.mixer.driver.name == 'dummy' or par.fixdensity:
            self.log('No density mixing\n')
        else:
            self.log(self.density.mixer, '\n')
        self.density.fixed = par.fixdensity
        self.density.log = self.log

        if olddens is not None:
            self.density.initialize_from_other_density(olddens,
                                                       self.wfs.kptband_comm)

        if self.hamiltonian is None:
            self.create_hamiltonian(realspace, mode, xc)

        xc.initialize(self.density, self.hamiltonian, self.wfs)

        description = xc.get_description()
        if description is not None:
            self.log('XC parameters: {}\n'
                     .format('\n  '.join(description.splitlines())))

        if xc.type == 'GLLB' and olddens is not None:
            xc.heeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeelp(olddens)

        self.print_memory_estimate(maxdepth=memory_estimate_depth + 1)

        print_parallelization_details(self.wfs, self.hamiltonian, self.log)

        self.log('Number of atoms:', natoms)
        self.log('Number of atomic orbitals:', self.wfs.setups.nao)
        self.log('Number of bands in calculation:', self.wfs.bd.nbands)
        self.log('Number of valence electrons:', self.wfs.nvalence)

        n = par.convergence.get('bands', 'occupied')
        if isinstance(n, int) and n < 0:
            n += self.wfs.bd.nbands
        self.log('Bands to converge:', n)

        self.log(flush=True)

        self.timer.print_info(self)

        if gpaw.dry_run:
            self.dry_run()

        if (realspace and
            self.hamiltonian.poisson.get_description() == 'FDTD+TDDFT'):
            self.hamiltonian.poisson.set_density(self.density)
            self.hamiltonian.poisson.print_messages(self.log)
            self.log.fd.flush()

        self.initialized = True
        self.log('... initialized\n')

    def create_setups(self, mode, xc):
        if self.parameters.filter is None and mode.name != 'pw':
            gamma = 1.6
            N_c = self.parameters.get('gpts')
            if N_c is None:
                h = (self.parameters.h or 0.2) / Bohr
            else:
                icell_vc = np.linalg.inv(self.atoms.cell)
                h = ((icell_vc**2).sum(0)**-0.5 / N_c).max() / Bohr

            def filter(rgd, rcut, f_r, l=0):
                gcut = np.pi / h - 2 / rcut / gamma
                ftmp = rgd.filter(f_r, rcut * gamma, gcut, l)
                f_r[:] = ftmp[:len(f_r)]
        else:
            filter = self.parameters.filter

        Z_a = self.atoms.get_atomic_numbers()
        self.setups = Setups(Z_a,
                             self.parameters.setups, self.parameters.basis,
                             xc, filter, self.world)
        self.log(self.setups)

    def create_grid_descriptor(self, N_c, cell_cv, pbc_c,
                               domain_comm, parsize_domain):
        return GridDescriptor(N_c, cell_cv, pbc_c, domain_comm,
                              parsize_domain)

    def create_occupations(self, cell_cv, magmom, orbital_free):
        dct = self.parameters.occupations

        if dct is None:
            if orbital_free:
                dct = {'name': 'orbital-free'}
            else:
                if self.atoms.pbc.any():
                    dct = {'name': 'fermi-dirac',
                           'width': 0.1}  # eV
                else:
                    dct = {'width': 0.0}
        elif not isinstance(dct, dict):
            return dct

        if self.wfs.nspins == 1:
            dct.pop('fixmagmom', None)

        occ = create_occ_calc(
            dct,
            parallel_layout=ParallelLayout(self.wfs.bd,
                                           self.wfs.kd.comm,
                                           self.wfs.gd.comm),
            fixed_magmom_value=magmom,
            rcell=np.linalg.inv(cell_cv).T,
            monkhorst_pack_size=self.wfs.kd.N_c,
            bz2ibzmap=self.wfs.kd.bz2ibz_k)

        self.log(occ)
        return occ

    def create_scf(self, nvalence, mode):
        # if mode.name == 'lcao':
        #     niter_fixdensity = 0
        # else:
        #     niter_fixdensity = 2

        nv = max(nvalence, 1)
        cc = self.parameters.convergence
        self.scf = SCFLoop(
            cc.get('eigenstates', 4.0e-8) / Ha**2 * nv,
            cc.get('energy', 0.0005) / Ha * nv,
            cc.get('density', 1.0e-4) * nv,
            cc.get('forces', np.inf) / (Ha / Bohr),
            self.parameters.maxiter,
            # XXX make sure niter_fixdensity value is *always* set from default
            # Subdictionary defaults seem to not be set when user provides
            # e.g. {}.  We should change that so it works like the ordinary
            # parameters.
            self.parameters.experimental.get('niter_fixdensity', 0),
            nv)
        self.log(self.scf)

    def create_symmetry(self, magmom_av, cell_cv, reading):
        symm = self.parameters.symmetry
        if symm == 'off':
            symm = {'point_group': False, 'time_reversal': False}

        if 'do_not_symmetrize_the_density' in symm:
            symm = symm.copy()
            dnstd = symm.pop('do_not_symmetrize_the_density')
            if dnstd is not None:
                info = 'Ignoring your "do_not_symmetrize_the_density" keyword!'
                if reading:
                    self.log(info)
                else:
                    warnings.warn(info + ' Please remove it.')

        if self.parameters.external is not None:
            symm = symm.copy()
            symm['point_group'] = False

        if reading and self.reader.version <= 1:
            symm['allow_invert_aperiodic_axes'] = False

        m_av = magmom_av.round(decimals=3)  # round off
        id_a = [id + tuple(m_v) for id, m_v in zip(self.setups.id_a, m_av)]
        self.symmetry = Symmetry(id_a, cell_cv, self.atoms.pbc, **symm)
        self.symmetry.analyze(self.spos_ac)

    def create_eigensolver(self, xc, nbands, mode):
        # Number of bands to converge:
        nbands_converge = self.parameters.convergence.get('bands', 'occupied')
        if nbands_converge == 'all':
            nbands_converge = nbands
        elif isinstance(nbands_converge, int):
            if nbands_converge < 0:
                nbands_converge += nbands
        eigensolver = get_eigensolver(self.parameters.eigensolver, mode,
                                      self.parameters.convergence)
        eigensolver.nbands_converge = nbands_converge
        # XXX Eigensolver class doesn't define an nbands_converge property

        if isinstance(xc, SIC):
            eigensolver.blocksize = 1

        self.wfs.set_eigensolver(eigensolver)

        self.log('Eigensolver\n  ', self.wfs.eigensolver, '\n')

    def create_density(self, realspace, mode, background, h):
        gd = self.wfs.gd

        big_gd = gd.new_descriptor(comm=self.world)
        # Check whether grid is too small.  8 is smallest admissible.
        # (we decide this by how difficult it is to make the tests pass)
        # (Actually it depends on stencils!  But let the user deal with it)
        N_c = big_gd.get_size_of_global_array(pad=True)
        too_small = np.any(N_c / big_gd.parsize_c < 8)
        if (self.parallel['augment_grids'] and not too_small and
            mode.name != 'pw'):
            aux_gd = big_gd
        else:
            aux_gd = gd

        redistributor = GridRedistributor(self.world,
                                          self.wfs.kptband_comm,
                                          gd, aux_gd)

        # Construct grid descriptor for fine grids for densities
        # and potentials:
        finegd = aux_gd.refine()

        kwargs = dict(
            gd=gd, finegd=finegd,
            nspins=self.wfs.nspins,
            collinear=self.wfs.collinear,
            charge=self.parameters.charge + self.wfs.setups.core_charge,
            redistributor=redistributor,
            background_charge=background)

        if realspace:
            self.density = RealSpaceDensity(stencil=mode.interpolation,
                                            **kwargs)
        else:
            if h is None:
                ecut = 2 * self.wfs.pd.ecut
            else:
                ecut = 0.5 * (np.pi / h)**2
            self.density = pw.ReciprocalSpaceDensity(ecut=ecut,
                                                     **kwargs)

        self.log(self.density, '\n')

    def create_hamiltonian(self, realspace, mode, xc):
        dens = self.density
        kwargs = dict(
            gd=dens.gd, finegd=dens.finegd,
            nspins=dens.nspins,
            collinear=dens.collinear,
            setups=dens.setups,
            timer=self.timer,
            xc=xc,
            world=self.world,
            redistributor=dens.redistributor,
            vext=self.parameters.external,
            psolver=self.parameters.poissonsolver)
        if realspace:
            self.hamiltonian = RealSpaceHamiltonian(stencil=mode.interpolation,
                                                    **kwargs)
            xc.set_grid_descriptor(self.hamiltonian.finegd)
        else:
            # This code will work if dens.redistributor uses
            # ordinary density.gd as aux_gd
            gd = dens.finegd

            xc_redist = None
            if self.parallel['augment_grids']:
                from gpaw.grid_descriptor import BadGridError
                try:
                    aux_gd = gd.new_descriptor(comm=self.world)
                except BadGridError as err:
                    import warnings
                    warnings.warn('Ignoring augment_grids: {}'
                                  .format(err))
                else:
                    bcast_comm = dens.redistributor.broadcast_comm
                    xc_redist = GridRedistributor(self.world, bcast_comm,
                                                  gd, aux_gd)

            self.hamiltonian = pw.ReciprocalSpaceHamiltonian(
                pd2=dens.pd2, pd3=dens.pd3, realpbc_c=self.atoms.pbc,
                xc_redistributor=xc_redist,
                **kwargs)
            xc.set_grid_descriptor(self.hamiltonian.xc_gd)

        self.hamiltonian.soc = self.parameters.experimental.get('soc')
        self.log(self.hamiltonian, '\n')

    def create_kpoint_descriptor(self, nspins):
        par = self.parameters

        # Zero cell vectors that are not periodic so that ASE's
        # kpts2ndarray can handle 1-d and 2-d correctly:
        atoms = Atoms(cell=self.atoms.cell * self.atoms.pbc[:, np.newaxis],
                      pbc=self.atoms.pbc)
        bzkpts_kc = kpts2ndarray(par.kpts, atoms)

        kpt_refine = par.experimental.get('kpt_refine')
        if kpt_refine is None:
            kd = KPointDescriptor(bzkpts_kc, nspins)

            self.timer.start('Set symmetry')
            kd.set_symmetry(self.atoms, self.symmetry, comm=self.world)
            self.timer.stop('Set symmetry')

        else:
            self.timer.start('Set k-point refinement')
            kd = create_kpoint_descriptor_with_refinement(
                kpt_refine,
                bzkpts_kc, nspins, self.atoms,
                self.symmetry, comm=self.world,
                timer=self.timer)
            self.timer.stop('Set k-point refinement')
            # Update quantities which might have changed, if symmetry
            # was changed
            self.symmetry = kd.symmetry
            self.setups.set_symmetry(kd.symmetry)

        self.log(kd)

        return kd

    def create_wave_functions(self, mode, realspace,
                              nspins, collinear, nbands, nao, nvalence,
                              setups, cell_cv, pbc_c, N_c):
        par = self.parameters

        kd = self.create_kpoint_descriptor(nspins)

        parallelization = mpi.Parallelization(self.world,
                                              kd.nibzkpts)

        parsize_kpt = self.parallel['kpt']
        parsize_domain = self.parallel['domain']
        parsize_bands = self.parallel['band']

        ndomains = None
        if parsize_domain is not None:
            ndomains = np.prod(parsize_domain)
        parallelization.set(kpt=parsize_kpt,
                            domain=ndomains,
                            band=parsize_bands)
        comms = parallelization.build_communicators()
        domain_comm = comms['d']
        kpt_comm = comms['k']
        band_comm = comms['b']
        kptband_comm = comms['D']
        domainband_comm = comms['K']

        self.comms = comms

        kd.set_communicator(kpt_comm)

        parstride_bands = self.parallel['stridebands']

        bd = BandDescriptor(nbands, band_comm, parstride_bands)

        # Construct grid descriptor for coarse grids for wave functions:
        gd = self.create_grid_descriptor(N_c, cell_cv, pbc_c,
                                         domain_comm, parsize_domain)

        if hasattr(self, 'time') or mode.force_complex_dtype or not collinear:
            dtype = complex
        else:
            if kd.gamma:
                dtype = float
            else:
                dtype = complex

        wfs_kwargs = dict(gd=gd, nvalence=nvalence, setups=setups,
                          bd=bd, dtype=dtype, world=self.world, kd=kd,
                          kptband_comm=kptband_comm, timer=self.timer)

        if self.parallel['sl_auto']:
            # Choose scalapack parallelization automatically

            for key, val in self.parallel.items():
                if (key.startswith('sl_') and key != 'sl_auto' and
                    val is not None):
                    raise ValueError("Cannot use 'sl_auto' together "
                                     "with '%s'" % key)

            max_scalapack_cpus = bd.comm.size * gd.comm.size
            sl_default = suggest_blocking(nbands, max_scalapack_cpus)
        else:
            sl_default = self.parallel['sl_default']

        if mode.name == 'lcao':
            assert collinear
            # Layouts used for general diagonalizer
            sl_lcao = self.parallel['sl_lcao']
            if sl_lcao is None:
                sl_lcao = sl_default

            elpasolver = None
            if self.parallel['use_elpa']:
                elpasolver = self.parallel['elpasolver']
            lcaoksl = get_KohnSham_layouts(sl_lcao, 'lcao',
                                           gd, bd, domainband_comm, dtype,
                                           nao=nao, timer=self.timer,
                                           elpasolver=elpasolver)

            self.wfs = mode(lcaoksl, **wfs_kwargs)

        elif mode.name == 'fd' or mode.name == 'pw':
            # Use (at most) all available LCAO for initialization
            lcaonbands = min(nbands, nao)

            try:
                lcaobd = BandDescriptor(lcaonbands, band_comm,
                                        parstride_bands)
            except RuntimeError:
                initksl = None
            else:
                # Layouts used for general diagonalizer
                # (LCAO initialization)
                sl_lcao = self.parallel['sl_lcao']
                if sl_lcao is None:
                    sl_lcao = sl_default
                initksl = get_KohnSham_layouts(sl_lcao, 'lcao',
                                               gd, lcaobd, domainband_comm,
                                               dtype, nao=nao,
                                               timer=self.timer)

            reuse_wfs_method = par.experimental.get('reuse_wfs_method', 'paw')
            sl = (domainband_comm,) + (self.parallel['sl_diagonalize'] or
                                       sl_default or
                                       (1, 1, None))
            self.wfs = mode(sl, initksl,
                            reuse_wfs_method=reuse_wfs_method,
                            collinear=collinear,
                            **wfs_kwargs)
        else:
            self.wfs = mode(self, collinear=collinear, **wfs_kwargs)

        self.log(self.wfs, '\n')

    def dry_run(self):
        # Can be overridden like in gpaw.atom.atompaw
        print_cell(self.wfs.gd, self.atoms.pbc, self.log)
        print_positions(self.atoms, self.log, self.density.magmom_av)
        self.log.fd.flush()

        # Write timing info now before the interpreter shuts down:
        self.__del__()

        # Disable timing output during shut-down:
        del self.timer

        raise SystemExit

    def get_atomic_electrostatic_potentials(self) -> List[float]:
        r"""Return the electrostatic potential at the atomic sites.

        Return list of energies in eV, one for each atom:

        .. math::

            Y_{00}
            \int d\mathbf{r}
            \tilde{v}_H(\mathbf{r})
            \hat{g}_{00}^a(\mathbf{r} - \mathbf{R}^a)

        """
        ham = self.hamiltonian
        dens = self.density
        self.initialize_positions()
        dens.interpolate_pseudo_density()
        dens.calculate_pseudo_charge()
        ham.update(dens)
        W_aL = ham.calculate_atomic_hamiltonians(dens)
        return np.array([W_L[0] / (4 * np.pi)**0.5 * Ha
                         for W_L in W_aL.values()])

    def linearize_to_xc(self, newxc):
        """Linearize Hamiltonian to difference XC functional.

        Used in real time TDDFT to perform calculations with various kernels.
        """
        if isinstance(newxc, str):
            newxc = XC(newxc)
        self.log('Linearizing xc-hamiltonian to ' + str(newxc))
        newxc.initialize(self.density, self.hamiltonian, self.wfs)
        self.hamiltonian.linearize_to_xc(newxc, self.density)

    def attach(self, function, n=1, *args, **kwargs):
        """Register observer function.

        Call *function* using *args* and
        *kwargs* as arguments.

        If *n* is positive, then
        *function* will be called every *n* iterations + the
        final iteration if it would not be otherwise

        If *n* is negative, then *function* will only be
        called on iteration *abs(n)*.

        If *n* is 0, then *function* will only be called
        on convergence"""

        try:
            slf = function.__self__
        except AttributeError:
            pass
        else:
            if slf is self:
                # function is a bound method of self.  Store the name
                # of the method and avoid circular reference:
                function = function.__func__.__name__

        # Replace self in args with another unique reference
        # to avoid circular reference
        if not hasattr(self, 'self_ref'):
            self.self_ref = object()
        self_ = self.self_ref
        args = tuple([self_ if arg is self else arg for arg in args])

        self.observers.append((function, n, args, kwargs))

    def call_observers(self, iter, final=False):
        """Call all registered callback functions."""
        for function, n, args, kwargs in self.observers:
            call = False
            # Call every n iterations, including the last
            if n > 0:
                if ((iter % n) == 0) != final:
                    call = True
            # Call only on iteration n
            elif n < 0 and not final:
                if iter == abs(n):
                    call = True
            # Call only on convergence
            elif n == 0 and final:
                call = True
            if call:
                if isinstance(function, str):
                    function = getattr(self, function)
                # Replace self reference with self
                self_ = self.self_ref
                args = tuple([self if arg is self_ else arg for arg in args])
                function(*args, **kwargs)

    def get_reference_energy(self):
        return self.wfs.setups.Eref * Ha

    def get_homo_lumo(self, spin=None):
        """Return HOMO and LUMO eigenvalues.

        By default, return the true HOMO-LUMO eigenvalues (spin=None).

        If spin is 0 or 1, return HOMO-LUMO eigenvalues taken among
        only those states with the given spin."""
        return self.wfs.get_homo_lumo(spin) * Ha

    def estimate_memory(self, mem):
        """Estimate memory use of this object."""
        for name, obj in [('Density', self.density),
                          ('Hamiltonian', self.hamiltonian),
                          ('Wavefunctions', self.wfs)]:
            obj.estimate_memory(mem.subnode(name))

    def print_memory_estimate(self, log=None, maxdepth=-1):
        """Print estimated memory usage for PAW object and components.

        maxdepth is the maximum nesting level of displayed components.

        The PAW object must be initialize()'d, but needs not have large
        arrays allocated."""
        # NOTE.  This should work with "--gpaw dry_run=N"
        #
        # However, the initial overhead estimate is wrong if this method
        # is called within a real mpirun/gpaw-python context.
        if log is None:
            log = self.log
        log('Memory estimate:')

        mem_init = maxrss()  # initial overhead includes part of Hamiltonian!
        log('  Process memory now: %.2f MiB' % (mem_init / 1024.0**2))

        mem = MemNode('Calculator', 0)
        mem.indent = '  '
        try:
            self.estimate_memory(mem)
        except AttributeError as m:
            log('Attribute error: %r' % m)
            log('Some object probably lacks estimate_memory() method')
            log('Memory breakdown may be incomplete')
        mem.calculate_size()
        mem.write(log.fd, maxdepth=maxdepth, depth=1)
        log()

    def converge_wave_functions(self):
        """Converge the wave-functions if not present."""

        if self.scf and self.scf.converged:
            if isinstance(self.wfs.kpt_u[0].psit_nG, np.ndarray):
                return
            if self.wfs.kpt_u[0].psit_nG is not None:
                self.wfs.initialize_wave_functions_from_restart_file()
                return

        if not self.initialized:
            self.initialize()

        self.set_positions()

        self.scf.converged = False
        fixed = self.density.fixed
        self.density.fixed = True
        self.calculate(system_changes=[])
        self.density.fixed = fixed

    def diagonalize_full_hamiltonian(self, nbands=None, ecut=None,
                                     scalapack=None,
                                     expert=False):
        if not self.initialized:
            self.initialize()
        nbands = self.wfs.diagonalize_full_hamiltonian(
            self.hamiltonian, self.atoms, self.log,
            nbands, ecut, scalapack, expert)
        self.parameters.nbands = nbands

    def get_number_of_bands(self) -> int:
        """Return the number of bands."""
        return self.wfs.bd.nbands

    def get_xc_functional(self) -> str:
        """Return the XC-functional identifier.

        'LDA', 'PBE', ..."""

        xc = self.parameters.get('xc', 'LDA')
        if isinstance(xc, dict):
            xc = xc['name']
        return xc

    def get_number_of_spins(self):
        return self.wfs.nspins

    def get_spin_polarized(self):
        """Is it a spin-polarized calculation?"""
        return self.wfs.nspins == 2

    def get_bz_k_points(self):
        """Return the k-points."""
        return self.wfs.kd.bzk_kc.copy()

    def get_ibz_k_points(self):
        """Return k-points in the irreducible part of the Brillouin zone."""
        return self.wfs.kd.ibzk_kc.copy()

    def get_bz_to_ibz_map(self):
        """Return indices from BZ to IBZ."""
        return self.wfs.kd.bz2ibz_k.copy()

    def get_k_point_weights(self):
        """Weights of the k-points.

        The sum of all weights is one."""

        return self.wfs.kd.weight_k

    def get_pseudo_density(self, spin=None, gridrefinement=1,
                           pad=True, broadcast=True):
        """Return pseudo-density array.

        If *spin* is not given, then the total density is returned.
        Otherwise, the spin up or down density is returned (spin=0 or
        1)."""

        if gridrefinement == 1:
            nt_sG = self.density.nt_sG
            gd = self.density.gd
        elif gridrefinement == 2:
            if self.density.nt_sg is None:
                self.density.interpolate_pseudo_density()
            nt_sG = self.density.nt_sg
            gd = self.density.finegd
        else:
            raise NotImplementedError

        if spin is None:
            if self.density.nspins == 1:
                nt_G = nt_sG[0]
            else:
                nt_G = nt_sG.sum(axis=0)
        else:
            if self.density.nspins == 1:
                nt_G = 0.5 * nt_sG[0]
            else:
                nt_G = nt_sG[spin]

        nt_G = gd.collect(nt_G, broadcast=broadcast)

        if nt_G is None:
            return None

        if pad:
            nt_G = gd.zero_pad(nt_G)

        return nt_G / Bohr**3

    get_pseudo_valence_density = get_pseudo_density  # Don't use this one!

    def get_effective_potential(self, spin=0, pad=True, broadcast=True):
        """Return pseudo effective-potential."""
        vt_G = self.hamiltonian.gd.collect(self.hamiltonian.vt_sG[spin],
                                           broadcast=broadcast)
        if vt_G is None:
            return None

        if pad:
            vt_G = self.hamiltonian.gd.zero_pad(vt_G)
        return vt_G * Ha

    def get_electrostatic_potential(self):
        """Return the electrostatic potential.

        This is the potential from the pseudo electron density and the
        PAW-compensation charges.  So, the electrostatic potential will
        only be correct outside the PAW augmentation spheres.
        """

        ham = self.hamiltonian
        dens = self.density
        self.initialize_positions()
        dens.interpolate_pseudo_density()
        dens.calculate_pseudo_charge()
        return ham.get_electrostatic_potential(dens) * Ha

    def get_pseudo_density_corrections(self):
        """Integrated density corrections.

        Returns the integrated value of the difference between the pseudo-
        and the all-electron densities at each atom.  These are the numbers
        you should add to the result of doing e.g. Bader analysis on the
        pseudo density."""
        if self.wfs.nspins == 1:
            return np.array([self.density.get_correction(a, 0)
                             for a in range(len(self.atoms))])
        else:
            return np.array([[self.density.get_correction(a, spin)
                              for a in range(len(self.atoms))]
                             for spin in range(2)])

    def get_all_electron_density(self, spin=None, gridrefinement=2,
                                 pad=True, broadcast=True, collect=True,
                                 skip_core=False):
        """Return reconstructed all-electron density array."""
        n_sG, gd = self.density.get_all_electron_density(
            self.atoms, gridrefinement=gridrefinement, skip_core=skip_core)
        if spin is None:
            if self.density.nspins == 1:
                n_G = n_sG[0]
            else:
                n_G = n_sG.sum(axis=0)
        else:
            if self.density.nspins == 1:
                n_G = 0.5 * n_sG[0]
            else:
                n_G = n_sG[spin]

        if collect:
            n_G = gd.collect(n_G, broadcast=broadcast)

        if n_G is None:
            return None

        if pad:
            n_G = gd.zero_pad(n_G)

        return n_G / Bohr**3

    def get_fermi_level(self):
        """Return the Fermi-level."""
        assert self.wfs.fermi_levels is not None
        if len(self.wfs.fermi_levels) != 1:
            raise ValueError('There are two Fermi-levels!')
        return self.wfs.fermi_levels[0] * Ha

    def get_fermi_levels(self):
        """Return the Fermi-levels in case of fixed-magmom."""
        assert self.wfs.fermi_levels is not None
        if len(self.wfs.fermi_levels) != 2:
            raise ValueError('There is only one Fermi-level!')
        return self.wfs.fermi_levels * Ha

    def get_wigner_seitz_densities(self, spin):
        """Get the weight of the spin-density in Wigner-Seitz cells
        around each atom.

        The density assigned to each atom is relative to the neutral atom,
        i.e. the density sums to zero.
        """
        from gpaw.analyse.wignerseitz import wignerseitz
        atom_index = wignerseitz(self.wfs.gd, self.atoms)

        nt_G = self.density.nt_sG[spin]
        weight_a = np.empty(len(self.atoms))
        for a in range(len(self.atoms)):
            # XXX Optimize! No need to integrate in zero-region
            smooth = self.wfs.gd.integrate(np.where(atom_index == a,
                                                    nt_G, 0.0))
            correction = self.density.get_correction(a, spin)
            weight_a[a] = smooth + correction

        return weight_a

    def get_dos(self, spin=0, npts=201, width=None):
        """The total DOS.

        Fold eigenvalues with Gaussians, and put on an energy grid.

        returns an (energies, dos) tuple, where energies are relative to the
        vacuum level for non-periodic systems, and the average potential for
        periodic systems.
        """
        if width is None:
            width = 0.1

        w_k = self.wfs.kd.weight_k
        Nb = self.wfs.bd.nbands
        energies = np.empty(len(w_k) * Nb)
        weights = np.empty(len(w_k) * Nb)
        x = 0
        for k, w in enumerate(w_k):
            energies[x:x + Nb] = self.get_eigenvalues(k, spin)
            weights[x:x + Nb] = w
            x += Nb

        from gpaw.utilities.dos import fold
        return fold(energies, weights, npts, width)

    def get_wigner_seitz_ldos(self, a, spin=0, npts=201, width=None):
        """The Local Density of States, using a Wigner-Seitz basis function.

        Project wave functions onto a Wigner-Seitz box at atom ``a``, and
        use this as weight when summing the eigenvalues."""
        if width is None:
            width = 0.1

        from gpaw.utilities.dos import fold, raw_wignerseitz_LDOS
        energies, weights = raw_wignerseitz_LDOS(self, a, spin)
        return fold(energies * Ha, weights, npts, width)

    def get_orbital_ldos(self, a,
                         spin=0, angular='spdf', npts=201, width=None,
                         nbands=None, spinorbit=False):
        """The Local Density of States, using atomic orbital basis functions.

        Project wave functions onto an atom orbital at atom ``a``, and
        use this as weight when summing the eigenvalues.

        The atomic orbital has angular momentum ``angular``, which can be
        's', 'p', 'd', 'f', or any combination (e.g. 'sdf').

        An integer value for ``angular`` can also be used to specify a specific
        projector function to project onto.

        Setting nbands limits the number of bands included. This speeds up the
        calculation if one has many bands in the calculator but is only
        interested in the DOS at low energies.
        """
        from gpaw.utilities.dos import fold, raw_orbital_LDOS
        if width is None:
            width = 0.1

        if not spinorbit:
            energies, weights = raw_orbital_LDOS(self, a, spin, angular,
                                                 nbands)
        else:
            raise DeprecationWarning(
                'Please use GPAW.dos(soc=True, ...).raw_pdos(...)')

        return fold(energies * Ha, weights, npts, width)

    def get_lcao_dos(self, atom_indices=None, basis_indices=None,
                     npts=201, width=None):
        """Get density of states projected onto orbitals in LCAO mode.

        basis_indices is a list of indices of basis functions on which
        to project.  To specify all basis functions on a set of atoms,
        you can supply atom_indices instead.  Both cannot be given
        simultaneously."""

        both_none = atom_indices is None and basis_indices is None
        neither_none = atom_indices is not None and basis_indices is not None
        if both_none or neither_none:
            raise ValueError('Please give either atom_indices or '
                             'basis_indices but not both')

        if width is None:
            width = 0.1

        if self.wfs.S_qMM is None:
            from gpaw.utilities.dos import RestartLCAODOS
            lcaodos = RestartLCAODOS(self)
        else:
            from gpaw.utilities.dos import LCAODOS
            lcaodos = LCAODOS(self)

        if atom_indices is not None:
            basis_indices = lcaodos.get_atom_indices(atom_indices)

        eps_n, w_n = lcaodos.get_subspace_pdos(basis_indices)
        from gpaw.utilities.dos import fold
        return fold(eps_n * Ha, w_n, npts, width)

    def get_all_electron_ldos(self, mol, spin=0, npts=201, width=None,
                              wf_k=None, P_aui=None, lc=None, raw=False):
        """The Projected Density of States, using all-electron wavefunctions.

        Projects onto a pseudo_wavefunctions (wf_k) corresponding to some band
        n and uses P_aui ([paw.nuclei[a].P_uni[:,n,:] for a in atoms]) to
        obtain the all-electron overlaps.
        Instead of projecting onto a wavefunction, a molecular orbital can
        be specified by a linear combination of weights (lc)
        """
        from gpaw.utilities.dos import all_electron_LDOS, fold

        if raw:
            return all_electron_LDOS(self, mol, spin, lc=lc,
                                     wf_k=wf_k, P_aui=P_aui)
        if width is None:
            width = 0.1

        energies, weights = all_electron_LDOS(self, mol, spin,
                                              lc=lc, wf_k=wf_k, P_aui=P_aui)
        return fold(energies * Ha, weights, npts, width)

    def get_pseudo_wave_function(self, band=0, kpt=0, spin=0, broadcast=True,
                                 pad=True, periodic=False):
        """Return pseudo-wave-function array.

        Units: 1/Angstrom^(3/2)
        """
        if self.wfs.mode == 'lcao' and not self.wfs.positions_set:
            self.initialize_positions()

        if pad:
            psit_G = self.get_pseudo_wave_function(band, kpt, spin, broadcast,
                                                   pad=False,
                                                   periodic=periodic)
            if psit_G is None:
                return
            else:
                return self.wfs.gd.zero_pad(psit_G)

        psit_G = self.wfs.get_wave_function_array(band, kpt, spin,
                                                  periodic=periodic)
        if broadcast:
            if self.wfs.world.rank != 0:
                psit_G = self.wfs.gd.empty(dtype=self.wfs.dtype,
                                           global_array=True)
            psit_G = np.ascontiguousarray(psit_G)
            self.wfs.world.broadcast(psit_G, 0)
            return psit_G / Bohr**1.5
        elif self.wfs.world.rank == 0:
            return psit_G / Bohr**1.5

    def get_eigenvalues(self, kpt=0, spin=0, broadcast=True):
        """Return eigenvalue array."""
        assert 0 <= kpt < self.wfs.kd.nibzkpts, kpt
        eps_n = self.wfs.collect_eigenvalues(kpt, spin)
        if broadcast:
            if self.wfs.world.rank != 0:
                eps_n = np.empty(self.wfs.bd.nbands)
            self.wfs.world.broadcast(eps_n, 0)
        return eps_n * Ha

    def get_occupation_numbers(self, kpt=0, spin=0, broadcast=True):
        """Return occupation array."""
        f_n = self.wfs.collect_occupations(kpt, spin)
        if broadcast:
            if self.wfs.world.rank != 0:
                f_n = np.empty(self.wfs.bd.nbands)
            self.wfs.world.broadcast(f_n, 0)
        return f_n

    def get_xc_difference(self, xc):
        if isinstance(xc, (str, dict)):
            xc = XC(xc)
        xc.set_grid_descriptor(self.density.finegd)
        xc.initialize(self.density, self.hamiltonian, self.wfs)
        xc.set_positions(self.spos_ac)
        if xc.orbital_dependent:
            self.converge_wave_functions()
        return self.hamiltonian.get_xc_difference(xc, self.density) * Ha

    def initial_wannier(self, initialwannier, kpointgrid, fixedstates,
                        edf, spin, nbands):
        """Initial guess for the shape of wannier functions.

        Use initial guess for wannier orbitals to determine rotation
        matrices U and C.
        """
        from ase.dft.wannier import rotation_from_projection
        proj_knw = self.get_projections(initialwannier, spin)
        U_kww = []
        C_kul = []
        for fixed, proj_nw in zip(fixedstates, proj_knw):
            U_ww, C_ul = rotation_from_projection(proj_nw[:nbands],
                                                  fixed,
                                                  ortho=True)
            U_kww.append(U_ww)
            C_kul.append(C_ul)

        U_kww = np.asarray(U_kww)
        return C_kul, U_kww

    def get_wannier_localization_matrix(self, nbands, dirG, kpoint,
                                        nextkpoint, G_I, spin):
        """Calculate integrals for maximally localized Wannier functions."""

        # Due to orthorhombic cells, only one component of dirG is non-zero.
        k_kc = self.wfs.kd.bzk_kc
        G_c = k_kc[nextkpoint] - k_kc[kpoint] - G_I

        return self.get_wannier_integrals(spin, kpoint,
                                          nextkpoint, G_c, nbands)

    def get_wannier_integrals(self, s, k, k1, G_c, nbands=None):
        """Calculate integrals for maximally localized Wannier functions."""

        assert s <= self.wfs.nspins
        kpt_rank, u = divmod(k + len(self.wfs.kd.ibzk_kc) * s,
                             len(self.wfs.kpt_u))
        kpt_rank1, u1 = divmod(k1 + len(self.wfs.kd.ibzk_kc) * s,
                               len(self.wfs.kpt_u))
        kpt_u = self.wfs.kpt_u

        # XXX not for the kpoint/spin parallel case
        assert self.wfs.kd.comm.size == 1

        # If calc is a save file, read in tar references to memory
        # For lcao mode just initialize the wavefunctions from the
        # calculated lcao coefficients
        if self.wfs.mode == 'lcao':
            self.wfs.initialize_wave_functions_from_lcao()
        else:
            self.wfs.initialize_wave_functions_from_restart_file()

        # Get pseudo part
        Z_nn = self.wfs.gd.wannier_matrix(kpt_u[u].psit_nG,
                                          kpt_u[u1].psit_nG, G_c, nbands)

        # Add corrections
        self.add_wannier_correction(Z_nn, G_c, u, u1, nbands)

        self.wfs.gd.comm.sum(Z_nn)

        return Z_nn

    def add_wannier_correction(self, Z_nn, G_c, u, u1, nbands=None):
        r"""Calculate the correction to the wannier integrals.

        See: (Eq. 27 ref1)::

                          -i G.r
            Z   = <psi | e      |psi >
             nm       n             m

                           __                __
                   ~      \              a  \     a*   a    a
            Z    = Z    +  ) exp[-i G . R ]  )   P   dO    P
             nmx    nmx   /__            x  /__   ni   ii'  mi'

                           a                 ii'

        Note that this correction is an approximation that assumes the
        exponential varies slowly over the extent of the augmentation sphere.

        ref1: Thygesen et al, Phys. Rev. B 72, 125119 (2005)
        """

        if nbands is None:
            nbands = self.wfs.bd.nbands

        P_ani = self.wfs.kpt_u[u].P_ani
        P1_ani = self.wfs.kpt_u[u1].P_ani
        for a, P_ni in P_ani.items():
            P_ni = P_ani[a][:nbands]
            P1_ni = P1_ani[a][:nbands]
            dO_ii = self.wfs.setups[a].dO_ii
            e = np.exp(-2.j * np.pi * np.dot(G_c, self.spos_ac[a]))
            Z_nn += e * np.dot(np.dot(P_ni.conj(), dO_ii), P1_ni.T)

    def get_projections(self, locfun, spin=0):
        """Project wave functions onto localized functions

        Determine the projections of the Kohn-Sham eigenstates
        onto specified localized functions of the format::

          locfun = [[spos_c, l, sigma], [...]]

        spos_c can be an atom index, or a scaled position vector. l is
        the angular momentum, and sigma is the (half-) width of the
        radial gaussian.

        Return format is::

          f_kni = <psi_kn | f_i>

        where psi_kn are the wave functions, and f_i are the specified
        localized functions.

        As a special case, locfun can be the string 'projectors', in which
        case the bound state projectors are used as localized functions.
        """

        wfs = self.wfs

        if locfun == 'projectors':
            f_kin = []
            for kpt in wfs.kpt_u:
                if kpt.s == spin:
                    f_in = []
                    for a, P_ni in kpt.P_ani.items():
                        i = 0
                        setup = wfs.setups[a]
                        for l, n in zip(setup.l_j, setup.n_j):
                            if n >= 0:
                                for j in range(i, i + 2 * l + 1):
                                    f_in.append(P_ni[:, j])
                            i += 2 * l + 1
                    f_kin.append(f_in)
            f_kni = np.array(f_kin).transpose(0, 2, 1)
            return f_kni.conj()

        from math import factorial as fac

        from gpaw.lfc import LocalizedFunctionsCollection as LFC
        from gpaw.spline import Spline

        nkpts = len(wfs.kd.ibzk_kc)
        nbf = np.sum([2 * l + 1 for pos, l, a in locfun])
        f_kni = np.zeros((nkpts, wfs.bd.nbands, nbf), wfs.dtype)

        spos_xc = []
        splines_x = []
        for spos_c, l, sigma in locfun:
            if isinstance(spos_c, int):
                spos_c = self.spos_ac[spos_c]
            spos_xc.append(spos_c)
            alpha = .5 * Bohr**2 / sigma**2
            r = np.linspace(0, 10. * sigma, 500)
            f_g = (fac(l) * (4 * alpha)**(l + 3 / 2.) *
                   np.exp(-alpha * r**2) /
                   (np.sqrt(4 * np.pi) * fac(2 * l + 1)))
            splines_x.append([Spline(l, rmax=r[-1], f_g=f_g)])

        lf = LFC(wfs.gd, splines_x, wfs.kd, dtype=wfs.dtype)
        lf.set_positions(spos_xc)

        assert wfs.gd.comm.size == 1
        k = 0
        f_ani = lf.dict(wfs.bd.nbands)
        for kpt in wfs.kpt_u:
            if kpt.s != spin:
                continue
            lf.integrate(kpt.psit_nG[:], f_ani, kpt.q)
            i1 = 0
            for x, f_ni in f_ani.items():
                i2 = i1 + f_ni.shape[1]
                f_kni[k, :, i1:i2] = f_ni
                i1 = i2
            k += 1

        return f_kni.conj()

    def get_number_of_grid_points(self):
        return self.wfs.gd.N_c

    def get_number_of_iterations(self):
        return self.scf.niter

    def get_number_of_electrons(self):
        return self.wfs.setups.nvalence - self.density.charge

    def get_electrostatic_corrections(self):
        """Calculate PAW correction to average electrostatic potential."""
        dEH_a = np.zeros(len(self.atoms))
        for a, D_sp in self.density.D_asp.items():
            setup = self.wfs.setups[a]
            dEH_a[a] = setup.dEH0 + np.dot(setup.dEH_p, D_sp.sum(0))
        self.wfs.gd.comm.sum(dEH_a)
        return dEH_a * Ha * Bohr**3

    def get_nonselfconsistent_energies(self, type='beefvdw'):
        from gpaw.xc.bee import BEEFEnsemble
        if type not in ['beefvdw', 'mbeef', 'mbeefvdw']:
            raise NotImplementedError('Not implemented for type = %s' % type)
        assert self.scf.converged
        bee = BEEFEnsemble(self)
        x = bee.create_xc_contributions('exch')
        c = bee.create_xc_contributions('corr')
        if type == 'beefvdw':
            return np.append(x, c)
        elif type == 'mbeef':
            return x.flatten()
        elif type == 'mbeefvdw':
            return np.append(x.flatten(), c)

    def embed(self, q_p, rc=0.2, rc2=np.inf, width=1.0):
        """Embed QM region in point-charges."""
        pc = PointChargePotential(q_p, rc=rc, rc2=rc2, width=width)
        self.set(external=pc)
        return pc

    def dos(self,
            soc: bool = False,
            theta: float = 0.0,
            phi: float = 0.0,
            shift_fermi_level: bool = True) -> DOSCalculator:
        """Create DOS-calculator.

        Default is to shift_fermi_level to 0.0 eV.  For soc=True, angles
        can be given in degrees.
        """
        return DOSCalculator.from_calculator(
            self, soc=soc,
            theta=theta, phi=phi,
            shift_fermi_level=shift_fermi_level)
