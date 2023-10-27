#!/usr/bin/env python
# coding: utf-8

# ![IN-CORE_resilience-logo.png](data:image/png;base64,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)
# 

# # Wood Pole Damage
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


hur_hazard_dict = {1: "Galv_EPNNodes_DataandHazard_Ike.csv", 
                   2: "Galv_EPNNodes_DataandHazard_50yr.csv",
                   3: "Galv_EPNNodes_DataandHazard_100yr.csv",
                   4: "Galv_EPNNodes_DataandHazard_500yr.csv",
                   5: "Galv_EPNNodes_DataandHazard_kriging.csv"}
hur_no = int(input('The No. of your desired hurricane simulation: '))


# In[8]:


EPN_inv_csv = hur_hazard_dict[hur_no]
EPN_inv_csv


# In[9]:


path_to_output = os.path.join(os.getcwd(), 'output', 'Results for Hurricane No{}' .format(hur_no))
if not os.path.exists(path_to_output):
    os.makedirs(path_to_output)


# # 4) Wood poles inventory, fragility, and damage

# ## INVENTORY

# In[10]:


Num_of_Conductors = 4
Dia_of_Conductors = 0.025 #m


# In[84]:


# Wood Poles Inventory Dataset
EPN_inv_df  = pd.read_csv(EPN_inv_csv)

Lon_EPNnodes = pd.read_csv(EPN_inv_csv, usecols=['LON'])
Lat_EPNnodes = pd.read_csv(EPN_inv_csv, usecols=['LAT'])

WindVel = pd.read_csv(EPN_inv_csv, usecols=['MaxWindVel']) 
WaterVel = pd.read_csv(EPN_inv_csv, usecols=['MaxWaterVel']) 
SurgeHeight = pd.read_csv(EPN_inv_csv, usecols=['MaxWSE']) 
WaveHeight = pd.read_csv(EPN_inv_csv, usecols=['MaxSigWaveHt']) 
WindDir = pd.read_csv(EPN_inv_csv, usecols=['MaxWaveDir']) 

Class = pd.read_csv(EPN_inv_csv, usecols=['CLASS']) 
Height = pd.read_csv(EPN_inv_csv, usecols=['HEIGHT']) 
Type = pd.read_csv(EPN_inv_csv, usecols=['TYPE']) 
Soil = pd.read_csv(EPN_inv_csv, usecols=['SOIL']) 
Age = pd.read_csv(EPN_inv_csv, usecols=['AGE']) 
SpanLength = pd.read_csv(EPN_inv_csv, usecols=['SpanLength']) 
ConSurArea = SpanLength*Num_of_Conductors*Dia_of_Conductors


# In[100]:


Class=np.array(Class) # <class 'numpy.float64'>
Type=np.array(Type)   # <class 'numpy.int64'> 
Soil=np.array(Soil)   # <class 'str'>

Soil


# In[96]:


def EPN_fail_prob(WindVel,WaterVel,SurgeHeight,WaveHeight,WindDir,Age,ConSurArea,Height,Class,Type,Soil):

    WindVel=np.array(WindVel)
    WaterVel=np.array(WaterVel)
    SurgeHeight=np.array(SurgeHeight)
    WaveHeight=np.array(WaveHeight)
    WindDir=np.array(WindDir)
    Age=np.array(Age)
    ConSurArea=np.array(ConSurArea)
    Height=np.array(Height)
    Class=np.array(Class)
    Type=np.array(Type)
    Soil=np.array(Soil)
    
    pf_woodpole_polerupture=[];
    for i in range(0, np.size(WindVel,0)):
        if Soil[i,0]  == 'Stiff': 
            a0 = -7.1325;
        elif Soil[i,0]  == 'Very Stiff': 
            a0 = -6.798
            a1 = 0.021067
            a2 = 0.040692
            a3 = 0.33019
            a4 = 0.033158 
            a5 = 0.002863
            a6 = 0.026811
            a7 = 0.56842
        pf_woodpole_polerupture.append(1/(1+math.exp(-(a0+a1*WindVel[i,0]+a2*(Height[i,0]/3.281-SurgeHeight[i,0]-WaveHeight[i,0])
                                           +a3*WaterVel[i,0]*SurgeHeight[i,0]+a4*WindVel[i,0]*math.sin(WindDir[i,0]*math.pi/180)
                                           +a5*WindVel[i,0]*ConSurArea[i,0]+a6*max(Age[i,0],25)+a7*WaveHeight[i,0]))))
        

    return pf_woodpole_polerupture


# In[97]:


PF_woodpole = EPN_fail_prob(WindVel,WaterVel,SurgeHeight,WaveHeight,WindDir,Age,ConSurArea,Height,Class,Type,Soil)


# In[98]:


np.size(PF_woodpole)
PF_woodpole


# In[ ]:


pf_woodpole_polerupture.append(a0+a1*WindVel[i,0]+a2*(Height[i,0]-SurgeHeight[i,0]-WaveHeight[i,0])
                                   +a3*WaterVel[i,0]*SurgeHeight[i,0]+a4*WindVel[i,0]*sin(WindDir[i,0]*3.14/180)
                                   +a5*WindVel[i,0]*ConSurArea[i,0]+a6*max(Age[i,0],25)+a7*WaveHeight[i,0])


# In[ ]:


def bridge_fail_prob(Clear,Mass,Elev,Surge,Wave):

    Clear=np.array(Clear)
    Mass=np.array(Mass)
    Elev=np.array(Elev)
    Surge=np.array(Surge)
    Wave=np.array(Wave)
    

    pf_bridge=[];
    for i in range(0, np.size(Clear,0)):
        if Mass[i,0]<5 :
            a = 0.6468
            b = 0.0406
            c =-0.1376; 
        elif Mass[i,0]>=5 and Mass[i,0]<10:
            a = 0.4166
            b = 0.0456
            c =-0.2343
        elif Mass[i,0]>=10 and Mass[i,0]<15:
            a = 0.3291
            b = 0.0546
            c =-0.2464
        elif Mass[i,0]>=15 and Mass[i,0]<20:
            a = 0.33
            b = 0.0576
            c =-0.2444
        elif Mass[i,0]>=20 and Mass[i,0]<25:
            a = 0.2843
            b = 0.0512
            c =-0.2421
        elif Mass[i,0]>=25 and Mass[i,0]<30:
            a = 0.2865
            b = 0.0881
            c =-0.2391
        elif Mass[i,0]>=30 and Mass[i,0]<35:
            a = 0.1870
            b = 0.0782
            c =-0.2618
                 
        pf_bridge.append(min(1,max(0,a+b*Wave[i,0]+c*(Clear[i,0]-Surge[i,0]+Elev[i,0]))))
    return pf_bridge



# In[23]:


# Bridge Inventory Dataset (Also available in INCORE)
Bridge_inv_csv = "Galv_bridge_dataandHazards.csv"
Building_inv_df  = pd.read_csv(Bridge_inv_csv)

Lon_Build = pd.read_csv("Galv_bridge_dataandHazards.csv", usecols=['LON'])
Lat_Build = pd.read_csv("Galv_bridge_dataandHazards.csv", usecols=['LAT'])
Surge= pd.read_csv("Galv_bridge_dataandHazards.csv", usecols=['Surge'])
Wave= pd.read_csv("Galv_bridge_dataandHazards.csv", usecols=['Wave'])
Mass= pd.read_csv("Galv_bridge_dataandHazards.csv", usecols=['Mass'])
Clear= pd.read_csv("Galv_bridge_dataandHazards.csv", usecols=['Clear'])
Elev= pd.read_csv("Galv_bridge_dataandHazards.csv", usecols=['Elev'])


# In[ ]:


def bridge_fail_prob(Clear,Mass,Elev,Surge,Wave):

    Clear=np.array(Clear)
    Mass=np.array(Mass)
    Elev=np.array(Elev)
    Surge=np.array(Surge)
    Wave=np.array(Wave)
    

    pf_bridge=[];
    for i in range(0, np.size(Clear,0)):
        if Mass[i,0]<5 :
            a0 = -7.1325
            a1 = 0.021686
            a2 = 0.048014
            a3 = 0.2974
            a4 = 0.026337
            a5 = 0.002212
            a6 = 0.028545
            a7 = 0.52904;
        elif Mass[i,0]>=5 and Mass[i,0]<10:
            a0 = 0.4166
            b = 0.0456
            c =-0.2343
        elif Mass[i,0]>=10 and Mass[i,0]<15:
            a0 = 0.3291
            b = 0.0546
            c =-0.2464
        elif Mass[i,0]>=15 and Mass[i,0]<20:
            a0 = 0.33
            b = 0.0576
            c =-0.2444
        elif Mass[i,0]>=20 and Mass[i,0]<25:
            a0 = 0.2843
            b = 0.0512
            c =-0.2421
        elif Mass[i,0]>=25 and Mass[i,0]<30:
            a0 = 0.2865
            b = 0.0881
            c =-0.2391
        elif Mass[i,0]>=30 and Mass[i,0]<35:
            a0 = 0.1870
            b = 0.0782
            c =-0.2618
                 
        pf_bridge.append(min(1,max(0,a0+b*Wave[i,0]+c*(Clear[i,0]-Surge[i,0]+Elev[i,0]))))
    return pf_bridge


# In[ ]:


PF_bridge = bridge_fail_prob(Clear,Mass,Elev,Surge,Wave)


# In[48]:


Mass=np.array(Mass)
print(type(Mass[1,0]))


# In[ ]:


def EPN_fail_prob(WindVel,WaterVel,SurgeHeight,WaveHeight,WindDir,Age,ConSurArea,Height,Class,Type,Soil):

    WindVel=np.array(WindVel)
    WaterVel=np.array(WaterVel)
    SurgeHeight=np.array(SurgeHeight)
    WaveHeight=np.array(WaveHeight)
    WindDir=np.array(WindDir)
    Age=np.array(Age)
    ConSurArea=np.array(ConSurArea)
    Height=np.array(Height)
    Class=np.array(Class)
    Type=np.array(Type)
    Soil=np.array(Soil)
    
    pf_woodpole_polerupture=[];
    for i in range(0, np.size(WindVel,0)):
        
        
        
        print(f"Running Analysis: {i}")
        if Type[i,0]  == 1 and Class[i,0] == 3 and Soil[i,0]  == 'Stiff': 
            a0 = -7.1325
            a1 = 0.021686
            a2 = 0.048014
            a3 = 0.2974
            a4 = 0.026337
            a5 = 0.002212
            a6 = 0.028545
            a7 = 0.52904;
        elif Type[i,0]  == 1 and Class[i,0] == 3 and Soil[i,0]  == 'Very Stiff': 
            a0 = -7.2476
            a1 = 0.02157
            a2 = 0.051976
            a3 = 0.29907
            a4 = 0.027067
            a5 = 0.002424
            a6 = 0.027865
            a7 = 0.51853
        elif Type[i,0]  == 1 and Class[i,0] == 4 and Soil[i,0]  == 'Medium': 
            a0 = -6.8655
            a1 = 0.022127
            a2 = 0.038238
            a3 = 0.30961
            a4 = 0.028689
            a5 = 0.002461
            a6 = 0.027454
            a7 = 0.53341
        elif Type[i,0]  == 1 and Class[i,0] == 4 and Soil[i,0]  == 'Stiff': 
            a0 = -6.8655
            a1 = 0.022127
            a2 = 0.038238
            a3 = 0.30961
            a4 = 0.028689
            a5 = 0.002461
            a6 = 0.027454
            a7 = 0.53341
        elif Type[i,0]  == 1 and Class[i,0] == 4 and Soil[i,0]  == 'Very Stiff': 
            a0 = -6.9997
            a1 = 0.020323 
            a2 = 0.042443
            a3 = 0.30771
            a4 = 0.030009
            a5 = 0.00284
            a6 = 0.02892
            a7 = 0.53529
        elif Type[i,0]  == 1 and Class[i,0] == 5 and Soil[i,0]  == 'Medium': 
            a0 = -6.8029
            a1 = 0.019763
            a2 = 0.041838
            a3 = 0.33543
            a4 = 0.032922
            a5 = 0.002892
            a6 = 0.026793
            a7 = 0.57772
        elif Type[i,0]  == 1 and Class[i,0] == 5 and Soil[i,0]  == 'Stiff': 
            a0 = -6.8029
            a1 = 0.019763
            a2 = 0.041838
            a3 = 0.33543
            a4 = 0.032922
            a5 = 0.002892
            a6 = 0.026793
            a7 = 0.57772;
        elif Type[i,0]  == 1 and Class[i,0] == 5 and Soil[i,0]  == 'Very Stiff': 
            a0 = -6.798
            a1 = 0.021067
            a2 = 0.040692
            a3 = 0.33019
            a4 = 0.033158 
            a5 = 0.002863
            a6 = 0.026811
            a7 = 0.56842

        pf_woodpole_polerupture.append(a0+a1*WindVel[i,0]+a2*(Height[i,0]-SurgeHeight[i,0]-WaveHeight[i,0])
                                           +a3*WaterVel[i,0]*SurgeHeight[i,0]+a4*WindVel[i,0]*sin(WindDir[i,0]*3.14/180)
                                           +a5*WindVel[i,0]*ConSurArea[i,0]+a6*max(Age[i,0],25)+a7*WaveHeight[i,0])

    return pf_woodpole_polerupture

