# %%
# import libraries
import os
import pandas as pd

# %% 
# set path
#file_path = 'C:\\Users\\sancheac\\OneDrive - University of Birmingham\\Documents\\AHWM\\ahwm-eorr-dashboard\\data\\'
# %%
#################### attainment data ###########################
url_att = 'https://bham.sharepoint.com/sites/aimhigherwm-staff/Shared%20Documents/AHWM%202012%20Onwards/Evaluation%20-%20Cati/Regional%20Risk%20Register/ahwm-eorr-dashboard/data/202425_all_state_funded_pupils_characteristics_and_geography_breakdowns_revised.csv?d=w7acf5ef51c774f44823130d1aa6ef90f&csf=1&web=1&e=uIu8xJ'
df_att = pd.read_csv(url_att)
df_att['time_period'] = df_att['time_period'].astype(str)
df_att = df_att.sort_values("time_period")

#drop years where we don't have relevant data
to_drop = ['200910', '201011', '201112', '201213', '201314', '201415', '201516', '201617', '201718']
df_att = df_att[~df_att['time_period'].isin(to_drop)]

#last data available only
#df_att = df_att[df_att['time_period'] == '202425']

# select LAs in WM RAP, and National scores
LAs = [ 'National','Birmingham', 'Coventry', 'Dudley', 'Sandwell', 'Solihull', 'Walsall',
       'Wolverhampton', 'Worcestershire', 'Herefordshire, County of', 'Warwickshire']

df_att_wm = df_att[df_att['la_name'].isin(LAs)]

df_att_national = df_att[df_att['geographic_level'] == 'National']
df_att_national['la_name'] = 'National'

df_att_combined = pd.concat([df_att_national,df_att_wm], ignore_index=True)

# %%
#################### IMD data ###########################

#df_imd = pd.read_excel(os.path.join(file_path, 'File_1_IoD2025_Index_of_Multiple_Deprivation.xlsx'), sheet_name='IMD25')

#df_imd = df_imd[['Local Authority District name (2024)', 'Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOA']]

# %%
###################### school profiles ###############################
url_schools = 'https://bham.sharepoint.com/sites/aimhigherwm-staff/Shared%20Documents/AHWM%202012%20Onwards/Evaluation%20-%20Cati/Regional%20Risk%20Register/ahwm-eorr-dashboard/data/2023_10_12%20AHWM%20and%20EMWPREP%20Secondary%20School%20Profiles%20FINAL.xlsx?d=wb66ec47a4a144c178bd01ba6ce208f72&csf=1&web=1&e=Q8FTER'
df_schools = pd.read_excel(url_schools)
df_schools_wm = df_schools[df_schools['LA'].isin(LAs)]

cols_to_drop = ["GOR", "LAEstab Number", "Establishment Status", 
                "Phase Of Education", "Target School", "Total Met Criteria"]

df_schools_wm.drop(columns = cols_to_drop, inplace=True)

percent_cols = [
    col for col in df_schools_wm.columns
    if "%" in col
]

df_schools_wm[percent_cols] = df_schools_wm[percent_cols].mul(100).round(1)

# %%
# functions
def get_att_data():
    return df_att_combined, LAs

#def get_demog_data():
#    return df_att_combined, LAs

def get_school_data():
    return df_schools_wm, LAs

# %%
