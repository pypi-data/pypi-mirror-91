from ase.build import molecule

from gpaw import GPAW, FermiDirac
from gpaw.cluster import Cluster
from gpaw.lrtddft import LrTDDFT


def test_lrtddft(in_tmp_dir):
    from ase.vibrations.resonant_raman import ResonantRamanCalculator
    h = 0.25
    H2 = Cluster(molecule('H2'))
    H2.minimal_box(3., h=h)
    H2.calc = GPAW(h=h, occupations=FermiDirac(width=0.2),
                   symmetry='off')

    rr = ResonantRamanCalculator(
        H2, LrTDDFT, exkwargs={'restrict': {'energy_range': 15}})
    rr.run()
