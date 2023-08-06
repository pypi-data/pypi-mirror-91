import json
import sys
from math import pi
from pathlib import Path
from typing import Union

import numpy as np
from ase.units import Hartree

import gpaw.mpi as mpi
from gpaw.hybrids.paw import pawexxvv
from gpaw.xc import XC
from gpaw.xc.tools import vxc
from gpaw.xc.kernel import XCNull
from gpaw.response.pair import PairDensity
from gpaw.wavefunctions.pw import PWDescriptor
from gpaw.kpt_descriptor import KPointDescriptor
from gpaw.utilities import unpack, unpack2
from gpaw.response.wstc import WignerSeitzTruncatedCoulomb


def select_kpts(kpts, calc):
    """Function to process input parameters that take a list of k-points given
    in different format and returns a list of indices of the corresponding
    k-points in the IBZ."""
    if kpts is None:
        # Do all k-points in the IBZ:
        return np.arange(calc.wfs.kd.nibzkpts)

    if np.asarray(kpts).ndim == 1:
        return kpts

    # Find k-points:
    bzk_Kc = calc.get_bz_k_points()
    indices = []
    for k_c in kpts:
        d_Kc = bzk_Kc - k_c
        d_Kc -= d_Kc.round()
        K = abs(d_Kc).sum(1).argmin()
        if not np.allclose(d_Kc[K], 0):
            raise ValueError('Could not find k-point: {k_c}'
                             .format(k_c=k_c))
        k = calc.wfs.kd.bz2ibz_k[K]
        indices.append(k)
    return indices


class EXX(PairDensity):
    def __init__(self, calc, xc=None, kpts=None, bands=None, ecut=None,
                 stencil=2,
                 omega=None, world=mpi.world, txt=sys.stdout, timer=None):
        """Non self-consistent hybrid functional calculations.

        Eigenvalues and total energy can be calculated.

        calc: str or PAW object
            GPAW calculator object or filename of saved calculator object.
        xc: str
            Name of functional.  Use one of EXX, PBE0, HSE03, HSE06 or B3LYP.
            Default is EXX.
        kpts: list of in or list of list of int
            List of indices of the IBZ k-points to calculate the quasi particle
            energies for.  Default is all k-points.  One can also specify the
            coordiantes of the k-point.  As an example, Gamma and X for an
            FCC crystal would be: kpts=[[0, 0, 0], [1 / 2, 1 / 2, 0]].
        bands: tuple of two ints
            Range of band indices, like (n1, n2), to calculate the quasi
            particle energies for. Bands n where n1<=n<n2 will be
            calculated.  Note that the second band index is not included.
            Default is all occupied bands.
        ecut: float
            Plane wave cut-off energy in eV.  Default it the same as was used
            for the ground-state calculations.
        """

        PairDensity.__init__(self, calc, ecut, world=world, txt=txt,
                             timer=timer)

        def _xc(name):
            return {'name': name, 'stencil': stencil}

        if xc is None or xc == 'EXX':
            self.exx_fraction = 1.0
            xc = XC(XCNull())
        elif xc == 'PBE0':
            self.exx_fraction = 0.25
            xc = XC(_xc('HYB_GGA_XC_PBEH'))
        elif xc == 'HSE03':
            omega = 0.106
            self.exx_fraction = 0.25
            xc = XC(_xc('HYB_GGA_XC_HSE03'))
        elif xc == 'HSE06':
            omega = 0.11
            self.exx_fraction = 0.25
            xc = XC(_xc('HYB_GGA_XC_HSE06'))
        elif xc == 'B3LYP':
            self.exx_fraction = 0.2
            xc = XC(_xc('HYB_GGA_XC_B3LYP'))

        self.xc = xc
        self.omega = omega
        self.exc = np.nan  # density dependent part of xc-energy

        self.kpts = select_kpts(kpts, self.calc)

        if bands is None:
            # Do all occupied bands:
            bands = [0, self.nocc2]

        print('Calculating exact exchange contributions for band index',
              '%d-%d' % (bands[0], bands[1] - 1), file=self.fd)
        print('for IBZ k-points with indices:',
              ', '.join(str(i) for i in self.kpts), file=self.fd)

        self.bands = bands

        if self.ecut is None:
            self.ecut = self.calc.wfs.pd.ecut
        print('Plane-wave cutoff: %.3f eV' % (self.ecut * Hartree),
              file=self.fd)

        shape = (self.calc.wfs.nspins, len(self.kpts), bands[1] - bands[0])
        self.exxvv_sin = np.zeros(shape)   # valence-valence exchange energies
        self.exxvc_sin = np.zeros(shape)   # valence-core exchange energies
        self.f_sin = np.empty(shape)       # occupation numbers

        # The total EXX energy will not be calculated if we are only
        # interested in a few eigenvalues for a few k-points
        self.exx = np.nan    # total EXX energy
        self.exxvv = np.nan  # valence-valence
        self.exxvc = np.nan  # valence-core
        self.exxcc = 0.0     # core-core

        self.mysKn1n2 = None  # my (s, K, n1, n2) indices
        self.distribute_k_points_and_bands(0, self.nocc2)

        # All occupied states:
        self.mykpts = [self.get_k_point(s, K, n1, n2)
                       for s, K, n1, n2 in self.mysKn1n2]

        if omega is None:
            print('Using Wigner-Seitz truncated coulomb interaction.',
                  file=self.fd)
            self.wstc = WignerSeitzTruncatedCoulomb(self.calc.wfs.gd.cell_cv,
                                                    self.calc.wfs.kd.N_c,
                                                    self.fd)
        self.iG_qG = {}  # cache

        # PAW matrices:
        self.V_asii = []  # valence-valence correction
        self.C_aii = []   # valence-core correction
        self.initialize_paw_exx_corrections()

    def calculate(self, restart: Union[Path, str] = None):
        """Do the calculation.

        restart_filename: str or Path
            Name of restart json-file.  Allows for incremental calculation
            of eigenvalues.
        """
        kd = self.calc.wfs.kd
        nspins = self.calc.wfs.nspins

        if restart:
            if isinstance(restart, str):
                restart = Path(restart)

            if restart.is_file():
                data = json.loads(restart.read_text())
                n = len(data)
                print('Restarting from {restart}.  '
                      'Read {n} spin+k-point pairs.'
                      .format(**locals()),
                      file=self.fd)
            else:
                data = []
        else:
            data = []

        n = 0
        for s in range(nspins):
            for i, k1 in enumerate(self.kpts):
                if n < len(data):
                    f_n, exxvv_n, exxvc_n = data[n]
                    self.f_sin[s, i] = f_n
                    self.exxvc_sin[s, i] = exxvc_n
                    self.exxvv_sin[s, i] = exxvv_n
                    n += 1
                    continue

                K1 = kd.ibz2bz_k[k1]
                kpt1 = self.get_k_point(s, K1, *self.bands)
                self.f_sin[s, i] = kpt1.f_n
                for kpt2 in self.mykpts:
                    if kpt2.s == s:
                        self.calculate_q(i, kpt1, kpt2)

                self.calculate_paw_exx_corrections(i, kpt1)

                self.world.sum(self.exxvv_sin[s, i])

                if restart and self.world.rank == 0:
                    data.append([x_n.tolist()
                                 for x_n in [self.f_sin[s, i],
                                             self.exxvc_sin[s, i],
                                             self.exxvv_sin[s, i]]])
                    assert isinstance(restart, Path)  # for mypy
                    tmp = restart.with_name(restart.name + '.tmp')
                    tmp.write_text(json.dumps(data))
                    # Overwrite restart-file in in almost atomic step that
                    # hopefully does not crash due to job running out of time:
                    tmp.rename(restart)

                n += 1

        # Calculate total energy if we have everything needed:
        if (len(self.kpts) == kd.nibzkpts and
            self.bands[0] == 0 and
            self.bands[1] >= self.nocc2):
            exxvv_i = (self.exxvv_sin * self.f_sin).sum(axis=2).sum(axis=0)
            exxvc_i = 2 * (self.exxvc_sin * self.f_sin).sum(axis=2).sum(axis=0)
            self.exxvv = np.dot(kd.weight_k[self.kpts], exxvv_i) / nspins
            self.exxvc = np.dot(kd.weight_k[self.kpts], exxvc_i) / nspins
            self.exx = self.exxvv + self.exxvc + self.exxcc
            print('Exact exchange energy:', file=self.fd)
            for kind, exx in [('valence-valence', self.exxvv),
                              ('valence-core', self.exxvc),
                              ('core-core', self.exxcc),
                              ('total', self.exx)]:
                print('%16s%11.3f eV' % (kind + ':', exx * Hartree),
                      file=self.fd)

            self.exc = self.calculate_hybrid_correction()

        exx_sin = self.exxvv_sin + self.exxvc_sin
        print('EXX eigenvalue contributions in eV:', file=self.fd)
        print(np.array_str(exx_sin * Hartree, precision=3), file=self.fd)

    def get_exx_energy(self):
        return self.exx * Hartree

    def get_total_energy(self):
        ham = self.calc.hamiltonian
        return (self.exx * self.exx_fraction + self.exc +
                ham.e_total_free - ham.e_xc) * Hartree

    def get_eigenvalue_contributions(self):
        b1, b2 = self.bands
        e_sin = vxc(self.calc, self.xc)[:, self.kpts, b1:b2] / Hartree
        e_sin += (self.exxvv_sin + self.exxvc_sin) * self.exx_fraction
        return e_sin * Hartree

    def calculate_q(self, i, kpt1, kpt2):
        wfs = self.calc.wfs

        q_c = wfs.kd.bzk_kc[kpt2.K] - wfs.kd.bzk_kc[kpt1.K]
        qd = KPointDescriptor([q_c])
        pd = PWDescriptor(self.ecut, wfs.gd, wfs.dtype, kd=qd)

        Q_G = self.get_fft_indices(kpt1.K, kpt2.K, q_c, pd,
                                   kpt1.shift_c - kpt2.shift_c)

        Q_aGii = self.initialize_paw_corrections(pd, soft=True)

        for n in range(kpt1.n2 - kpt1.n1):
            ut1cc_R = kpt1.ut_nR[n].conj()
            C1_aGi = [np.dot(Q_Gii, P1_ni[n].conj())
                      for Q_Gii, P1_ni in zip(Q_aGii, kpt1.P_ani)]
            n_mG = self.calculate_pair_densities(ut1cc_R, C1_aGi, kpt2,
                                                 pd, Q_G)
            e = self.calculate_n(pd, n_mG, kpt2)
            self.exxvv_sin[kpt1.s, i, n] += e

    def calculate_n(self, pd, n_mG, kpt2):
        iG_G = self.get_coulomb_kernel(pd)
        x = 4 * pi / self.calc.wfs.kd.nbzkpts / pd.gd.dv**2

        e = 0.0
        for f, n_G in zip(kpt2.f_n, n_mG):
            x_G = n_G * iG_G
            e -= x * f * pd.integrate(x_G, x_G).real

        return e

    def get_coulomb_kernel(self, pd):
        if self.omega is not None:
            G2_G = pd.G2_qG[0]
            iG_G = np.empty_like(G2_G)
            if pd.kd.gamma:
                iG_G[0] = 1 / (2 * self.omega)
            else:
                iG_G[0] = ((1 - np.exp(-G2_G[0] / (4 * self.omega**2))) /
                           G2_G[0])**0.5
            iG_G[1:] = ((1 - np.exp(-G2_G[1:] / (4 * self.omega**2))) /
                        G2_G[1:])**0.5
            return iG_G

        key = tuple((pd.kd.bzk_kc[0] * self.calc.wfs.kd.N_c).round())
        iG_G = self.iG_qG.get(key)
        if iG_G is None:
            v_G = self.wstc.get_potential(pd)
            iG_G = (v_G / (4 * pi))**0.5
            self.iG_qG[key] = iG_G
        return iG_G

    def initialize_paw_exx_corrections(self):
        for a, atomdata in enumerate(self.calc.wfs.setups):
            V_sii = []
            for D_p in self.calc.density.D_asp[a]:
                D_ii = unpack2(D_p)
                V_ii = pawexxvv(atomdata, D_ii)
                V_sii.append(V_ii)
            if atomdata.X_p is None:
                C_ii = D_ii * 0.0
            else:
                C_ii = unpack(atomdata.X_p)
            self.V_asii.append(V_sii)
            self.C_aii.append(C_ii)
            self.exxcc += atomdata.ExxC or 0.0

    def calculate_paw_exx_corrections(self, i, kpt):
        x = self.calc.wfs.nspins / self.world.size
        s = kpt.s

        for V_sii, C_ii, P_ni in zip(self.V_asii, self.C_aii, kpt.P_ani):
            V_ii = V_sii[s]
            v_n = (np.dot(P_ni, V_ii) * P_ni.conj()).sum(axis=1).real
            c_n = (np.dot(P_ni, C_ii) * P_ni.conj()).sum(axis=1).real
            self.exxvv_sin[s, i] -= v_n * x
            self.exxvc_sin[s, i] -= c_n

    def calculate_hybrid_correction(self):
        dens = self.calc.density
        if dens.nt_sg is None:
            dens.interpolate_pseudo_density()
        exc = self.xc.calculate(dens.finegd, dens.nt_sg)
        for a, D_sp in dens.D_asp.items():
            atomdata = dens.setups[a]
            exc += self.xc.calculate_paw_correction(atomdata, D_sp)
        return exc
