from ase import Atom, Atoms
from gpaw import GPAW, Mixer
from gpaw.test import equal

# This test would be useful if it did anything with mixers that the
# other tests didn't.  Maybe verify that it uses mixing history
# correctly, or the long-range damping, or something.  Preferebly
# without a self-consistent calculation.


def test_generic_mixer(in_tmp_dir):
    a = 2.7
    bulk = Atoms([Atom('Li')], pbc=True, cell=(a, a, a))
    k = 2
    g = 16
    calc = GPAW(gpts=(g, g, g), kpts=(k, k, k), nbands=2,
                mixer=Mixer(nmaxold=5))
    bulk.calc = calc
    e = bulk.get_potential_energy()
    calc.write('Li.gpw')
    GPAW('Li.gpw')

    energy_tolerance = 0.0001
    equal(e, -1.20257, energy_tolerance)
