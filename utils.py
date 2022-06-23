import numpy as np
from PIL import Image


def normalise(arr: Image) -> Image:
    """
    From https://stackoverflow.com/questions/7422204/intensity-normalization-of-image-using-pythonpil-speed-issues
    Linear normalization
    http://en.wikipedia.org/wiki/Normalization_%28image_processing%29
    """
    arr = np.array(arr)
    arr = arr.astype("float")
    # Do not touch the alpha channel
    for i in range(3):
        minval = arr[..., i].min()
        maxval = arr[..., i].max()
        if minval != maxval:
            arr[..., i] -= minval
            arr[..., i] *= 255.0 / (maxval - minval)

    arr = Image.fromarray(arr.astype("uint8"), "RGB")
    return arr
