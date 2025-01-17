## imports
import xarray as xr
import numpy as np
import requests
import os

# Télécharger le fichier GRIB
def download_grib_file(date, cycle, offset_time, top_lat, left_lon, right_lon, btm_lat):
    print(f"date:{date}")
    print(f"cycle:{cycle}")
    print(f"offset_time:{offset_time}")
    print(f"top_lat:{top_lat}")
    print(f"left_lon:{left_lon}")
    print(f"right_lon:{right_lon}")
    print(f"btm_lat:{btm_lat}")
    # url_test = f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?dir=%2Fgfs.20250111%2F12%2Fatmos&file=gfs.t12z.pgrb2.0p25.f020&var_HGT=on&var_TMP=on&var_UGRD=on&var_VGRD=on&lev_1000_mb=on&lev_900_mb=on&lev_800_mb=on&lev_700_mb=on&lev_600_mb=on&lev_500_mb=on&lev_400_mb=on&lev_300_mb=on&lev_200_mb=on&lev_100_mb=on&lev_50_mb=on&lev_10_mb=on&lev_5_mb=on&lev_1_mb=on&lev_0.4_mb=on&lev_0.1_mb=on&lev_0.04_mb=on&lev_0.01_mb=on&subregion=&toplat={top_lat}&leftlon={left_lon}&rightlon={right_lon}&bottomlat={btm_lat}"

    base_url = "https://nomads.ncep.noaa.gov/cgi-bin/"
    filter_url = "filter_gfs_0p25_1hr.pl?dir=%2Fgfs."
    current_time_url = f"{date}%2F{cycle}%2Fatmos&file=gfs.t{cycle}z.pgrb2.0p25.f{str(offset_time).zfill(3)}&"
    next_time_url= f"{date}%2F{cycle}%2Fatmos&file=gfs.t{cycle}z.pgrb2.0p25.f{str(offset_time+1).zfill(3)}&"
    weather_vars_url = "var_DZDT=on&var_HGT=on&var_RH=on&var_TMP=on&var_UGRD=on&var_VGRD=on&lev_1000_mb=on&lev_975_mb=on&lev_950_mb=on&lev_925_mb=on&lev_900_mb=on&lev_850_mb=on&lev_800_mb=on&lev_750_mb=on&lev_700_mb=on&lev_650_mb=on&lev_600_mb=on&lev_550_mb=on&lev_500_mb=on&lev_450_mb=on&lev_400_mb=on&lev_350_mb=on&lev_300_mb=on&lev_250_mb=on&lev_200_mb=on&lev_150_mb=on&lev_100_mb=on&lev_70_mb=on&lev_50_mb=on&lev_40_mb=on&lev_30_mb=on&lev_20_mb=on&lev_15_mb=on&lev_10_mb=on&lev_7_mb=on&lev_5_mb=on&lev_3_mb=on&lev_2_mb=on&lev_1_mb=on&lev_surface=on&"
    region_url = f"subregion=&toplat={top_lat}&leftlon={left_lon}&rightlon={right_lon}&bottomlat={btm_lat}"

    current_url = base_url + filter_url + current_time_url + weather_vars_url + region_url
    next_url = base_url + filter_url + next_time_url + weather_vars_url + region_url
    current_r = requests.get(current_url)
    # current_r = requests.get(url_test)
    next_r = requests.get(next_url)

    if current_r.status_code == 200:
        current_file_path = os.path.join("assets", f"d{date}c{cycle}o{str(offset_time).zfill(3)}bl{btm_lat}tl{top_lat}ll{left_lon}rl{right_lon}")
        with open(current_file_path, "wb") as file:
            file.write(current_r.content)
        print("Le téléchargement CURRENT à réussi!")
    else:
        print(f"Erreur {current_r.status_code}: Le téléchargement CURRENT a échoué.")
    if next_r.status_code == 200:
        next_file_path = os.path.join("assets", f"d{date}c{cycle}o{str(offset_time+1).zfill(3)}bl{btm_lat}tl{top_lat}ll{left_lon}rl{right_lon}")
        with open(next_file_path, "wb") as file:
            file.write(next_r.content)
        print("Le téléchargement NEXT à réussi!")
    else:
        print(f"Erreur {next_r.status_code}: Le téléchargement NEXT a échoué.")
    return current_file_path,next_file_path

# Télécharger le fichier GRIB suivant
def download_next_grib_file(date, cycle, offset_time, top_lat, left_lon, right_lon, btm_lat):
    base_url = "https://nomads.ncep.noaa.gov/cgi-bin/"
    filter_url = "filter_gfs_0p25_1hr.pl?dir=%2Fgfs."
    next_time_url= f"{date}%2F{cycle}%2Fatmos&file=gfs.t{cycle}z.pgrb2.0p25.f{str(offset_time).zfill(3)}&"
    weather_vars_url = "var_DZDT=on&var_HGT=on&var_RH=on&var_TMP=on&var_UGRD=on&var_VGRD=on&lev_1000_mb=on&lev_975_mb=on&lev_950_mb=on&lev_925_mb=on&lev_900_mb=on&lev_850_mb=on&lev_800_mb=on&lev_750_mb=on&lev_700_mb=on&lev_650_mb=on&lev_600_mb=on&lev_550_mb=on&lev_500_mb=on&lev_450_mb=on&lev_400_mb=on&lev_350_mb=on&lev_300_mb=on&lev_250_mb=on&lev_200_mb=on&lev_150_mb=on&lev_100_mb=on&lev_70_mb=on&lev_50_mb=on&lev_40_mb=on&lev_30_mb=on&lev_20_mb=on&lev_15_mb=on&lev_10_mb=on&lev_7_mb=on&lev_5_mb=on&lev_3_mb=on&lev_2_mb=on&lev_1_mb=on&lev_surface=on&"
    region_url = f"subregion=&toplat={top_lat}&leftlon={left_lon}&rightlon={right_lon}&bottomlat={btm_lat}"

    next_url = base_url + filter_url + next_time_url + weather_vars_url + region_url
    next_r = requests.get(next_url)

    if next_r.status_code == 200:
        next_file_path = os.path.join("assets", f"d{date}c{cycle}o{offset_time}bl{btm_lat}tl{top_lat}ll{left_lon}rl{right_lon}")
        with open(next_file_path, "wb") as file:
            file.write(next_r.content)
        print("Téléchargement NEXT réussi!")
    else:
        print(f"Erreur {next_r.status_code}: Le téléchargement NEXT a échoué.")
    return next_file_path


def load_grib_data(file_path_1,file_path_2,timeee, target_lat,target_lon,i=0):
    pressure_filter = {
        'typeOfLevel': 'isobaricInhPa',
        'shortName': ['u', 'v', 'isobaricInhPa', 'longitude', 'latitude', 'wz', 'r', 't', 'gh']}
    surface_filter = {
        'typeOfLevel': 'surface',
        'shortName': ['orog']}
    
    current_ds_pressure_levels = xr.open_dataset(file_path_1, engine='cfgrib', filter_by_keys=pressure_filter)
    next_ds_pressure_levels = xr.open_dataset(file_path_2, engine='cfgrib', filter_by_keys=pressure_filter)
    
    ds_surface_level = xr.open_dataset(file_path_1, engine='cfgrib', filter_by_keys=surface_filter)
    print(ds_surface_level.dims)
    print(f"i1:{i}")
    print(f"i2:{i+1}")
    latitudes = np.arange((round(target_lat*4)/4)-1,(round(target_lat*4)/4)+1,0.25)
    longitudes = np.arange((round(target_lon*4)/4)-1,(round(target_lon*4)/4)+1,0.25)
    print(f"latttttt:{latitudes}")
    print(f"loonnnnnn:{longitudes}")
    sliced_current_ds_pressure_level= current_ds_pressure_levels.sel(
        latitude = slice(latitudes[0],latitudes[-1]),
        longitude = slice(longitudes[0],longitudes[-1]),
        longitude = slice(longitudes[0],longitudes[-1]),
    )
    sliced_next_ds_pressure_level= next_ds_pressure_levels.sel(
        latitude = slice(latitudes[0],latitudes[-1]),
        longitude = slice(longitudes[0],longitudes[-1]),
    )
    sliced__ds_surface_level= ds_surface_level.sel(
        latitude = slice(latitudes[0],latitudes[-1]),
        longitude = slice(longitudes[0],longitudes[-1]),
    )
    print(f"{sliced_current_ds_pressure_level}")
    current_ds_pressure_levels = sliced_current_ds_pressure_level.assign_coords(time =i*3600)
    next_ds_pressure_levels = sliced_next_ds_pressure_level.assign_coords(time =(i+1)*3600)
    
    combined_pressure_levels = xr.concat([current_ds_pressure_levels,next_ds_pressure_levels],dim = "time")
    print(combined_pressure_levels.time.values)
    data = {
        'pressure': combined_pressure_levels.isobaricInhPa.values,
        'latitude': latitudes,
        'longitude': longitudes,
        'gph': combined_pressure_levels.gh.interp(time = timeee).values,
        'u_wind': combined_pressure_levels.u.interp(time = timeee).values,
        'v_wind': combined_pressure_levels.v.interp(time = timeee).values,
        'surface': sliced__ds_surface_level.orog.values,
        'w_wind': combined_pressure_levels.wz.interp(time = timeee).values,
        'humidity': combined_pressure_levels.r.interp(time = timeee).values,
        'temp': combined_pressure_levels.t.interp(time = timeee).values
    }
    print(type(combined_pressure_levels.u))
    return data

# def interpolate_data(data,time):
#     print(f"time:{time}")
#     #print(f"time:{data['u_wind']}")
#     # print(f"time:{data['u_wind'].dims}")
    
#     interpolated_data = {
#         'pressure': data['pressure'],
#         'latitude': data['latitude'],
#         'longitude': data['longitude'],
#         'gph': xr.DataArray(data['gph']).interp(dim_0 = time).values,
#         'u_wind': xr.DataArray(data['u_wind']).interp(dim_0 = time).values,
#         'v_wind': xr.DataArray(data['v_wind']).interp(dim_0 = time).values,
#         'surface': data['surface'],
#         'w_wind': xr.DataArray(data['w_wind']).interp(dim_0 = time).values,
#         'humidity': xr.DataArray(data['humidity']).interp(dim_0 = time).values,
#         'temp': xr.DataArray(data['temp']).interp(dim_0 = time).values 
#         }
#     print(type(interpolated_data['u_wind']))
#     print(type(xr.DataArray(data['u_wind'])))
#     print(f"xxxx:{xr.DataArray(data['u_wind']).dim_0.values}")
#     return interpolated_data
