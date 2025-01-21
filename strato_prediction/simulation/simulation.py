import numpy as np
from pyproj import Geod
from scipy.interpolate import RegularGridInterpolator, interp1d
from .utils import calculate_air_density

class Balloon:
    def __init__(self, data, start_lon, start_lat, start_pressure, w_speed=4.96, time_step=1., mass=3.1, parachute_surface=2.01, drag_coeff=1.3):
        self.lon = start_lon
        self.lat = start_lat
        self.pressure = start_pressure
        self.time_flying = 0
        self.w_speed = w_speed
        self.u_interpolator = None
        self.v_interpolator = None
        self.w_interpolator = None
        self.gph_interpolator = None
        self.surface_interpolator = None
        self.humidity_interpolator = None
        self.temp_interpolator = None
        self.prepare_interpolators(data)
        self.altitude = self.get_surface_level_at_coords()
        self.time_step = time_step
        self.trajectory = {
            'longitudes' : [self.lon,],
            'latitudes' : [self.lat,],
            'altitudes' : [self.altitude,],
            'times' : [self.time_flying,]
        }
        # Variables nécassaires pour la phase de descente
        self.mass = mass
        self.gravity = 9.80665 # approximation. A ajuster plus tard pour plus de précision
        self.C = drag_coeff # approximation. A ajuster plus tard pour plus de précision
        self.parachute_surface = parachute_surface
        self.descent_time = 0

    def reset(self, data, start_lon, start_lat, start_pressure):
        self.lon = start_lon
        self.lat = start_lat
        self.pressure = start_pressure
        self.time_flying = 0
        self.u_interpolator = None
        self.v_interpolator = None
        self.w_interpolator = None
        self.gph_interpolator = None
        self.surface_interpolator = None
        self.humidity_interpolator = None
        self.temp_interpolator = None
        self.prepare_interpolators(data)
        self.altitude = self.get_surface_level_at_coords()
        self.trajectory = {
            'longitudes' : [self.lon,],
            'latitudes' : [self.lat,],
            'altitudes' : [self.altitude,],
            'times':  [self.time_flying,]
        }

    def prepare_interpolators(self, data):
        self.u_interpolator = RegularGridInterpolator(
            (data['pressure'], data['latitude'], data['longitude']),
            data['u_wind'],
            method='cubic',
            bounds_error=False,
            fill_value=69420
        )
        
        self.v_interpolator = RegularGridInterpolator(
            (data['pressure'], data['latitude'], data['longitude']),
            data['v_wind'],
            method='cubic',
            bounds_error=False,
            fill_value=69420
        )

        self.w_interpolator = RegularGridInterpolator(
            (data['pressure'], data['latitude'], data['longitude']),
            data['w_wind'],
            method='cubic',
            bounds_error=False,
            fill_value=69420
        )

        self.gph_interpolator = RegularGridInterpolator(
            (data['pressure'], data['latitude'], data['longitude']),
            data['gph'],
            method='linear',
            bounds_error=False,
            fill_value=69420
        )

        self.surface_interpolator = RegularGridInterpolator(
            (data['latitude'], data['longitude']),
            data['surface'],
            method='cubic',
            bounds_error=False,
            fill_value=69420
        )

        self.humidity_interpolator = RegularGridInterpolator(
            (data['pressure'], data['latitude'], data['longitude']),
            data['humidity'],
            method='cubic',
            bounds_error=False,
            fill_value=69420
        )

        self.temp_interpolator = RegularGridInterpolator(
            (data['pressure'], data['latitude'], data['longitude']),
            data['temp'],
            method='cubic',
            bounds_error=False,
            fill_value=69420
        )

    def prepare_pressure_interpolator(self, data):
        points = np.array([data['pressure'], np.full_like(data['pressure'], self.lat), np.full_like(data['pressure'], self.lon)]).T
        gph_at_coords = self.gph_interpolator(points)
        pressure_interpolator = interp1d(gph_at_coords, data['pressure'], kind='linear', fill_value='extrapolate')############# EXTRAPOLATE??????
        return pressure_interpolator

    def get_wind_at_point(self):
        point = np.array([self.pressure, self.lat, self.lon])
        return self.u_interpolator(point)[0], self.v_interpolator(point)[0], self.w_interpolator(point)[0]
    
    def get_gph_at_point(self):
        point = np.array([self.pressure, self.lat, self.lon])
        return self.gph_interpolator(point)[0]
    
    def get_pressure_at_point(self, data):
        pressure_interpolator = self.prepare_pressure_interpolator(data)
        return pressure_interpolator(self.altitude)
    
    def get_temp_at_point(self):
        point = np.array([self.pressure, self.lat, self.lon])
        return self.temp_interpolator(point)[0]
    
    def get_humidity_at_point(self):
        point = np.array([self.pressure, self.lat, self.lon])
        return self.humidity_interpolator(point)[0]
    

    def get_fall_speed_at_point(self):
        # Calcul de la vitesse terminal
        temp = self.get_temp_at_point()
        humidity = self.get_humidity_at_point()
        rho = calculate_air_density(self.pressure, temp, humidity)
        k = 0.5 * self.C * rho * self.parachute_surface
        v_t = np.sqrt(self.mass * self.gravity / k)

        # Temps et vitesse en fonction du temps
        self.descent_time += self.time_step
        self.w_speed = - v_t * np.tanh((self.gravity / v_t) * self.descent_time)
        
    def get_next_point(self, data, down=0):
        geod = Geod(ellps="WGS84")

        u_wind, v_wind, w_wind = self.get_wind_at_point()
        delta_lon = u_wind * self.time_step  # Distance est-ouest (m/s * s)
        delta_lat = v_wind * self.time_step  # Distance nord-sud (m/s * s)

        # Calcul de l'azimut (direction) et de la distance
        azimut = np.degrees(np.arctan2(delta_lon, delta_lat)) % 360  # En degrés
        distance = np.hypot(delta_lon, delta_lat)  # Distance totale (mètres)

        # Calcul du nouveau point (géodésique)
        lon_new, lat_new, _ = geod.fwd(self.lon, self.lat, azimut, distance)
        

        if(down):
            self.get_fall_speed_at_point()
        delta_altitude = (self.w_speed + w_wind) * self.time_step  # En mètres
        self.altitude = self.get_gph_at_point()
        altitude_new = self.altitude + delta_altitude

        # Mise à jour du self.alt pour calcul de la nouvelle pression
        self.altitude = altitude_new
        pressure_new = self.get_pressure_at_point(data)

        time_new = self.time_flying + self.time_step

        # Mise à jour des données du ballon
        self.pressure = pressure_new
        self.lon = lon_new
        self.lat = lat_new 
        self.time_flying = time_new

        # Ajout du point dans trajectoire
        self.trajectory['longitudes'].append(lon_new)
        self.trajectory['latitudes'].append(lat_new)
        self.trajectory['altitudes'].append(altitude_new)
        self.trajectory['times'].append(time_new)

    def get_surface_level_at_coords(self):
        coords = np.array([self.lat, self.lon])
        return self.surface_interpolator(coords)[0]