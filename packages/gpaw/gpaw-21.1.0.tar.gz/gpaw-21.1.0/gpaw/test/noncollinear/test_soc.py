"""Test HOMO and LUMO band-splitting for MoS2."""
import pytest
import numpy as np
from ase.build import mx2

from gpaw import GPAW
from gpaw.spinorbit import soc_eigenstates
from gpaw.mpi import size


def check(E, hsplit, lsplit):
    print(E)
    h1, h2, l1, l2 = E[24:28]  # HOMO-1, HOMO, LUMO, LUMO+1
    print(h2 - h1)
    print(l2 - l1)
    assert abs(h2 - h1 - hsplit) < 0.01
    assert abs(l2 - l1 - lsplit) < 0.002


params = dict(mode='pw',
              kpts={'size': (3, 3, 1),
                    'gamma': True})


@pytest.mark.soc
@pytest.mark.skipif(size > 1, reason='Does not work in parallel')
def test_soc_self_consistent():
    """Self-consistent SOC."""
    a = mx2('MoS2')
    a.center(vacuum=3, axis=2)

    a.calc = GPAW(experimental={'magmoms': np.zeros((3, 3)),
                                'soc': True},
                  convergence={'bands': 28},
                  **params)
    a.get_potential_energy()
    eigs = a.calc.get_eigenvalues(kpt=2)
    check(eigs, 0.15, 0.002)


@pytest.mark.soc
@pytest.mark.skipif(size > 2, reason='Does not work with more than 2 cores')
def test_non_collinear_plus_soc():
    a = mx2('MoS2')
    a.center(vacuum=3, axis=2)

    a.calc = GPAW(experimental={'magmoms': np.zeros((3, 3)),
                                'soc': False},
                  convergence={'bands': 28},
                  parallel={'domain': 1},
                  **params)
    a.get_potential_energy()

    bzwfs = soc_eigenstates(a.calc, n2=28)
    eigs = bzwfs.eigenvalues()[8]
    check(eigs, 0.15, 0.007)


@pytest.mark.soc
def test_soc_non_self_consistent():
    """Non self-consistent SOC."""
    a = mx2('MoS2')
    a.center(vacuum=3, axis=2)

    a.calc = GPAW(convergence={'bands': 14},
                  **params)
    a.get_potential_energy()

    bzwfs = soc_eigenstates(a.calc, n2=14)
    eigs = bzwfs.eigenvalues()[8]
    check(eigs, 0.15, 0.007)
