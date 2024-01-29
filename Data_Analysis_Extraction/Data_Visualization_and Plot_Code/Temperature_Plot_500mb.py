import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

file_path = "c:/Users/customer/Desktop/NIOT/adaptor.mars.internal-1686554371.730475-11151-18-cb9df2af-172d-4188-b746-3987b89f6e32.nc"
ds = xr.open_dataset(file_path)

unique_latitudes = ds['latitude'].values
unique_longitudes = ds['longitude'].values
unique_pressure_levels = ds['level'].values
unique_time = ds['time'].values.flatten()

buoy_data = {
    'AD06': {'lat': 18.31, 'lon': 67.33},   
}

for buoy_id, coordinates in buoy_data.items():
    buoy_data[buoy_id]['lat'] = round(coordinates['lat'] * 2) / 2
    buoy_data[buoy_id]['lon'] = round(coordinates['lon'] * 2) / 2

filtered_latitudes = [i['lat'] for i in buoy_data.values()]
filtered_longitudes = [i['lon'] for i in buoy_data.values()]

plt.figure(figsize=(12, 8))

for lat, lon in zip(filtered_latitudes, filtered_longitudes):
    temperature_diff = []
    times = []

    for time1 in unique_time:
        data_for_params = ds.sel(latitude=lat, longitude=lon, time=time1, method='nearest')
        temperature_at_500 = data_for_params['t'].sel(level=500).values
        temperature_at_850 = data_for_params['t'].sel(level=850).values

        celcius_at_500 = int(temperature_at_500 - 273.15)
        temperature_diff.append(celcius_at_500)
        times.append(time1)

    temperature_diff = np.array(temperature_diff).flatten()
    times = np.array(times).flatten()

    plt.plot(times, temperature_diff, label=f'{lat}E / {lon}N')

plt.xlabel('Time')
plt.ylabel('Temperature (C)')
plt.title(f'Temperature At 500mb')
plt.legend()
plt.show()
