import os

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix


def confusion_plot(y, y_pred, 
    directory: str=None, 
    file_name: str=None, 
    figsize: tuple=(7, 7), 
    text_size:int =14, 
    save: bool=False, 
    show: bool=False, 
    normalize:bool=False, 
    title:str='Confusion matrix', 
    xlabel:str='Predicted class', 
    ylabel:str='Actual class', 
    cbar:bool=False):
    """Does Scikit Confusion Plot with colour format
    
    Args:
        y ([type]): [description]
        y_pred ([type]): [description]
        directory (str, optional): [description]. Defaults to None.
        file_name (str, optional): [description]. Defaults to None.
        figsize (tuple, optional): [description]. Defaults to (7, 7).
        text_size (int, optional): [description]. Defaults to 14.
        save (bool, optional): [description]. Defaults to False.
        show (bool, optional): [description]. Defaults to False.
        normalize (bool, optional): [description]. Defaults to False.
        title (str, optional): [description]. Defaults to 'Confusion matrix'.
        xlabel (str, optional): [description]. Defaults to 'Predicted class'.
        ylabel (str, optional): [description]. Defaults to 'Actual class'.
        cbar (bool, optional): [description]. Defaults to False.
    """
    labels = sorted(list(set(y)))
    cm = confusion_matrix(y, y_pred)

    if normalize:
        cm = cm.astype('float') * 100 / cm.sum(axis=1)[:, np.newaxis]

    mpl.rc("figure", figsize=figsize)  # subplot size

    hm = sns.heatmap(cm,
                     cbar=cbar,
                     annot=True,
                     square=True,
                     yticklabels=labels,
                     xticklabels=labels,
                     cmap='Blues',
                     linewidths=.5,
                     annot_kws={'size': text_size},  # text size
                     fmt='g'
                     )
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    if save:
        path = os.path.join(directory, file_name + '_confusion_matrix.png')
        plt.savefig(path, dpi=100)
    if show:
        plt.show()
    plt.clf()
