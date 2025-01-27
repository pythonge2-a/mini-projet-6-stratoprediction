import numpy as np
from pyproj import Geod
from scipy.interpolate import RegularGridInterpolator, interp1d
from .utils import calculate_air_density

class Balloon:
    """
    Classe représentant un ballon atmosphérique pour simuler son déplacement.
    """

    def __init__(self, data, start_lon, start_lat, start_pressure, w_speed=5.32, time_step=1., mass=1.0, parachute_surface=1.13, drag_coeff=1.2):
        # Initialisation des paramètres du ballon
        self.lat = start_lat
        self.lon = start_lon
        self.pressure = start_pressure
        self.w_speed = w_speed 
        self.time_step = time_step
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
            'longitudes': [self.lon],
            'latitudes': [self.lat],
            'altitudes': [self.altitude],
            'times': [self.time_flying]
        }
        # Variables nécessaires pour la phase de descente
        self.mass = mass
        self.gravity = 9.80665
        self.C = drag_coeff  # Coefficient de traînée
        self.parachute_surface = parachute_surface
        self.descent_time = 0

    def reset(self, data, start_lon, start_lat, start_pressure):
        """
        Réinitialise le ballon avec de nouveaux paramètres initiaux.
        """
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
        self.altitude = 932 #self.get_surface_level_at_coords()
        self.trajectory = {
            'longitudes': [self.lon],
            'latitudes': [self.lat],
            'altitudes': [self.altitude],
            'times': [self.time_flying]
        }

    def prepare_interpolators(self, data):
        """
        Configure les interpolateurs pour les données atmosphériques (vents, géopotentiel, etc.).
        """
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

    def prepare_air_density_interpolators(self, data):
        """
        Prépare les interpolateurs pour l'humidité et la température.
        """
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
        """
        Prépare un interpolateur pour obtenir la pression en fonction de l'altitude.
        """
        points = np.array([data['pressure'], np.full_like(data['pressure'], self.lat), np.full_like(data['pressure'], self.lon)]).T
        gph_at_coords = self.gph_interpolator(points)
        pressure_interpolator = interp1d(gph_at_coords, data['pressure'], kind='linear', fill_value='extrapolate')
        return pressure_interpolator

    def get_wind_at_point(self):
        """
        Renvoie les composantes U, V, W du vent au point actuel.
        """
        point = np.array([self.pressure, self.lat, self.lon])
        return self.u_interpolator(point)[0], self.v_interpolator(point)[0], self.w_interpolator(point)[0]
    
    def get_gph_at_point(self):
        """
        Renvoie l'altitude géopotentielle au point actuel.
        """
        point = np.array([self.pressure, self.lat, self.lon])
        return self.gph_interpolator(point)[0]
    
    def get_pressure_at_point(self, data):
        """
        Renvoie la pression en fonction de l'altitude actuelle.
        """
        pressure_interpolator = self.prepare_pressure_interpolator(data)
        return pressure_interpolator(self.altitude)
    
    def get_temp_at_point(self):
        """
        Renvoie la température au point actuel.
        """
        point = np.array([self.pressure, self.lat, self.lon])
        return self.temp_interpolator(point)[0]
    
    def get_humidity_at_point(self):
        """
        Renvoie l'humidité au point actuel.
        """
        point = np.array([self.pressure, self.lat, self.lon])
        return self.humidity_interpolator(point)[0]
    
    def get_fall_speed_at_point(self):
        """
        Calcule la vitesse de chute terminale en tenant compte de la densité de l'air.
        """
        temp = self.get_temp_at_point()
        humidity = self.get_humidity_at_point()
        rho = calculate_air_density(self.pressure, temp, humidity)  # Densité de l'air
        k = 0.5 * self.C * rho * self.parachute_surface # Constante pour calcul v_t
        v_t = np.sqrt(self.mass * self.gravity / k)  # Vitesse terminale

        # Temps et vitesse en fonction du temps
        self.descent_time += self.time_step
        self.w_speed = -v_t * np.tanh((self.gravity / v_t) * self.descent_time)
        
    def get_next_point(self, data, down=0):
        """
        Calcule la position suivante du ballon en fonction des vents et des conditions.
        """
        geod = Geod(ellps="WGS84")

        u_wind, v_wind, w_wind = self.get_wind_at_point()
        delta_lon = u_wind * self.time_step  # Déplacement en longitude
        delta_lat = v_wind * self.time_step  # Déplacement en latitude

        # Calcul de l'azimut et de la distance
        azimut = np.degrees(np.arctan2(delta_lon, delta_lat)) % 360
        distance = np.hypot(delta_lon, delta_lat)

        # Nouveau point géodésique
        lon_new, lat_new, _ = geod.fwd(self.lon, self.lat, azimut, distance)
        
        # Calcul de vitesse en W (axe z)
        if down:
            self.get_fall_speed_at_point()
        delta_altitude = (self.w_speed + w_wind) * self.time_step
        self.altitude = self.get_gph_at_point()
        altitude_new = self.altitude + delta_altitude

        # Mise à jour de l'altitude et de la pression
        self.altitude = altitude_new
        pressure_new = self.get_pressure_at_point(data)

        # Mise à jour du temps
        time_new = self.time_flying + self.time_step

        # Mise à jour des attributs du ballon
        self.pressure = pressure_new
        self.lon = lon_new
        self.lat = lat_new 
        self.time_flying = time_new

        # Ajout aux trajectoires
        self.trajectory['longitudes'].append(lon_new)
        self.trajectory['latitudes'].append(lat_new)
        self.trajectory['altitudes'].append(altitude_new)
        self.trajectory['times'].append(time_new)

    def get_surface_level_at_coords(self):
        """
        Renvoie l'altitude de la surface au point actuel.
        """
        coords = np.array([self.lat, self.lon])
        return self.surface_interpolator(coords)[0]
