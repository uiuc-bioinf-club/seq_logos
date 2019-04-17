import matplotlib as mpl
mpl.use('agg')
import seaborn
import matplotlib.pyplot as plt
plt.style.use('seaborn-ticks')
from matplotlib import transforms
import matplotlib.patheffects
from matplotlib.font_manager import FontProperties
import numpy as np
import argparse

COLOR_SCHEME = {'G': 'orange', 
                'A': 'red', 
                'C': 'blue', 
                'T': 'darkgreen'}

BASES = list(COLOR_SCHEME.keys())

class Scale(matplotlib.patheffects.RendererBase):
    def __init__(self, sx, sy=None):
        self._sx = sx
        self._sy = sy

    def draw_path(self, renderer, gc, tpath, affine, rgbFace):
        affine = affine.identity().scale(self._sx, self._sy)+affine
        renderer.draw_path(gc, tpath, affine, rgbFace)
        
def logo_from_map(all_scores, fontfamily='Arial', size=80, stretch=5, savefile=None):
    if fontfamily == 'xkcd':
        plt.xkcd()
    else:
        mpl.rcParams['font.family'] = fontfamily

    fig, ax = plt.subplots(figsize=(len(all_scores), 2.5))

    font = FontProperties()
    font.set_size(size)
    font.set_weight('bold')

    ax.set_xticks(np.arange(0,len(all_scores)+1))    
    ax.set_yticks(np.arange(-1,2))
#     ax.set_xticklabels(range(1,len(all_scores)+1), rotation=90)
    ax.set_yticklabels(np.arange(-1,2)/stretch)    
    seaborn.despine(ax=ax, trim=True)
    ax.spines['bottom'].set_position("center")
    trans_offset = transforms.offset_copy(ax.transData, 
                                          fig=fig, 
                                          x=0.5, 
                                          y=0, 
                                          units='dots')## as opposed to 'points'
   

    for index, scores in enumerate(all_scores):
        
        yshift = 0
        for base, score in sorted([x for x in scores if x[-1]>=0], key=lambda x: x[-1]):
            txt = ax.text(index+0.5, 
                          yshift, 
                          base, 
                          transform=trans_offset,
                          fontsize=30, 
                          color=COLOR_SCHEME[base],
                          ha='center',
                          fontproperties=font,
                         )
            txt.set_path_effects([Scale(1.0, stretch*score)])
            fig.canvas.draw()
            window_ext = txt.get_window_extent(txt._renderer)
            yshift += stretch*score
            
        yshift = 0
        for base, score in sorted([x for x in scores if x[-1]<0], key=lambda x: x[-1], reverse=True):
            yshift += stretch*score
            txt = ax.text(index+0.5, 
                          yshift, 
                          base, 
                          transform=trans_offset,
                          fontsize=30, 
                          color=COLOR_SCHEME[base],
                          ha='center',
                          fontproperties=font,
                         )
            txt.set_path_effects([Scale(1.0, stretch*np.abs(score))])
            fig.canvas.draw()
            window_ext = txt.get_window_extent(txt._renderer)

    plt.gca().axes.get_xaxis().set_visible(False)
    if savefile:
        plt.savefig(savefile, format='eps', bbox='tight')
    
def make_tuples(l):
    return [('A',l[0]),
           ('C',l[1]),
           ('G',l[2]),
           ('T',l[3])]

def draw_logo(beta, savefile=None, stretch=5):
    logo_from_map(list(map(make_tuples, beta.reshape(-1,4))), savefile=savefile, stretch=stretch)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Make sequence logo from array of coeffecients")
    parser.add_argument("-o", "--output", type=str, default="output")
    parser.add_argument("-f", "--input", type=str)
    parser.add_argument("-d", "--delimiter", type=str, default=",")
    parser.add_argument("-s", "--stretch", type=int, default=1)

    args = parser.parse_args()

    sequence = np.loadtxt(args.input, delimiter=args.delimiter)

    draw_logo(sequence, savefile=args.output, stretch=args.stretch)





