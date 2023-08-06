from ase import Atoms
from ase.calculators.test import numeric_force
from gpaw import GPAW, Mixer, FermiDirac, Davidson
from gpaw.test import equal


def test_generic_H_force():
    a = 4.0
    n = 16
    atoms = Atoms('H',
                  positions=[[1.234, 2.345, 3.456]],
                  cell=(a, a, a),
                  pbc=True)
    calc = GPAW(nbands=1,
                gpts=(n, n, n),
                txt=None,
                eigensolver=Davidson(4),
                mixer=Mixer(0.3, 3, 1),
                convergence={'energy': 1e-7},
                occupations=FermiDirac(0.0))
    atoms.calc = calc
    e1 = atoms.get_potential_energy()
    f1 = atoms.get_forces()[0]
    for i in range(3):
        f2i = numeric_force(atoms, 0, i)
        print(f1[i], f2i)
        equal(f1[i], f2i, 0.00025)

    energy_tolerance = 0.001
    force_tolerance = 0.004
    equal(e1, -0.5318, energy_tolerance)
    f1_ref = [-0.29138, -0.3060, -0.3583]
    for i in range(3):
        equal(f1[i], f1_ref[i], force_tolerance)
