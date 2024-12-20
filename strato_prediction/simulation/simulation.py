# import strato_prediction.simulation.conversions
from .utils import Conversion

class Balloon:
    def __init__(self, start_lon, start_lat, pressure_start, ascendion_speed=5, time_step=60):
        self.pressure = pressure_start
        self.lat = start_lat
        self.lon = start_lon
        self.pressure_alt0 = 1000
        self.z_speed = ascendion_speed
        self.u_speed_interp = None
        self.v_speed_interp = None
        self.temperature_alt0_interp = None
        self.time_step = time_step
        self.trajectory = {
            "altitudes" : [],
            "latitudes" : [],
            "longitudes" : []
        }

    #calculations
    def get_wind_at_point(self, interpolatorU, interpolatorV):
        self.u_speed_interp = interpolatorU((self.pressure, self.lat, self.lon))
        self.v_speed_interp = interpolatorV((self.pressure, self.lat, self.lon))

    def get_temperature_at_point(self, temp_interp):
        self.temperature_alt0_interp = temp_interp((self.pressure_alt0, self.lat, self.lon))
    
    def get_next_point(self):
        conversions = Conversion()
        
        d_lat = self.u_speed_interp*self.time_step
        d_lon = self.v_speed_interp*self.time_step
        
        altitude = conversions.pressure_to_altitude(self.pressure, self.temperature_alt0_interp)
        d_lat_degrees = conversions.meters_to_latitude(d_lat)
        d_lon_degrees = conversions.meters_to_longitude(d_lon)
        
        new_altitude = float(altitude + self.z_speed*self.time_step)
        new_latitude = float(self.lat + d_lat_degrees)
        new_longitude = float(self.lon+ d_lon_degrees)
        
        self.trajectory["altitudes"].append(new_altitude)
        self.trajectory["latitudes"].append(new_latitude)
        self.trajectory["longitudes"].append(new_longitude)
        
        
