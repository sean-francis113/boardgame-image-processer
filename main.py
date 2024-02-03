import skimage as ski
import pytesseract as tess
import os

import library as l
import library.helper as h

# The List of Games Currently Able to Process Images For
game_profile_list = ["GOA2"]

# The Filepath to the Tesseract EXE
path_to_tesseract = f"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Which Directory Are We Processing (if processing multiple images)
image_dir = f""

# The Filepath of the Image to Process (if processing a single image)
image_filepath = f""

# The Current Game Profile Being Processed
curr_game_profile = f""

#h.display_image_data(f"E:\\Tabletop_Sim_Custom\\Guards_of_Atlantis_II\\editted_images\\Arien\\arcane_swap.png", greyscale=True)