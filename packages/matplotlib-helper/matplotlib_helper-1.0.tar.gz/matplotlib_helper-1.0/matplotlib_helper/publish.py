import matplotlib.pyplot as plt 

def add_labels(ax,fontsize=12,labels=[],x=-.12,y=1.02):
    """Add labels to axis in top left corner

    Args:
        ax (axis): list of axis
        fontsize (float, optional): font size. Defaults to 12.
        labels (list, optional): labels. Defaults to [].
        x (float, optional): x axis position. Defaults to -.12.
        y (float, optional): y axis position. Defaults to 1.02.
    """
    if len(labels)==0:
        for j,i in enumerate(ax):i.text(x,y,f"({chr(97+j)})",horizontalalignment='center',
                                                    verticalalignment='center',
                                                    transform = i.transAxes,fontsize=fontsize)
    