import numpy as np
from pyproj import Geod
from scipy.interpolate import RegularGridInterpolator, interp1d
import xarray as xr 

class Balloon:
    def __init__(self, data, lon_start, lat_start, pressure_start, ascension_speed=5., time_step=10., mass=5, parachute_surface=1, drag_coeff=1.5, ):
        self.lon = lon_start
        self.lat = lat_start
        self.pressure = pressure_start
        self.ascension_speed = ascension_speed
        self.u_interpolator = None
        self.v_interpolator = None
        self.z_interpolator = None
        self.gph_interpolator = None
        self.surface_interpolator = None
        self.humidity_interpolator = None
        self.temp_interpolator = None
        self.prepare_interpolators(data)
        self.altitude = self.get_gph_at_point()
        self.time_step = time_step
        self.trajectory = {
            'longitudes' : [self.lon,],
            'latitudes' : [self.lat,],
            'altitudes' : [self.altitude,]
        }
        # Variables nécassaires pour la phase de descente
        self.mass = mass
        self.gravity = 9.80665 # approximation. A ajuster plus tard pour plus de précision
        self.R = 287  # Constante gaz parfait. Approximation pour air sec. A ajuster plus tard pour plus de précision
        self.C = drag_coeff # approximation. A ajuster plus tard pour plus de précision
        self.parachute_surface = parachute_surface

    def reset(self, lon_start, lat_start, pressure_start):
        self.lon = lon_start
        self.lat = lat_start
        self.pressure = pressure_start
        self.altitude = self.get_gph_at_point()
        self.trajectory = {
            'longitudes' : [self.lon,],
            'latitudes' : [self.lat,],
            'altitudes' : [self.altitude,]
        }

    def prepare_interpolators(self, data):
        """Prépare les interpolateurs pour U et V"""
        self.u_interpolator = RegularGridInterpolator(
            (data['pressure'], data['latitude'], data['longitude']),
            data['u_wind'],
            method='cubic',
            bounds_error=False,
            fill_value=None
        )
        
        self.v_interpolator = RegularGridInterpolator(
            (data['pressure'], data['latitude'], data['longitude']),
            data['v_wind'],
            method='cubic',
            bounds_error=False,
            fill_value=None
        )

        # self.z_interpolator = RegularGridInterpolator(
        #     (data['pressure'], data['latitude'], data['longitude']),
        #     data['v_wind'],
        #     method='cubic',
        #     bounds_error=False,
        #     fill_value=None
        # )

        self.gph_interpolator = RegularGridInterpolator(
            (data['pressure'], data['latitude'], data['longitude']),
            data['gph'],
            method='linear',
            bounds_error=False,
            fill_value=None
        )

        self.surface_interpolator = RegularGridInterpolator(
            (data['latitude'], data['longitude']),
            data['surface'],
            method='cubic',
            bounds_error=False,
            fill_value=None
        )

        # self.humidity_interpolator = RegularGridInterpolator(
        #     (data['pressure'], data['latitude'], data['longitude']),
        #     data['humidity'],
        #     method='cubic',
        #     bounds_error=False,
        #     fill_value=None
        # )

        # self.temp_interpolator = RegularGridInterpolator(
        #     (data['pressure'], data['latitude'], data['longitude']),
        #     data['temp'],
        #     method='cubic',
        #     bounds_error=False,
        #     fill_value=None
        # )

    def prepare_pressure_interpolator(self, data):
        points = np.array([data['pressure'], np.full_like(data['pressure'], self.lat), np.full_like(data['pressure'], self.lon)]).T
        gph_at_coords = self.gph_interpolator(points)
        pressure_interpolator = interp1d(gph_at_coords, data['pressure'], kind='linear', fill_value='extrapolate')############# EXTRAPOLATE??????
        return pressure_interpolator

    def get_wind_at_point(self):
        """Obtient les composantes du vent à un point donné"""
        point = np.array([self.pressure, self.lat, self.lon])
        return self.u_interpolator(point)[0], self.v_interpolator(point)[0]
    
    def get_gph_at_point(self):
        point = np.array([self.pressure, self.lat, self.lon])
        return self.gph_interpolator(point)[0]
    
    def get_pressure_at_point(self, data):
        pressure_interpolator = self.prepare_pressure_interpolator(data)
        return pressure_interpolator(self.altitude)

    def get_fall_speed_at_point(self):
        pass

    def get_next_point(self, data):
        geod = Geod(ellps="WGS84")

        u_wind, v_wind = self.get_wind_at_point()
        #print("interp of u ,v : ", u_wind,v_wind)
        delta_lon = u_wind * self.time_step  # Distance est-ouest (m/s * s)
        delta_lat = v_wind * self.time_step  # Distance nord-sud (m/s * s)
        #Tests de différents codes
        code = 0
        if(code == 0):
            # Calcul de l'azimut (direction) et de la distance
            azimut = np.degrees(np.arctan2(delta_lon, delta_lat)) % 360  # En degrés
            distance = np.hypot(delta_lon, delta_lat)  # Distance totale (mètres)

            # Calcul du nouveau point (géodésique)
            lon_new, lat_new, _ = geod.fwd(self.lon, self.lat, azimut, distance)
        
        if(code == 1):
            # Conversion des distances en degrés
            delta_lon_deg = delta_lon / (111320. * np.cos(np.radians(self.lat)))  # 1° longitude ≈ 111.32 km * cos(latitude)
            delta_lat_deg = delta_lat / 110540.  # 1° latitude ≈ 110.54 km

            # Calcul de la nouvelle position géographique
            lon_new = self.lon + delta_lon_deg
            lat_new = self.lat + delta_lat_deg

        # if(up):
        #     delta_altitude = self.ascension_speed * self.time_step  # En mètres
        # else:
        #     fall_speed = self.get_fall_speed_at_point()
        #     delta_altitude = fall_speed * self.time_step
        delta_altitude = self.ascension_speed * self.time_step  # En mètres
        self.altitude = self.get_gph_at_point()
        altitude_new = self.altitude + delta_altitude

        # Mise à jour du self.alt pour calcul de la nouvelle pression
        self.altitude = altitude_new
        pressure_new = self.get_pressure_at_point(data)

        # Mise à jour des données du ballon
        self.pressure = pressure_new
        self.lon = lon_new
        self.lat = lat_new 

        # Ajout du point dans trajectoire
        self.trajectory['longitudes'].append(lon_new)
        self.trajectory['latitudes'].append(lat_new)
        self.trajectory['altitudes'].append(altitude_new)

    def get_surface_level_at_coords(self):
        coords = np.array([self.lat, self.lon])
        return self.surface_interpolator(coords)[0]