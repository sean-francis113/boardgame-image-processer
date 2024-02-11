import library.settings as settings

import skimage as ski
import numpy

def load_image(img_path, grayscale = False):
    """Takes an Image's Filepath, Loads It (As Greyscale If Requested) with Skimage, Then Returns the Loaded Image.
    
    Parameters
    ----------
    img_path : str, required
        The Full Filepath of the Image 
    """

    settings.log_file.enter(f"Attempting to Load {img_path} With Grayscale={grayscale}")
    # Attempts to Load Image
    img = ski.io.imread(img_path, as_gray=grayscale)

    # Check if Image Was Not Loaded as Greyscale
    if(grayscale == False):

        # The Number of Color Channels in the Image (3 = RGB, 4 = RGBA)
        max_channels = img.shape[-1]
        settings.log_file.enter(f"Channels: {max_channels}", True)
        
        if(max_channels != 4):
            settings.log_file.enter(f"Converting Image to RGBA")
            img = rgb2rgba(img)
        
    return img

def rgb2rgba(img):
    """Converts the Provided Image from RGB to RGBA, Adding Alpha Values to Every Pixel.
    
    Parameters
    ----------
    img : ndarray, required
        The Loaded Image to Convert
    
    Returns
    -------
    The Converted Image, as an ndarray
    """
    
    return numpy.insert(img, 3, 255, axis=2)

def display_image_data(img_path, grayscale = False):
    """Tester Function to Display the Dimensions and Channels of an Image.
    
    Parameters
    ----------
    img_path : str, required
        The Full Filepath of the Image
    """
    
    img = load_image(img_path, grayscale)
    print(img.shape)
    print(img[0,0])
    
def ensure_folder_path(path:str):
    """Ensures There is a Forwardslash (\\) at the End of the Folder Path
    
    Parameters
    ----------
    path : str, required
        The Path to Ensure
    """
    
    if(path[-1] != "\\"):
        return f"{path}\\"
    else:
        return path
    
def seperate_file_info(filepath:str, parent_dir=""):
    """Seperates the Filepath Into Filename, True Filepath, File Extension, and Relative Filepath. 
    If parent_dir is Provided, Relative Filepath is the Filepath with parent_dir Removed. Otherwise, it is an Empty String.

    Args:
        filepath (str): The Filepath to Seperate Out.
        parent_dir (str, optional): The Directory to Remove from Relative Filepath. If Not Provided, Relative Filepath is Empty. Defaults to "".
    """
    
    str_list = filepath.split("\\")
    file_name_full = str_list[-1]
    file_name = file_name_full.split(".")[0]
    true_filepath = ensure_folder_path("\\".join(str_list[:-1]))
    file_extension = f".{file_name_full.split('.')[1]}"
    relative_filepath = ""
    if(parent_dir != ""):
        relative_filepath = ensure_folder_path(true_filepath.replace(parent_dir, ""))
        
    return file_name, true_filepath, file_extension, relative_filepath