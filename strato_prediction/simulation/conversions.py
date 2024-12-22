from scipy.interpolate import RegularGridInterpolator
from metpy.calc import pressure_to_height_std, height_to_pressure_std
from metpy.units import units

def prepare_wind_interpolators(data):
    """Prépare les interpolateurs pour U et V"""
    u_interpolator = RegularGridInterpolator(
        (data['pressure'], data['latitude'], data['longitude']),
        data['u_wind'],
        method='cubic',
        bounds_error=False,
        fill_value=None
    )
    
    v_interpolator = RegularGridInterpolator(
        (data['pressure'], data['latitude'], data['longitude']),
        data['v_wind'],
        method='cubic',
        bounds_error=False,
        fill_value=None
    )
    return u_interpolator, v_interpolator

def pressure_to_altitude(pressure):
    altitude = pressure_to_height_std(pressure*units.hPa)
    return altitude.magnitude*1000

def altitude_to_pressure(altitude):
    pressure = height_to_pressure_std(altitude*units.meter)
    return pressure.magnitude

def latitude_to_meters(lat):
    pass

def longitude_to_meters(lon):
    pass

def meters_to_latitude(d_lat):
    pass

def meters_to_longitude(d_lon):
    pass