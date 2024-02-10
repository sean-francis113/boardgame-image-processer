import library.settings as settings

import skimage as ski
import pytesseract as tess
import os
import numpy as np

import library as l
import classes as c
import classes.image as image
import classes.log as log
import library.helper as h
import library.cropper as crop

# The List of Games Currently Able to Process Images For
game_profile_list = ["GOA2", "Generic"]

# The Filepath to the Tesseract EXE
path_to_tesseract = f"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Which Directory Are We Processing (if processing multiple images)
image_dir = f""

# The Filepath of the Image to Process (if processing a single image)
image_filepath = f""

# The Current Game Profile Being Processed
curr_game_profile = f""

settings.log_file = log.log(
    "logs/"
)

settings.log_file.enter("Creating New Image")

test_img = image.image(
    n="arcane_swap_croptest",
    fp="E:\\Tabletop_Sim_Custom\\Guards_of_Atlantis_II\\editted_images\\Arien\\",
    ie=".png", 
    c=h.load_image("E:\\Tabletop_Sim_Custom\\Guards_of_Atlantis_II\\editted_images\\Arien\\arcane_swap_croptest.png"),
    g=h.load_image("E:\\Tabletop_Sim_Custom\\Guards_of_Atlantis_II\\editted_images\\Arien\\arcane_swap_croptest.png", greyscale=True)
    )

original_img = image.image(
    n="multi_card_croptest_original",
    fp="E:\\Tabletop_Sim_Custom\\Guards_of_Atlantis_II\\editted_images\\Arien\\",
    ie=".png"
)
original_img.copy_from(test_img)

settings.log_file.enter(f"Created Image:\n\t{test_img}", True)

settings.log_file.enter(f"Starting Crop of {test_img.name}")
final_img = crop.crop_image(test_img, crop.find_boundries(test_img))

if(type(final_img) == image.image):
    settings.log_file.enter(f"Cropped Image:\n\t{final_img}", True)
    final_img.save(to_save="both")
    settings.log_file.close()
elif(type(final_img) == list):
    for img in final_img:
        settings.log_file.enter(f"Cropped Image:\n\t{img}", True)
        img.save(to_save="both")
    
    settings.log_file.close()