## imports
import xarray as xr

# Télécharger le fichier GRIB
def download_grib_file(url, output_path):
    pass

def load_grib_data(file_path):
    filter_keys = {"typeOfLevel": "isobaricInhPa"}
    ds = xr.open_dataset(file_path, engine="cfgrib", filter_by_keys=filter_keys)

    # Structure contenant toutes les données grib nécessaires
    data = {
        "pressure": ds.variables["isobaricInhPa"],
        "latitude": ds.variables["latitude"],
        "longitude": ds.variables["longitude"],
        
        "u_wind": ds.variables["u"],
        "v_wind": ds.variables["v"],
        "temperature": ds.variables["t"]
    }
    return data