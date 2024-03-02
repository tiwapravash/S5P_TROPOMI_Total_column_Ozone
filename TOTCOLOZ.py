#Import Necessary Libraries 
import os
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy import stats
import glob
import pandas as pd
dir = '/Users/pravash/Downloads/Xuzhou_oz/'
file = "S5P_RPRO_L2__O3_____20180430T052420_20180430T070550_02821_03_020401_20221003T085043.SUB.nc4"
os.path.join(dir, file)
ds = xr.open_dataset(os.path.join(dir, file), group='PRODUCT')
#Extract Variables#
time_coord = ds['time']
year=time_coord.dt.year
year_np=year.values
month=time_coord.dt.month
month_np=month.values
day=time_coord.dt.day
day_np=day.values
lat = ds['latitude'].values.flatten()
lon = ds['longitude'].values.flatten()
ozone = ds['ozone_total_vertical_column'].values.flatten()
qa=ds['qa_value'].values.flatten()
#Get the lengths of the scanline and ground_pixel coordinates
scanline_length = len(ds['scanline'])
ground_pixel_length = len(ds['ground_pixel'])
# Create meshgrid for latitude and longitude
scanline, ground_pixel = np.meshgrid(range(scanline_length), range(ground_pixel_length), indexing='ij')
# Flatten the meshgrid pair
flattened_meshgrid = np.column_stack((scanline.flatten(), ground_pixel.flatten()))
# Repeat time information for each spatial location
time_info = np.column_stack((np.repeat(year_np, scanline_length * ground_pixel_length),
                             np.repeat(month_np, scanline_length * ground_pixel_length),
                             np.repeat(day_np, scanline_length * ground_pixel_length)))

# Concatenate repeated time information with flattened meshgrid pair
data = np.column_stack((time_info, flattened_meshgrid))
# Concatenate longitude, latitude, ozone, and qa_values arrays as consecutive columns
data = np.column_stack((data, lon.flatten(), lat.flatten(), ozone.flatten(), qa.flatten()))
print("Shape of time_info:", time_info.shape)
print("Shape of flattened_meshgrid:", flattened_meshgrid.shape)
print("Shape of lon:", lon.flatten().shape)
print("Shape of lat:", lat.flatten().shape)
print("Shape of ozone:", ozone.flatten().shape)
print("Shape of qa_values:", qa.flatten().shape)
print("Shape of data:", data.shape)
# Convert to DataFrame
df = pd.DataFrame(data, columns=['Year', 'Month', 'Day', 'Scanline', 'Ground_Pixel', 'Longitude', 'Latitude', 'Ozone', 'QA'])
###Apply Quality Assurance with QA > 0.5 only accepted
filtered_df = df[df['QA'] > 0.5]
print(filtered_df)
###Convert Unit to Dobsobn Unit (DU)
filtered_df.loc[:, 'Ozone'] *= 2241.15
filtered_df




