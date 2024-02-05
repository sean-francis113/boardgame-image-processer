import datetime

class log:
    folder_path = ""
    filename = ""
    file_extension = ""
    file = None
    start_time = None
    log_list = []
    
    def __init__(self, fp, fn="", fe=".txt"):
        start_time = datetime.datetime.now()
        self.folder_path = fp
        if(fn==""): self.filename = f"log_{start_time.year}-{start_time.month}-{start_time.day}_{start_time.hour}-{start_time.minute}-{start_time.second}"
        else: self.filename = fn
        self.file_extension = fe
        
        self.file = open(f"{self.folder_path}{self.filename}{self.file_extension}", "w")
        
        self.enter("Opened Log")
        
    def enter(self, str, remove_ellipses=False):
        """Adds a New Entry to the Log and Prints the String.
        
        Parameters
        ----------
        str : string, required
            The String to Add to Log.
        """
        
        date = datetime.datetime.now()
        
        date_str = f"[{date.month}-{date.day}-{date.year}: {date.hour}:{date.minute}:{date.second}]"
        
        if(remove_ellipses): date_str = f"{date_str}: {str}\n"
        else: date_str = f"{date_str}: {str}...\n"
        
        self.file.write(date_str)
        print(date_str)
        
    def close(self):
        """Closes the Log File, After Adding One Last Message to it."""
        
        self.enter("Closing Log")
        self.file.close()