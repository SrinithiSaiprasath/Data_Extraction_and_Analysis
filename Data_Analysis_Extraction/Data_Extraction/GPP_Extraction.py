#Data for year 2020
#Input Datasets req : 
#1)Relative Humidity Data 
#2)Wind Componenets Data
#3)TCHP Data

#Importing required Libraries
import csv
import os
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import random 

file_path = 'd:/ERA5_Data_2011-22/Other_Files/RTVO_2020/adaptor.mars.internal-1685734833.388182-26707-5-b22969f0-fa5c-4834-8f74-50098322803e.nc'
ds = xr.open_dataset(file_path)
print("RH data retrieved ")

file_path1 = 'adaptor.mars.internal-1685749364.8796782-30003-12-91d7717a-e38d-4aec-9966-c80a0edf86d0.nc'
ds1 = xr.open_dataset(file_path1)
print("Wind Data Retrieved")

file_path2 = "c:/Users/customer/Downloads/TCHP_TCHP.nc"
ds2 = xr.open_dataset(file_path2)
print('TCHP data retrived')

unique_latitudes = ds['latitude'].values
unique_longitudes = ds['longitude'].values
unique_pressure_levels = ds['level'].values
unique_time = ds['time'].values.flatten()
D26 = ds2['D26'].values
tchp_lat = ds2['lat'].values
tchp_lon = ds2['lon'].values

#Bouy Data / Predefined Latitude and Longitude Values in dict
buoy_data = {'sample1': {'lat': 11.4, 'lon': 86.0}}
a = {'sample2':{'lat': 11.7 , 'lon':86.0}, 'sample3':{'lat':12.9,'lon':86.2} , 'sample4' : {'lat':13.4 , 'lon' : 86.2} , 'sample5' : {'lat' : 16.5 , 'lon' : 86.9}}
b= {'sample2': {'lat': 14, 'lon': 80},
    'AD06': {'lat': 18.31, 'lon': 67.33},
    'AD07': {'lat': 14.92, 'lon': 68.98},
    'AD08': {'lat': 12.06, 'lon': 68.62},
    'AD09': {'lat': 8.11, 'lon': 73.28},
    'AD10': {'lat': 10.32, 'lon': 72.6},
    'BD08': {'lat': 17.83, 'lon': 89.2},
    'BD09': {'lat': 17.46, 'lon': 89.15},
    'BD10': {'lat': 16.33, 'lon': 87.99},
    'BD11': {'lat': 13.46, 'lon': 84.15},
    'BD12': {'lat': 10.46, 'lon': 94.12},
    'BD13': {'lat': 14, 'lon': 87},
    'BD14': {'lat': 6.6, 'lon': 88.4}
}

#Input Values

#Function to convert 
def convert(a):
    base1 = a - int(a)
    base=round(base1,1)
    if(base == 0.1 or base == 0):
        base = 0
    elif(base ==0.2 or base ==0.3):
        base= 0.25
    elif(base == 0.4 or base== 0.5 or base == 0.6):
        base= 0.5
    elif(base == 0.7 or base == 0.8):
        base=0.75
    else:
        base=1
    res = int(a) + base
    return res 

#Uncomment the lines for dynamic input 
#mylat = float(input("Enter latitude "))
#mylon = float(input(''Enter longitude "))

mylat = 10.31  #predefined
mylon = 86.95  #predefined

#approximating decimal input to 0.0 or 0.25 or 0.75  form 
lat = convert(mylat)
lon = convert(mylon)
print("Input Values Taken")

#uncomment for reading & processing buoy data in dictionary 
'''
for buoy_id, coordinates in buoy_data.items():
    buoy_data[buoy_id]['lat'] = round(coordinates['lat'] * 2) / 2
    buoy_data[buoy_id]['lon'] = round(coordinates['lon'] * 2) / 2

filtered_latitudes = [i['lat'] for i in buoy_data.values()]
filtered_longitudes = [i['lon'] for i in buoy_data.values()]

'''
#Main directory for storing all data 
output_directory = f"_Data_{lat}_{lon}"

'''for lat, lon in zip(filtered_latitudes, filtered_longitudes):'''   # uncomment this line and indent below lines for accessing lat lon values in dict

#Directory creation
print(f"{lat} {lon}")
csv_file_path = os.path.join(output_directory, f"GPP_{lat}_{lon}.csv")
os.makedirs(output_directory, exist_ok=True)

with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    header = ["Date", "Time","E_850","M_(RH)","I_sub" ,"S_Val","TCHP","GPP"]
    csv_writer.writerow(header)
    #Time based Data retriva; 
    for time1 in unique_time :
        #fetching dataa wrt to time from all data sets 
        data_for_params = ds.sel(latitude=lat, longitude=lon, time=time1, method='nearest')   
        data_for_wind = ds1.sel(latitude=lat, longitude=lon, time=time1, method='nearest')
        data_for_tchp = ds2.sel(lat=lat, lon=lon, time=time1, method = 'nearest')
        
        time_data_array = str(np.array(time1, dtype='datetime64'))
        date, time1 = time_data_array.split("T")
        time2, unn = time1.split(".")
        time_val = time2.replace(":", "-")  
        year = date[-1:-5]


        #Variables 
        temperature_data = data_for_params['t']
        pressure_data = data_for_params['level']
        relative_humidity_data = data_for_params['r']
        vorticity_data = data_for_params['vo']

        #pressure data
        pressure_at_500 = pressure_data.sel(level=500).values
        pressure_at_850 = pressure_data.sel(level=850).values

        #temperature data 
        temperature_at_500 = temperature_data.sel(level=500).values
        temperature_at_850 = temperature_data.sel(level=850).values

        #Conversion of temperature in kelvin to Celcius 
        celcius_at_500 = temperature_data.sel(level=500).values - 273.15
        celcius_at_850 = temperature_data.sel(level=850).values - 273.15

        #Temperature diffrence in celcius(Variable I )
        temperature_diffrence = (celcius_at_850 - celcius_at_500).round(decimals= 5)# I

        #Relative Humidity (Variable M )
        mid_troposphere_relative_humidity_at_700 = relative_humidity_data.sel(level=700).values
        mid_troposphere_relative_humidity_at_500 = relative_humidity_data.sel(level=500).values
        average_relative_humidity = (mid_troposphere_relative_humidity_at_500 +mid_troposphere_relative_humidity_at_700) / 2  #Average Relative Humidity
        mid_troposphere_relative_humidity = ((average_relative_humidity - 40) / 30) .round(decimals = 5) # M

        #Vorticity (Variable E_850)
        vorticity_at_850 = (vorticity_data.sel(level=850).values).round(decimals = 5)

        #Wind Data 

        #U-Component
        u_at_200 = data_for_wind['u'].sel(level=200).values
        u_at_850 = data_for_wind['u'].sel(level=850).values
        u_sq = (u_at_200 - u_at_850)**2
        #V-Component
        v_at_200 = data_for_wind['v'].sel(level=200).values
        v_at_850 = data_for_wind['v'].sel(level=850).values
        v_sq = (v_at_200 - v_at_850)**2
        #W-Component
        w_at_200 = data_for_wind['w'].sel(level=200).values
        w_at_850 = data_for_wind['w'].sel(level=200).values
        w_sub = ((w_at_200 - w_at_850))

        #Calculation of Vertical Wind Shear (Variable S)
        S = (((u_sq) + (v_sq))**(1/2)).round(decimals = 5)
        
        #TCHP
        tchp_1 = data_for_tchp['Tropical_Cyclone_Heat_Potential'].values

        if(mid_troposphere_relative_humidity > 0 and vorticity_at_850 > 0 and temperature_diffrence > 0):
            gpp1 = ((vorticity_at_850 * mid_troposphere_relative_humidity *temperature_diffrence) / S)*(tchp_1 / 40)
            gpp = gpp1
        else:
            gpp = 0

        row_data=[date, time2,vorticity_at_850,mid_troposphere_relative_humidity,temperature_diffrence,S,tchp_1,gpp]
        print(f"{date},{time2},{vorticity_at_850},{mid_troposphere_relative_humidity},{temperature_diffrence},{S},{tchp_1},{gpp}")
        csv_writer.writerow(row_data)

print(f"CSV file for {lat}N {lon}E is written in file : " , csv_file_path)


#GPP-Plot
gpp_data = pd.read_csv(csv_file_path)
gpp_data['Date'] = pd.to_datetime(gpp_data['Date'])
gpp_data = gpp_data.set_index('Date')
plt.figure(figsize=(10, 6))
plt.plot(gpp_data.index, gpp_data['GPP'], marker='o', linestyle='-', color='b')
plt.title('Daily GPP Values')
plt.xlabel('Date')
plt.ylabel('GPP')
plt.tight_layout()
plt.savefig("GPP-Plot.png")
print("GPP plotted")

#E_850-Plot
gpp_data = pd.read_csv(csv_file_path)
gpp_data['Date'] = pd.to_datetime(gpp_data['Date'])
gpp_data = gpp_data.set_index('Date')
plt.figure(figsize=(10, 6))
plt.plot(gpp_data.index, gpp_data['E_850'], marker='o', linestyle='-', color='b')
plt.title('low level Relative Vorticity at 850hPa Plot')
plt.xlabel('Date')
plt.ylabel('E_850')
plt.tight_layout()
plt.savefig("E_850-Plot.png")
print("E_850 plotted")

#M-Plot
gpp_data = pd.read_csv(csv_file_path)
gpp_data['Date'] = pd.to_datetime(gpp_data['Date'])
gpp_data = gpp_data.set_index('Date')
plt.figure(figsize=(10, 6))
plt.plot(gpp_data.index, gpp_data['M_(RH)'], marker='o', linestyle='-', color='b')
plt.title("Mid Troposphere Relative Humidity (Between 700hPa & 850hPa)")
plt.xlabel('Date')
plt.ylabel('Relative Humidity (M)')
plt.tight_layout()
plt.savefig("Mid Troposphere Relative Humidity.png")
print(" M plotted")


#I-Plot
gpp_data = pd.read_csv(csv_file_path)
gpp_data['Date'] = pd.to_datetime(gpp_data['Date'])
gpp_data = gpp_data.set_index('Date')
plt.figure(figsize=(10, 6))
plt.plot(gpp_data.index, gpp_data['I_sub'], marker='o', linestyle='-', color='b')
plt.title("Mid Troposphere Instability (Between 850hPa & 500hPa)")
plt.xlabel('Date')
plt.ylabel('Temperature Diffrence (Celcius)')
plt.tight_layout()
plt.savefig("Temperature Diffrence_PLot.png")
print(" I plotted")

#S-Plot
gpp_data = pd.read_csv(csv_file_path)
gpp_data['Date'] = pd.to_datetime(gpp_data['Date'])
gpp_data = gpp_data.set_index('Date')
plt.figure(figsize=(10, 6))
plt.plot(gpp_data.index, gpp_data['S_Val'], marker='o', linestyle='-', color='b')
plt.title("Vertical Wind Shear (between 200hPa & 850hPa)")
plt.xlabel('Date')
plt.ylabel('Wind Shear (S)')
plt.tight_layout()
plt.savefig("Wind_Shear_PLot.png")
print(" S plotted")

#TCHP-Plot
gpp_data = pd.read_csv(csv_file_path)
gpp_data['Date'] = pd.to_datetime(gpp_data['Date'])
gpp_data = gpp_data.set_index('Date')
plt.figure(figsize=(10, 6))
plt.plot(gpp_data.index, gpp_data['TCHP'], marker='o', linestyle='-', color='b')
plt.title("Tropical Cyclone Heat Potentail")
plt.xlabel('Date')
plt.ylabel('TCHP (KJ/cm^2)')
plt.tight_layout()
plt.savefig("TCHP_PLot.png")
print(" TCHP plotted")