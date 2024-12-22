import numpy as np
from pyproj import Geod
from .conversions import pressure_to_altitude, altitude_to_pressure

class Balloon:
    def __init__(self, lon_start, lat_start, pressure_start, ascendion_speed=5, time_step=60):
        self.lon = lon_start
        self.lat = lat_start
        self.pressure = pressure_start
        self.altitude = pressure_to_altitude(self.pressure)
        self.z_speed = ascendion_speed
        self.u_speed_interp = None
        self.v_speed_interp = None
        self.time_step = time_step
        self.trajectory = {
            'longitudes' : [self.lon,],
            'latitudes' : [self.lat,],
            'altitudes' : [self.altitude,]
        } #list coord 3d (lon, lat, pres/alt)

    #calculations

    def get_wind_at_point(self, u_interpolator, v_interpolator):
        """Obtient les composantes du vent à un point donné"""
        point = np.array([self.pressure, self.lat, self.lon])
        return {
            'u': u_interpolator(point),
            'v': v_interpolator(point)
        }
    
    def get_next_point(self, u_interpolator, v_interpolator):
        geod = Geod(ellps="WGS84")

        wind = self.get_wind_at_point(u_interpolator, v_interpolator)
        u_wind = wind['u']
        v_wind = wind['v']

        # Calcul de la distance parcourue (delta_lat et delta_lon)
        delta_lon = u_wind * self.time_step  # Distance est-oust (m)
        delta_lat = v_wind * self.time_step  # Distance nord-sud (m)

        # Calcul de l'azimut et de la distance
        azimut = np.arctan2(delta_lat, delta_lon) * (180 / np.pi)  # Convertir en degrés
        distance = np.hypot(delta_lon, delta_lat)  # Distance totale en mètres

        # Calcul de la nouvelle position géographique
        lon_new, lat_new, _ = geod.fwd(self.lon, self.lat, azimut, distance)

        lon_new, lat_new, _ = geod.fwd(self.lon, self.lat, np.arctan2(delta_lat, delta_lon), np.hypot(delta_lon, delta_lat))

        # Mise à jour de la pression via la vitesse d'ascension
        delta_altitude = self.z_speed * self.time_step  # En mètres
        altitude_new = pressure_to_altitude(self.pressure) + delta_altitude
        pressure_new = altitude_to_pressure(altitude_new)

        self.pressure = pressure_new
        self.altitude = altitude_new
        self.lon = lon_new
        self.lat = lat_new 

        self.trajectory['longitudes'].append(lon_new)
        self.trajectory['latitudes'].append(lat_new)
        self.trajectory['altitudes'].append(altitude_new)

        return lat_new, lon_new, altitude_new, pressure_new
