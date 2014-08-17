import numpy as np
import matplotlib.pyplot as plt


def generate(title, y_label, y_values, x_values):
    N = len(y_values)
    menStd = (2, 3, 4, 5)

    ind = np.arange(N)
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, y_values, width, color='r', yerr=menStd)

    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(ind+width)
    ax.set_xticklabels( x_values )

    add_labels(rects1,ax)

    plt.show()

def add_labels(rects, ax):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height), ha='center', va='bottom')
