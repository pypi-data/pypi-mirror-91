import numpy as np
import pytest

from gpaw.atom.generator2 import generate
from gpaw.setup import Setup
from gpaw.xc import XC


@pytest.mark.serial
def test_lithium(in_tmp_dir):
    G = generate('Li', 3, '2s,2p,s', [2.1, 2.1], 2.0, None, 2, 'PBE', True)
    assert G.check_all()
    basis = G.create_basis_set()
    basis.write_xml()
    setup = G.make_paw_setup('test')
    setup.write_xml()


@pytest.mark.serial
def test_pseudo_h(in_tmp_dir):
    G = generate('H', 1.25, '1s,s', [0.9], 0.7, None, 2, 'PBE', True)
    assert G.check_all()
    basis = G.create_basis_set()
    basis.write_xml()
    setup = G.make_paw_setup('test')
    setup.write_xml()

    xc = XC('PBE')
    T_Lqp = Setup(setup,
                  xc,
                  lmax=2).calculate_T_Lqp(1, 3, 2,
                                          jlL_i=[(0, 0, 0), (1, 0, 0)])
    print(T_Lqp)
    assert (T_Lqp[1:] == 0.0).all()
    assert T_Lqp[0] == pytest.approx(np.eye(3) / (4 * np.pi)**0.5)
