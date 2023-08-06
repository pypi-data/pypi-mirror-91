from .._tier0 import create
from .._tier1 import minimum_sphere
from .._tier1 import maximum_sphere
from .._tier1 import add_images_weighted
from .._tier0 import plugin_function
from .._tier0 import Image

@plugin_function(categories=['filter', 'background removal'])
def top_hat_sphere(input : Image, destination : Image = None, radius_x : float = 1, radius_y : float = 1, radius_z : float = 1):
    """Applies a top-hat filter for background subtraction to the input image.
    
    Parameters
    ----------
    input : Image
        The input image where the background is subtracted from.
    destination : Image
        The output image where results are written into.
    radius_x : Image
        Radius of the background determination region in X.
    radius_y : Image
        Radius of the background determination region in Y.
    radius_z : Image
        Radius of the background determination region in Z.
     
    
    Returns
    -------
    destination
    
    Examples
    --------
    >>> import pyclesperanto_prototype as cle
    >>> cle.top_hat_sphere(input, destination, radiusX, radiusY, radiusZ)
    
    References
    ----------
    .. [1] https://clij.github.io/clij2-docs/reference_topHatSphere
    """


    temp1 = create(input.shape)
    temp2 = create(input.shape)

    minimum_sphere(input, temp1, radius_x, radius_y, radius_z)
    maximum_sphere(temp1, temp2, radius_x, radius_y, radius_z)
    add_images_weighted(input, temp2, destination, 1, -1)
    return destination