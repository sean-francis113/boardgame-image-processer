import skimage as ski
import numpy

def load_image(img_path, greyscale = False):
    """Takes an Image's Filepath, Loads It (As Greyscale If Requested) with Skimage, Then Returns the Loaded Image.
    
    Parameters
    ----------
    img_path : str, required
        The Full Filepath of the Image 
    """

    # Attempts to Return the Loaded Image
    img = ski.io.imread(img_path, as_gray=greyscale)

    # Check if Image Was Not Loaded as Greyscale
    if(greyscale == False):

        # The Number of Color Channels in the Image (2 = Greyscale, 3 = RGB, 4 = RGBA)
        max_channels = img.shape[-1]
        
        if(max_channels != 4):
            img = rgb2rgba(img)
        
    return img

def rgb2rgba(img):
    return numpy.insert(img, 3, 255, axis=2)

def display_image_data(img_path, greyscale = False):
    """Tester Function to Display the Dimensions and Channels of an Image.
    
    Parameters
    ----------
    img_path : str, required
        The Full Filepath of the Image
    """
    
    img = load_image(img_path, greyscale)
    print(img.shape)
    print(img[0,0])