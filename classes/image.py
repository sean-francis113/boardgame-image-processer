import library.settings as settings

import datetime
import skimage as ski
import os

from copy import deepcopy

class image:
    """Class for Holding Data About an Image, Including a Grayscale Copy, Edges, Changes Made, and More."""

    name = ""
    folder_path = ""
    image_extension = ""
    color = None
    grayscale = None
    row_size = 0
    col_size = 0
    edits_done = []
    
    def __init__(self, n, fp, ie, c=None, g=None, ed=[]) -> None:
        self.name = n
        self.folder_path = fp
        self.image_extension = ie
        self.color = c
        self.grayscale = g
        
        if(c is None and g is None):
            self.row_size = 0
            self.col_size = 0
        else:
            if(c is not None):
                self.row_size = c.shape[0]
                self.col_size = c.shape[1]
            elif(g is not None):
                self.row_size = g.shape[0]
                self.col_size = g.shape[1]
                
        self.add_edit(f"{n} Created.")
        
        if len(ed) > 0:
            for edit in ed:
                self.add_edit(f"{edit}")
                
    def __str__(self) -> str:
        return f"Name: {self.name}\n\tPath: {self.folder_path}\n\tImage Type: {self.image_extension}\n\tImage Size: {self.row_size} X {self.col_size}\n"
                
    def crop(self, boundries):
        """Crops Both the Color and Grayscale Image Arrays to Keep Both Versions Synced.
        
        Parameters
        ----------
        boundries : list, required
            The Boundries to Crop the Image Arrays to. Order is Left, Upper, Right, Lower.
        """
        
        self.color = self.color[boundries[1]:boundries[3]+1,boundries[0]:boundries[2]+1]
        self.grayscale = self.grayscale[boundries[1]:boundries[3]+1,boundries[0]:boundries[2]+1]
        self.row_size = (boundries[3]+1) - (boundries[1])
        self.col_size = (boundries[2]+1) - (boundries[0])
                
        self.add_edit(f"{self.name} Image Cropped. \n\tBoundries = {boundries}; Final Size = [{self.row_size}, {self.col_size}]")
        
        return self
        
    def save(self, to_save="color"):
        """Saves the Image to Its Folder Path.
        
        Parameters
        ----------
        to_save : str, optional
            Which Way to Save the Image: Colored (\"color\"), Grayscale (\"gray\"), or Both (\"both\").
            Defaults to \"color\".
        """
        
        settings.log_file.enter(f"Attempting to Save {self.name}")
        
        to_save = to_save.lower()
        
        if(not os.path.exists(self.folder_path)): os.mkdir(self.folder_path)
        
        if(to_save == "color"):
            settings.log_file.enter(f"Saving Color Image Only")
            ski.io.imsave(f"{self.folder_path}{self.name}{self.image_extension}", self.color)
            self.add_edit(f"{self.name} (Colored) Saved to {self.folder_path}{self.name}{self.image_extension}")
        elif(to_save == "gray"):
            settings.log_file.enter(f"Saving Grayscale Image Only")
            ski.io.imsave(f"{self.folder_path}{self.name}{self.image_extension}", ski.util.img_as_ubyte(self.grayscale))
            self.add_edit(f"{self.name} (Grayscale) Saved to {self.folder_path}{self.name}{self.image_extension}")
        elif(to_save == "both"):
            settings.log_file.enter(f"Saving Both Color and Grayscale Images")
            ski.io.imsave(f"{self.folder_path}{self.name}_color{self.image_extension}", self.color)
            self.add_edit(f"{self.name} (Colored) Saved to {self.folder_path}{self.name}_color{self.image_extension}")
            ski.io.imsave(f"{self.folder_path}{self.name}_grayscale{self.image_extension}", ski.util.img_as_ubyte(self.grayscale))
            self.add_edit(f"{self.name} (Grayscale) Saved to {self.folder_path}{self.name}_grayscale{self.image_extension}")
                
        edits_file = open(f"{self.folder_path}{self.name}_edits.txt", "a")
        for edit in self.edits_done:
            edits_file.write(f"{edit}\n")
        edits_file.close()
                    
    def add_edit(self, str):
        """Adds a New Edit to the Image's Edits Done and Prints the String.
        
        Parameters
        ----------
        str : string, required
            The String to Add to Edits Done.
        """
        
        date = datetime.datetime.now()
        
        date_str = f"[{date.month}-{date.day}-{date.year}: {date.hour}:{date.minute}:{date.second}]"
        
        edit_str = f"{date_str}: {str}"
        
        self.edits_done.append(edit_str)
        settings.log_file.enter(edit_str)
        
    def white_out(self, boundries):
        """Sets All Pixels Inside of Boundry to White.
        
        Parameters
        ----------
        boundry : list, required
            The Boundries to Set the Pixels in.
        """
        
        row_iter = boundries[1]
        col_iter = boundries[0]
        
        while(row_iter < boundries[3] + 1):
            col_iter = boundries[0]
            while(col_iter < boundries[2] + 1):
                self.color[row_iter, col_iter] = [255,255,255,255]
                self.grayscale[row_iter, col_iter] = 1.0
                col_iter += 1
            row_iter += 1
        
        return self
    
    def copy_from(self, img):
        """Copies the Color and Greyscale Images from img.

        Args:
            img (classes.image): The Image to Copy From
        """
        
        self.color = deepcopy(img.color)
        self.grayscale = deepcopy(img.grayscale)
        self.row_size = deepcopy(img.row_size)
        self.col_size = deepcopy(img.col_size)
        
        self.add_edit(f"Copied Images from {img.name}")