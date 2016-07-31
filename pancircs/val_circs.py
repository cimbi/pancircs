# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 23:36:55 2016

Library of circles evaluating values of nodes.

Ing.,Mgr. (MSc.) Jan Cimbálník
Biomedical engineering
International Clinical Research Center
St. Anne's University Hospital in Brno
Czech Republic
&
Mayo systems electrophysiology lab
Mayo Clinic
200 1st St SW
Rochester, MN
United States
"""

# %% Imports

from .utils import *

import matplotlib.pyplot as plt

# %% The histogram of counts - do grouping - look at seaborn later

# TODO - group by - channel name in this case


def hist_circ(nodes, heat, data, r, max_height, orderby=None, groupby=None,
              ax=None, method='sum', cmap='jet', labels=True,
              headlayer=None, codein=['height']):

    """
    Creates a histogram circle.

    Parameters:
    -----------
    nodes - column name with node names\n
    heat - column name with the values for the histogram\n
    data - pandas dataframe\n
    r - radius of the circle\n
    max_height - maximum height of the histogram columns\n
    orderby - column name by which the nodes are ordered\n
    groupby - column name with node groups\n
    ax - axes to which the circle is plotted\n
    method - method by which the values in heat column are processed the optins
    are 'sum' or 'mean'\n
    cmap - matplotlib cmap for colorcoding\n
    create_labels - wether to create node and group labels\n
    headlayer - leading layer where node positions are specified\n
    codein - list of methods for histogram value coding, options are:
    'height','color','opacity'\n

    Returns:
    --------
    ax - plot axes
    layer - layer object
    """

    # Create colormap
    colormap = plt.get_cmap(cmap)

    # Order by
    if orderby is not None:
        data = data.sort_values(by=orderby)

    # Create node list
    if headlayer is None:
        node_list, node_width = create_node_list(nodes, data, r,
                                                 orderby=orderby,
                                                 groupby=groupby)
    else:
        node_list = headlayer.node_list
        node_list = reuse_nodes(node_list, nodes, data, r, sublayers=None,
                                r_increment=0.1)
        node_width = headlayer.node_width

    # Assign relative value to each node
    if method == 'mean':
        used_method = np.mean
    elif method == 'sum':
        used_method = np.sum

    rel_val_df = data.groupby(nodes)[heat].apply(used_method)
    max_value = rel_val_df.max()
    min_value = rel_val_df.min()
    val_range = max_value - min_value
    rel_val_df = (rel_val_df - min_value) / val_range

    for node in node_list:
        # In case the value is not in the dataframe
        if node.label in rel_val_df.keys():
            node.relative_value = rel_val_df[node.label]
        else:
            node.relative_value = 0

    if ax is None:
        plt.figure(facecolor='w')
        ax = plt.subplot(111, projection='polar')
        ax.spines['polar'].set_visible(False)

    for node in node_list:

        # Code relative value
        if 'color' in codein:
            node.color = colormap(node.relative_value)
        if 'height' in codein:
            bar_height = max_height*node.relative_value
        else:
            bar_height = max_height
        if 'opacity' in codein:
            node.opacity = node.relative_value

        # Create node in plot
        bar = ax.bar(node.position[0], bar_height, width=node_width, bottom=r,
                     color=node.color, edgecolor="None",
                     alpha=node.opacity)[0]

        node.patch = bar

        # TODO KWARGS to bar, later

    if labels:
        create_labels(node_list, node_width, ax)
        if any([x.group for x in node_list]):
            create_group_labels(node_list, node_width, ax)

    # In the end create layer instance
    layer = CircLayer('hist_circo', r, max_height, node_list, node_width)

    return ax, layer

# %% Plot the heatmap - this is colour coded histogram
# - many times - just relative values are different


def heat_map_circ(nodes, sublayers, heat, data, r, row_height, orderby=None,
                  groupby=None, ax=None, cmap='jet', labels=True,
                  headlayer=None, codein=['color']):

    # TODO - add separation and sorting later by structure for example

    """
    Creates a heat map circle.

    Parameters:
    -----------
    nodes - column name with node names\n
    sublayers - column name with rows of for the heatmap\n
    heat - column name with the values for the heatmap\n
    data - pandas dataframe\n
    r - radius of the circle\n
    row_height - height of one row of the heatmap\n
    orderby - column name by which the nodes are ordered\n
    groupby - column name with node groups\n
    ax - axes to which the circle is plotted\n
    cmap - matplotlib cmap for colorcoding\n
    create_labels - wether to create node and group labels\n
    headlayer - leading layer where node positions are specified\n
    codein - list of methods for histogram value coding, options are:
    'color','opacity'\n

    Returns:
    --------
    ax - plot axes
    layer - layer object
    """

    # Create colormap
    colormap = plt.get_cmap(cmap)

    # Order by
    if orderby is not None:
        data = data.sort_values(by=orderby)

    N_sublayers = len(data[sublayers].unique())
    # Create node list
    if headlayer is None:
        node_list, node_width = create_node_list(nodes, data, r,
                                                 orderby=orderby,
                                                 groupby=groupby,
                                                 sublayers=sublayers,
                                                 r_increment=row_height)
    else:
        node_list = headlayer.node_list
        node_list = reuse_nodes(node_list, nodes, data, r,
                                sublayers=sublayers, r_increment=row_height)
        node_width = headlayer.node_width

    # Assign relative value to each node
    used_method = np.sum

    rel_val_df = data.groupby([nodes, sublayers])[heat].apply(used_method)
    max_value = rel_val_df.max()
    min_value = rel_val_df.min()
    val_range = max_value - min_value
    rel_val_df = (rel_val_df - min_value) / val_range

    for node in node_list:
        if (node.label in rel_val_df.keys().levels[0] and
                node.sublayer in rel_val_df[node.label].keys()):
            node.relative_value = rel_val_df[node.label][node.sublayer]
        else:
            node.relative_value = 0

    # If no axis is passed, create one
    if ax is None:
        plt.figure(facecolor='w')
        ax = plt.subplot(111, projection='polar')
        ax.spines['polar'].set_visible(False)

    for node in node_list:

        # Code relative value
        if 'color' in codein:
            node.color = colormap(node.relative_value)
        if 'opacity' in codein:
            node.opacity = node.relative_value

        # Create node in plot
        node.color = colormap(node.relative_value)

        bar = ax.bar(node.position[0], row_height, width=node_width,
                     bottom=node.position[1], color=node.color,
                     edgecolor=node.color, alpha=node.opacity)[0]

        node.patch = bar
        # TODO KWARGS to bar, later

    # TODO kwargs for text and check if text is already there
    if labels:
        create_labels([x for x in node_list if x.position[1] == r],
                      node_width, ax)
        if any([x.group for x in node_list]):
            create_group_labels([x for x in node_list if x.position[1] == r],
                                node_width, ax)

    # In the end create layer instance and return it
    layer = CircLayer('heat_circo', r, (N_sublayers*row_height - r),
                      node_list, node_width)

    return ax, layer
