import pyclesperanto_prototype as cle
import numpy as np

def test_mode_of_touching_neighbors_map():

    intensities = cle.push(np.asarray([
        [0, 0, 2, 5],
        [0, 3, 1, 2],
        [0, 4, 3, 0],
        [0, 0, 0, 0]
    ]))

    labels = cle.push(np.asarray([
        [0, 0, 2, 5],
        [0, 3, 1, 2],
        [0, 4, 3, 0],
        [0, 0, 0, 0],
    ]))

    reference = cle.push(np.asarray([
        [0, 0, 1, 2],
        [0, 1, 2, 1],
        [0, 3, 1, 0],
        [0, 0, 0, 0],
    ]
    )) # not sure if this is deterministically always those values... let's see over time

    result = cle.mode_of_touching_neighbors_map(intensities, labels)

    a = cle.pull(result)
    b = cle.pull(reference)

    print(a)
    print(b)

    assert (np.allclose(a, b, 0.001))
