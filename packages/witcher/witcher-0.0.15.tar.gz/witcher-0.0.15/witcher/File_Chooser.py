############################################
#### Date   : 2021-01-17              ######
#### Author : Babak Emami             ######
#### Model  : Filechooser             ######
############################################

###### import requirments ##################

from ipywidgets import *
from tkinter import *
from tkinter.filedialog import *
import traitlets
from ipywidgets import widgets
from IPython.display import display
from tkinter import Tk, filedialog
import pandas as pd
import numpy as np
import cv2


############################################

class SelectFilesButton(widgets.Button):
    """
       Just call the function and get the filename, file path
        
       The magic function will read the CSV, Excel, SAS and image files automatically :)
       Example :
       File_chooser = SelectFilesButton()
       File_chooser # This will display the button in the context of Jupyter Notebook
    """
    def __init__(self,runapp=False):
        super(SelectFilesButton, self).__init__()
        # Add the selected_files trait
        self.add_traits(files=traitlets.traitlets.List())
        # Create the button.
        self.description = "Select Files"
        self.icon = "square-o"
        self.style.button_color = "orange"
        # Set on click behavior.
        self.on_click(self.select_files)
        
        
    def reader(file_path):
        tem=""
        file_type=file_path.split(".")[-1]
        tem_type=""
        if file_type in ['xport', 'sas7bdat']:
            tem_type ="sas"
        elif "xl" in file_type:
            tem_type = "excel" 
        elif "csv" in file_type:
            tem_type = "csv"  
        elif file_type in ["jpg","png","gif","jpeg"]:
            tem_type = "img"    
        else:
            tem_type=file_type
        tem="read_"+tem_type
        if tem_type in ['csv','excel','sas']:
            return getattr(pd,tem )(file_path, encoding=None)
        elif tem_type in ["img"]: 
            return cv2.imread(file_path)
        else:            
            return np.nan
    @staticmethod
    def select_files(b):
        """Generate instance of tkinter.filedialog.
        Parameters
        ----------
        b : obj:
            An instance of ipywidgets.widgets.Button 
        """
        # Create Tk root
        root = Tk()
        # Hide the main window
        root.withdraw()
        # Raise the root to the top of all windows.
        root.call('wm', 'attributes', '.', '-topmost', True)
        # List of selected fileswill be set to b.value
        b.files = filedialog.askopenfilename(multiple=True)

        b.description = "Files Selected"
        b.icon = "check-square-o"
        b.style.button_color = "lightgreen"
        print(b.files[0])
        tem=b.files[0].split(".")[-1]
        if tem in ["csv","xls","xlsx","sas","png","gif","jp"]:
            b.df=SelectFilesButton.reader(b.files[0])
                  
###################################################################################
#### sample:
#### my_button = SelectFilesButton()
#### my_button # This will display the button in the context of Jupyter Notebook
###################################################################################

###################################################################################


###################################################################################



        
    
    
    
    
