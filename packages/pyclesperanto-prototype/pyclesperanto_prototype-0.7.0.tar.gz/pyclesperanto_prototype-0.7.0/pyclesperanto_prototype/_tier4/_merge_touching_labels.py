from pyclesperanto_prototype._tier0 import plugin_function
from pyclesperanto_prototype._tier0 import Image


@plugin_function
def merge_touching_labels(labels_input: Image, labels_destination: Image = None):
    """
    Takes a label image, determines which labels are touching, merges them, renumbers them and produces a new label
    image.

    Parameters
    ----------
    labels_input : Image
    labels_destination : Image

    Returns
    -------
    labels_destination : Image

    """
    from .._tier1 import generate_touch_matrix
    from .._tier1 import set_ramp_y
    from .._tier1 import transpose_xy
    from .._tier0 import create
    from .._tier1 import binary_or
    from .._tier1 import set_where_x_equals_y
    from .._tier1 import set_column
    from .._tier1 import set_row
    from .._tier1 import multiply_images
    from .._tier1 import maximum_y_projection
    from .._tier3 import close_index_gaps_in_label_map
    from .._tier1 import replace_intensities

    # touch matrices are half-filled. The upper right corner is empth
    touch_matrix = generate_touch_matrix(labels_input)

    # make a full matrix (in CLIJ2 we call them adjacency matrix
    touch_matrix_t = transpose_xy(touch_matrix)
    sum_touch_matrix = binary_or(touch_matrix, touch_matrix_t)
    set_where_x_equals_y(sum_touch_matrix, 1)

    # eliminate touches with background to not merge them
    set_column(sum_touch_matrix, 0, 0)
    set_row(sum_touch_matrix, 0, 0)

    # make a touch-matrix where intensities correspond to the label-ID
    label_id_vector = create([touch_matrix.shape[0], 1])
    set_ramp_y(label_id_vector)
    multiply_images(sum_touch_matrix, label_id_vector, touch_matrix)

    # the new list of label-IDs for each label is the maximum-y-projection of the matrix
    # if labels 2 and 3 should be merged, both have then label-ID 3
    label_id_vector = create([1, touch_matrix.shape[0]])
    maximum_y_projection(touch_matrix, label_id_vector)

    # renumber the labels
    new_labels = close_index_gaps_in_label_map(label_id_vector)

    # write the new labels into the label image
    labels_destination = replace_intensities(labels_input, new_labels, labels_destination)
    return labels_destination
