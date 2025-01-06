import numpy as np
import xarray as xr
from scipy.interpolate import RegularGridInterpolator, interp1d
from strato_prediction.GRIB import load_grib_data

# Chargement du fichier GRIB (avec cfgrib)
file_path = "assets/gfs.t12z.pgrb2.0p25(4).f000"
data = load_grib_data(file_path)

# Créer un interpolateur 3D avec RegularGridInterpolator
print(data['pressure'])
print(data['latitude'])
print(data['longitude'])
gph_interpolator = RegularGridInterpolator(
    (data['pressure'], data['latitude'], data['longitude']),  # Grilles 3D
    data['gph'],  # Valeurs de géopotentielle
    method='linear',  # Interpolation linéaire
    bounds_error=False,
    fill_value=0
)

# Coordonnées cibles
lat_target = 47.1
lon_target = 7.1

points = np.array([data['pressure'], np.full_like(data['pressure'], lat_target), np.full_like(data['pressure'], lon_target)]).T
#point = np.array([pressure_at_target,lat_target,lon_target])
# Sélectionner les hatueurs géopotentielles aux coordonnées cibles (latitude, longitude)
gph_at_coords = gph_interpolator(points)
print(gph_at_coords)

# Créer un interpolateur pour les niveaux de pression et GPH
pressure_interpolator = interp1d(gph_at_coords, data['pressure'], kind='linear', fill_value=None)

# Hauteur géopotentielle cible (en mètres)
gph_target = 5000.  # Exemple : 5000 m

# Interpolation de la pression
interpolated_pressure = pressure_interpolator(gph_target)

point = np.array([interpolated_pressure, lat_target, lon_target])
gph_new = gph_interpolator(point)[0]

# Afficher les résultats
print(f"Pression interpolée à GPH      = {gph_target} m                 : {interpolated_pressure} hPa")
print(f"Altitude interpolée à Pressure = {interpolated_pressure} hPa : {gph_new} m")
