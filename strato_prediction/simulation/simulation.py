# import strato_prediction.simulation.conversions
from .utils import Conversion

class Balloon:
    def __init__(self, start_lon, start_lat, pressure_start, ascendion_speed=5, time_step=60):
        self.pressure = pressure_start
        self.altitude = 0
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
        # print(f"U:{self.u_speed_interp}")
        # print(f"V:{self.v_speed_interp}")

    def get_temperature_at_point(self, temp_interp):
        self.temperature_alt0_interp = temp_interp((self.pressure_alt0, self.lat, self.lon))
    
    def get_next_point(self):
        conversions = Conversion()
        
        d_lat = self.v_speed_interp*self.time_step
        d_lon = self.u_speed_interp*self.time_step
        
        self.altitude = conversions.pressure_to_altitude(self.pressure, self.temperature_alt0_interp)
        d_lat_degrees = conversions.meters_to_latitude(d_lat)
        d_lon_degrees = conversions.meters_to_longitude(d_lon, self.lat)
        print(f"d_lat_deg:{self.v_speed_interp}")
        print(f"d_lon_deg:{self.u_speed_interp}")
        
        new_altitude = float(self.altitude + self.z_speed*self.time_step)
        new_latitude = float(self.lat + d_lat_degrees)
        new_longitude = float(self.lon+ d_lon_degrees)
        new_pressure = conversions.altitude_to_pressure(new_altitude, self.temperature_alt0_interp)
        
        # if (new_latitude) > 48:
        #     self.lat = 48
        # else:
        #     self.lat = new_latitude
        # if (new_latitude) < 45:
        #     self.lat = 45
        # else:
        #     self.lat = new_latitude
            
        # if (new_longitude) > 11:
        #     self.lon = 11
        # else:
        #     self.lon = new_longitude
        # if (new_longitude) < 5:
        #     self.lon = 5
        # else:
        #     self.lon = new_longitude
        
        # if new_pressure < 1:
        #     self.altitude = 1
        # else:
        #     self.altitude = new_altitude
        # if new_pressure > 1000:
        #     self.altitude = 1000
        # else:
        #     self.altitude = new_altitude
        
        self.altitude = new_altitude
        self.pressure = new_pressure
        self.lat = new_latitude
        self.lon = new_longitude
        self.trajectory["altitudes"].append(new_altitude)
        self.trajectory["latitudes"].append(new_latitude)
        self.trajectory["longitudes"].append(new_longitude)
