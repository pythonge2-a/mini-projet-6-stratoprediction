## imports
import xarray as xr
import numpy as np
import requests
import os

# Télécharger le fichier GRIB
def download_grib_file(date, cycle, offset_time, geo_bounds):
    print(f"date:{date}")
    print(f"cycle:{cycle}")
    print(f"offset_time:{offset_time}")
    print(f"top_lat:{geo_bounds['top_lat']}")
    print(f"left_lon:{geo_bounds['left_lon']}")
    print(f"right_lon:{geo_bounds['right_lon']}")
    print(f"btm_lat:{geo_bounds['btm_lat']}")
    # url_test = f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?dir=%2Fgfs.20250111%2F12%2Fatmos&file=gfs.t12z.pgrb2.0p25.f020&var_HGT=on&var_TMP=on&var_UGRD=on&var_VGRD=on&lev_1000_mb=on&lev_900_mb=on&lev_800_mb=on&lev_700_mb=on&lev_600_mb=on&lev_500_mb=on&lev_400_mb=on&lev_300_mb=on&lev_200_mb=on&lev_100_mb=on&lev_50_mb=on&lev_10_mb=on&lev_5_mb=on&lev_1_mb=on&lev_0.4_mb=on&lev_0.1_mb=on&lev_0.04_mb=on&lev_0.01_mb=on&subregion=&toplat={top_lat}&leftlon={left_lon}&rightlon={right_lon}&bottomlat={btm_lat}"

    base_url = "https://nomads.ncep.noaa.gov/cgi-bin/"
    filter_url = "filter_gfs_0p25_1hr.pl?dir=%2Fgfs."
    current_time_url = f"{date}%2F{cycle}%2Fatmos&file=gfs.t{cycle}z.pgrb2.0p25.f{str(offset_time).zfill(3)}&"
    next_time_url= f"{date}%2F{cycle}%2Fatmos&file=gfs.t{cycle}z.pgrb2.0p25.f{str(offset_time+1).zfill(3)}&"
    weather_vars_url = "var_DZDT=on&var_HGT=on&var_RH=on&var_TMP=on&var_UGRD=on&var_VGRD=on&lev_1000_mb=on&lev_975_mb=on&lev_950_mb=on&lev_925_mb=on&lev_900_mb=on&lev_850_mb=on&lev_800_mb=on&lev_750_mb=on&lev_700_mb=on&lev_650_mb=on&lev_600_mb=on&lev_550_mb=on&lev_500_mb=on&lev_450_mb=on&lev_400_mb=on&lev_350_mb=on&lev_300_mb=on&lev_250_mb=on&lev_200_mb=on&lev_150_mb=on&lev_100_mb=on&lev_70_mb=on&lev_50_mb=on&lev_40_mb=on&lev_30_mb=on&lev_20_mb=on&lev_15_mb=on&lev_10_mb=on&lev_7_mb=on&lev_5_mb=on&lev_3_mb=on&lev_2_mb=on&lev_1_mb=on&lev_surface=on&"
    region_url = f"subregion=&toplat={geo_bounds['top_lat']}&leftlon={geo_bounds['left_lon']}&rightlon={geo_bounds['right_lon']}&bottomlat={geo_bounds['btm_lat']}"

    current_url = base_url + filter_url + current_time_url + weather_vars_url + region_url
    next_url = base_url + filter_url + next_time_url + weather_vars_url + region_url
    current_r = requests.get(current_url)
    # current_r = requests.get(url_test)
    next_r = requests.get(next_url)

    if current_r.status_code == 200:
        current_file_path = os.path.join("assets", f"d{date}c{cycle}o{str(offset_time).zfill(3)}bl{geo_bounds['btm_lat']}tl{geo_bounds['top_lat']}ll{geo_bounds['left_lon']}rl{geo_bounds['right_lon']}")
        with open(current_file_path, "wb") as file:
            file.write(current_r.content)
        print("Le téléchargement CURRENT à réussi!")
    else:
        print(f"Erreur {current_r.status_code}: Le téléchargement CURRENT a échoué.")
    if next_r.status_code == 200:
        next_file_path = os.path.join("assets", f"d{date}c{cycle}o{str(offset_time+1).zfill(3)}bl{geo_bounds['btm_lat']}tl{geo_bounds['top_lat']}ll{geo_bounds['left_lon']}rl{geo_bounds['right_lon']}")
        with open(next_file_path, "wb") as file:
            file.write(next_r.content)
        print("Le téléchargement NEXT à réussi!")
    else:
        print(f"Erreur {next_r.status_code}: Le téléchargement NEXT a échoué.")
    return current_file_path,next_file_path

# Télécharger le fichier GRIB suivant
def download_next_grib_file(date, cycle, offset_time, geo_bounds):
    base_url = "https://nomads.ncep.noaa.gov/cgi-bin/"
    filter_url = "filter_gfs_0p25_1hr.pl?dir=%2Fgfs."
    next_time_url= f"{date}%2F{cycle}%2Fatmos&file=gfs.t{cycle}z.pgrb2.0p25.f{str(offset_time).zfill(3)}&"
    weather_vars_url = "var_DZDT=on&var_HGT=on&var_RH=on&var_TMP=on&var_UGRD=on&var_VGRD=on&lev_1000_mb=on&lev_975_mb=on&lev_950_mb=on&lev_925_mb=on&lev_900_mb=on&lev_850_mb=on&lev_800_mb=on&lev_750_mb=on&lev_700_mb=on&lev_650_mb=on&lev_600_mb=on&lev_550_mb=on&lev_500_mb=on&lev_450_mb=on&lev_400_mb=on&lev_350_mb=on&lev_300_mb=on&lev_250_mb=on&lev_200_mb=on&lev_150_mb=on&lev_100_mb=on&lev_70_mb=on&lev_50_mb=on&lev_40_mb=on&lev_30_mb=on&lev_20_mb=on&lev_15_mb=on&lev_10_mb=on&lev_7_mb=on&lev_5_mb=on&lev_3_mb=on&lev_2_mb=on&lev_1_mb=on&lev_surface=on&"
    region_url = f"subregion=&toplat={geo_bounds['top_lat']}&leftlon={geo_bounds['left_lon']}&rightlon={geo_bounds['right_lon']}&bottomlat={geo_bounds['btm_lat']}"

    next_url = base_url + filter_url + next_time_url + weather_vars_url + region_url
    next_r = requests.get(next_url)

    if next_r.status_code == 200:
        next_file_path = os.path.join("assets", f"d{date}c{cycle}o{offset_time}bl{geo_bounds['btm_lat']}tl{geo_bounds['top_lat']}ll{geo_bounds['left_lon']}rl{geo_bounds['right_lon']}")
        with open(next_file_path, "wb") as file:
            file.write(next_r.content)
        print("Téléchargement NEXT réussi!")
    else:
        print(f"Erreur {next_r.status_code}: Le téléchargement NEXT a échoué.")
    return next_file_path


def load_grib_data(file_path_1, file_path_2):
    pressure_filter = {
        'typeOfLevel': 'isobaricInhPa',
        'shortName': ['u', 'v', 'isobaricInhPa', 'longitude', 'latitude', 'wz', 'r', 't', 'gh']}
    surface_filter = {
        'typeOfLevel': 'surface',
        'shortName': ['orog']}
    
    current_pressure_dataset = xr.open_dataset(file_path_1, engine='cfgrib', filter_by_keys=pressure_filter)
    next_pressure_dataset = xr.open_dataset(file_path_2, engine='cfgrib', filter_by_keys=pressure_filter)
    surface_dataset = xr.open_dataset(file_path_1, engine='cfgrib', filter_by_keys=surface_filter)

    return current_pressure_dataset, next_pressure_dataset, surface_dataset

def interpolate_data(current_pressure_dataset, next_pressure_dataset, surface_dataset, target_time, lat, lon, pressure, hour=0):
    pressure_levels = current_pressure_dataset.isobaricInhPa.values
    target_index = (abs(pressure_levels - pressure)).argmin()  # Indice le plus proche
    indices = slice(max(0, target_index - 2), min(len(pressure_levels), target_index + 2))
    print(indices)
    current_pressure_subset = current_pressure_dataset.isel(isobaricInhPa=indices).sel(
        latitude = slice(lat - 0.5, lat + 0.5),
        longitude = slice(lon - 0.5, lon + 0.5)
    )
    next_pressure_subset = next_pressure_dataset.isel(isobaricInhPa=indices).sel(
        latitude = slice(lat - 0.5, lat + 0.5),
        longitude = slice(lon - 0.5, lon + 0.5)
    )

    surface_subset = surface_dataset.sel(
        latitude = slice(lat - 0.5, lat + 0.5),
        longitude = slice(lon - 0.5, lon + 0.5)
    )

    current_pressure_subset = current_pressure_subset.assign_coords(time =hour*3600)
    next_pressure_subset = next_pressure_subset.assign_coords(time =(hour+1)*3600)
    
    combined_pressure_subset = xr.concat([current_pressure_subset,next_pressure_subset], dim = "time")

    data = {
        'pressure': combined_pressure_subset.isobaricInhPa.values,
        'latitude': combined_pressure_subset.latitude.values,
        'longitude': combined_pressure_subset.longitude.values,
        'gph': combined_pressure_subset.gh.interp(time = target_time).values,
        'u_wind': combined_pressure_subset.u.interp(time = target_time).values,
        'v_wind': combined_pressure_subset.v.interp(time = target_time).values,
        'surface': surface_subset.orog.values,
        'w_wind': combined_pressure_subset.wz.interp(time = target_time).values,
        'humidity': combined_pressure_subset.r.interp(time = target_time).values,
        'temp': combined_pressure_subset.t.interp(time = target_time).values
    }
    
    return data
