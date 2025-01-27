#Imports
from strato_prediction.CLI import console, args_retrieval
from strato_prediction.GRIB import download_grib_file, load_grib_data, download_next_grib_file, interpolate_data
from strato_prediction.simulation import Balloon, get_bounding_square
from scipy.interpolate import interp1d
from strato_prediction.display import plot_trajectories_2d, plot_trajectories_3d, show_on_map

import numpy as np
#Permet de pouvoir afficher un nb illimité de ligne dans la console
np.set_printoptions(threshold=np.inf)

def main():
    args = args_retrieval()

    geo_bounds = get_bounding_square(args['start_lat'], args['start_lon'])
    current_file_path, next_file_path = download_grib_file(args['date'],
                                                          args['cycle'],
                                                          args['offset_time'],
                                                          geo_bounds)
    reset_c_f_p, reset_n_f_p = current_file_path, next_file_path
    current_file_data, next_file_data, surface_data = load_grib_data(current_file_path, next_file_path)
    interpolated_data = interpolate_data(current_file_data, 
                                         next_file_data, 
                                         surface_data,
                                         args['time_m']%3600, 
                                         args['start_lat'], 
                                         args['start_lon'], 
                                         0)
    
    balloon = Balloon(interpolated_data, args['start_lon'], args['start_lat'], 0)
    balloon.pressure = balloon.get_pressure_at_point(interpolated_data)
    trajectories = []
    hour = 0

    for burst_altitude in args['burst_altitude']:
        print(burst_altitude)
        for ascent_rate in args['ascent_rate']:
            balloon.w_speed = ascent_rate
            ## ASCENT ##
            print('ASSSSSSSSCENT')
            while balloon.altitude < burst_altitude:
                if ((args['time_m']+balloon.time_flying) % 3600) == 0:
                    hour+=1
                    geo_bounds = get_bounding_square(balloon.lat,balloon.lon)
                    current_file_path = next_file_path
                    next_file_path = download_next_grib_file(args['date'],
                                                            args['cycle'],
                                                            args['offset_time']+hour,
                                                            geo_bounds)
                    current_file_data, next_file_data, surface_data = load_grib_data(current_file_path, next_file_path)
                if balloon.time_flying % 60 == 0:
                    interpolated_data = interpolate_data(current_file_data, 
                                                        next_file_data, 
                                                        surface_data,
                                                        (args['time_m']%3600)+balloon.time_flying, 
                                                        balloon.lat, 
                                                        balloon.lon, 
                                                        balloon.pressure, 
                                                        hour)
                    balloon.prepare_interpolators(interpolated_data)
                balloon.get_next_point(interpolated_data, 0)
            
            ## DESCENT ##
            print('DESSSSSSSSSSSSSSSCENT')
            surface = balloon.get_surface_level_at_coords()
            balloon.prepare_air_density_interpolators(interpolated_data)
            while balloon.altitude > surface:
                if ((args['time_m']+balloon.time_flying) % 3600) == 0:
                    hour+=1
                    geo_bounds = get_bounding_square(balloon.lat,balloon.lon)
                    current_file_path = next_file_path
                    next_file_path = download_next_grib_file(args['date'],
                                                            args['cycle'],
                                                            args['offset_time']+hour,
                                                            geo_bounds)
                    current_file_data, next_file_data, surface_data = load_grib_data(current_file_path, next_file_path)
                if balloon.time_flying % 60 == 0:
                    interpolated_data = interpolate_data(current_file_data, 
                                                        next_file_data, 
                                                        surface_data, 
                                                        (args['time_m']%3600)+balloon.time_flying, 
                                                        balloon.lat, 
                                                        balloon.lon, 
                                                        balloon.pressure, 
                                                        hour)
                    balloon.prepare_interpolators(interpolated_data)
                    balloon.prepare_air_density_interpolators(interpolated_data)
                balloon.get_next_point(interpolated_data, 1)
                surface = balloon.get_surface_level_at_coords()

            trajectories.append(balloon.trajectory)
            
            current_file_path, next_file_path = reset_c_f_p, reset_n_f_p
            current_file_data, next_file_data, surface_data = load_grib_data(current_file_path, next_file_path)
            print('HEYOOOOOOOO')
            interpolated_data = interpolate_data(current_file_data, 
                                            next_file_data, 
                                            surface_data,
                                            args['time_m']%3600, 
                                            args['start_lat'], 
                                            args['start_lon'], 
                                            0)
            balloon.reset(interpolated_data, args['start_lon'], args['start_lat'], 0)
            balloon.pressure = balloon.get_pressure_at_point(interpolated_data)
            hour = 0
    plot_trajectories_2d(trajectories, args['ascent_rate'], args['burst_altitude'])
    plot_trajectories_3d(trajectories, args['ascent_rate'], args['burst_altitude'])
    show_on_map(trajectories, args['ascent_rate'], args['burst_altitude'], args['start_lat'], args['start_lon'])        


if __name__ == "__main__":
    main()
