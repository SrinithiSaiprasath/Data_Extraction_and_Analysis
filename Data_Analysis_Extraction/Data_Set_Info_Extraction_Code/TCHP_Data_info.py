from netCDF4 import Dataset
import pandas as pd

file_path = "c:/Users/customer/Downloads/TCHP_TCHP.nc"
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