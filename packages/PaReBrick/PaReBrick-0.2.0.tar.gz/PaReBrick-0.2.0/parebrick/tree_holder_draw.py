from parebrick.tree.tree_holder import TreeHolder

import logging
from collections import defaultdict
from ete3 import Tree


BALANCED_COLORS = ['White', 'LightBlue', 'LightGreen', 'LightPink', 'LightGreen', 'Peru', 'NavajoWhite', 'LightPink',
                   'LightCoral', 'Purple', 'Navy', 'Olive', 'Teal', 'SaddleBrown', 'SeaGreen', 'DarkCyan',
                   'DarkOliveGreen', 'DarkSeaGreen']

if __name__ == '__main__':
    th = TreeHolder('((Strain 1:1,Strain 2:1):2,((Strain 3:1,Strain 4:1),Strain 5:2):1);', logging.getLogger(), scale=2)
    # th = TreeHolder('((((Strain 1,Strain 2),Strain 3:2), (Strain 4,Strain 5):2), (Strain 6,Strain 7):3);', logging.getLogger(), scale=2)

    th.count_innovations_fitch({
        'Strain 1': 0,
        'Strain 2': 1,
        'Strain 3': 0,
        'Strain 4': 1,
        'Strain 5': 0,
        'Strain 6': 0,
        'Strain 7': 0,
    })

    # th.count_innovations_fitch(defaultdict(lambda: 1))
    th.draw('pic1.pdf', BALANCED_COLORS, show_branch_support=False, show_scale=False, color_internal_nodes=False)
