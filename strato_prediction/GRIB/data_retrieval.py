## imports
import xarray as xr
import requests
import os

# Télécharger le fichier GRIB
def download_grib_file(date, cycle, offset_time, top_lat, left_lon, right_lon, btm_lat):

    base_url = "https://nomads.ncep.noaa.gov/cgi-bin/"
    filter_url = "filter_gfs_0p25_1hr.pl?dir=%2Fgfs."
    time_url = f"{date}%2F{cycle}%2Fatmos&file=gfs.t{cycle}z.pgrb2.0p25.f{offset_time}&"
    weather_vars_url = "var_HGT=on&var_TMP=on&var_UGRD=on&var_VGRD=on&lev_1000_mb=on&lev_900_mb=on&lev_800_mb=on&lev_700_mb=on&lev_600_mb=on&lev_500_mb=on&lev_400_mb=on&lev_300_mb=on&lev_200_mb=on&lev_100_mb=on&lev_50_mb=on&lev_10_mb=on&lev_5_mb=on&lev_1_mb=on&lev_0.4_mb=on&lev_0.1_mb=on&lev_0.04_mb=on&lev_0.01_mb=on&"
    region_url = f"subregion=&toplat={top_lat}&leftlon={left_lon}&rightlon={right_lon}&bottomlat={btm_lat}"

    url = base_url + filter_url + time_url + weather_vars_url + region_url
    r = requests.get(url)

    if r.status_code == 200:
        file_path = os.path.join("assets", f"d{date}c{cycle}o{offset_time}bl{btm_lat}tl{top_lat}ll{left_lon}rl{right_lon}")
        with open(file_path, "wb") as file:
            file.write(r.content)
        print("Téléchargement réussi!")
    else:
        print(f"Erreur {r.status_code}: Le téléchargement a échoué.")
    return file_path

def load_grib_data(file_path):
    filter_keys = {
        'typeOfLevel': 'isobaricInhPa',
        'shortName': ['u', 'v', 't', 'gh']  # On ne charge que les variables dont on a besoin
    }
    ds = xr.open_dataset(file_path, engine='cfgrib', filter_by_keys=filter_keys, backend_kwargs={'errors': 'ignore'})
    # print(f"time:{ds.time.values}")
    # print(f"step:{ds.step.values}")
    # print(f"dataLat:{ds.latitude}")
    # print(f"dataLatU:{ds.u.values.max()}")
    # print(f"dataLatU:{ds.u.values}")
    # # print(f"dataLatU:{ds.u}")
    # # print(f"dataLon:{ds.longitude}")
    # # print(f"dataLonV:{ds.v}")
    # print(f"dataLonV:{ds.v.values.max()}")
    # print(f"dataLonV:{ds.v.values}")
    # print(f"dataLat:{ds.latitude.values}")
    # print(f"dataLon:{ds.longitude.values}")
    # print(f"dataLon:{ds.isobaricInhPa.values}")
    # print(f"dataLon:{ds.t.values}")
    # print(ds)
    # Structure contenant toutes les données grib nécessaires
    #print(f"gph:{ds.gh.values}")
    print(ds.gh.values)
    data = {
        "pressure": ds.isobaricInhPa.values,
        "latitude": ds.latitude.values,
        "longitude": ds.longitude.values,
        
        "u_wind": ds.u.values,
        "v_wind": ds.v.values,
        "temperature": ds.t.values,
        "gp_height": ds.gh.values
    }
    return data