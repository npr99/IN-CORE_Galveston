#!/usr/bin/env python
# coding: utf-8

# ![IN-CORE_resilience-logo.png](data:image/png;base64,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)
# 

# # Building Damage
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


# ## 2) Setting up an alternative plotting function to plot spatially

# In[5]:


from mpl_toolkits.axes_grid1 import make_axes_locatable
def plot_gdf_map(gdf, column, category=False, basemap=True, source=ctx.providers.OpenStreetMap.Mapnik, **kwargs):
    """
    Taken from pyincore-viz. 
    Not using the pyincore-viz version b/c it's limited on plotting options
        - Added **kwargs for more control over the geopandas plotting function
    """
    fig, ax = plt.subplots(1,1, figsize=(10,15))
    gdf = gdf.to_crs(epsg=3857)

    if category == False: # adding a colorbar to side
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)

        ax = gdf.plot(figsize=(10, 10), 
                      column=column,
                      categorical=category, 
                      legend=True,
                      ax=ax,
                      cax=cax,
                     **kwargs)

    elif category == True:
        ax = gdf.plot(figsize=(10, 10), 
                      column=column,
                      categorical=category, 
                      legend=True,
                      ax=ax,
                     **kwargs)

        
    if basemap:
        ctx.add_basemap(ax, source=source)

import matplotlib 
matplotlib.rc('xtick', labelsize=20) 
matplotlib.rc('ytick', labelsize=20) 


# ## 3) Hazard Model (Hurricane)

# In[6]:


hazard_type = "hurricane"


# There are currently five hurricane hazard data for Galveston testbed. Four of them were created using the dynamically coupled versions of the Advanced Circulation (ADCIRC) and Simulating Waves Nearshore (SWAN) models. One of them is a surrogate model developed using USACE datasets.
# 
# | No. | Simulation type | Name | GUID | More details |
# | --- | --- | --- | --- | --- |
# | 1 | Coupled ADCIRC+SWAN | Hurricane Ike Hindcast | <font color='red'>5fa5a228b6429615aeea4410 </font> | Darestani et al. (2021) |
# | 2 | Coupled ADCIRC+SWAN | 2% AEP Hurricane Simulation | <font color='red'>5fa5a83c7e5cdf51ebf1adae </font> | Darestani et al. (2021) |
# | 3 | Coupled ADCIRC+SWAN | 1% AEP Hurricane Simulation | <font color='red'>5fa5a9497e5cdf51ebf1add2 </font> | Darestani et al. (2021) |
# | 4 | Coupled ADCIRC+SWAN | 0.2% AEP Hurricane Simulation | <font color='red'>5fa5aa19b6429615aeea4476 </font> | Darestani et al. (2021) |
# | 5 | Kriging-based surrogate model | Galveston Deterministic Hurricane - Kriging | <font color='red'>5f15cd627db08c2ccc4e3bab </font> | Fereshtehnejad et al. (2021) |
# 
# 
# ### Coupled ADCIRC+SWAN
# Galveston Island was struck by Hurricane Ike in September, 2008, with maximum windspeeds of 49 m/s (95 kts) and storm surge elevations reaching at least +3.5 m (NAVD88) on Galveston Island. A full hindcast of Hurricane Ike’s water levels, and wave conditions along with 2% (50-yr return period), 1% (100-yr return period), and 0.2% (500-yr return period) Annual Exceedance Probabilities (AEP) hurricane simulations were created using ADCIRC+SWAN models. These hurricane hazard events contain **eight hazardDatasets**, which is five more than the current pyincore hurricane schema. Please be sure to adjust your codes accordingly if you need to incorporate the five new intensity measures (IMs). The existing schema includes the peak significant wave height, peak surge level, and inundation duration. These new events include those as well as maximum inundation depth, peak wave period, wave direction, maximum current speed, and maximum wind speed. 
# 
# ### Kriging-based surrogate model
# **Three hazardDatasets** of kriging-based surrogate models are developed for peak significant wave height, peak surge level, and inundation duration. Training datasets for developing the Kriging surorgate models were collected through USACE. For the peak significant wave height, peak surge level, and inundation duration the training datasets included 61, 251, and 254 synthetic storms, respectively. 

# ### What is the your desired hurricane simulation?

# In[7]:


hur_hazard_dict = {1: "5fa5a228b6429615aeea4410", 
                   2: "5fa5a83c7e5cdf51ebf1adae",
                   3: "5fa5a9497e5cdf51ebf1add2",
                   4: "5fa5aa19b6429615aeea4476",
                   5: "5f15cd627db08c2ccc4e3bab"}
hur_no = int(input('The No. of your desired hurricane simulation: '))


# In[8]:


hazard_id=hur_hazard_dict[hur_no]
hazard_id


# In[9]:


path_to_output = os.path.join(os.getcwd(), 'output', 'Results for Hurricane No{}' .format(hur_no))
if not os.path.exists(path_to_output):
    os.makedirs(path_to_output)


# # 4) Residential buildings inventory, fragility, and damage

# ## INVENTORY

# The building inventory for Galveston consists of 18,962 individual residential households. 

# In[10]:


bldg_dataset_id = "60354b6c123b4036e6837ef7"                    # defining building dataset (GIS point layer)       
bldg_dataset = Dataset.from_data_service(bldg_dataset_id, data_service)

geoviz.plot_map(bldg_dataset, column='age_group',category='True')
print('Galveston testbed building inventory as a function of age group')

bldg_df = bldg_dataset.get_dataframe_from_shapefile()
print('Number of buildings: {}' .format(len(bldg_df)))


# ## FRAGILITY

# The fragility model used to estimate failure probability during storm surge events is extracted from:
# 
# >[Tomiczek, T. Kennedy, A, and Rogers, S., 2013. Collapse limit state fragilities of wood-framed residences from storm surge and waves during Hurricane Ike. Journal of Waterway, Port, Coastal, and Ocean Engineering, 140(1), pp.43-55.](https://ascelibrary.org/doi/full/10.1061/%28ASCE%29WW.1943-5460.0000212)
# 
# This empirical fragility model was developed based on Hurricane Ike surveys of almost 2000 individual wood-frame buildings coupled with high resolution hindcast of the hurricane. For this study two states of damage, “Collapse” and “Survival” were considered.
# ________________________________________
# <font color='red'>**INPUT:**</font>
# 
# * Surge: surge level (m) coming from hazard data
# 
# * Hs: Significant wave height (m) coming from hazard data
# 
# * LHSM: Elevation of the lowest horizontal structural member (ft) coming from building inventory
# 
# * age_group: Age group of the building (1, 2,3, and 4 representing age group pre-1974, 1974–1987, 1987–1995, and 1995– 2008, respectively) coming from building Inventory
# 
# * G_elev: Elevation of the building with respect to the ground (m) coming from building inventory
# _______________________________________
# <font color='red'>**OUTPUT:**</font>
# * Pf: probability of failure
# ________________________________________
# <font color='blue'>**FRAGILITY FUNCTION:**</font>
# 
# In order to calculate the probability of failure, first we need to estimate the relative surge height compared to the ground level from:
# 
# \begin{equation*}
# ds=Surge-G_{elev}
# \end{equation*}
# 
# Subsequently, we need to calculate the following parameter:
# 
# 
# \begin{equation*}
# FB_{hs} = -(ds+0.7*Hs-LHSM*0.3048)
# \end{equation*} 
# 
# Then:
# 
# For FB_hs >= -2.79*Hs =====> \begin{equation*}P_f = Φ(-3.56+1.52*Hs-1.73*Hs*FB_{hs}-0.31*FB_{hs}^2-0.141*age_{group}^2)\end{equation*}
# 
# For FB_hs < -2.79*Hs =====> \begin{equation*}P_f = Φ(-3.56+1.52*Hs+2.42*FB_{hs}^2-0.141*age_{group}^2)\end{equation*}
# 
# where Φ denotes the Cumulative Density Function (CDF) of standard normal distribution.
# ________________________________________
# <font color='blue'>**EXAMPLE:**</font>
# 
# If Surge=3 m, Hs =2 m, LHSM=9 ft, age_group=4; G_elev =1 m
# 
# Then Pf= 0.2620
# ________________________________________
# <font color='blue'>**VISUALIZATION:**</font>

# In[64]:


# use utility method of pyicore-viz package to visualize the fragility
fragility_set = FragilityCurveSet(FragilityService(client).get_dfr3_set("5f6ccf67de7b566bb71b202d"))
plt = plotviz.get_fragility_plot_3d(fragility_set, 
                                            title="Galveston empirical fragility model developed "
                                            "based on Hurricane Ike surveys",
                                            limit_state="LS_0")
plt.show()


# ## DAMAGE

# In[65]:


result_name = os.path.join(path_to_output, 'Galveston_bldg_dmg_result_hurNo{}' .format(hur_no))
result_name


# In[66]:


mapping_id = "602c381a1d85547cdc9f0675"
mapping_set = MappingSet(fragility_service.get_mapping(mapping_id))

bldg_dmg = BuildingDamage(client)
bldg_dmg.load_remote_input_dataset("buildings", bldg_dataset_id)
bldg_dmg.set_input_dataset("dfr3_mapping_set", mapping_set)

bldg_dmg.set_parameter("fragility_key", "Hurricane SurgeLevel and WaveHeight Fragility ID Code")
bldg_dmg.set_parameter("result_name", result_name)
bldg_dmg.set_parameter("hazard_type", hazard_type)
bldg_dmg.set_parameter("hazard_id", hazard_id)
bldg_dmg.set_parameter("num_cpu", 4)


# In[67]:


bldg_dmg.run_analysis()
print('Damage analysis is done for', np.size(bldg_df,0) ,'buildings')


# In[68]:


for filepath in glob.iglob(result_name+ '*.csv'):
    Galveston_bldg_dmg_result_df = pd.read_csv(filepath)
bldg_df = bldg_df.to_crs(epsg=3857)

# merging the two above
bldg_df_forplot = pd.merge(bldg_df, Galveston_bldg_dmg_result_df ['DS_3'], left_index=True, right_index=True)
plot_gdf_map(bldg_df_forplot, column='DS_3', vmin=0, vmax=1, cmap='tab20b', linewidth=4)


# In[17]:


# Another option for plotting

# for filepath in glob.iglob(result_name+ '*.csv'):
#     Galveston_bldg_dmg_result_df = pd.read_csv(filepath)
# Galveston_bldg_dmg_result_df = Galveston_bldg_dmg_result_df['DS_3']
# Galveston_bldg_dmg_result_df = np.array(Galveston_bldg_dmg_result_df)

# bldg_df = bldg_df.to_crs(epsg=3857)
# # To fix the error you may try this in command window: pip uninstall pyproj and pip install pyproj
# fig, ax = plt.subplots(figsize=(24, 12))
# bldg_df.plot(column=Galveston_bldg_dmg_result_df,categorical=False,legend=True,ax=ax,alpha=0.1)
# ctx.add_basemap(ax)
# ax.set_axis_off()
# plt.show()

