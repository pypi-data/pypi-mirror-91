import numpy as np
from gpaw.mpi import world, send, receive, broadcast_array


def test_send_receive_object():
    if world.size == 1:
        return
    obj = (42, 'hello')
    if world.rank == 0:
        send(obj, 1, world)
    elif world.rank == 1:
        assert obj == receive(0, world)


def test_bcast_array():
    new = world.new_communicator

    if world.size == 2:
        comms = [world]
    elif world.size == 4:
        ranks = np.array([[0, 1], [2, 3]])
        comms = [new(ranks[world.rank // 2]),
                 new(ranks[:, world.rank % 2])]
    elif world.size == 8:
        ranks = [[[0, 1], [0, 2], [0, 4]],
                 [[0, 1], [1, 3], [1, 5]],
                 [[2, 3], [0, 2], [2, 6]],
                 [[2, 3], [1, 3], [3, 7]],
                 [[4, 5], [4, 6], [0, 4]],
                 [[4, 5], [5, 7], [1, 5]],
                 [[6, 7], [4, 6], [2, 6]],
                 [[6, 7], [5, 7], [3, 7]]]
        comms = [new(r) for r in ranks[world.rank]]
    else:
        return

    array = np.zeros(3, int)
    if world.rank == 0:
        array[:] = 42

    out = broadcast_array(array, *comms)
    assert (out == 42).all()
