## imports
import xarray as xr

# Télécharger le fichier GRIB
def download_grib_file(url, output_path):
    pass

def load_grib_data(file_path):
    filter_keys = {'typeOfLevel': "isobaricInhPa"}
    ds = xr.open_dataset(file_path, engine='cfgrib', filter_by_keys=filter_keys)

    # Structure contenant toutes les données grib nécessaires
    data = {
        'pressure': ds.isobaricInhPa.values,
        'latitude': ds.latitude.values,
        'longitude': ds.longitude.values,
        'u_wind': ds.u.values,
        'v_wind': ds.v.values
    }
    return data