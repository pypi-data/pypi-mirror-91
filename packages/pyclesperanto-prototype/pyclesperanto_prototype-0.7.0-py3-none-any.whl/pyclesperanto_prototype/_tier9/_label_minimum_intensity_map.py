from .._tier0 import plugin_function
from .._tier0 import Image
from .._tier0 import push
from .._tier1 import replace_intensities
from .._tier1 import set_column

@plugin_function(categories=['combine', 'label measurement', 'map', 'in assistant'], priority=-1)
def label_minimum_intensity_map(intensity_image : Image, labels : Image, minimum_intensity_map : Image = None):
    """

    Parameters
    ----------
    intensity_image
    labels
    minimum_intensity_map

    Returns
    -------

    """
    from .._tier9 import statistics_of_background_and_labelled_pixels

    regionprops = statistics_of_background_and_labelled_pixels(intensity_image, labels)
    from .._tier9 import push_regionprops_column

    values_vector = push_regionprops_column(regionprops, 'min_intensity')

    set_column(values_vector, 0, 0)

    minimum_intensity_map = replace_intensities(labels, values_vector, minimum_intensity_map)

    return minimum_intensity_map
