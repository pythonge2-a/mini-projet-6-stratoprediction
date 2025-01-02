# import strato_prediction.simulation.conversions
from .utils import Conversion

class Balloon:
    def __init__(self, start_lon, start_lat, pressure_start, ascendion_speed=5, time_step=60):
        self.pressure = pressure_start
        self.altitude = 0
        self.lat = start_lat
        self.lon = start_lon
        self.file_lat = start_lat
        self.file_lon = start_lon
        self.pressure_alt0 = 1000
        self.max_wind = 100
        self.z_speed = ascendion_speed
        self.u_speed_interp = None
        self.v_speed_interp = None
        self.temperature_alt0_interp = float
        self.time_step = time_step
        self.time_lauching = 0
        self.gp_height_interp = None
        self.trajectory = {
            "altitudes" : [],
            "latitudes" : [self.lat],
            "longitudes" : [self.lon]
        }


    #calculations
    def get_wind_at_point(self, interpolatorU, interpolatorV):
        self.u_speed_interp = interpolatorU((self.pressure, self.lat, self.lon))
        self.v_speed_interp = interpolatorV((self.pressure, self.lat, self.lon))
        # print(f"U:{self.u_speed_interp}")
        # print(f"V:{self.v_speed_interp}")

    def get_temperature_at_point(self, temp_interp):
        self.temperature_alt0_interp = temp_interp((self.pressure_alt0, self.lat, self.lon))
    
    def get_gp_height_at_point(self, gp_height_interp):
        self.gp_height_interp = gp_height_interp((self.pressure, self.lat, self.lon))
    
    def get_next_point(self):
        #print(f"t0interp:{self.temperature_alt0_interp}")
        conversions = Conversion()
        
        d_lat = self.v_speed_interp*self.time_step
        d_lon = self.u_speed_interp*self.time_step
        
        self.altitude = conversions.pressure_to_altitude(self.pressure, self.temperature_alt0_interp)
        
        
        d_lat_degrees = conversions.meters_to_latitude(d_lat)
        d_lon_degrees = conversions.meters_to_longitude(d_lon, self.lat)
        # print(f"d_lat_deg:{self.v_speed_interp}")
        # print(f"d_lon_deg:{self.u_speed_interp}")
        
        new_altitude = float(self.altitude + self.z_speed*self.time_step)
        new_latitude = float(self.lat + d_lat_degrees)
        new_longitude = float(self.lon+ d_lon_degrees)
        new_pressure = conversions.altitude_to_pressure(new_altitude, self.temperature_alt0_interp)
        
        self.altitude = new_altitude
        self.pressure = new_pressure
        self.lat = new_latitude
        self.lon = new_longitude
        self.trajectory["altitudes"].append(new_altitude)
        self.trajectory["latitudes"].append(new_latitude)
        self.trajectory["longitudes"].append(new_longitude)
        self.time_lauching = self.time_lauching + self.time_step
        #print(self.time_lauching)
        
    def get_next_pointGP(self):
        conversions = Conversion()
        
        d_lat = self.v_speed_interp*self.time_step
        d_lon = self.u_speed_interp*self.time_step
        
        
        d_lat_degrees = conversions.meters_to_latitude(d_lat)
        d_lon_degrees = conversions.meters_to_longitude(d_lon, self.lat)
        # print(f"d_lat_deg:{self.v_speed_interp}")
        # print(f"d_lon_deg:{self.u_speed_interp}")
        
        new_gp_height = float(self.altitude + self.z_speed*self.time_step)
        new_latitude = float(self.lat + d_lat_degrees)
        new_longitude = float(self.lon+ d_lon_degrees)
        self.pressure = conversions.altitude_to_pressure(new_gp_height, 288)
        
        self.altitude = new_gp_height
        self.lat = new_latitude
        self.lon = new_longitude
        self.trajectory["altitudes"].append(new_gp_height)
        self.trajectory["latitudes"].append(new_latitude)
        self.trajectory["longitudes"].append(new_longitude)
        self.time_lauching = self.time_lauching + self.time_step

    
    def get_bounding_square(self):
        conversions = Conversion()
        
        d_max = self.max_wind * 3600
        if (self.time_lauching % 3600) == 0:
            d_max_lat = conversions.meters_to_latitude(d_max)
            d_max_lon = conversions.meters_to_longitude(d_max,self.lat)
            top_lat = self.lat + d_max_lat 
            btm_lat = self.lat - d_max_lat
            right_lon = self.lon + d_max_lon 
            left_lon = self.lon - d_max_lon
        return top_lat,btm_lat,right_lon,left_lon
            
            
            
        
        