import numpy as np
from math import pi, cos, sin
from ase import Atom, Atoms
from gpaw import GPAW, setup_paths
from gpaw.poisson import FDPoissonSolver
from gpaw.xas import XAS
from gpaw.test import equal
from gpaw.atom.generator2 import generate
import gpaw.mpi as mpi


def test_corehole_h2o(in_tmp_dir):
    # Generate setup for oxygen with half a core-hole:
    gen = generate('O', 8, '2s,s,2p,p,d', [1.2], 1.0, None, 2,
                   core_hole='1s,0.5')
    setup = gen.make_paw_setup('hch1s')
    setup.write_xml()
    if setup_paths[0] != '.':
        setup_paths.insert(0, '.')

    a = 5.0
    d = 0.9575
    t = pi / 180 * 104.51
    H2O = Atoms([Atom('O', (0, 0, 0)),
                 Atom('H', (d, 0, 0)),
                 Atom('H', (d * cos(t), d * sin(t), 0))],
                cell=(a, a, a), pbc=False)
    H2O.center()
    calc = GPAW(nbands=10, h=0.2, setups={'O': 'hch1s'},
                experimental={'niter_fixdensity': 2},
                poissonsolver=FDPoissonSolver(use_charge_center=True))
    H2O.calc = calc
    _ = H2O.get_potential_energy()

    if mpi.size == 1:
        xas = XAS(calc)
        x, y = xas.get_spectra()
        e1_n = xas.eps_n
        de1 = e1_n[1] - e1_n[0]

    calc.write('h2o-xas.gpw')

    if mpi.size == 1:
        calc = GPAW('h2o-xas.gpw', txt=None,
                    poissonsolver=FDPoissonSolver(use_charge_center=True))
        calc.initialize()
        xas = XAS(calc)
        x, y = xas.get_spectra()
        e2_n = xas.eps_n
        w_n = np.sum(xas.sigma_cn.real**2, axis=0)
        de2 = e2_n[1] - e2_n[0]

        equal(de2, 2.064, 0.005)
        equal(w_n[1] / w_n[0], 2.22, 0.01)

        assert de1 == de2

    if 0:
        import matplotlib.pyplot as plt
        plt.plot(x, y[0])
        plt.plot(x, sum(y))
        plt.show()
