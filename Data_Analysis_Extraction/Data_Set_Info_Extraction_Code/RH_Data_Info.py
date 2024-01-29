from netCDF4 import Dataset
import pandas as pd

file_path = "d:ERA5_Data_2011-22/Other_Files/RTVO_2011/adaptor.mars.internal-1685691364.56267-22705-3-4bfe8305-01f2-4be9-a991-e75b4307e647.nc"
with Dataset(file_path, "r") as nc_file:
    for var_name, var in nc_file.variables.items():
        print(f"Variable label: {var_name}")
        print(f"Shape: {var.shape}")
        print("Attributes")
        for i in var.__dict__.keys():
            print("\t",i ,":", var.__dict__[i])
        print()
        
    time_var = nc_file.variables['time']
    time_values = time_var[:]