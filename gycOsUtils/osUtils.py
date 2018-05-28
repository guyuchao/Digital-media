import os

class osutils:
    def add_tmp_in_filename(self,filename):
        filename, extension = os.path.splitext(filename)
        new_filename=filename+"_tmp"+extension
        return new_filename

    def get_extension(self,filename):
        _, extension = os.path.splitext(filename)
        return extension