import pytest
from ase import Atom, Atoms
from ase.units import Bohr
from ase.parallel import parprint
from gpaw import GPAW
from gpaw.test import equal
from gpaw.lrtddft import LrTDDFT
from gpaw.mpi import world
from gpaw.lrtddft.excited_state import ExcitedState


@pytest.fixture
def H2struct():
    R = 0.7  # approx. experimental bond length
    a = 3.0
    c = 4.0
    return Atoms([Atom('H', (a / 2, a / 2, (c - R) / 2)),
                  Atom('H', (a / 2, a / 2, (c + R) / 2))],
                 cell=(a, a, c))


@pytest.fixture
def H2(H2struct):
    H2 = H2struct.copy()
    H2.calc = GPAW(xc='PBE',
                   poissonsolver={'name': 'fd'},
                   nbands=3, spinpol=False)
    H2.get_potential_energy()
    return H2


@pytest.fixture
def H2spin(H2struct):
    H2 = H2struct.copy()
    H2.calc = GPAW(xc='PBE', nbands=2,
                   poissonsolver={'name': 'fd'},
                   spinpol=True, parallel={'domain': world.size})
    H2.get_potential_energy()
    return H2


@pytest.fixture
def lr(H2):
    """LrTDDFT object without spin"""
    lr = LrTDDFT(H2.calc, xc='LDA')
    lr.diagonalize()
    return lr


@pytest.fixture
def lr_vspin(H2):
    lr = LrTDDFT(H2.calc, xc='LDA', nspins=2)
    lr.diagonalize()
    return lr


@pytest.fixture
def lr_spin(H2spin):
    lr = LrTDDFT(H2spin.calc, xc='LDA', nspins=2)
    lr.diagonalize()
    return lr


def test_finegrid(H2, lr):
    for finegrid in [1, 0]:
        lr2 = LrTDDFT(H2.calc, xc='LDA', finegrid=finegrid)
        lr2.diagonalize()
        parprint('finegrid, t1, t3=', finegrid, lr[0], lr2[0])
        equal(lr[0].get_energy(), lr2[0].get_energy(), 5.e-4)


def test_velocity_form(lr):
    for ozr, ozv in zip(lr[0].get_oscillator_strength(),
                        lr[0].get_oscillator_strength('v')):
        equal(ozr, ozv, 0.1)


def test_singlet_triplet(lr_vspin, lr_spin):
    # singlet/triplet separation
    singlet, triplet = lr_vspin.singlets_triplets()

    # singlet/triplet separation
    precision = 1.e-5
    singlet.diagonalize()
    equal(singlet[0].get_energy(), lr_spin[1].get_energy(), precision)
    equal(singlet[0].get_oscillator_strength()[0],
          lr_spin[1].get_oscillator_strength()[0], precision)
    triplet.diagonalize()
    equal(triplet[0].get_oscillator_strength()[0], 0)
    equal(triplet[0].get_energy(), lr_spin[0].get_energy(), precision)
    equal(triplet[0].get_oscillator_strength()[0], 0)


def test_spin(lr, lr_vspin, lr_spin):
    # without spin
    t1 = lr[0]
    ex = ExcitedState(lr, 0)
    den = ex.get_pseudo_density() * Bohr**3

    # with spin

    # the triplet is lower, so that the second is the first singlet
    # excited state
    t2 = lr_vspin[1]
    ex_vspin = ExcitedState(lr_vspin, 1)
    den_vspin = ex_vspin.get_pseudo_density() * Bohr**3

    parprint('with virtual/wo spin t2, t1=',
             t2.get_energy(), t1 .get_energy())
    equal(t1.get_energy(), t2.get_energy(), 5.e-7)
    gd = lr.calculator.density.gd
    finegd = lr.calculator.density.finegd
    ddiff = gd.integrate(abs(den - den_vspin))
    parprint('   density integral, difference=',
             gd.integrate(den), gd.integrate(den_vspin), ddiff)
    parprint('   aed density integral',
             finegd.integrate(ex.get_all_electron_density() * Bohr**3),
             finegd.integrate(ex_vspin.get_all_electron_density() *
                              Bohr**3))
    assert(ddiff < 1.e-4)

    for i in range(2):
        parprint('i, real, virtual spin: ', i, lr_vspin[i], lr_spin[i])
        equal(lr_vspin[i].get_energy(), lr_spin[i].get_energy(), 6.e-6)
        ex_vspin = ExcitedState(lr_vspin, i)
        den_vspin = ex_vspin.get_pseudo_density() * Bohr**3
        ex_spin = ExcitedState(lr_spin, i)
        den_spin = ex_spin.get_pseudo_density() * Bohr**3
        ddiff = gd.integrate(abs(den_vspin - den_spin))
        parprint('   density integral, difference=',
                 gd.integrate(den_vspin), gd.integrate(den_spin),
                 ddiff)
        parprint('   aed density integral',
                 finegd.integrate(ex_vspin.get_all_electron_density()
                                  * Bohr**3),
                 finegd.integrate(ex_spin.get_all_electron_density()
                                  * Bohr**3))
        assert(ddiff < 3.e-3), ddiff


def test_io(in_tmp_dir, lr):
    fname = 'lr.dat.gz'
    lr.write(fname)
    world.barrier()

    lr2 = LrTDDFT.read(fname)
    lr2.diagonalize()
    
    equal(lr[0].get_energy(), lr2[0].get_energy(), 1e-6)
