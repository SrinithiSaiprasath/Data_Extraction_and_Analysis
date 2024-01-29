import xarray as xr
import matplotlib.pyplot as plt
import mplcursors
from datetime import datetime

dataset = xr.open_dataset("C:/Users/customer/Downloads/adaptor.mars.internal-1686634317.6059375-22265-12-cadc50c5-a662-48f1-b391-6e241067044a.nc")

latitude = dataset['latitude'].values
longitude = dataset['longitude'].values
temperature_data = dataset['t'].isel(time=0, level=500).values  # Assuming level=0 for simplicity
time_info = dataset['time'].values

date = datetime.utcfromtimestamp(time_info.astype(int)[0] * 1e-9).strftime('%Y-%m-%D')
time = datetime.utcfromtimestamp(time_info.astype(int)[1] * 1e-9).strftime("%H-%M-%S")

fig, ax = plt.subplots()
contour = ax.contourf(longitude, latitude, temperature_data, cmap='viridis')
plt.colorbar(contour, label='Temperature (K)')  # Replace 'units' with the actual units of your temperature data

ax.set_title(f'Temperature Distribution\nDate: {date}, Time : {time} level : 500mb ')
ax.set_xlabel('Longitude (E)')
ax.set_ylabel('Latitude(N)')

cursor = mplcursors.cursor(hover=True)
cursor.connect("add")

def on_add(sel):
    lat_index = int(sel.target[1])
    lon_index = int(sel.target[0])
    temperature = temperature_data[lat_index, lon_index]
    pressure = dataset['pressure'].isel(time=0, level=0).values
    label = f'Time: {date}, Pressure: {pressure}, Temperature: {temperature}'
    sel.annotation.set_text(label)
plt.show()