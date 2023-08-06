import pytest
from ase import Atoms
from ase.calculators.test import numeric_force
from gpaw import GPAW, PW, Davidson


@pytest.mark.libxc
def test_exx_double_cell(in_tmp_dir):
    L = 4.0
    a = Atoms('H2',
              [[0, 0, 0], [0.5, 0.5, 0]],
              cell=[L, L, 1],
              pbc=1)
    a.center()

    a.calc = GPAW(
        mode=PW(400, force_complex_dtype=True),
        parallel={'kpt': 1, 'band': 1},
        eigensolver=Davidson(1),
        symmetry='off',
        kpts={'size': (1, 1, 4), 'gamma': True},
        txt='H.txt',
        xc='HSE06')
    e1 = a.get_potential_energy()
    eps1 = a.calc.get_eigenvalues(1)[0]
    f1 = a.get_forces()
    f1n = numeric_force(a, 1, 0, 0.001)
    assert abs(f1[1, 0] - f1n) < 0.0005

    a *= (1, 1, 2)
    a.calc = GPAW(
        mode=PW(400, force_complex_dtype=True),
        kpts={'size': (1, 1, 2), 'gamma': True},
        parallel={'kpt': 1, 'band': 1},
        eigensolver=Davidson(1),
        symmetry='off',
        txt='H2.txt',
        xc='HSE06')
    e2 = a.get_potential_energy()
    eps2 = a.calc.get_eigenvalues(0)[0]
    f2 = a.get_forces()

    f2[:2] -= f1
    f2[2:] -= f1

    assert abs(e2 - 2 * e1) < 0.002
    assert abs(eps1 - eps2) < 0.001
    assert abs(f2).max() < 0.0005


if __name__ == '__main__':
    from cProfile import Profile
    prof = Profile()
    prof.enable()
    test_exx_double_cell(1)
    prof.disable()
    from gpaw.mpi import rank, size
    prof.dump_stats(f'prof-{size}.{rank}')
