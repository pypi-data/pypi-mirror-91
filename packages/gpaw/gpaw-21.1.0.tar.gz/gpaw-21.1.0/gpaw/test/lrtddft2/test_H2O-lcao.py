import numpy as np

from ase.build import molecule

from gpaw import GPAW
from gpaw.lrtddft2 import LrTDDFT2
from gpaw.test import equal


def test_lrtddft2_H2O_lcao(in_tmp_dir):
    name = 'H2O-lcao'
    atoms = molecule('H2O')
    atoms.center(vacuum=4)

    # Ground state
    calc = GPAW(h=0.4, mode='lcao', basis='dzp', txt='%s-gs.out' % name,
                poissonsolver={'name': 'fd'},
                nbands=8, xc='LDA')
    atoms.calc = calc
    atoms.get_potential_energy()
    calc.write('%s.gpw' % name, mode='all')

    # LrTDDFT2
    calc = GPAW('%s.gpw' % name, txt='%s-lr.out' % name)
    lr = LrTDDFT2(name, calc, fxc='LDA')
    lr.calculate()
    results = lr.get_transitions()[0:2]

    if 0:
        np.set_printoptions(precision=10)
        refstr = repr(results)
        refstr = refstr.replace('array', 'np.array')
        # Format a pep-compatible output
        refstr = ' '.join(refstr.split())
        refstr = refstr.replace('[ ', '[')
        refstr = refstr.replace(', np', ',\n       np')
        refstr = refstr.replace(', ', ',\n                 ')
        print('ref = %s' % refstr)

    ref = (np.array([6.0832418565,
                     8.8741524165,
                     13.5935582927,
                     14.291759976,
                     15.9923574087,
                     16.9926770576,
                     17.6505087373,
                     17.6924715713,
                     24.092978682,
                     25.0027646421,
                     25.6208743025,
                     26.9649406073,
                     29.5294888977,
                     29.8439220428]),
           np.array([3.6910848669e-02,
                     5.4510953134e-24,
                     3.0995301001e-01,
                     2.1335662795e-02,
                     7.8725024176e-22,
                     6.3875174151e-02,
                     1.0288169027e-01,
                     1.7216407337e-01,
                     2.8901383040e-02,
                     3.9354412451e-01,
                     2.1917641289e-02,
                     6.7746017219e-01,
                     7.9561718249e-02,
                     1.0625830362e-02]))

    tol = 1e-3
    for r0, r1 in zip(results, ref):
        equal(r0, r1, tol)
