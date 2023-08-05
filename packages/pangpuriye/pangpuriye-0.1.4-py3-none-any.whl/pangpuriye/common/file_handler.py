import os

class FileHandler:
    
    def __init__(self):
        pass
    
    def get_byte(self, fpath):
        fbyte = None
        fname = None
        with open(fpath, "rb") as f:
            fname = os.path.splitext(os.path.basename(f.name))[0]
            fbyte = f.read()
        return fname, fbyte