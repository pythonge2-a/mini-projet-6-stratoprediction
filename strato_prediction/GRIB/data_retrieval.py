# Imports
import xarray as xr
import requests
import os

# Télécharger le fichier GRIB
def download_grib_file(date, cycle, offset_time, geo_bounds):
    """
    Télécharge les fichiers GRIB correspondant au temps actuel (current_time) et au temps suivant (next_time).

    Paramètres:
        date (str): La date au format AAAAMMJJ.
        cycle (str): Le cycle horaire de prévision (par exemple, "00", "06", "12", "18").
        offset_time (int): L'heure de prévision en décalage (par exemple, 3 pour 3 heures après le début du cycle).
        geo_bounds (dict): Dictionnaire définissant les limites géographiques de la zone, avec les clés suivantes:
            - 'top_lat' (float): Limite supérieure de latitude.
            - 'btm_lat' (float): Limite inférieure de latitude.
            - 'right_lon' (float): Limite supérieure de longitude.
            - 'left_lon' (float): Limite inférieure de longitude.

    Retourne:
        tuple: Chemins des fichiers téléchargés pour le temps actuel (current_time) et le temps suivant (next_time).
            - current_file_path (str): Chemin du fichier GRIB pour le temps actuel.
            - next_file_path (str): Chemin du fichier GRIB pour le temps suivant.
    """
    # Construction des URLs pour les fichiers GRIB actuels et suivants
    base_url = "https://nomads.ncep.noaa.gov/cgi-bin/"
    filter_url = "filter_gfs_0p25_1hr.pl?dir=%2Fgfs."
    current_time_url = f"{date}%2F{cycle}%2Fatmos&file=gfs.t{cycle}z.pgrb2.0p25.f{str(offset_time).zfill(3)}&"
    next_time_url= f"{date}%2F{cycle}%2Fatmos&file=gfs.t{cycle}z.pgrb2.0p25.f{str(offset_time+1).zfill(3)}&"
    weather_vars_url = "var_DZDT=on&var_HGT=on&var_RH=on&var_TMP=on&var_UGRD=on&var_VGRD=on&lev_1000_mb=on&lev_975_mb=on&lev_950_mb=on&lev_925_mb=on&lev_900_mb=on&lev_850_mb=on&lev_800_mb=on&lev_750_mb=on&lev_700_mb=on&lev_650_mb=on&lev_600_mb=on&lev_550_mb=on&lev_500_mb=on&lev_450_mb=on&lev_400_mb=on&lev_350_mb=on&lev_300_mb=on&lev_250_mb=on&lev_200_mb=on&lev_150_mb=on&lev_100_mb=on&lev_70_mb=on&lev_50_mb=on&lev_40_mb=on&lev_30_mb=on&lev_20_mb=on&lev_15_mb=on&lev_10_mb=on&lev_7_mb=on&lev_5_mb=on&lev_3_mb=on&lev_2_mb=on&lev_1_mb=on&lev_surface=on&"
    
    # Construction de la zone géographique pour la demande
    region_url = f"subregion=&toplat={geo_bounds['top_lat']}&leftlon={geo_bounds['left_lon']}&rightlon={geo_bounds['right_lon']}&bottomlat={geo_bounds['btm_lat']}"
    
    # URLs complètes pour le fichier actuel et le fichier suivant
    current_url = base_url + filter_url + current_time_url + weather_vars_url + region_url
    next_url = base_url + filter_url + next_time_url + weather_vars_url + region_url
    
    # Chemins des fichiers téléchargés
    current_file_path = os.path.join("assets", f"d{date}c{cycle}o{str(offset_time).zfill(3)}bl{geo_bounds['btm_lat']}tl{geo_bounds['top_lat']}ll{geo_bounds['left_lon']}rl{geo_bounds['right_lon']}")
    next_file_path = os.path.join("assets", f"d{date}c{cycle}o{str(offset_time+1).zfill(3)}bl{geo_bounds['btm_lat']}tl{geo_bounds['top_lat']}ll{geo_bounds['left_lon']}rl{geo_bounds['right_lon']}")
    
    # Vérification si les fichiers existent déjà
    if os.path.exists(current_file_path) and os.path.exists(next_file_path):
        print("Le fichier existe déjà. Téléchargement ignoré.")
        return current_file_path, next_file_path
    
    # Demande HTTP pour télécharger le fichier actuel et suivant
    current_request = requests.get(current_url)
    next_request = requests.get(next_url)
    
    # Vérification du succès du téléchargement du fichier actuel
    if current_request.status_code == 200:
        with open(current_file_path, "wb") as file:
            file.write(current_request.content)
        print("Le téléchargement CURRENT à réussi!")
    else:
        print(f"Erreur {current_request.status_code}: Le téléchargement CURRENT a échoué.")
        
    # Vérification du succès du téléchargement du fichier suivant
    if next_request.status_code == 200:
        with open(next_file_path, "wb") as file:
            file.write(next_request.content)
        print("Le téléchargement NEXT à réussi!")
    else:
        print(f"Erreur {next_request.status_code}: Le téléchargement NEXT a échoué.")
    return current_file_path,next_file_path

# Télécharger le fichier GRIB suivant
def download_next_grib_file(date, cycle, offset_time, geo_bounds):
    """
    Télécharge le fichier GRIB correspondant au temps suivant (next_time).

    Paramètres:
        date (str): La date au format AAAAMMJJ.
        cycle (str): Le cycle horaire de prévision (par exemple, "00", "06", "12", "18").
        offset_time (int): L'heure de prévision en décalage (par exemple, 3 pour 3 heures après le début du cycle).
        geo_bounds (dict): Dictionnaire définissant les limites géographiques de la zone, avec les clés suivantes:
            - 'top_lat' (float): Limite supérieure de latitude.
            - 'btm_lat' (float): Limite inférieure de latitude.
            - 'right_lon' (float): Limite supérieure de longitude.
            - 'left_lon' (float): Limite inférieure de longitude.

    Retourne:
        str: Chemin du fichier téléchargé pour le temps suivant (next_time).
            - next_file_path (str): Chemin du fichier GRIB téléchargé.
    """
    # Construction de l'URL pour le fichier suivant
    base_url = "https://nomads.ncep.noaa.gov/cgi-bin/"
    filter_url = "filter_gfs_0p25_1hr.pl?dir=%2Fgfs."
    time_url= f"{date}%2F{cycle}%2Fatmos&file=gfs.t{cycle}z.pgrb2.0p25.f{str(offset_time+1).zfill(3)}&"
    weather_vars_url = "var_DZDT=on&var_HGT=on&var_RH=on&var_TMP=on&var_UGRD=on&var_VGRD=on&lev_1000_mb=on&lev_975_mb=on&lev_950_mb=on&lev_925_mb=on&lev_900_mb=on&lev_850_mb=on&lev_800_mb=on&lev_750_mb=on&lev_700_mb=on&lev_650_mb=on&lev_600_mb=on&lev_550_mb=on&lev_500_mb=on&lev_450_mb=on&lev_400_mb=on&lev_350_mb=on&lev_300_mb=on&lev_250_mb=on&lev_200_mb=on&lev_150_mb=on&lev_100_mb=on&lev_70_mb=on&lev_50_mb=on&lev_40_mb=on&lev_30_mb=on&lev_20_mb=on&lev_15_mb=on&lev_10_mb=on&lev_7_mb=on&lev_5_mb=on&lev_3_mb=on&lev_2_mb=on&lev_1_mb=on&lev_surface=on&"
    # Construction de la zone géographique pour la demande
    region_url = f"subregion=&toplat={geo_bounds['top_lat']}&leftlon={geo_bounds['left_lon']}&rightlon={geo_bounds['right_lon']}&bottomlat={geo_bounds['btm_lat']}"

    # Création des variations de +/- 0.1 autour de geo_bounds
    variations = [
        {"btm_lat": geo_bounds['btm_lat'] - 0.1, "top_lat": geo_bounds['top_lat'] - 0.1, "left_lon": geo_bounds['left_lon'] - 0.1, "right_lon": geo_bounds['right_lon'] - 0.1},
        {"btm_lat": geo_bounds['btm_lat'] - 0.1, "top_lat": geo_bounds['top_lat'] - 0.1, "left_lon": geo_bounds['left_lon'] + 0.1, "right_lon": geo_bounds['right_lon'] + 0.1},
        {"btm_lat": geo_bounds['btm_lat'] + 0.1, "top_lat": geo_bounds['top_lat'] + 0.1, "left_lon": geo_bounds['left_lon'] - 0.1, "right_lon": geo_bounds['right_lon'] - 0.1},
        {"btm_lat": geo_bounds['btm_lat'] + 0.1, "top_lat": geo_bounds['top_lat'] + 0.1, "left_lon": geo_bounds['left_lon'] + 0.1, "right_lon": geo_bounds['right_lon'] + 0.1},
    ]

    # Vérification si un fichier autour des variations existe
    for var in variations:
        # Chemins du fichier suivant téléchargé
        next_file_path = os.path.join("assets", f"d{date}c{cycle}o{str(offset_time+1).zfill(3)}bl{var['btm_lat']}tl{var['top_lat']}ll{var['left_lon']}rl{var['right_lon']}")

        if os.path.exists(next_file_path):
            print("Le fichier existe déjà. Téléchargement ignoré.")
            return next_file_path
    
    # URL complète pour le fichier suivant
    next_url = base_url + filter_url + time_url + weather_vars_url + region_url

    # Demande HTTP pour télécharger le fichier suivant
    next_request = requests.get(next_url)
    
    # Vérification du succès du téléchargement du fichier suivant
    if next_request.status_code == 200:
        with open(next_file_path, "wb") as file:
            file.write(next_request.content)
        print("Téléchargement NEXT réussi!")
    else:
        print(f"Erreur {next_request.status_code}: Le téléchargement NEXT a échoué.")
    return next_file_path

def load_grib_data(current_file_path, next_file_path):
    """
    Charge les données GRIB des fichiers spécifiés et applique des filtres pour extraire les variables et niveaux nécessaires.

    Paramètres:
        current_file_path (str): Chemin vers le fichier GRIB correspondant au temps actuel.
        next_file_path (str): Chemin vers le fichier GRIB correspondant au temps suivant.

    Retourne:
        tuple: Contient trois ensembles de données Xarray:
            - current_pressure_dataset (xarray.Dataset): Données à différents niveaux isobariques pour le temps actuel.
            - next_pressure_dataset (xarray.Dataset): Données à différents niveaux isobariques pour le temps suivant.
            - surface_dataset (xarray.Dataset): Données de surface pour le temps actuel.
    """
    # Définition du filtre pour les niveaux isobariques
    pressure_filter = {
        'typeOfLevel': 'isobaricInhPa', # Niveau isobarique en hPa
        'shortName': ['u', 'v', 'isobaricInhPa', 'longitude', 'latitude', 'wz', 'r', 't', 'gh']} # Variables à extraire
    
    # Définition du filtre pour les données de surface
    surface_filter = {
        'typeOfLevel': 'surface', # Niveau de surface
        'shortName': ['orog']} # Variables de surface à extraire
    
    # Ouverture du fichier GRIB pour le temps actuel et extraction des données isobariques
    current_pressure_dataset = xr.open_dataset(current_file_path, engine='cfgrib', filter_by_keys=pressure_filter)
    
    # Ouverture du fichier GRIB pour le temps suivant et extraction des données isobariques
    next_pressure_dataset = xr.open_dataset(next_file_path, engine='cfgrib', filter_by_keys=pressure_filter)
    
    # Ouverture du fichier GRIB pour le temps actuel et extraction des données de surface
    surface_dataset = xr.open_dataset(current_file_path, engine='cfgrib', filter_by_keys=surface_filter)

    return current_pressure_dataset, next_pressure_dataset, surface_dataset

def interpolate_data(current_pressure_dataset, next_pressure_dataset, surface_dataset, target_time, lat, lon, pressure, hour=0):
    # pressure_levels = current_pressure_dataset.isobaricInhPa.values
    # target_index = (abs(pressure_levels - pressure)).argmin()  # Indice le plus proche
    # indices = slice(max(0, target_index - 2), min(len(pressure_levels), target_index + 3))
    current_pressure_subset = current_pressure_dataset.sel(
        latitude = slice(lat - 1., lat + 1.),
        longitude = slice(lon - 1., lon + 1.)
    )
    next_pressure_subset = next_pressure_dataset.sel(
        latitude = slice(lat - 1., lat + 1.),
        longitude = slice(lon - 1., lon + 1.)
    )
    # next_pressure_subset = next_pressure_dataset.isel(isobaricInhPa=indices).sel(
    #     latitude = slice(lat - 1., lat + 1.),
    #     longitude = slice(lon - 1., lon + 1.)
    # )
    surface_subset = surface_dataset.sel(
        latitude = slice(lat - 1., lat + 1.),
        longitude = slice(lon - 1., lon + 1.)
    )

    current_pressure_subset = current_pressure_subset.assign_coords(time =hour*3600)
    next_pressure_subset = next_pressure_subset.assign_coords(time =(hour+1)*3600)
    
    combined_pressure_subset = xr.concat([current_pressure_subset,next_pressure_subset], dim = "time")
    print(hour, target_time)
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
