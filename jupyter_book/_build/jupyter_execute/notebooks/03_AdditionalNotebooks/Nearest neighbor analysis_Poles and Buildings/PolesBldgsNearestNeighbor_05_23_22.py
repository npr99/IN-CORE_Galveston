#!/usr/bin/env python
# coding: utf-8

# # Pole-Building Assignment
# 
# **Jupyter Notebook Created by**:
#    - Kooshan Amini, Ph.D. Student at Rice University (Kooshan.Amini@rice.edu)
#    - Mehrzad Rahimi, Postdoctoral fellow at Rice University (mr77@rice.edu)

# ## 1) Initialization

# In[1]:


import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import geopandas as gpd
import numpy as np
import sys 
import os
import json
import matplotlib.pyplot as plt
from pyincore import IncoreClient, Dataset, DataService, HazardService, FragilityService, MappingSet, FragilityCurveSet


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


# In[284]:


path_to_output = os.path.join(os.getcwd(), 'output',)
if not os.path.exists(path_to_output):
    os.makedirs(path_to_output)


# ## 2) Getting needed data

# In[285]:


# Buildings geopandas
bldg_dataset_id = "60354b6c123b4036e6837ef7"                    # defining building dataset (GIS point layer)       
bldg_dataset = Dataset.from_data_service(bldg_dataset_id, data_service)
bldg_df = bldg_dataset.get_dataframe_from_shapefile()
bldg_df.rename(columns={"guid": "bldg_guid"}, inplace=True)


# In[286]:


# Poles geopandas
galv_elec_id = "62fc000f88470b319561b58d"
galv_elec = Dataset.from_data_service(galv_elec_id, data_service)
galv_elec_df = galv_elec.get_dataframe_from_shapefile()


# Here, first the poles and substations have became seperated and then been plotted:

# In[287]:


galv_elec_df


# In[288]:


poles_df = galv_elec_df[(galv_elec_df['utilfcltyc'] == '1') | (galv_elec_df['utilfcltyc'] == '2')]
poles_df.rename(columns={"guid": "poles_guid"}, inplace=True)
substations_df = galv_elec_df[galv_elec_df['utilfcltyc'] == '20']
substations_df.rename(columns={"guid": "substations_guid"}, inplace=True)


fig, axes=plt.subplots(nrows=1, ncols=2, figsize=(20,12.5))

# Plot buildings
bldg_df.plot(ax=axes[0],markersize=0.2, alpha=0.5)
axes[0].set_title('Buildings')

# Plot Poles
poles_df.plot(ax=axes[1], markersize=0.2, alpha=0.5, color='black')

# Plot Substations
substations_df.plot(ax=axes[1], markersize=20, color='red')
axes[1].set_title('Poles and Substations');


# In[289]:


poles_df


# In[290]:


substations_df


# ## 3) Poles-substations-building matching

# we can see from the coordinates and the map that both of the layers share the same coordinate reference system. Hence, we are ready to find closest pole (on the right) for each building on the left map. Let’s first prepare a couple of functions that does the work

# In[291]:


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


# Okay, now we have our functions defined. So let’s use them and find the nearest neighbors!

# In[292]:


# Find closest pole and substation for each building and get also the distance based on haversine distance
# Note: haversine distance which is implemented here is a bit slower than using e.g. 'euclidean' metric
# but useful as we get the distance between points in meters
closest_poles = nearest_neighbor(bldg_df, poles_df, return_dist=True)
closest_substations = nearest_neighbor(bldg_df, substations_df, return_dist=True)


# In[293]:


closest_poles


# In[294]:


closest_substations


# ## 4) Exporting results

# In[295]:


df_final = pd.merge(bldg_df[["bldg_guid","geometry"]], closest_poles[["poles_guid","geometry"]], left_index=True, right_index=True)
df_final = pd.merge(df_final, closest_substations[["substations_guid","geometry"]], left_index=True, right_index=True)


# In[296]:


df_final


# In[297]:


result_name = os.path.join(path_to_output, 'closest_poles_to_bldgs')


# In[298]:


df_final.to_csv(result_name+'.csv')


# Making JSON file:

# In[299]:


df_nested = df_final[["bldg_guid","poles_guid","substations_guid"]]
df_nested


# In[300]:


j = (df_nested.groupby('bldg_guid')
       .apply(lambda x: x[['poles_guid','substations_guid']].to_dict('record'))
       .to_json(orient='index'))
parsed = json.loads(j)
final = json.dumps(parsed, indent=4)
with open(result_name+".json", "w") as outfile:
    outfile.write(final)

