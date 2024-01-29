import pandas as pd 
import matplotlib.pyplot as plt 
#I
gpp_data = pd.read_csv("New_Cyclone_Track_12.5_86.0/GPP_12.5_86.0.csv")
gpp_data['Date'] = pd.to_datetime(gpp_data['Date'])
gpp_data = gpp_data.set_index('Date')
plt.figure(figsize=(10, 6))
plt.plot(gpp_data.index, gpp_data['I_sub'], marker='o', linestyle='-', color='b')
plt.title("Mid Troposphere Instability (Between 850hPa & 500hPa)")
plt.xlabel('Date')
plt.ylabel('Temperature Diffrence (Celcius)')
plt.tight_layout()
plt.savefig("Temperature Diffrence_PLot_C.png")
print(" I plotted")
