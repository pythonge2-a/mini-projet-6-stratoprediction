class Balloon:
    def __init__(self, lon_start, lat_start, pressure_start, ascendion_speed=5, time_step=60):
        self.lon = lon_start
        self.lat = lat_start
        self.pressure = pressure_start
        self.z_speed = ascendion_speed
        self.u_speed_interp = None
        self.v_speed_interp = None
        self.time_step = time_step
        self.trajectory = None #list coord 3d (lon, lat, pres/alt)

    #calculations
    def prepare_wind_interpolators(self, data):
        pass
    def get_wind_at_point(self, data):
        pass
    def get_next_point(self, data):
        pass