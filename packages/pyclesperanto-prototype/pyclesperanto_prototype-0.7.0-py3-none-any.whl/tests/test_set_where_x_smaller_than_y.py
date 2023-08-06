import pyclesperanto_prototype as cle
import numpy as np


def test_set_where_x_smaller_than_y():
    result = cle.push(np.asarray([
        [0, 0, 0, 1],
        [0, 0, 3, 1],
        [0, 0, 3, 1],
        [1, 1, 1, 1]
    ]).T)

    reference = cle.push(np.asarray([
        [0, 3, 3, 3],
        [0, 0, 3, 3],
        [0, 0, 3, 3],
        [1, 1, 1, 1]
    ]).T)

    cle.set_where_x_smaller_than_y(result, 3)

    a = cle.pull(result)
    b = cle.pull(reference)
    print(a)

    assert (np.array_equal(a, b))
