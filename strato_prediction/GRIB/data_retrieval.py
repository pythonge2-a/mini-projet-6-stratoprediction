## imports
import xarray as xr

# Télécharger le fichier GRIB
def download_grib_file(url, output_path):
    pass

def load_grib_data(file_path):
    filter_keys = {
        'typeOfLevel': 'isobaricInhPa',
        'shortName': ['u', 'v', 't']  # On ne charge que les variables dont on a besoin
    }
    ds = xr.open_dataset(file_path, engine='cfgrib', filter_by_keys=filter_keys, backend_kwargs={'errors': 'ignore'})
    # print(f"time:{ds.time.values}")
    # print(f"step:{ds.step.values}")
    # print(f"dataLat:{ds.latitude}")
    # print(f"dataLatU:{ds.u.values}")
    # print(f"dataLatU:{ds.u}")
    # print(f"dataLon:{ds.longitude}")
    # print(f"dataLonV:{ds.v}")
    # print(f"dataLonV:{ds.v.values}")
    print(f"dataLat:{ds.latitude.values}")
    print(f"dataLon:{ds.longitude.values}")
    print(f"dataLon:{ds.isobaricInhPa.values}")
    
    # Structure contenant toutes les données grib nécessaires
    data = {
        "pressure": ds.isobaricInhPa.values,
        "latitude": ds.latitude.values,
        "longitude": ds.longitude.values,
        
        "u_wind": ds.u.values,
        "v_wind": ds.v.values,
        "temperature": ds.t.values
    }
    return data