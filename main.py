import sys
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
import library.enhancer as en

# The List of Games Currently Able to Process Images For
game_profile_list = ["GOA2", "Generic"]

# Supported Image Types
img_types_supported = [".png", ".jpg", ".jpeg"]

# The Filepath to the Tesseract EXE
path_to_tesseract = f"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Which Directory Are We Processing (if processing multiple images)
main_image_dir = f""

# All Subdirectories Within the Main Directory
dir_list = []

# All Image Files Within All Directories (Including Main Directory)
file_list = []

# The List of Images (classes.image) to Process
image_list = []

# The Filepath of the Image to Process (if processing a single image)
image_filepath = f""

# The Current Game Profile Being Processed
curr_game_profile = f""

# The Root Directory Where Edited Images Will Be Saved
save_dest = ""

def main():
    # Opening Log File
    settings.log_file = log.log(
        "logs/"
    )
    
    # Checking For and Grabbing Commandline Arguments
    if(len(sys.argv) > 1):
        args = sys.argv[1:] # Grab All Commandline Arguments
    else:
        settings.log_file.enter(f"A Source File or Directory Must Be Provided. Such As:\n\tmain.py C:\\Documents\\source.png")
        settings.log_file.close()
        sys.exit()
    
    source = args[0]
    
    settings.log_file.enter(f"Confirming Source Existance")
    if(not os.path.exists(source)):
        settings.log_file.enter(f"The Provided Source Filepath Does Not Exist!")
        settings.log_file.close()
        sys.exit()
    
    is_directory = os.path.isdir(source)
    
    if(is_directory):
        settings.log_file.enter(f"The Source is a Directory. Preparing to Edit All Images Inside")
        
        sub_dir_iter = 0
        main_image_dir = source
        
        # Ensure Proper Saving
        main_image_dir = h.ensure_folder_path(main_image_dir)
            
        # Grab Everything Within Main Image Directory
        settings.log_file.enter(f"Getting Information From {main_image_dir} and Subdirectories")
        for (dir_path, dir_names, file_names) in os.walk(main_image_dir):
            path = h.ensure_folder_path(dir_path)
            
            for dir in dir_names:
                dir_list.append(f"{path}{dir}\\")
            
            # Ensure Only Supported Image Files Are Grabbed
            for file in file_names:
                if(file[-4:] in img_types_supported or file[-5:] in img_types_supported): # file[-5:] Used to Catch .jpeg
                    file_list.append(f"{path}{file}")
                    
        settings.log_file.enter(f"Found: {len(dir_list)} Subdirectories and {len(file_list)} Images.", True)
        settings.log_file.enter(f"Preparing Image Files for Editing")
                          
        for file in file_list:
            filename, t_filepath, image_extension, r_filepath = h.seperate_file_info(file)
            new_img = image.image(
                n=filename,
                tfp=t_filepath,
                ie=image_extension,
                rfp=r_filepath,
                c=h.load_image(file),
                g=h.load_image(file, grayscale=True)
            )
            image_list.append(new_img)
            
        for img in image_list:
            settings.log_file.enter(f"Starting Edits of {img}")
            final_img = crop.crop_image(img, crop.find_boundries(img))
            
            if(type(final_img) == image.image):
                settings.log_file.enter(f"Cropped Image:\n\t{final_img}", True)
                settings.log_file.enter(f"Cleaning {final_img.name}'s Edges")
                final_img = crop.clean_image(final_img)
                settings.log_file.enter(f"Sharpening {final_img.name}")
                final_img = en.sharpen_image(final_img)
                if(save_dest == ""):
                    final_img.save(to_save="both")
                else:
                    final_img.save(to_save="both", dest=f"{save_dest}{final_img.relative_folder_path}")
            elif(type(final_img) == list):
                img_iter = 1
                for i in final_img:
                    i.name = f"{i.name}_{img_iter:02d}"
                    settings.log_file.enter(f"Cropped Image:\n\t{i}", True)
                    settings.log_file.enter(f"Cleaning {i.name}'s Edges")
                    i = crop.clean_image(i)
                    settings.log_file.enter(f"Sharpening {i.name}")
                    i = en.sharpen_image(i)
                    if(save_dest == ""):
                        i.save(to_save="both")
                    else:
                        i.save(to_save="both", dest=f"{save_dest}{final_img.relative_folder_path}")
                    img_iter += 1 
        
    else:
        settings.log_file.enter(f"The Source is a File. Preparing to Edit File")

        filename, t_filepath, image_extension, r_filepath = h.seperate_file_info(source)
        img = image.image(
            n=filename,
            tfp=t_filepath,
            ie=image_extension,
            rfp=r_filepath,
            c=h.load_image(source),
            g=h.load_image(source, grayscale=True)
        )
        
        settings.log_file.enter(f"Starting Edits of {img}")
        final_img = crop.crop_image(img, crop.find_boundries(img))

        if(type(final_img) == image.image):
            settings.log_file.enter(f"Cropped Image:\n\t{final_img}", True)
            settings.log_file.enter(f"Cleaning {final_img.name}'s Edges")
            final_img = crop.clean_image(final_img)
            settings.log_file.enter(f"Sharpening {final_img.name}")
            final_img = en.sharpen_image(final_img)
            if(save_dest == ""):
                final_img.save(to_save="both")
            else:
                final_img.save(to_save="both", dest=f"{save_dest}{final_img.relative_folder_path}")
        elif(type(final_img) == list):
            img_iter = 1
            for i in final_img:
                i.name = f"{i.name}_{img_iter:02d}"
                settings.log_file.enter(f"Cropped Image:\n\t{i}", True)
                settings.log_file.enter(f"Cleaning {i.name}'s Edges")
                i = crop.clean_image(i)
                settings.log_file.enter(f"Sharpening {i.name}")
                i = en.sharpen_image(i)
                if(save_dest == ""):
                    i.save(to_save="both")
                else:
                    i.save(to_save="both", dest=f"{save_dest}{final_img.relative_folder_path}")
                img_iter += 1 
        
    settings.log_file.close()
    
main()

