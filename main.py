import skimage as ski
import pytesseract as tess
import os
import numpy as np

import library as l
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

test_img = h.load_image("E:\\Tabletop_Sim_Custom\\Guards_of_Atlantis_II\\editted_images\\Arien\\arcane_swap_croptest.png")
print(f"Loading arcane_swap_croptest.png as Grayscale")
print(f"Starting to Crop")
cropped_img = crop.crop_image(test_img, crop.find_boundries(test_img))

print(f"Original Image: {test_img.shape}\n\n")
print(f"Cropped Image: {cropped_img.shape}")
print(f"Cropped Image Center Pixel = {cropped_img[int(cropped_img.shape[0] / 2), int(cropped_img.shape[1] / 2)]}")
ski.io.imsave("E:\\Tabletop_Sim_Custom\\Guards_of_Atlantis_II\\editted_images\\Arien\\arcane_swap_croptest_result.png", cropped_img)