#!/usr/bin/env python
# coding: utf-8

# ![IN-CORE_resilience-logo.png](data:image/png;base64,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)
# 

# # Pole-Building Assignment
# 
# **Jupyter Notebook Created by**:
#    - Mehrzad Rahimi, Postdoctoral fellow at Rice University (mr77@rice.edu)
#    - Jamie E. Padgett, Professor at Rice University (jamie.padgett@rice.edu)

# ## 1) Initialization

# In[1]:


import warnings
warnings.filterwarnings("ignore")
import os
import pandas as pd
import geopandas as gpd 
import numpy as np
import sys 
import os 
import glob
import matplotlib.pyplot as plt
import contextily as ctx
import copy
import math
from scipy.stats import norm
from pathlib import Path
import networkx as nx

from pyincore import IncoreClient, Dataset, DataService, HazardService, FragilityService, MappingSet, FragilityCurveSet
from pyincore_viz.geoutil import GeoUtil as geoviz
from pyincore_viz.plotutil import PlotUtil as plotviz

# importing pyIncone analyses:
from pyincore.analyses.buildingdamage import BuildingDamage
from pyincore.analyses.bridgedamage import BridgeDamage
from pyincore.analyses.roaddamage import RoadDamage
from pyincore.analyses.epfdamage import EpfDamage
from pyincore.analyses.buildingfunctionality import BuildingFunctionality
from pyincore.analyses.housingunitallocation import HousingUnitAllocation
from pyincore.analyses.populationdislocation import PopulationDislocation, PopulationDislocationUtil
from pyincore.analyses.housingrecoverysequential import HousingRecoverySequential


# In[2]:


# Check package versions - good practice for replication
print("Python Version ", sys.version)
print("pandas version: ", pd.__version__)
print("numpy version: ", np.__version__)


# In[3]:


# Check working directory - good practice for relative path access
os.getcwd()


# In[4]:


client = IncoreClient()
# IN-CORE caches files on the local machine, it might be necessary to clear the memory
#client.clear_cache() 
data_service = DataService(client) # create data_service object for loading files
hazard_service = HazardService(client)
fragility_service = FragilityService(client)


# In[5]:


path_to_output = os.path.join(os.getcwd(), 'output',)
if not os.path.exists(path_to_output):
    os.makedirs(path_to_output)


# ## Poles-Buildings matching

# In[6]:


# Buildings geopandas
bldg_dataset_id = "60354b6c123b4036e6837ef7"                    # defining building dataset (GIS point layer)       
bldg_dataset = Dataset.from_data_service(bldg_dataset_id, data_service)
bldg_df = bldg_dataset.get_dataframe_from_shapefile()


# In[7]:


# Poles geopandas
Galv_WoodPoles_df = gpd.read_file('Galv_WoodPoles.shp')
Galv_PrestressedPoles_df = gpd.read_file('Galv_PrestressedPoles.shp')
Galv_Poles_df = gpd.GeoDataFrame( pd.concat( [Galv_WoodPoles_df, Galv_PrestressedPoles_df], ignore_index=True) )


# ### Let’s also make maps out of them to get a better understanding of the data

# In[8]:


fig, axes=plt.subplots(nrows=1, ncols=2, figsize=(20,10))

# Plot buildings
bldg_df.plot(ax=axes[0],markersize=0.2, alpha=0.5)
axes[0].set_title('Buildings')

# Plot poles
Galv_Poles_df.plot(ax=axes[1], markersize=0.2, alpha=0.5, color='red')
axes[1].set_title('Poles');


# ### we can see from the coordinates and the map that both of the layers share the same coordinate reference system. Hence, we are ready to find closest pole (on the right) for each building on the left map. Let’s first prepare a couple of functions that does the work

# In[9]:


from sklearn.neighbors import BallTree

def get_nearest(src_points, candidates, k_neighbors=1):
    """Find nearest neighbors for all source points from a set of candidate points"""

    # Create tree from the candidate points
    tree = BallTree(candidates, leaf_size=15, metric='haversine')

    # Find closest points and distances
    distances, indices = tree.query(src_points, k=k_neighbors)

    # Transpose to get distances and indices into arrays
    distances = distances.transpose()
    indices = indices.transpose()

    # Get closest indices and distances (i.e. array at index 0)
    # note: for the second closest points, you would take index 1, etc.
    closest = indices[0]
    closest_dist = distances[0]

    # Return indices and distances
    return (closest, closest_dist)

def nearest_neighbor(left_gdf, right_gdf, return_dist=False):
    """
    For each point in left_gdf, find closest point in right GeoDataFrame and return them.

    NOTICE: Assumes that the input Points are in WGS84 projection (lat/lon).
    """

    left_geom_col = left_gdf.geometry.name
    right_geom_col = right_gdf.geometry.name

    # Ensure that index in right gdf is formed of sequential numbers
    right = right_gdf.copy().reset_index(drop=True)

    # Parse coordinates from points and insert them into a numpy array as RADIANS
    left_radians = np.array(left_gdf[left_geom_col].apply(lambda geom: (geom.x * np.pi / 180, geom.y * np.pi / 180)).to_list())
    right_radians = np.array(right[right_geom_col].apply(lambda geom: (geom.x * np.pi / 180, geom.y * np.pi / 180)).to_list())

    # Find the nearest points
    # -----------------------
    # closest ==> index in right_gdf that corresponds to the closest point
    # dist ==> distance between the nearest neighbors (in meters)

    closest, dist = get_nearest(src_points=left_radians, candidates=right_radians)

    # Return points from right GeoDataFrame that are closest to points in left GeoDataFrame
    closest_points = right.loc[closest]

    # Ensure that the index corresponds the one in left_gdf
    closest_points = closest_points.reset_index(drop=True)

    # Add distance if requested
    if return_dist:
        # Convert to meters from radians
        earth_radius = 6371000  # meters
        closest_points['distance'] = dist * earth_radius

    return closest_points


# ### Okay, now we have our functions defined. So let’s use them and find the nearest neighbors!

# In[10]:


# Find closest pole for each building and get also the distance based on haversine distance
# Note: haversine distance which is implemented here is a bit slower than using e.g. 'euclidean' metric
# but useful as we get the distance between points in meters
closest_poles = nearest_neighbor(bldg_df, Galv_Poles_df, return_dist=True)

# And the result looks like ..
closest_poles


# In[11]:


# Now we should have exactly the same number of closest_stops as we have buildings
print(len(closest_poles), '==', len(bldg_df))


# In[12]:


closest_poles_to_bldgs = pd.merge(bldg_df[["guid","geometry"]], closest_poles, left_index=True, right_index=True)


# In[13]:


result_name = os.path.join(path_to_output, 'closest_poles_to_bldgs')


# In[15]:


closest_poles_to_bldgs.to_csv(result_name+'.csv')

