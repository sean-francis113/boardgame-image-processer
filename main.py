import skimage as ski
import pytesseract as tess
import os
import numpy as np

import library as l
import classes as c
import classes.image as image
import library.helper as h
import library.cropper as crop

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

test_img = image.image(
    "arcane_swap_croptest",
    "E:\\Tabletop_Sim_Custom\\Guards_of_Atlantis_II\\editted_images\\Arien\\",
    ".png", 
    h.load_image("E:\\Tabletop_Sim_Custom\\Guards_of_Atlantis_II\\editted_images\\Arien\\arcane_swap_croptest.png"),
    h.load_image("E:\\Tabletop_Sim_Custom\\Guards_of_Atlantis_II\\editted_images\\Arien\\arcane_swap_croptest.png", greyscale=True)
    )
original_img = test_img

print(f"Starting Crop of {test_img.name}")
test_img = crop.crop_image(test_img, crop.find_boundries(test_img))

print(f"Original Image: {original_img.color.shape}\n\n")
print(f"Cropped Image: {test_img.color.shape}")
test_img.save(to_save="both")