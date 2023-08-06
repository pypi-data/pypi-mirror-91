import pytest
from ase import Atoms
from gpaw import GPAW


def test_fixdensity(in_tmp_dir):
    a = 2.5
    slab = Atoms('Li', cell=(a, a, 2 * a), pbc=1)
    slab.calc = GPAW(kpts=(3, 3, 1), txt='li-1.txt',
                     parallel=dict(kpt=1))
    slab.get_potential_energy()
    slab.calc.write('li.gpw')

    # Gamma point:
    e1 = slab.calc.get_eigenvalues(kpt=0)[0]
    f1 = slab.calc.get_fermi_level()

    kpts = [(0, 0, 0)]

    # Fix density and continue:
    calc = slab.calc.fixed_density(
        txt='li-2.txt',
        nbands=5,
        kpts=kpts)
    e2 = calc.get_eigenvalues(kpt=0)[0]
    f2 = calc.get_fermi_level()

    # Start from gpw-file:
    calc = GPAW('li.gpw', txt=None)
    calc = calc.fixed_density(
        txt='li-3.txt',
        nbands=5,
        kpts=kpts)
    e3 = calc.get_eigenvalues(kpt=0)[0]
    f3 = calc.get_fermi_level()

    assert f2 == pytest.approx(f1, abs=1e-10)
    assert f3 == pytest.approx(f1, abs=1e-10)
    assert e2 == pytest.approx(e1, abs=3e-5)
    assert e3 == pytest.approx(e1, abs=3e-5)

    calc = GPAW('li.gpw',
                txt='li-4.txt',
                fixdensity=True,
                nbands=5,
                kpts=kpts,
                symmetry='off')

    with pytest.warns(DeprecationWarning):
        calc.get_potential_energy()
    e4 = calc.get_eigenvalues(kpt=0)[0]

    assert e4 == pytest.approx(e1, abs=3e-5)
