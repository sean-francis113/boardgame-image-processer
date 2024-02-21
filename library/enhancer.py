import library.settings as settings
import skimage as ski
import classes.image as image
import library.helper as h

from copy import deepcopy

def sharpen_image(img : image, radius=2.5, amount=2.0):
    """Sharpens the Provided Image and Returns It.

    Parameters
    ----------
    img : classes.image, required

    """

    s_img : image = deepcopy(img)

    # Convert Color Image to YUV
    settings.log_file.enter(f"Converting {s_img.name} to YUV")
    h.rgba2rgb(s_img)
    s_img.name += "_simg"
    s_img.save(to_save="color")
    s_img.name = s_img.name.replace("_simg", "")
    h.rgb2yuv(s_img)
    s_img.name += "_yuv"
    s_img.save(to_save="color")
    s_img.name = s_img.name.replace("_yuv", "")

    # Grab Luminence Band
    settings.log_file.enter(f"Grabbing Luminence Band of {s_img.name}")
    y_band = s_img.color[..., 0]
    
    # Sharpen The Image
    y_band = ski.filters.unsharp_mask(y_band, radius, amount)
    s_img.grayscale = ski.filters.unsharp_mask(s_img.grayscale, radius, amount)
    s_img.add_edit(f"Sharpened {s_img.name} With Radius {radius} and Amount {amount}")

    # Add Y Band Back Into Image
    settings.log_file.enter(f"Adding Luminence Back to {s_img.name}")
    row_iter = 0
    col_iter = 0
    while row_iter < s_img.row_size:
        col_iter = 0
        while col_iter < s_img.col_size:
            s_img.color[row_iter, col_iter][0] = y_band[row_iter, col_iter]
            col_iter += 1
        row_iter += 1

    # Convert Image Back to RGBA
    settings.log_file.enter(f"Converting {s_img.name} to RGBA")
    s_img.color = ski.color.yuv2rgb(s_img.color)
    s_img.color = h.rgb2rgba(s_img.color)

    # Restore Transparency
    settings.log_file.enter(f"Restoring {s_img.name}'s Transparency")
    s_img.restore_transparency()

    print(s_img.color.shape)

    return s_img
