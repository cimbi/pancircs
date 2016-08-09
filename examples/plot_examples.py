# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 21:56:20 2016

Testing scripy for circ library

@author: jan_cimbalnik
"""


import pandas as pd

from pancircs import hist_circ, heat_map_circ, conn_circ, patch_circ, line_circ


# %% Load data


# Load publicly availabe dataset
data_url = ('https://raw.githubusercontent.com/cimbi/pancircs/'
            'master/MOCK_DATA.csv')
data = pd.read_csv(data_url)
# %% Value circles

# Histogram circle
hist_circ('person_one', 'messages', data, r=6, max_height=1,
          method='mean', labels=True, codein=['color', 'height'])

# Line circle
line_circ('person_one', 'messages', data, r=6, max_height=1,
          method='mean', labels=True, codein=['height'])

# Heat mat circle
heat_map_circ('person_one', 'month', 'messages', data,
              r=6, row_height=0.1, labels=True)

# %% Patch circles

patch_circ('person_one', 'gender', data, r=6, patch_height=0.2,
           group_colors=['b', 'g'], group_order=['Male', 'Female'],
           labels=True)

# %% Connection circles

conn_circ('person_one', 'person_two', 'messages', data, r=6, labels=True,
          codein=['opacity', 'color'])

conn_circ('person_one', 'person_two', 'messages', data, r=6, labels=True,
          causality=True, codein=['opacity', 'color'])

# %% Multicircle

# Numer of messages the person sent
ax, lead_layer = hist_circ('person_one', 'messages', data, r=6, max_height=1,
                           groupby='gender', method='sum', labels=False,
                           codein=['color', 'height', 'opacity'])

# Number of messages the person sent in a particular month
heat_map_circ('person_one', 'month', 'messages', data, headlayer=lead_layer,
              r=4, row_height=0.1, labels=False, ax=ax,
              codein=['opacity', 'color'])

# Number of messages the person sent to another person (strength of connection)
conn_circ('person_one', 'person_two', 'messages', data, ax=ax, r=4,
          labels=False, headlayer=lead_layer,
          codein=['opacity', 'color'])

# Gender of the people
patch_circ('person_one', 'gender', data, r=8, patch_height=0.2,
           ax=ax, headlayer=lead_layer, group_colors=['b', 'g'],
           group_order=['Male', 'Female'], labels=True)
