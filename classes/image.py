import datetime
import skimage as ski

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
    
    def __init__(self, n, fp, ie, c, g, ed=[]):
        self.name = n
        self.folder_path = fp
        self.image_extension = ie
        self.color = c
        self.grayscale = g
        self.row_size = c.shape[0]
        self.col_size = c.shape[1]
        
        self.add_edit(f"{n} Created.")
        
        if len(ed) > 0:
            for edit in ed:
                self.add_edit(f"{edit}")
                
    def crop(self, boundries):
        """Crops Both the Color and Grayscale Image Arrays to Keep Both Versions Synced.
        
        Parameters
        ----------
        boundries : list, required
            The Boundries to Crop the Image Arrays to. Order is Left, Upper, Right, Lower.
        """
        
        self.color = self.color[boundries[1]:boundries[3]+1,boundries[0]:boundries[2]+1]
        self.grayscale = self.grayscale[boundries[1]:boundries[3]+1,boundries[0]:boundries[2]+1]
        row_size = self.color.shape[0]
        col_size = self.color.shape[1]
                
        self.add_edit(f"{self.name} Image Cropped. \n\tBoundries = {boundries}; Final Size = [{row_size}, {col_size}]")
        
        return self
        
    def save(self, to_save="color"):
        """Saves the Image to Its Folder Path.
        
        Parameters
        ----------
        to_save : str, optional
            Which Way to Save the Image: Colored (\"color\"), Grayscale (\"gray\"), or Both (\"both\").
            Defaults to \"color\".
        """
        
        to_save = to_save.lower()
        
        if(to_save == "color"):
            ski.io.imsave(f"{self.folder_path}{self.name}{self.image_extension}", self.color)
            self.add_edit(f"{self.name} (Colored) Saved to {self.folder_path}{self.name}{self.image_extension}")
        elif(to_save == "gray"):
            ski.io.imsave(f"{self.folder_path}{self.name}{self.image_extension}", ski.util.img_as_ubyte(self.grayscale))
            self.add_edit(f"{self.name} (Grayscale) Saved to {self.folder_path}{self.name}{self.image_extension}")
        elif(to_save == "both"):
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
        print(edit_str)