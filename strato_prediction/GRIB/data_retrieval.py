## imports
import xarray as xr
import numpy as np

# Télécharger le fichier GRIB
def download_grib_file(url, output_path):
    pass

def load_grib_data(file_path):
    pressure_filter = {
        'typeOfLevel': 'isobaricInhPa',
        'shortName': ['u', 'v', 'isobaricInhPa', 'longitude', 'latitude', 'wz', 'r', 't', 'gh']}
    surface_filter = {
        'typeOfLevel': 'surface',
        'shortName': ['orog']}
    ds_pressure_levels = xr.open_dataset(file_path, engine='cfgrib', filter_by_keys=pressure_filter)
    ds_surface_level = xr.open_dataset(file_path, engine='cfgrib', filter_by_keys=surface_filter)
    data = {
        'pressure': ds_pressure_levels.isobaricInhPa.values,
        'latitude': ds_pressure_levels.latitude.values,
        'longitude': ds_pressure_levels.longitude.values,
        'gph': ds_pressure_levels.gh.values,
        'u_wind': ds_pressure_levels.u.values,
        'v_wind': ds_pressure_levels.v.values,
        'surface': ds_surface_level.orog.values,
        'w_wind': ds_pressure_levels.wz.values,
        'humidity': ds_pressure_levels.r.values,
        'temp': ds_pressure_levels.t.values
    }
    return data