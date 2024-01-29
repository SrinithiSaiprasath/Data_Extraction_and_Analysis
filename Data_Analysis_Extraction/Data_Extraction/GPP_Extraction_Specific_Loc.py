import csv
import os
import numpy as np
import xarray as xr
#Data for whole year 2020 specific to Lat Lon 
#Data specific to the while year 2020
'''Input values are
1.file path for year specific to RH 
2.Wind COMPONENTS DATA 
3.lat lon  '''

file_path = 'd:/ERA5_Data_2011-22/Other_Files/RTVO_2020/adaptor.mars.internal-1685734833.388182-26707-5-b22969f0-fa5c-4834-8f74-50098322803e.nc'
ds = xr.open_dataset(file_path)
print("RH data retrieved ")

file_path1 = 'adaptor.mars.internal-1685749364.8796782-30003-12-91d7717a-e38d-4aec-9966-c80a0edf86d0.nc'
ds1 = xr.open_dataset(file_path1)
print("Wind Data Retrieved")

unique_latitudes = ds['latitude'].values
unique_longitudes = ds['longitude'].values
unique_pressure_levels = ds['level'].values
unique_time = ds['time'].values.flatten()
print("RH data fetched")

buoy_data = {'sample1': {'lat': 11.4, 'lon': 86.0},'sample2':{'lat': 11.7 , 'lon':86.0}, 'sample3':{'lat':12.9,'lon':86.2} , 'sample4' : {'lat':13.4 , 'lon' : 86.2} , 'sample5' : {'lat' : 16.5 , 'lon' : 86.9}}

#Other buoy data
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

print("Buoy data read")
mylat = float(input("Enter latitude"))
mylon = float(input("Enter longitude"))

lat = round(mylat*2) / 2
lon = round(mylon*2 ) / 2  
#for buoy_id, coordinates in buoy_data.items():
#    buoy_data[buoy_id]['lat'] = round(coordinates['lat'] * 2) / 2
#    buoy_data[buoy_id]['lon'] = round(coordinates['lon'] * 2) / 2

#filtered_latitudes = [i['lat'] for i in buoy_data.values()]
#filtered_longitudes = [i['lon'] for i in buoy_data.values()]

output_directory = f"GPP_Cyclone_Track"

#for lat, lon in zip(filtered_latitudes, filtered_longitudes):

print(f"{lat} {lon}")
csv_file_path = os.path.join(output_directory, f"output_data_{lat}_{lon}.csv")
os.makedirs(output_directory, exist_ok=True)

with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(f"{lat}N,{lon}E")
    header = ["Date", "Time","E_850","M_(RH)","I_sub" ,"S_Val", "GPP"]
    csv_writer.writerow(header)
    
    for time1 in unique_time:
        data_for_params = ds.sel(latitude=lat, longitude=lon, time=time1, method='nearest')
        data_for_wind = ds1.sel(latitude=lat, longitude=lon, time=time1, method='nearest')

        time_data_array = str(np.array(time1, dtype='datetime64'))
        date, time1 = time_data_array.split("T")
        time2, unn = time1.split(".")
        time_val = time2.replace(":", "-")
        year = date[-1:-5]
    
        temperature_data = data_for_params['t']
        pressure_data = data_for_params['level']
        relative_humidity_data = data_for_params['r']
        vorticity_data = data_for_params['vo']

        pressure_at_500 = pressure_data.sel(level=500).values
        pressure_at_850 = pressure_data.sel(level=850).values

        temperature_at_500 = temperature_data.sel(level=500).values
        temperature_at_850 = temperature_data.sel(level=850).values

        celcius_at_500 = temperature_data.sel(level=500).values - 273.15
        celcius_at_850 = temperature_data.sel(level=850).values - 273.15

        temperature_diffrence = temperature_at_850 - temperature_at_500  # I

        mid_troposphere_relative_humidity_at_700 = relative_humidity_data.sel(level=700).values
        mid_troposphere_relative_humidity_at_500 = relative_humidity_data.sel(level=500).values

        average_relative_humidity = (mid_troposphere_relative_humidity_at_500 +
                                    mid_troposphere_relative_humidity_at_700) / 2
        mid_troposphere_relative_humidity = ((average_relative_humidity - 40) / 30)  # M

        vorticity_at_850 = vorticity_data.sel(level=850).values

        u_at_200 = data_for_wind['u'].sel(level=200).values
        u_at_850 = data_for_wind['u'].sel(level=850).values
        u_sq = (u_at_200 - u_at_850)**2
        
        v_at_200 = data_for_wind['v'].sel(level=200).values
        v_at_850 = data_for_wind['v'].sel(level=850).values
        v_sq = (v_at_200 - v_at_850)**2
        
        w_at_200 = data_for_wind['w'].sel(level=200).values
        w_at_850 = data_for_wind['w'].sel(level=200).values
        w_sub = ((w_at_200 - w_at_850))

        S = ((u_sq) + (v_sq))**(1/2)

        if(mid_troposphere_relative_humidity > 0 and vorticity_at_850 > 0 and temperature_diffrence > 0):
            gpp1 = ((vorticity_at_850 * mid_troposphere_relative_humidity *temperature_diffrence) / S)
            gpp = gpp1
        else:
            gpp = 0

        row_data=[date, time2,vorticity_at_850,mid_troposphere_relative_humidity,temperature_diffrence,S,gpp]
        print(f"{date},{time2},{vorticity_at_850},{mid_troposphere_relative_humidity},{temperature_diffrence},{S} ,{gpp}")
        csv_writer.writerow(row_data)
        
print("CSV file is written")