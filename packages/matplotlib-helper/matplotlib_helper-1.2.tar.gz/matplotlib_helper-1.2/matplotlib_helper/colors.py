import pickle
try:
    from colour import Color
except:
    print("please install colours package")
from math import sqrt
import pkgutil
import os
import random
this_dir, this_filename = os.path.split(__file__)



class colors():
    def __init__(self):
        DATA_PATH = os.path.join(this_dir, ".", "colors.data")
        self.data=pickle.load(open(DATA_PATH,"rb"))
        
        # self.data=pickle.load(pkgutil.get_data(__name__, "colors.data"))
        try:
            self.palette=[[Color("#"+i) for i in pal_list] for pal_list in self.data]
            self.colors=[[Color("#"+i) for i in pal_list] for pal_list in self.data]
        except:
            print("please install colours package")
        self.colors_string=[["#"+i for i in pal_list] for pal_list in self.data]
        self.n_colors=len(self.colors_string)
    def get_all_colors(self):
        return self.palette
    
    def get_random_colors(self,n=1,seed=2):
        """Generate random colors

        Args:
            n (int, optional): number of colors. Defaults to 1.
            seed (int, optional): seed for random. Defaults to 2.

        Returns:
            list: color list
        """        
        if n>1:
            colors=[]
            random.seed=seed
            for i in range(n):
                i=random.randrange(0,self.n_colors)
                j=random.randrange(0,len(self.colors[i]))
                colors.append(self.colors_string[i][j])
            return colors
        else:
            i=random.randrange(0,self.n_colors)
            j=random.randrange(0,len(self.colors[i]))
            return self.colors_string[i][j]
    