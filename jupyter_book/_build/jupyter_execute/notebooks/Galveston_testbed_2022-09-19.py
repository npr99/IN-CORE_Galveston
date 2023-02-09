#!/usr/bin/env python
# coding: utf-8

# ![IN-CORE_resilience-logo.png](images/IN-CORE_resilience-logo.png)

# # Galveston Testbed
# 
# **Jupyter Notebook Created by**:
#    - Mehrzad Rahimi, Postdoctoral fellow at Rice University (mr77@rice.edu)
#    - Omar M. Nofal, Postdoctoral fellow at Colorado State University (omar.nofal@colostate.edu)
#    - Ram K. Mazumder, Postdoctoral fellow at University of Kansas (rkmazumder@ku.edu)
#    - Nathanael Rosenheim, Research Associate Professor at Texas A&M University (nrosenheim@arch.tamu.edu)
#    - Yousef M. Darestani, Assistant Professor at Michigan Technological University (ydaresta@mtu.edu) 
#    - Jamie E. Padgett, Professor at Rice University (jamie.padgett@rice.edu)
#    - Elaina J. Sutley, Associate Professor at University of Kansas (enjsutley@ku.edu) 
#    - John W. van de Lindt, Professor at Colorado State University (john.van_de_lindt@colostate.edu)

# # IN-CORE Flowchart - Galveston
# This notebook uses the Galveston testbed to demonstrate the following components of the IN-CORE flowchart.

# ![incore-flowchart.png](attachment:incore-flowchart.png)

# # Background
# The **Galveston Testbed** is an ongoing effort of the Center to test model chaining an integration across coupled systems. The current Galveston Testbed and Jupyter notebooks released with IN-CORE focus on **Galveston Island** as a barrier island exposed to hurricane hazards. Our ongoing work extends this analysis to Galveston County, further exploring the interplay between economic activity and recovery efforts between the mainland and the island. As shown in the following figure, Galveston County is located in the southeastern part of Texas, along the Gulf Coast adjacent to Galveston Bay.
# 
# Galveston Island is located in southern Galveston County with a total length of 43.5 km and a width of 4.8 km. The Island is surrounded by West Bay from the west, the Gulf of Mexico from the south and east, and Galveston Bay in the North. The Galveston Island is connected to the rest of Galveston County by interstate highway I-45. Based on the 2015 county parcel data the total number of buildings within Galveston County was 172,534 buildings with 29,541 buildings located on Galveston Island. In 2010, the total population living on Galveston Island was 48,726 people with a racial/ethnic composition of 46% non-Hispanic White, 18% non-Hispanic Black, and 31% Hispanic. Galveston, Texas has a long history with hurricanes including the Great Galveston Hurricane in 1900 which is considered the deadliest natural disaster in U.S. history. More recently, the island was affected by Hurricane Ike (2008) and Hurricane Harvey (2017), each posing unique challenges in terms of coastal multi-hazards and recovery challenges, and with billions of dollars in economic impacts. 

# ![Figure.png](attachment:Figure.png)

# # General info
# 
# Some of the main objectives of the Galveston Testbed include:
# 
# 1. Investigate the multi-hazard surge, wave, inundation, and wind hazards in coastal settings.
# 2. Consider interdependent infrastructure systems including buildings, transportation, and power.
# 3. Leverage historical social-science data, informing population dislocation and recovery modeling.
# 4. Evaluate hybrid metrics of community resilience, such as those that require coupled modeling between social and physical systems.
# 
# More information about the testbed and the field study can be found in this publication:
# 1. Fereshtehnejad, E., Gidaris, I., Rosenheim, N., Tomiczek, T., Padgett, J. E., Cox, D. T., ... & Gillis Peacock, W. (2021). Probabilistic risk assessment of coupled natural-physical-social systems: cascading impact of hurricane-induced damages to civil infrastructure in Galveston, Texas. Natural Hazards Review, 22(3), 04021013.
# 
# The current notebook is a WORK-IN-PROGRESS that consists of the following modules:
# 1. Community Description with Housing Unit Allocation  
# 2. Hazard Model: Flood Surge, Wave, and Inundation Modeling with Building Damage
# 3. Functionality Models: Phycial Infrastructure and Population Dislocation
# 4. Recovery Models with Household-Level Housing Recovery Analysis
# 6. Policy Lever Analysis
# 
# The models used in this testbed come from:
# 1. Nofal, O. M., Van De Lindt, J. W., Do, T. Q., Yan, G., Hamideh, S., Cox, D. T., & Dietrich, J. C. (2021). Methodology for Regional Multihazard Hurricane Damage and Risk Assessment. Journal of Structural Engineering, 147(11), 04021185.
# 
# 2. Darestani, Y. M., Webb, B., Padgett, J. E., Pennison, G., & Fereshtehnejad, E. (2021). Fragility Analysis of Coastal Roadways and Performance Assessment of Coastal Transportation Systems Subjected to Storm Hazards. Journal of Performance of Constructed Facilities, 35(6), 04021088.
# 
# 3. Darestani, Y., Padgett, J., & Shafieezadeh, A. (2022). Parametrized Wind–Surge–Wave Fragility Functions for Wood Utility Poles. Journal of Structural Engineering, 148(6), 04022057.
# 
# 1. Rosenheim, N., Guidotti, R., Gardoni, P., & Peacock, W. G. (2019). Integration of detailed household and housing unit characteristic data with critical infrastructure for post-hazard resilience modeling. Sustainable and Resilient Infrastructure, 6(6), 385-401.
# 
# 2. Sutley, E. J., & Hamideh, S. (2020). Postdisaster housing stages: a markov chain approach to model sequences and duration based on social vulnerability. Risk Analysis, 40(12), 2675-2695.
# 
# Prerequisites:
# The following packages are necessary to run this notebook. To ensure dependencies are correct, install all modules through **conda**.
# 
# 
# | Module | Version | Notes |
# | --- | --- | --- |
# | pyIncore | =>1.7.0 | see: https://incore.ncsa.illinois.edu/doc/incore/install_pyincore.html |
# | pyIncore_viz | =>1.5.0 | see: https://incore.ncsa.illinois.edu/doc/pyincore_viz/index.html |

# # Start

# ![start.png](attachment:start.png)

# The following codes are preparing the analysis by checking versions and connecting to IN-CORE web service. Also, all of the necessary pyIncore analyses are being imported. In this analysis, the following pyIncore analyses are utilized:
# * **Building damage**: Computes building damage based on a particular hazard (hurricane in this testbed).
# * **Building functionality**: Calculates building functionality probabilities.
# * **Housing unit allocation**: Sets up a detailed critical infrastructure inventory with housing unit level characteristics. 
# * **Population dislocation**: Computes population dislocation based on a particular hazard (hurricane in this testbed).
# * **Household-level housing sequential recovery**: Computes the series of household recovery states given a population dislocation dataset.
# * **Policy Lever Demonstration**: Modify Building Inventory to reduce building damage.

# In[1]:


import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import geopandas as gpd 
import numpy as np
import sys 
import os 
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
from pyincore.analyses.buildingfunctionality import BuildingFunctionality
from pyincore.analyses.combinedwindwavesurgebuildingdamage import CombinedWindWaveSurgeBuildingDamage
from pyincore.analyses.epfdamage import EpfDamage
from pyincore.analyses.housingunitallocation import HousingUnitAllocation
from pyincore.analyses.populationdislocation import PopulationDislocation, PopulationDislocationUtil
from pyincore.analyses.housingrecoverysequential import HousingRecoverySequential
from pyincore.analyses.socialvulnerability import SocialVulnerability


# In[2]:


# Functions for visualizing the population data results as tables
from pyincore_viz.analysis.popresultstable import PopResultsTable as poptable


# In[3]:


# Check package versions - good practice for replication
print("Python Version ", sys.version)
print("pandas version: ", pd.__version__)
print("numpy version: ", np.__version__)


# In[4]:


# Check working directory - good practice for relative path access
os.getcwd()


# In[5]:


client = IncoreClient()
# IN-CORE caches files on the local machine, it might be necessary to clear the memory
# client.clear_cache() 
data_service = DataService(client) # create data_service object for loading files
hazard_service = HazardService(client)
fragility_services = FragilityService(client)


# # 1) Initial community description

# ![initialcommunitydescription.png](attachment:initialcommunitydescription.png)

# Step 1 in IN-CORE is to establish initial community description at time 0 and with policy levers and decision combinations (PD) set to K (baseline case). The community description includes three parts including **1a) Built Environment**, **1b) Social Systems**, and **1c) Economic Systems**.

# ## 1a) Built Environment
# The Galveston testbed consists of five infrastructure systems as buildings, transportation network, electric power transmission and distribution network, water/wastewater network, and critical facilities. Each infrastructure system may be composed of different infrastructure components. For example, the transportation network consists of bridges and roadways. The infrastructure systems and components are shown below along with their IN-CORE GUID.
# 
# | No. | Infrastructure System | Infrastructure Component | GUID | More details |
# | --- | --- | --- | --- | --- |
# | 1 | Buildings | - | 63053ddaf5438e1f8c517fed| Ref. |
# | 2 | Transportation network | Bridges | 60620320be94522d1cb9f7f0| Ref. |
# | - | Transportation network | Roadways | 5f15d04f33b2700c11fc9c4e| Ref. |
# | 3 | Electric power network | Connectivity | Outside of IN-CORE| Ref. |
# | - | Electric power network | Poles and Towers | Outside of IN-CORE| Ref. |
# | - | Electric power network | Substation | Outside of IN-CORE| Ref. |
# | - | Electric power network | Transmission | Outside of IN-CORE| Ref. |
# | - | Electric power network | Underground | Outside of IN-CORE| Ref. |
# | 4 | Water/wastewater network | Water mains | Outside of IN-CORE| Ref. |
# | - | Water/wastewater network | Water plants | Outside of IN-CORE| Ref. |
# | - | Water/wastewater network | Wastewater mains | Outside of IN-CORE| Ref. |
# | 5 | Critical facilities | Hospitals | Outside of IN-CORE| Ref. |
# | - | Critical facilities | Urgent care | Outside of IN-CORE| Ref. |
# | - | Critical facilities | Emergency medical facilities | Outside of IN-CORE| Ref. |
# | - | Critical facilities | Fire stations | Outside of IN-CORE| Ref. |
# | 6 | Fiber Optic Network | - | Outside of IN-CORE| Ref. |
# 
# **Note**: The built environment in the Galveston testbed are in the Galveston Island. However, as the goal is to capture flow of people during recovery stages, buildings and transportation networks in the Galveston mainland are considered as well.

# ### Buildings
# The building inventory for Galveston consists of 172,534 individual buildings. This inventory is also mappable to housing unit info of 132,553 individual households explained later in this notebook. It should be noted that the reason that the building and household data are different in terms of numbers is that each individual building can be composed of a few households or no households in the case of commercial or industrial buildings. The building inventory consists of major parameters that are used to estimate the fragility of buildings explained shortly later in this notebook.
# 

# In[6]:


bldg_dataset_id = "63053ddaf5438e1f8c517fed" # Prod              # defining building dataset (GIS point layer)       

bldg_dataset = Dataset.from_data_service(bldg_dataset_id, data_service)
# geoviz.plot_map(bldg_dataset, column='arch_flood',category='True')
print('Galveston testbed building inventory as a function of age group')

bldg_df = bldg_dataset.get_dataframe_from_shapefile()
#bldg_df.set_index('guid', inplace=True)
print('Number of buildings: {}' .format(len(bldg_df)))


# ## 1b) Social Systems
# The Galveston County, TX has a permanent resident population of approximately 53,695 people (US Census, 2020). In 2010, the total population living on Galveston County was 291,309 with 48,726 people living on Galveston, Island [(US Census, 2010)](https://data.census.gov/cedsci/table?g=0500000US48167_1600000US4828068,4837252&tid=DECENNIALSF12010.P1). This section performs a housing unit allocation. The housing unit inventory includes characteristics for individual households and housing units that can be linked to residential buildings. For more information see 
# 
# > Rosenheim, Nathanael (2021) “Detailed Household and Housing Unit Characteristics: Data and Replication Code.” DesignSafe-CI. https://doi.org/10.17603/ds2-jwf6-s535 v2
# 

# In[7]:


# Housing Unit inventory
housing_unit_inv_id = "626322a7e74a5c2dfb3a72b0"
# load housing unit inventory as pandas dataframe
housing_unit_inv = Dataset.from_data_service(housing_unit_inv_id, data_service)
filename = housing_unit_inv.get_file_path('csv')
print("The IN-CORE Dataservice has saved the Housing Unit Inventory on your local machine: "+filename)


# In[8]:


housing_unit_inv_df = pd.read_csv(filename, header="infer")
housing_unit_inv_df.head()


# In[9]:


housing_unit_inv_df['huid'].describe()


# In[10]:


poptable.pop_results_table(housing_unit_inv_df, 
                  who = "Total Population by Householder", 
                  what = "by Race, Ethnicity",
                  where = "Galveston County TX",
                  when = "2010",
                  row_index = "Race Ethnicity",
                  col_index = 'Tenure Status')


# ## 1a + 1b) Interdependent Community Description
# 
# Explore building inventory and social systems. Specifically look at how the building inventory connects with the housing unit inventory using the housing unit allocation.
# The housing unit allocation method will provide detail demographic characteristics for the community allocated to each structure.
# 
# To run the HUA Algorithm, three input datasets are required:
# 
# 1. Housing Unit Inventory - Based on 2010 US Census Block Level Data
# 
# 2. Address Point Inventory - A list of all possible residential/business address points in a community. Address points are the link between buildings and housing units.
# 
# 3. Building Inventory - A list of all buildings within a community.
# 

# ### Set Up and Run Housing Unit Allocation
# The building and housing unit inventories have already by loaded. The address point inventory is needed to link the population with the structures.

# In[11]:


# Create housing allocation 
hua = HousingUnitAllocation(client)

address_point_inv_id = "6320da3661fe1122867c2fa2"

# Load input dataset
hua.load_remote_input_dataset("housing_unit_inventory", housing_unit_inv_id)
hua.load_remote_input_dataset("address_point_inventory", address_point_inv_id)
hua.load_remote_input_dataset("buildings", bldg_dataset_id)

# Specify the result name
result_name = "Galveston_HUA"

seed = 1238
iterations = 1

# Set analysis parameters
hua.set_parameter("result_name", result_name)
hua.set_parameter("seed", seed)
hua.set_parameter("iterations", iterations)


# In[12]:


# Run Housing unit allocation analysis - temporarily disabled - read from dataset instead
# hua.run_analysis()


# ### Explore results from Housing Unit Allocation

# In[13]:


# Retrieve result dataset
# hua_result = hua.get_output_dataset("result")
# NOTE to USER - pyincore 1.7.0 has internal error and this notebook includes a workaround for the HUA analysis
hua_result_id = "6328a9b873b4ed0eefbacad6"

hua_result = Dataset.from_data_service(hua_result_id, data_service)

# Convert dataset to Pandas DataFrame
hua_df = hua_result.get_dataframe_from_csv(low_memory=False)

# Display top 5 rows of output data
hua_df[['guid','numprec','incomegroup','geometry']].head()


# In[14]:


hua_df[['guid','huid']].describe()


# In[15]:


# Limit HUA Results to only observations with GUID and HUID
hua_df_buildings = hua_df.loc[(hua_df['guid'].notnull()) & 
            (hua_df['huid'].notnull())].copy()
hua_df_buildings[['guid','huid']].describe()


# In[16]:


# Update HUA results with housing unit inventory linked to buildings
hua_result = Dataset.from_dataframe(dataframe = hua_df_buildings,
                                    name = result_name+"_"+str(seed)+"buildings.csv",
                                    data_type='incore:housingUnitAllocation')


# In[17]:


poptable.pop_results_table(hua_df_buildings, 
                  who = "Total Population by Householder", 
                  what = "by Race, Ethnicity",
                  where = "Galveston County, TX - Buildings in Inventory",
                  when = "2010",
                  row_index = "Race Ethnicity",
                  col_index = 'Tenure Status')


# In[18]:


poptable.pop_results_table(hua_df_buildings, 
                  who = "Median Household Income", 
                  what = "by Race, Ethnicity",
                  where = "Galveston County, TX - Buildings in Inventory",
                  when = "2010",
                  row_index = "Race Ethnicity",
                  col_index = 'Tenure Status')


# #### Validate the Housing Unit Allocation has worked
# Notice that the population count totals for the community should match (pretty closely) data collected for the 2010 Decennial Census.
# This can be confirmed by going to data.census.gov
# 
# [Total Population by Race and Ethnicity](https://data.census.gov/cedsci/table?q=DECENNIALPL2010.P5&g=0500000US48167_1600000US4828068,4837252&tid=DECENNIALSF12010.P5)
# 
# Median Income by Race and Ethnicity:
# - [All Households](https://data.census.gov/cedsci/table?g=0500000US48167_1600000US4828068,4837252&tid=ACSDT5Y2012.B19013)
# - [Black Households](https://data.census.gov/cedsci/table?g=0500000US48167_1600000US4828068,4837252&tid=ACSDT5Y2012.B19013B)
# - [White, not Hispanic Households](https://data.census.gov/cedsci/table?g=0500000US48167_1600000US4828068,4837252&tid=ACSDT5Y2012.B19013H)
# - [Hispanic Households](https://data.census.gov/cedsci/table?g=0500000US48167_1600000US4828068,4837252&tid=ACSDT5Y2012.B19013I)
#     
# Differences in the housing unit allocation and the Census count may be due to differences between political boundaries and the building inventory. 
# 
# > Rosenheim, Nathanael (2021) “Detailed Household and Housing Unit Characteristics: Data and Replication Code.” DesignSafe-CI. https://doi.org/10.17603/ds2-jwf6-s535 v2
# 
# The housing unit allocation, plus the building results will become the input for the social science models such as the population dislocation model.

# # 2) Hazards and Damages

# ![HazardsandDamages.png](attachment:HazardsandDamages.png)

# ## 2a) Hazard Model (Hurricane)
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

# ### Building damage
# 
# ### 2.1 Building Fragility
# 
# The impact of the surge-wave action on buildings was assumed to be independent of the wind impacts. The surge-wave action was modeled using the surge-wave fragility surfaces developed by Do. et al. (2020), while the wind action was modeled using the wind fragility functions developed by Memari et al. (2018) assuming that the maximum hurricane wind speed does not occur with the maximum surge and wave height. None of the surge-wave and wind fragility used herein accounts for content damage. Therefore, the flood fragility functions developed by Nofal and van de Lindt (2020b) were used to account for content damage, i.e. due to surge. The vulnerability of structural components (e.g., roof, walls, foundation, slabs, etc.) was derived from the surge-wave fragility surface developed and the wind fragility curves developed after extracting the intensities of surge, wave, and wind speed from the hazard maps. The vulnerability of the interior contents and other non-structural components were calculated from flood fragility functions (e.g., depth fragility function, depth-duration fragility function) based on the extracted surge height.
# 
# ### Building Damage:
# 
# The developed multi-hazard hurricane damage approach uses five input variables - significant wave height, the surge depth, building elevation from the ground, maximum wind speed, and flood duration, respectively. All these variables were used as inputs for three stages of fragility analysis to account for structure and content damage and losses for each building within the community. First, the significant wave height, the surge water depth, and elevation from the ground were used to account for the structural system exceedance probability of each DS using the multi-variate 3-D surge-wave fragility function developed by Do et al. (2020). Second, the maximum wind speed for each building was used to account for another list of exceedance probabilities for each DS using the fragility portfolio developed by Memari et al. (2018). Then, flood depth, and the building elevation from the ground for each building were used in a static flood fragility functions developed by Nofal and van de Lindt (2020) to account for content damage. For damage analysis, a single DS was assigned to each building based on the maximum DS calculated from surge-wave, wind, and flood Eq. (1). 
# 

# <img src="data:image/jpeg;base64,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YSB+Dv5yNv611dAEFje2+o2EF7ZSrNb3EayxSL0ZSMg/lU9cp4CH2G31jQwTs0nU5YoQf4YpMTIPoBJj8K6ugAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAK5H4eHdZa8x6tr17k+v7zH9K66uO+G6BNP10L31++PX/prQB2NZ2v3l5p+g3l5psdtJPbxNKEupDHGQoycsAccDritGue8aMZ9Gh0pCd+q3Udnx/cJ3Sf+Q1egCp8NPGp+IHge2157RbOSWSSN4Ek3hCrEdcDtg9O9QfEX4hQeBrGxigtl1DWNTuFt7Gx8zZ5jEgFicHCjPXHUiuW+FOqW3hfQ/GlpeZEWleIblI4kGWfeV2Io7licAepqhcaXca98fPDttqoV72xtn1m/CnKwfwQQKfROue5LHvQB7FYG9Nkh1RYEuf41t2LIPoSAT+VWawvFniiHwvpcUvkNd3t5OtrY2aHDXEzfdXPYdyewBNcp471rxX4T8N2N5a6pb3GsalexWMdobdfs6vKcZT+MlcZyzEHHQUAekUVyXxBfxNYeC7vUfC2pRw3un27TtHJarKLnYMsv+zkA9BVbw9qniXxbcaJ4isLu0svDlxb75bGSAtPPuThw/8AD83Qegyc5wACx8T/APkST/1/2X/pVFXXVxXxa/5EE/8AYRsf/SqKu1oAK4GDxn4jvPibqXhK003TCthapdPeNcSYCuflQrt4bv1xxXfEgAknAHU1498LrzVNRvfFvi+w0kX39tao6W0jXKxjyYfkQHIyB15GfpQB23hnxqdY8T6x4a1OzFlrGkbHkWOTzIponGVkQkA9xkEce9a/iXXbfwz4Y1HWr3/U2Nu0zD+9gcD8TgfjWB4L8EXOia9rXiXXrqO61zWnHm+QCIreJfuRJnk4GMk4zjpXN/tI3klt8GruOJiv2q6ghbHcbt2P/HaAOn+GFpcDwRa6vqh36rrY/tC8lPUtJyq/7qptUDsBW34n1O40Xwzf6naLbu9nA85W4cqhVVJIyASO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sDP9z3oA7KsK/wDGOj6Zr1vpF7LcRz3MixRy/ZZDD5jfdQy7dgY9gTmqVhNqjahAJpPEZjLjcLi3sxHj/aKrux9OaoeMbw32oWK6DrFvcX+m6jB5+jEJIJcsMlhjepVW3hs4G0HFAHc0UUUAFFUNa1vT/Duky6nrE/2e0hKh5AjPgswUDaoJOSQOBWFbfE3wtd3UVvBd3plmcRoG0q6UEk4HJjwPqeKAOsooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKwdc8a6H4cvUtNWnuY5nQSKIrGeYbckdY0Ydumc0Ab1FYWgeM9C8T3Nxb6LdySzWyK8sctrLCyqxIU4kVcg7T09K3aACiiigAooooAKKKKAOV8O/wDI/eMP+u1p/wCk611Vcr4d/wCR+8Yf9drT/wBJ1rqqACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKoa5o9vr+h3el3u4RXMZQspwyHqGHoQQCPcVfooAw/DmqXUsJ0zXAI9XtF2y8YW5UcCZPVW7j+E5B7Z2mjRyC6KxHTIzikeGKR0eSNWaM5RiMlT7elPoAjWCFG3JEit6hQKkoooAKakaR58tFXPXaMZp1FABXP61rmvafqHkaV4SutWg2BvtEV7bxDPddruDx9K6CigDjv8AhKvFv/RO7/8A8Gdn/wDHK623kkltopJoTBIyBniZgShI5XI4OOnFSUUAR+RD/wA8k65+6KkoooA8r8cWttN4x17ztPurlZPDEkYK2ssiNPvJQKQCu/GCMc1Z8FyFfHluyW13Elz4btvtLyWsqLJcq53b2ZQDIFPfnFel0UAeR3ENw/jqx1CLTb22kh8SSJOxtpZJWhMTqHabGPJY7dqDKjjJz0lis9M0jxZFqMWjzy+Hr7UWZLUWEha0vVXb9p2bMiNsY9AcMOvHq9FABRRRQAUUUhAZSCMgjBFAHLa4p8W3y6DbZbTIZVfVLgfdfaQwt1Pc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dNKiigAooooAKKKKACiiigAooooAKKKKACsvS/Dum6NqWp32nwtHcarMJ7tjIW3uF2ggE8celalFABRRRQAUUUUAFFFFAFe/tXvbGW2iupbRpBt86EgOo77SQcHHftTdN0200jTYbDToVgtoF2oi9vfPck8knkk1aooAKKKKACiiigAooooAKzbXQ7ew1q61CyZ4Ptg3XNuuPLkk4xJjs2BgkdeM9K0qKACiiigAooooAKKKKACiiigAooooAKKKKACiiigDLuPDum3Xiaz1+aFjqNnA8EMnmEBUf7w25welalFFABRRRQAUUUUAFNkVmjZUfYxBAbGdp9adRQBn6NotrolrJFbF5JZpDNcXEp3STyHqzH16D0AAAwBVHXNT8S2V6keheHLfVLcoC00upi3Ktk/LtMbZ4xznvW9RQBxvhmy8Qz+NtU13xBpNvpaXFjBaxRRXouCxR5GJJCrj74rsqKKACiiigAooooAKKKwPEeo3UqnRNCY/2pdptMwGVsozwZWPqB91epOOwJABQ8BD7ZJ4h1ocpqWrS+S396OELCp+mY2P4111VNK0y20XSLXTbBNlvaxLFGCcnAHc9z71boAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigBiQxxM7RxqjSHLlRjcfU0+iigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigApkcMcRcxRqhdtzFRjcfU+tPooAKKKKACiiigD/9k=" />

# where Bldg_DS(IMs = x1: x5) is the building DS corresponding to the five intensity measures. P[DS_SWi|(IM = x1:x3)] = the exceedance probability of DS_SWi at (IMs = x1:x3) calculated from the surge-wave fragility, and  P[DS_SW i+1|(IM = x1:x3)] = the exceedance probability of DS_SWi+1 at (IMs = x1: x3) calculated from the surge-wave fragility. P[DS_Wi|(IM = x4)] = the exceedance probability of DS_Wi at (IMs = x4) calculated from the wind fragility, and  P[DS_W i+1|(IM = x4)] = the exceedance probability of DS_Wi+1 at (IMs = x1, x2,x3) calculated from the wind fragility. P[DS_Fi|(IM = x1, x3, x5)] = the exceedance probability of DS_Fi at (IMs = x1, x3, x5) calculated from the flood fragility, and  P[DS_F i+1|(IM = x1, x3, x5)] = the exceedance probability of DS_Fi+1 at (IMs = x1, x2,x3) calculated from the flood fragility.

# In[19]:


# use utility method of pyicore-viz package to visualize the fragility
fragility_set = FragilityCurveSet(FragilityService(client).get_dfr3_set("5f6ccf67de7b566bb71b202d"))
plt = plotviz.get_fragility_plot_3d(fragility_set, 
                                            title="Galveston empirical fragility model developed "
                                            "based on Hurricane Ike surveys",
                                            limit_state="LS_0")
plt.show()


# In[20]:


hazard_type = "hurricane"
# Galveston deterministic Hurricane, 3 datasets - Kriging
hazard_id = "5fa5a228b6429615aeea4410"

# visualization
wave_height_id = "5f15cd62c98cf43417c10a3f"
surge_level_id = "5f15cd5ec98cf43417c10a3b"

# Hurricane building mapping (with equation)
mapping_id = "602c381a1d85547cdc9f0675"
fragility_service = FragilityService(client)
mapping_set = MappingSet(fragility_service.get_mapping(mapping_id))

# Building Wind Fragility mapping
wind_mapping_id = "62fef3a6cef2881193f2261d"
wind_mapping_set = MappingSet(fragility_service.get_mapping(wind_mapping_id))

# Surge-wave mapping
sw_mapping_id = "6303e51bd76c6d0e1f6be080"
sw_mapping_set = MappingSet(fragility_service.get_mapping(sw_mapping_id))

# flood mapping
flood_mapping_id = "62fefd688a30d30dac57bbd7"
flood_mapping_set = MappingSet(fragility_service.get_mapping(flood_mapping_id))


# In[21]:


# visualize wave height
dataset = Dataset.from_data_service(wave_height_id, DataService(client))
map = geoviz.map_raster_overlay_from_file(dataset.get_file_path('tif'))
map


# In[22]:


# add opacity control - NOTE: It takes time before the opacity takes effect.
map.layers[1].interact(opacity=(0.0,1.0,0.01))


# In[23]:


# visualize surge level
dataset = Dataset.from_data_service(surge_level_id, DataService(client))
map = geoviz.map_raster_overlay_from_file(dataset.get_file_path('tif'))
map


# In[24]:


# add opacity control - NOTE: It takes time before the opacity takes effect.
map.layers[1].interact(opacity=(0.0,1.0,0.01))


# ### 2.2 Building Damage

# ### 2.2.1 Wind building damage

# In[25]:


# wind building damage
w_bldg_dmg = BuildingDamage(client)
w_bldg_dmg.load_remote_input_dataset("buildings", bldg_dataset_id)
w_bldg_dmg.set_input_dataset('dfr3_mapping_set', wind_mapping_set)
w_bldg_dmg.set_parameter("result_name", "Galveston-wind-dmg")
w_bldg_dmg.set_parameter("hazard_type", hazard_type)
w_bldg_dmg.set_parameter("hazard_id", hazard_id)
w_bldg_dmg.set_parameter("num_cpu", 4)
w_bldg_dmg.run_analysis()


# ### 2.2.2 Surge-Wave building damage

# In[26]:


# surge-wave building damage
bldg_dmg = BuildingDamage(client)
bldg_dmg.load_remote_input_dataset("buildings", bldg_dataset_id)
bldg_dmg.set_input_dataset('dfr3_mapping_set', sw_mapping_set)
bldg_dmg.set_parameter("result_name", "Galveston-sw-dmg")
bldg_dmg.set_parameter("hazard_type", hazard_type)
bldg_dmg.set_parameter("hazard_id", hazard_id)
bldg_dmg.set_parameter("num_cpu", 4)
bldg_dmg.run_analysis()


# ### Flood building damage

# In[27]:


# flood building damage
f_bldg_dmg = BuildingDamage(client)
f_bldg_dmg.load_remote_input_dataset("buildings", bldg_dataset_id)
f_bldg_dmg.set_input_dataset('dfr3_mapping_set', flood_mapping_set)
f_bldg_dmg.set_parameter("result_name", "Galveston-flood-dmg")
f_bldg_dmg.set_parameter("hazard_type", hazard_type)
f_bldg_dmg.set_parameter("hazard_id", hazard_id)
f_bldg_dmg.set_parameter("num_cpu", 4)
f_bldg_dmg.run_analysis()


# ### Combine wind, wave and surge building damage

# In[28]:


surge_wave_damage = bldg_dmg.get_output_dataset("ds_result")
wind_damage = w_bldg_dmg.get_output_dataset("ds_result")
flood_damage = f_bldg_dmg.get_output_dataset("ds_result")

result_name = "Galveston-combined-dmg"
combined_bldg_dmg = CombinedWindWaveSurgeBuildingDamage(client)
combined_bldg_dmg.set_input_dataset("surge_wave_damage", surge_wave_damage)
combined_bldg_dmg.set_input_dataset("wind_damage", wind_damage)
combined_bldg_dmg.set_input_dataset("flood_damage", flood_damage)
combined_bldg_dmg.set_parameter("result_name", result_name)
# combined_bldg_dmg.run_analysis()

# combined_dmg = combined_bldg_dmg.get_output_dataset("result")
# combined_dmg_df = combined_dmg.get_dataframe_from_csv(low_memory=False)

# Display top 5 rows of output data
# combined_dmg_df.head()


# ### 2.3 Electric Power Facility Damage

# In[29]:


# EPF fragility mapping
epf_mapping_id = "62fac92ecef2881193f22613"
epf_mapping_set = MappingSet(fragility_service.get_mapping(epf_mapping_id))

epf_dmg_hurricane_galveston = EpfDamage(client)
epf_dmg_hurricane_galveston.load_remote_input_dataset("epfs", "62fc000f88470b319561b58d")
epf_dmg_hurricane_galveston.set_input_dataset('dfr3_mapping_set', epf_mapping_set)
epf_dmg_hurricane_galveston.set_parameter("result_name", "Galveston-hurricane-epf-damage")
epf_dmg_hurricane_galveston.set_parameter("fragility_key", "Non-Retrofit Fragility ID Code")
epf_dmg_hurricane_galveston.set_parameter("hazard_type", hazard_type)
epf_dmg_hurricane_galveston.set_parameter("hazard_id", hazard_id)
epf_dmg_hurricane_galveston.set_parameter("num_cpu", 8)

# Run Analysis
epf_dmg_hurricane_galveston.run_analysis()


# # 3) Functionality

# ## 3a) Functionality Models

# ![functionality.png](attachment:functionality.png)

# ## 3b) Functionality of Physical Infrastructure

# In[30]:


# Retrieve result dataset from surge_wave_damage
building_dmg_result = bldg_dmg.get_output_dataset('ds_result')


# In[31]:


# Convert dataset to Pandas DataFrame
bdmg_df = building_dmg_result.get_dataframe_from_csv(low_memory=False)

# Display top 5 rows of output data
bdmg_df.head()


# In[32]:


bdmg_df.DS_0.describe()


# In[33]:


bdmg_df.DS_3.describe()


# ## 3d) Social Science Modules

# Population Dislocation
# Population dislocation refers to households that will be forced to leave their pre-event residence due to hazard related damages. Population dislocation is a function of structure value loss due to damage, neighborhood characteristics and structure type.

# #### 3d.1 Use new pyincore-data utility to obtain Block Group Data for County

# In[34]:


from pyincore_data.censusutil import CensusUtil
state_counties = ['48167']
blockgroup_df, bgmap = CensusUtil.get_blockgroupdata_for_dislocation(state_counties, 
                                                out_csv=True, 
                                                out_shapefile=False, 
                                                out_html=False,
                                                program_name = "BlockGroupData",
                                                geo_name = "Galveston")


# In[35]:


blockgroup_df.head()


# In[36]:


bg_data = Dataset.from_file(
    'BlockGroupData/BlockGroupData_Galveston.csv',
    'incore:blockGroupData')


# #### 3d.2 Population Dislocation

# In[37]:


pop_dis = PopulationDislocation(client)


# In[38]:


# Value loss parameters DS 0-3
value_loss = "60354810e379f22e16560dbd"


# In[39]:


pop_dis.set_input_dataset("block_group_data", bg_data)
pop_dis.load_remote_input_dataset("value_loss_param", value_loss)

pop_dis.set_input_dataset("building_dmg", building_dmg_result)
pop_dis.set_input_dataset("housing_unit_allocation", hua_result)

result_name = "galveston-pop-disl-results"
seed = 1111

pop_dis.set_parameter("result_name", result_name)
pop_dis.set_parameter("seed", seed)


# In[40]:


pop_dis.run_analysis()


# #### 3.d.3 Explore Population Dislocation Results

# In[41]:


# Retrieve result dataset
population_dislocation_result = pop_dis.get_output_dataset("result")

# Convert dataset to Pandas DataFrame
pd_df = population_dislocation_result.get_dataframe_from_csv(low_memory=False)


# In[42]:


poptable.pop_results_table(pd_df, 
                  who = "Total Population by Households", 
                  what = "by Tenure Status and Dislocation",
                  where = "Galveston County TX",
                  when = "2010",
                  row_index = "Tenure Status",
                  col_index = 'Population Dislocation',
                  row_percent = '1 Dislocates')


# In[43]:


poptable.pop_results_table(pd_df.loc[pd_df['placeNAME10']=='Galveston'].copy(),
                  who = "Total Population by Households", 
                  what = "by Tenure Status and Dislocation",
                  where = "Galveston County TX",
                  when = "2010",
                  row_index = "Tenure Status",
                  col_index = 'Population Dislocation',
                  row_percent = '1 Dislocates')


# In[44]:


poptable.pop_results_table(pd_df.loc[pd_df['placeNAME10']=='Galveston'].copy(), 
                  who = "Total Population by Households", 
                  what = "by Race, Ethnicity and Dislocation",
                  where = "Galveston County TX",
                  when = "2010",
                  row_index = "Race Ethnicity",
                  col_index = 'Population Dislocation',
                  row_percent = '1 Dislocates')


# In[45]:


# Add household income group categories for table
# Code will be added to next release of pop_results_table on pyincore-viz
def add_label_cat_conditions_df(df, conditions):
    """Label Categorical Variable Values and add to dataframe.
    Use this function with values are based on conditions.
    
    Args:
        df (obj): Pandas DataFrame object.
        conditions (dict): Dictionary of conditions for value labels.
    Returns:
        object: Pandas DataFrame object.
    """

    cat_var = conditions['cat_var']['variable_label']

    df[cat_var] = "No Data"

    for item in conditions['condition_list'].keys():
        condition =  conditions['condition_list'][item]['condition']
        value_label = conditions['condition_list'][item]['value_label']
        df.loc[eval(condition), cat_var] = value_label

    # Set variable to missing if no data- makes tables look nicer
    df.loc[(df[cat_var] == "No Data"), 
        cat_var] = np.nan

    return df

def add_label_cat_values_df(df, valuelabels, variable = ''):
    """Label Categorical Variable Values and add to dataframe.
    Use this function with categorical values 
    are integer values.
    Args:
        df (obj): Pandas DataFrame object.
        valuelabels (dict): Dictionary of value labels.
        variable (str): Variable to label.
    Returns:
        object: Pandas DataFrame object with new column that has value labels.
    """

    if variable == '':
        variable  = valuelabels['categorical_variable']['variable']
    variable_label = valuelabels['categorical_variable']['variable_label']

    df[variable_label] = "No Data"

    for item in valuelabels['value_list'].keys():
        value =  valuelabels['value_list'][item]['value']
        value_label = valuelabels['value_list'][item]['value_label']
        df.loc[df[variable] == value, variable_label] = value_label

    # Set variable to missing if no data- makes tables look nicer
    df.loc[(df[variable_label] == "No Data"), 
        variable_label] = np.nan

    return df

hhinc_valuelabels = {'categorical_variable': {'variable' : 'hhinc',
                                'variable_label' : 'Household Income Group',
                                'notes' : '5 Household Income Groups based on random income.'},
                    'value_list' : {
                        1 : {'value': 1, 'value_label': "1 Less than $15,000"},
                        2 : {'value': 2, 'value_label': "2 $15,000 to $24,999"},
                        3 : {'value': 3, 'value_label': "3 $25,000 to $74,999"},
                        4 : {'value': 4, 'value_label': "4 $75,000 to $99,999"},
                        5 : {'value': 5, 'value_label': "5 $100,000 or more"}}
                    }

pd_df = add_label_cat_values_df(pd_df, valuelabels = hhinc_valuelabels)


# In[46]:


poptable.pop_results_table(pd_df.loc[pd_df['placeNAME10']=='Galveston'].copy(),
                  who = "Total Households", 
                  what = "by Household Income Group and Dislocation",
                  where = "Galveston Island TX",
                  when = "2010",
                  row_index = "Household Income Group",
                  col_index = 'Population Dislocation',
                  row_percent = '1 Dislocates')


# #### 3.d.4 Explore Population Dislocation and Building Damage Results

# In[47]:


ds3_conditions = {'cat_var' : {'variable_label' : 'Probability Complete Failure',
                         'notes' : 'Probability of complete failure based on damage state 3'},
              'condition_list' : {
                1 : {'condition': "(df['DS_3'] == 0)", 'value_label': "0 0%"},
                2 : {'condition': "(df['DS_3'] > 0)", 'value_label': "1 Less than 20%"},
                3 : {'condition': "(df['DS_3'] > .2)", 'value_label': "2 20-40%"},
                4 : {'condition': "(df['DS_3'] > .4)", 'value_label': "3 40-60%"},
                5 : {'condition': "(df['DS_3'] > .6)", 'value_label': "4 60-80%"},
                6 : {'condition': "(df['DS_3'] > .8)", 'value_label': "5 80-100%"},
                7 : {'condition': "(df['DS_3'] == 1)", 'value_label': "6 100%"}}
            }

      
dsf_valuelabels = {'categorical_variable' : {'variable' : 'd_sf',
                   'variable_label' : 'Single Family Dwelling',
                   'notes' : 'Categories for single family dwellings'},
              'value_list' : {
                1 : {'value': 0, 'value_label': "0 Not Single Family"},
                2 : {'value': 1, 'value_label': "1 Single Family"}}
            }


# In[48]:


pd_df = add_label_cat_conditions_df(pd_df, conditions = ds3_conditions)
pd_df = add_label_cat_values_df(pd_df, valuelabels = dsf_valuelabels)


# In[49]:


poptable.pop_results_table(pd_df.loc[pd_df['placeNAME10']=='Galveston'].copy(), 
                  who = "Total Households", 
                  what = "by Probability of Complete Failure and Dislocation",
                  where = "Galveston Island TX",
                  when = "2010",
                  row_index = 'Probability Complete Failure',
                  col_index = 'Population Dislocation',
                  row_percent = '1 Dislocates')


# In[50]:


poptable.pop_results_table(pd_df.loc[(pd_df['DS_3'] > .8) &
                                     (pd_df['placeNAME10']=='Galveston')].copy(),
                  who = "Total Population by Households", 
                  what = "for High Damaged Structures by Single Family Dwelling",
                  where = "Galveston Island TX",
                  when = "2010",
                  row_index = 'Single Family Dwelling',
                  col_index = 'Population Dislocation',
                  row_percent = '0 Does not dislocate')


# In[51]:


poptable.pop_results_table(pd_df.loc[(pd_df['DS_3'] > .8) &
                                     (pd_df['placeNAME10']=='Galveston')].copy(),
                  who = "Total Population by Households", 
                  what = "for High Damaged Structures by Race Ethnicity",
                  where = "Galveston Island TX",
                  when = "2010",
                  row_index = 'Race Ethnicity',
                  col_index = 'Population Dislocation',
                  row_percent = '0 Does not dislocate')


# # 4) Recovery

# ![Recovery.png](attachment:Recovery.png)

# * **j** is the index for time 
# * **m** is the community lifetime
# * **K** is the index for policy levers and decision combinations (PD)

# ### 4.1 Household-Level Housing Recovery Analysis
# 
# The Household-Level Housing Recovery (HHHR) model developed by Sutley and Hamideh (2020) is used to simulate the housing recovery process of dislocated households.
# 
# The computation operates by segregating household units into five zones as a way of assigning social vulnerability. Then, using this vulnerability in conjunction with the Transition Probability Matrix (TPM) and the initial state vector, a Markov chain computation simulates the most probable states to generate a stage history of housing recovery changes for each household. The detailed process of the HHHR model can be found in Sutley and Hamideh (2020).
# 
# >Sutley, E.J. and Hamideh, S., 2020. Postdisaster housing stages: a Markov chain approach to model sequences and duration based on social vulnerability. Risk Analysis, 40(12), pp.2675-2695.
# 
# The Markov chain model consists of five discrete states at any time throughout the housing recovery process. The five discrete states represent stages in the household housing recovery process, including emergency shelter (1), temporary shelter (2); temporary housing (3); permanent housing (4), and failure to recover (5). The model assumes that a household can be in any of the first four stages immediately after a disaster. If the household reported not being dislocated, household will begin in stage 4. 

# ### 4.2 Set Up and Run Household-level Housing Sequential Recovery

# In[52]:


# Parameters
state = "texas"
county = "galveston"
year = 2020


# In[53]:


# get fips code to use fetch census data
fips = CensusUtil.get_fips_by_state_county(state=state, county=county)
state_code = fips[:2]
county_code = fips[2:]


# In[54]:


def demographic_factors(state_number, county_number, year, geo_type="tract:*"):

    _, df_1 = CensusUtil.get_census_data(state=state_code, county=county_code, year=year,
                                                              data_source="acs/acs5",
                                                              columns="GEO_ID,B03002_001E,B03002_003E",
                                                              geo_type=geo_type)
    df_1["factor_white_nonHispanic"] = df_1[["B03002_001E","B03002_003E"]].astype(int).apply(lambda row: row["B03002_003E"]/row["B03002_001E"], axis = 1)

    _, df_2 = CensusUtil.get_census_data(state=state_code, county=county_code, year=year,
                                                  data_source="acs/acs5",
                                                  columns="B25003_001E,B25003_002E",
                                                  geo_type=geo_type)
    df_2["factor_owner_occupied"] = df_2.astype(int).apply(lambda row: row["B25003_002E"]/row["B25003_001E"], axis = 1)
    
    _, df_3 = CensusUtil.get_census_data(state=state_code, 
                                         county=county_code, 
                                         year=year,
                                         data_source="acs/acs5",
                                         columns="B17021_001E,B17021_002E",
                                         geo_type=geo_type)
    df_3["factor_earning_higher_than_national_poverty_rate"] = df_3.astype(int).apply(lambda row: 1-row["B17021_002E"]/row["B17021_001E"], axis = 1)
    
    _, df_4 = CensusUtil.get_census_data(state=state_code, 
                                         county=county_code, 
                                         year=year,
                                         data_source="acs/acs5", 
                                         columns="B15003_001E,B15003_017E,B15003_018E,B15003_019E,B15003_020E,B15003_021E,B15003_022E,B15003_023E,B15003_024E,B15003_025E",
                                         geo_type=geo_type)
    df_4["factor_over_25_with_high_school_diploma_or_higher"] = df_4.astype(int).apply(lambda row: (row["B15003_017E"] 
                                                                                                    + row["B15003_018E"] 
                                                                                                    + row["B15003_019E"] 
                                                                                                    + row["B15003_020E"] 
                                                                                                    + row["B15003_021E"] 
                                                                                                    + row["B15003_022E"] 
                                                                                                    + row["B15003_023E"] 
                                                                                                    + row["B15003_024E"] 
                                                                                                    + row["B15003_025E"])/row["B15003_001E"], axis = 1)

    if geo_type == 'tract:*':
        _, df_5 = CensusUtil.get_census_data(state=state_code, 
                                             county=county_code, 
                                             year=year,
                                             data_source="acs/acs5",
                                             columns="B18101_001E,B18101_011E,B18101_014E,B18101_030E,B18101_033E",
                                             geo_type=geo_type)
        df_5["factor_without_disability_age_18_to_65"] = df_5.astype(int).apply(lambda row: (row["B18101_011E"] + row["B18101_014E"] + row["B18101_030E"] + row["B18101_033E"])/row["B18101_001E"], axis = 1)
    
    elif geo_type == 'block%20group:*':
        _, df_5 = CensusUtil.get_census_data(state=state_code, 
                                             county=county_code, 
                                             year=year,
                                             data_source="acs/acs5",
                                             columns="B01003_001E,C21007_006E,C21007_009E,C21007_013E,C21007_016E",
                                             geo_type=geo_type)

        df_5['factor_without_disability_age_18_to_65'] = df_5.astype(int).apply(lambda row: (row['C21007_006E']+
                                                                                 row['C21007_006E']+
                                                                                 row['C21007_009E']+
                                                                                 row['C21007_013E'])
                                                                                /row['C21007_016E'], axis = 1)

    df_t = pd.concat([df_1[["GEO_ID","factor_white_nonHispanic"]],
                      df_2["factor_owner_occupied"],
                      df_3["factor_earning_higher_than_national_poverty_rate"], 
                      df_4["factor_over_25_with_high_school_diploma_or_higher"],
                      df_5["factor_without_disability_age_18_to_65"]], 
                     axis=1, join='inner')
    
    # extract FIPS from geo id
    df_t["FIPS"] = df_t.apply(lambda row: row["GEO_ID"].split("US")[1], axis = 1)
        
    return df_t


# In[55]:


def national_ave_values(year, data_source="acs/acs5"):
    _, nav1 = CensusUtil.get_census_data(state="*", county=None, year=year, data_source=data_source,
                             columns="B03002_001E,B03002_003E",geo_type=None)
    nav1 = nav1.astype(int)
    nav1_avg ={"feature": "NAV-1: White, nonHispanic", 
                "average": nav1['B03002_003E'].sum()/ nav1['B03002_001E'].sum()}

    _, nav2 = CensusUtil.get_census_data(state="*", county=None, year=year, data_source=data_source,
                             columns="B25003_001E,B25003_002E",geo_type=None)
    nav2 = nav2.astype(int)
    nav2_avg = {"feature": "NAV-2: Home Owners", 
                "average": nav2['B25003_002E'].sum()/nav2['B25003_001E'].sum()}

    _, nav3 = CensusUtil.get_census_data(state="*", county=None, year=year, data_source=data_source,
                             columns="B17021_001E,B17021_002E",geo_type=None)
    nav3 = nav3.astype(int)
    nav3_avg = {"feature": "NAV-3: earning higher than national poverty rate", 
                "average": 1-nav3['B17021_002E'].sum()/nav3['B17021_001E'].sum()}

    _, nav4 = CensusUtil.get_census_data(state="*", 
                                         county=None, 
                                         year=year,
                                         data_source="acs/acs5",
                                         columns="B15003_001E,B15003_017E,B15003_018E,B15003_019E,B15003_020E,B15003_021E,B15003_022E,B15003_023E,B15003_024E,B15003_025E",
                                         geo_type=None)
    nav4 = nav4.astype(int)
    nav4['temp'] = nav4.apply(lambda row: row['B15003_017E']+row['B15003_018E']+row['B15003_019E']+
                              row['B15003_020E']+row['B15003_021E']+row['B15003_022E']+row['B15003_023E']+
                              row['B15003_024E']+row['B15003_025E'], axis = 1)
    nav4_avg = {"feature": 'NAV-4: over 25 with high school diploma or higher', 
                "average": nav4['temp'].sum()/nav4['B15003_001E'].sum()}

    _, nav5 = CensusUtil.get_census_data(state="*", county=None, year=year, data_source=data_source,
                             columns="B18101_001E,B18101_011E,B18101_014E,B18101_030E,B18101_033E",
                                         geo_type=None)
    nav5 = nav5.astype(int)
    nav5['temp'] = nav5.apply(lambda row: row['B18101_011E']+row['B18101_014E']+row['B18101_030E']+row['B18101_033E'], axis = 1)
    nav5_avg = {"feature": 'NAV-5: without disability age 18 to 65', 
                "average": nav5["temp"].sum()/nav5["B18101_001E"].sum()}
    
    navs = [nav1_avg, nav2_avg, nav3_avg, nav4_avg, nav5_avg]
    
    return navs


# In[56]:


navs = national_ave_values(year=year)
national_vulnerability_feature_averages = Dataset.from_csv_data(navs, name="national_vulnerability_feature_averages.csv",
                                                                 data_type="incore:socialVulnerabilityFeatureAverages")

geo_type = "block%20group:*"
# geo_type = "tract:*"
social_vunlnerability_dem_factors_df = demographic_factors(state_code, county_code, year=year, geo_type=geo_type)

# Temp fix: remove bad data point
social_vunlnerability_dem_factors_df = social_vunlnerability_dem_factors_df.dropna()

social_vunlnerability_dem_factors = Dataset.from_dataframe(social_vunlnerability_dem_factors_df, 
                                                           name="social_vunlnerability_dem_factors",
                                                           data_type="incore:socialVulnerabilityDemFactors")


# In[57]:


social_vulnerability = SocialVulnerability(client)

social_vulnerability.set_parameter("result_name", "social_vulnerabilty")
social_vulnerability.set_input_dataset("national_vulnerability_feature_averages", national_vulnerability_feature_averages)
social_vulnerability.set_input_dataset("social_vulnerability_demographic_factors", social_vunlnerability_dem_factors)


# In[58]:


# Run social vulnerability damage analysis
result = social_vulnerability.run_analysis()


# In[59]:


# Retrieve result dataset
sv_result = social_vulnerability.get_output_dataset("sv_result")

# Convert dataset to Pandas DataFrame
df = sv_result.get_dataframe_from_csv()

# Display top 5 rows of output data
df.head()


# In[60]:


# Transition probability matrix per social vulnerability level, from Sutley and Hamideh (2020).
transition_probability_matrix = "60f5e2ae544e944c3cec0794"
# Initial mass probability function for household at time 0
initial_probability_vector = "60f5e918544e944c3cec668b"


# In[61]:


# Create housing recovery instance
housing_recovery = HousingRecoverySequential(client)

# Load input datasets from dislocation, tpm, and initial probability function
#housing_recovery.load_remote_input_dataset("population_dislocation_block", population_dislocation)
housing_recovery.set_input_dataset("population_dislocation_block", population_dislocation_result)

housing_recovery.load_remote_input_dataset("tpm", transition_probability_matrix)
housing_recovery.load_remote_input_dataset("initial_stage_probabilities", initial_probability_vector)


# In[62]:


# Initial value to seed the random number generator to ensure replication
seed = 1234
# A size of the analysis time step in month
t_delta = 1.0
# Total duration of Markov chain recovery process
t_final = 90.0


# In[63]:


# Specify the result name
result_name = "housing_recovery_result"

# Set analysis parameters
housing_recovery.set_parameter("result_name", result_name)
housing_recovery.set_parameter("seed", seed)
housing_recovery.set_parameter("t_delta", t_delta)
housing_recovery.set_parameter("t_final", t_final)

# Chain with SV output
housing_recovery.set_input_dataset('sv_result', sv_result)

# Run the household recovery sequence analysis - Markov model
housing_recovery.run()


# ## 6 a) Sufficient Quality Solutions Found?

# In[64]:


# Retrieve result dataset
housing_recovery_result = housing_recovery.get_output_dataset("ds_result")

# Convert dataset to Pandas DataFrame
df_hhrs = housing_recovery_result.get_dataframe_from_csv()

# Display top 5 rows of output data
df_hhrs.head()


# ### Explore Household-level Housing Recovery Results

# In[65]:


df_hhrs['1'].describe()


# In[66]:


# Locate observations where timestep 1 does not equal 4
df_hhrs[df_hhrs['13'] != 4].head()


# 
# > Plot Housing Recovery Sequence Results

# >view recovery sequence results for specific households

# In[67]:


df=df_hhrs.drop(['guid', 'huid', 'Zone', 'SV'], axis=1).copy()
df=df.to_numpy()
t_steps=int(t_final)-1

# Plot stage histories and stage changes using pandas.
# Generate timestep labels for dataframes.
label_timestep = []
for i4 in range(0, t_steps):
    label_timestep.append(str(i4))
    
ids = [9700,14343,48] # select specific household by id numbers
for id in ids:
    HH_stagehistory_DF = pd.DataFrame(np.transpose(df[id, 1:]),
                                      index=label_timestep)
    ax = HH_stagehistory_DF.reset_index().plot(x='index',
                                               yticks=[1, 2, 3, 4, 5],
                                               title='Household Recovery Sequences',
                                               legend=False)
    ax.set(xlabel='Timestep (months)', ylabel='Stage')
    y_ticks_labels = ['1','2','3','4','5']
    ax.set_xlim(0,80)
    ax.set_yticklabels(y_ticks_labels, fontsize = 14)


# > Plot recovery heatmap any stage of recovery

# In[68]:


df_hhrs.head()


# In[69]:


# Keep housing units for Galveston Island
pd_df_community = pd_df.loc[pd_df['placeNAME10']=='Galveston'].copy()
pd_df_community['placeNAME10'].describe()


# In[70]:


# merge household unit information with recovery results
pd_df_hs = pd.merge(left = pd_df_community, 
                    right = df_hhrs,
                    left_on=['guid','huid'],
                    right_on=['guid','huid'],
                    how='left')


# In[71]:


pd_df_hs[['guid','huid']].describe()


# ### Create recovery curve based on income groups
# Code will loop through data over time to create percent in permanent housing at each time step.

# In[72]:


def recovery_curve_byincome(pd_df_hs, 
                            filename,
                            subtitle : str = ""):
    """
    Generate a recovery curve based on building damage, population dislocation,
    and household housing recovery model.
    
    """
    total_housingunits = pd_df_hs.shape[0]
    total_households = pd_df_hs.loc[(pd_df_hs['randincome'].notnull())].shape[0]
    #print("Total housing units:", total_housingunits)
    #print("Total households:", total_households)

    # What is the distribution of housing units by income?
    pd_df_hs['income_quantile'] = pd.qcut(pd_df_hs['randincome'], 5, labels=False)
    #pd_df_hs[['randincome','income_quantile']].groupby('income_quantile').describe()

    total_lowincomehouseholds = pd_df_hs.loc[(pd_df_hs['income_quantile'] == 0)].shape[0]
    total_midincomehouseholds = pd_df_hs.loc[(pd_df_hs['income_quantile'] == 2)].shape[0]
    total_highincomehouseholds = pd_df_hs.loc[(pd_df_hs['income_quantile'] == 4)].shape[0]
    #print("Total low income households:", total_lowincomehouseholds)
    #print("Total mid income households:", total_midincomehouseholds)
    #print("Total high income households:", total_highincomehouseholds)

    # loop over variables 1 to 90
    dict = {}
    # Create dataframe to store values
    # Assume at time 0, all households are in permanent housing
    dict[str(0)] = pd.DataFrame([{'timestep' : 0,
                    'total_households' : total_housingunits,
                    'notperm': 0,
                    'total_highincomehouseholds': total_highincomehouseholds,
                    'total_midincomehouseholds': total_midincomehouseholds,
                    'total_lowincomehouseholds': total_lowincomehouseholds,
                    'lowincome_notperm': 0,
                    'midincome_notperm': 0,
                    'highincome_notperm': 0}])

    for i in range(1,91):
        # create dictionary entry that summarizes the number of households not in permanent housing
        households_notinpermanthousing = pd_df_hs.loc[(pd_df_hs[str(i)] != 4) & 
                                                    (pd_df_hs[str(i)].notnull()) &
                                                    (pd_df_hs['randincome'].notnull())].shape[0]
        lowincome_households_notinpermanthousing = pd_df_hs.loc[(pd_df_hs[str(i)] != 4) &
                                                    (pd_df_hs[str(i)].notnull()) &
                                                    (pd_df_hs['income_quantile'] == 0)].shape[0]
        midincome_households_notinpermanthousing = pd_df_hs.loc[(pd_df_hs[str(i)] != 4) &
                                                    (pd_df_hs[str(i)].notnull()) &
                                                    (pd_df_hs['income_quantile'] == 2)].shape[0]
        highincome_households_notinpermanthousing = pd_df_hs.loc[(pd_df_hs[str(i)] != 4) &
                                                    (pd_df_hs[str(i)].notnull()) &
                                                    (pd_df_hs['income_quantile'] == 4)].shape[0]
                                        
        # Create dataframe to store values
        dict[str(i)] = pd.DataFrame([{'timestep' : i,
                        'total_households' : total_households,
                        'notperm': households_notinpermanthousing,
                        'total_highincomehouseholds': total_highincomehouseholds,
                        'total_midincomehouseholds': total_midincomehouseholds,
                        'total_lowincomehouseholds': total_lowincomehouseholds,
                        'lowincome_notperm': lowincome_households_notinpermanthousing,
                        'midincome_notperm': midincome_households_notinpermanthousing,
                        'highincome_notperm': highincome_households_notinpermanthousing}])

    # convert dictionary to dataframe
    df_summary = pd.concat(dict.values())
    df_summary['percent_allperm'] = 1 - (df_summary['notperm']/ \
                                        df_summary['total_households'] )
    df_summary['percent_lowperm'] = 1 - (df_summary['lowincome_notperm']/ \
                                    df_summary['total_lowincomehouseholds'] )
    df_summary['percent_midperm'] = 1 - (df_summary['midincome_notperm']/ \
                                        df_summary['total_midincomehouseholds'] )
    df_summary['percent_highperm'] = 1 - (df_summary['highincome_notperm']/ \
                                    df_summary['total_highincomehouseholds'] )

    # plot
    # Start new figure
    fig = plt.figure(figsize=(10,6))
    plt.plot('timestep', 'percent_allperm',
            data = df_summary,
            linestyle='-', marker='o', color='black')
    plt.plot('timestep', 'percent_lowperm',
            data = df_summary,
            linestyle='-', marker='o')
    plt.plot('timestep', 'percent_midperm',
            data = df_summary,
            linestyle='-', marker='o')   
    plt.plot('timestep', 'percent_highperm',
            data = df_summary,
            linestyle='-', marker='o')
    # Set y-axis range
    # What is the minimum and maximum values of the percent of households in permanent housing?
    ylim_lower = df_summary['percent_allperm'].min()-.1
    ylim_upper = df_summary['percent_allperm'].max()+.1
    plt.ylim(ylim_lower,ylim_upper)
    # Relable legend
    plt.legend(['All Households','Low Income Households', 'Mid Income', 'High Income'],
                loc='lower right')
    # Add title
    plt.title('Percentage of households in permanent housing by income'+subtitle)
    # Add x and y labels
    plt.xlabel('Timestep (months)')
    plt.ylabel('Percentage')
    # save plot
    plt.savefig(f'{filename}.pdf', bbox_inches='tight', dpi = 1000)

    plt.show()
    # good practice to close the plt object.
    plt.close()


# In[73]:


# Create container to store filenames (use to make a GIF)
# https://towardsdatascience.com/basics-of-gifs-with-pythons-matplotlib-54dd544b6f30
filenames = []
i = 0
recovery_curve_byincome(pd_df_hs = pd_df_hs, 
                        filename = f'recovery_curve_byincome{i}',
                        subtitle=' Baseline')
filenames.append(filename)


# > Plot recovery heatmap after 12 months of recovery

# In[74]:


from ipyleaflet import Map, Heatmap, LayersControl, LegendControl

# What location should the map be centered on?
center_x = pd_df_hs['x'].mean()
center_y = pd_df_hs['y'].mean()

map = Map(center=[center_y, center_x], zoom=11)

stage5_data = pd_df_hs[['y','x','numprec']].loc[pd_df_hs['85']==5].values.tolist()
stage5 = Heatmap(
    locations = stage5_data,
    radius = 5, 
    max_val = 1000, 
    blur = 10, 
    gradient={0.2: 'yellow', 0.5: 'orange', 1.0: 'red'},
    name = 'Stage 5 - Failure to Recover',
)

stage4_data = pd_df_hs[['y','x','numprec']].loc[pd_df_hs['85']==4].values.tolist()
stage4 = Heatmap(
    locations = stage4_data,
    radius = 5, 
    max_val = 1000, 
    blur = 10, 
    gradient={0.2: 'purple', 0.5: 'blue', 1.0: 'green'},
    name = 'Stage 4 - Permanent Housing',
)

map.add_layer(stage4)
map.add_layer(stage5)


control = LayersControl(position='topright')
map.add_control(control)
map


# The five discrete states represent stages in the household housing recovery process, including emergency shelter (1), temporary shelter (2); temporary housing (3); permanent housing (4), and failure to recover (5). The model assumes that a household can be in any of the first four stages immediately after a disaster.

# In[75]:


hhrs_valuelabels = {'categorical_variable' : {'variable' : 'select time step',
                   'variable_label' : 'Household housing recovery stages',
                   'notes' : 'Sutley and Hamideh recovery stages'},
              'value_list' : {
                1 : {'value': 1, 'value_label': "1 Emergency Shelter"},
                2 : {'value': 2, 'value_label': "2 Temporary Shelter"},
                3 : {'value': 3, 'value_label': "3 Temporary Housing"},
                4 : {'value': 4, 'value_label': "4 Permanent Housing"},
                5 : {'value': 5, 'value_label': "5 Failure to Recover"}}
            }

permanenthousing_valuelabels = {'categorical_variable' : {'variable' : 'select time step',
                   'variable_label' : 'Permanent Housing',
                   'notes' : 'Sutley and Hamideh recovery stages'},
              'value_list' : {
                1 : {'value': 1, 'value_label': "0 Not Permanent Housing"},
                2 : {'value': 2, 'value_label': "0 Not Permanent Housing"},
                3 : {'value': 3, 'value_label': "0 Not Permanent Housing"},
                4 : {'value': 4, 'value_label': "1 Permanent Housing"},
                5 : {'value': 5, 'value_label': "0 Not Permanent Housing"}}
            }

pd_df_hs = add_label_cat_values_df(pd_df_hs, valuelabels = hhrs_valuelabels, variable = '13')
pd_df_hs = add_label_cat_values_df(pd_df_hs, valuelabels = permanenthousing_valuelabels,
                        variable = '13')


# In[76]:


poptable.pop_results_table(pd_df_hs.loc[(pd_df_hs['placeNAME10']=='Galveston')].copy(), 
                  who = "Total Population by Householder", 
                  what = "by Housing Type at T=13 by Race Ethnicity",
                  where = "Galveston Island TX",
                  when = "2010",
                  row_index = 'Race Ethnicity',
                  col_index = 'Household housing recovery stages',
                  row_percent = '2 Temporary Shelter'
                  )


# In[77]:


poptable.pop_results_table(pd_df_hs.loc[pd_df_hs['placeNAME10']=='Galveston'].copy(),
                  who = "Total Population by Householder", 
                  what = "by Permanent Housing at T=13 by Race Ethnicity",
                  where = "Galveston Island TX",
                  when = "2010",
                  row_index = 'Race Ethnicity',
                  col_index = 'Permanent Housing',
                  row_percent = "0 Not Permanent Housing"
                  )


# ## 8b) Policy Lever and Decision Combinations
# Hypothetical scenario to elevate all buildings in inventory.

# In[94]:


# Create container to store filenames (use to make a GIF)
# https://towardsdatascience.com/basics-of-gifs-with-pythons-matplotlib-54dd544b6f30
recovery_curve_filenames = []
bldg_gdf_policy2 = bldg_df.copy()
#for i in range(18): 
for i in range(4): 
    
    ################## 1a) updated building inventory ##################  
    print(f"Running Analysis: {i}")
    if i>0:
        bldg_gdf_policy2.loc[bldg_gdf_policy2['ffe_elev'].le(16), 'ffe_elev'] += 4
        #bldg_gdf_policy2.loc[bldg_gdf_policy2['lhsm_elev'].le(16), 'lhsm_elev'] += 1

        bldg_gdf_policy2.to_csv(f'input_df_{i}.csv')
    # Save new shapefile and then use as new input to building damage model
    bldg_gdf_policy2.to_file(driver = 'ESRI Shapefile', filename = f'bldg_gdf_policy_{i}.shp')
    # Plot and save
    #geoviz.plot_gdf_map(bldg_gdf_policy2, column='lhsm_elev',category='False')
    # Code to save the results here
    ####################################################################      
    #
    #
    ################## 2c) Damage to Physical Infrastructure ##################  
    building_inv_policy2 = Dataset.from_file(file_path = f'bldg_gdf_policy_{i}.shp',
                                        data_type='ergo:buildingInventoryVer7')
    # surge-wave building damage
    bldg_dmg = BuildingDamage(client)
    #bldg_dmg.load_remote_input_dataset("buildings", bldg_dataset_id)
    bldg_dmg.set_input_dataset("buildings", building_inv_policy2)
    bldg_dmg.set_input_dataset("dfr3_mapping_set", sw_mapping_set)

    result_name = "Galveston-sw-dmg"

    bldg_dmg.set_parameter("result_name", result_name)
    bldg_dmg.set_parameter("hazard_type", hazard_type)
    bldg_dmg.set_parameter("hazard_id", hazard_id)
    bldg_dmg.set_parameter("num_cpu", 4)

    bldg_dmg.run_analysis()
    ###########################################################################
    #
    #
    ################## 3b) Functionality of Physical Infrastructure ##################
    # Retrieve result dataset
    building_dmg_result_policy2 = bldg_dmg.get_output_dataset('ds_result')
    # Convert dataset to Pandas DataFrame
    bdmg_policy2_df = building_dmg_result_policy2.get_dataframe_from_csv(low_memory=False)
    bdmg_policy2_df.DS_0.describe()
    bdmg_policy2_df.DS_3.describe()
    # Save CSV files for post processing
    bdmg_policy2_df.to_csv(f"bld_damage_results_policy_{i}.csv")
    ##################################################################################
    #
    #
    ############################  3d) Social Science Modules ############################   
    # update building damage
    pop_dis.set_input_dataset("building_dmg", building_dmg_result_policy2)

    # Update file name for saving results
    result_name = "galveston-pop-disl-results_policy2"
    pop_dis.set_parameter("result_name", result_name)
    
    pop_dis.run_analysis()
    
    # Retrieve result dataset
    population_dislocation_result_policy2 = pop_dis.get_output_dataset("result")

    # Convert dataset to Pandas DataFrame
    pd_df_policy2 = population_dislocation_result_policy2.get_dataframe_from_csv(low_memory=False)
    # Save CSV files for post processing
    pd_df_policy2.to_csv(f"pd_df_results_policy_{i}.csv")
    ######################################################################################
    #
    #
    ############################  4) Recovery ############################   
    # Update population dislocation
    housing_recovery.set_input_dataset("population_dislocation_block", 
                            population_dislocation_result_policy2)
    # Update file name for saving results
    result_name = "housing_recovery_result_policy2"
    # Set analysis parameters
    housing_recovery.set_parameter("result_name", result_name)
    housing_recovery.set_parameter("seed", seed)
    
    # Run the household recovery sequence analysis - Markov model
    housing_recovery.run()
    
    # Retrieve result dataset
    housing_recovery_result_policy2 = housing_recovery.get_output_dataset("ds_result")

    # Convert dataset to Pandas DataFrame
    df_hhrs_policy2 = housing_recovery_result_policy2.get_dataframe_from_csv()
    # Save CSV files for post processing
    df_hhrs_policy2.to_csv(f"df_hhrs_results_policy_{i}.csv")

    # merge household unit information with recovery results
    pd_hhrs_df = pd.merge(left = pd_df_policy2, 
                        right = df_hhrs_policy2,
                        left_on=['guid','huid'],
                        right_on=['guid','huid'],
                        how='left')

    # Plot recovery curve
    filename = f"recovery_curve_policy_{i}"
    recovery_curve_byincome(pd_df_hs = pd_hhrs_df, 
                            filename = filename,
                            subtitle = f" Policy {i}")
    recovery_curve_filenames.append(filename)


# #### Goal - Make GIF from recovery curves
# - option - combine PDF files and convert to GIf
#     - https://convertio.co/pdf-gif/
# - Other options
#     - https://towardsdatascience.com/basics-of-gifs-with-pythons-matplotlib-54dd544b6f30
#     - https://www.tutorialspoint.com/how-to-clear-the-memory-completely-of-all-matplotlib-plots
#     

# # POST PROCESSING

# In[104]:


# choose i between 1 to 4 (1, 4, 8, 12, 16 feet elevation)
i = 4


# ## Postprocessing: Functionality of Physical Infrastructure

# In[107]:


bdmg_df = pd.read_csv ('bld_damage_results_policy_0.csv')
bdmg_policy2_df = pd.read_csv (f"bld_damage_results_policy_{i}.csv")


# In[110]:


bdmg_df.head()


# In[113]:


bdmg_df.guid.describe()


# In[108]:


bdmg_policy2_df.head()


# In[114]:


bdmg_policy2_df.guid.describe()


# In[111]:


# Merge policy i with policy j
bdmg_df_policies = pd.merge(left = bdmg_df,
                      right = bdmg_policy2_df,
                      on = 'guid',
                      suffixes = ('_policy0', f'_policy{i}'))


# In[112]:


bdmg_df_policies.head()


# In[109]:


# Merge policy i with policy j
bdmg_df_policies = pd.merge(left = bdmg_df,
                      right = bdmg_policy2_df,
                      on = 'guid',
                      suffixes = ('_policy0', f'_policy{i}'))
bdmg_df_policies[['DS_0_policy0',f'DS_0_policy{i}']].describe().T


# In[106]:


bdmg_df_policies[['DS_3_policy0',f'DS_3_policy{i}']].describe().T


# In[98]:


import matplotlib.pyplot as plt
# Scatter Plot
plt.scatter(bdmg_df_policies['DS_3_policy0'], bdmg_df_policies[f'DS_3_policy{i}'])
plt.title(f'Scatter plot Policy 0 vs Policy {i}')
plt.xlabel('Complete Damage Policy 0')
plt.ylabel(f'Complete Damage Policy {i}')
plt.savefig(f'CompleteDamage{i}.tif', dpi = 200)
plt.show()


# ## Postprocessing: Recovery

# In[99]:


df_hhrs_policy2 = pd.read_csv (f"df_hhrs_results_policy_{i}.csv")
# merge household unit information with recovery results
pd_df_hs_policy2 = pd.merge(left = pd_df_policy2, 
                    right = df_hhrs_policy2,
                    left_on=['guid','huid'],
                    right_on=['guid','huid'],
                    how='left')
pd_df_hs_policy2[['guid','huid']].describe()


# ## 6a) Sufficient Quality Solutions Found?

# In[100]:


pd_df_policy2 = pd.read_csv(f'pd_df_results_policy_{i}.csv')
df_hhrs_policy2 = pd.read_csv(f'df_hhrs_results_policy_{i}.csv')

pd_df_hs_policy2 = pd.merge(left = pd_df_policy2, 
                    right = df_hhrs_policy2,
                    left_on=['guid','huid'],
                    right_on=['guid','huid'],
                    how='left')


# In[101]:


# Add HHRS categories to dataframe
pd_df_hs_policy2 = add_label_cat_values_df(pd_df_hs_policy2, 
            valuelabels = hhrs_valuelabels, variable = '13')
pd_df_hs_policy2 = add_label_cat_values_df(pd_df_hs_policy2, 
            valuelabels = permanenthousing_valuelabels,
                        variable = '13')


# In[102]:


poptable.pop_results_table(pd_df_hs_policy2, 
                  who = "Total Population by Householder", 
                  what = "by Permanent Housing at T=13 by Race Ethnicity",
                  where = "Galveston Island TX",
                  when = "2010 - Policy 2 - All buildings elvated",
                  row_index = 'Race Ethnicity',
                  col_index = 'Permanent Housing',
                  row_percent = '0 Not Permanent Housing'
                  )


# In[103]:


poptable.pop_results_table(pd_df_hs, 
                  who = "Total Population by Householder", 
                  what = "by Permanent Housing at T=13 by Race Ethnicity",
                  where = "Galveston Island TX",
                  when = "2010 - Baseline",
                  row_index = 'Race Ethnicity',
                  col_index = 'Permanent Housing',
                  row_percent = '0 Not Permanent Housing'
                  )

