#Imports
from strato_prediction.CLI import args_retrieval
from strato_prediction.GRIB import download_grib_file, load_grib_data, download_next_grib_file, interpolate_data
from strato_prediction.simulation import Balloon, get_bounding_square
from scipy.interpolate import interp1d
from strato_prediction.display import plot_trajectory_3d

import numpy as np
#Permet de pouvoir afficher un nb illimité de ligne dans la console
np.set_printoptions(threshold=np.inf)

def main():
    args = args_retrieval()
    geo_bounds = get_bounding_square(args['init_latitude'], args['init_longitude'])
    current_file_path,next_file_path = download_grib_file(args['date'],
                                                          args['cycle'],
                                                          args['offset_time'],
                                                          geo_bounds)
    current_file_data, next_file_data, surface_data = load_grib_data(current_file_path, next_file_path)
    interpolated_data = interpolate_data(current_file_data, 
                                         next_file_data, 
                                         surface_data,
                                         args['time']%3600, 
                                         args['init_latitude'], 
                                         args['init_longitude'], 
                                         args['start_pressure'])
    
    balloon = Balloon(interpolated_data, args['init_longitude'], args['init_latitude'], args['start_pressure'])
    balloon.altitude = balloon.get_surface_level_at_coords()
    balloon.pressure = balloon.get_pressure_at_point(interpolated_data)

    trajectories = []
    hour = 0

    for ascent_rate in args['ascent_rate']:
        balloon.w_speed = ascent_rate
        ## ASCENT ##
        while balloon.altitude < args['burst_altitude']:
            if (args['time']+balloon.time_flying % 3600) == 0:
                hour+=1
                geo_bounds = get_bounding_square(balloon.lat,balloon.lon)
                current_file_path = next_file_path
                next_file_path = download_next_grib_file(args['date'],
                                                         args['cycle'],
                                                         args['offset_time']+hour,
                                                         geo_bounds)
                current_file_data, next_file_data, surface_data = load_grib_data(current_file_path, next_file_path)
            interpolated_data = interpolate_data(current_file_data, 
                                                 next_file_data, 
                                                 surface_data,
                                                 (args['time']%3600)+balloon.time_flying, 
                                                 balloon.lat, 
                                                 balloon.lon, 
                                                 balloon.pressure, 
                                                 hour)
            balloon.prepare_interpolators(interpolated_data)
            balloon.get_next_point(interpolated_data, 0)
            print('YES')
        
        ## DESCENT ##
        surface = balloon.get_surface_level_at_coords()
        while balloon.altitude > surface:
            if (args['time']+balloon.time_flying % 3600) == 0:
                hour+=1
                geo_bounds = get_bounding_square(balloon.lat,balloon.lon)
                current_file_path = next_file_path
                next_file_path = download_next_grib_file(args['date'],
                                                         args['cycle'],
                                                         args['offset_time']+hour,
                                                         geo_bounds)
                current_file_data, next_file_data, surface_data = load_grib_data(current_file_path, next_file_path)
            interpolated_data = interpolate_data(current_file_data, 
                                                 next_file_data, 
                                                 surface_data, 
                                                 (args['time']%3600)+balloon.time_flying, 
                                                 balloon.lat, 
                                                 balloon.lon, 
                                                 balloon.pressure, 
                                                 hour)
            balloon.prepare_interpolators(interpolated_data)
            balloon.get_next_point(interpolated_data, 1)
            balloon.get_surface_level_at_coords()
        trajectories.append(balloon.trajectory)
        balloon.reset(args['init_longitude'], args['init_latitude'], args['start_pressure'])
    plot_trajectory_3d(trajectories[0])            
            
        

if __name__ == "__main__":
    main()
