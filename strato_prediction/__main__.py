#Imports
#from strato_prediction.CLI import console, args_retrieval
from strato_prediction.GRIB import download_grib_file, load_grib_data, download_next_grib_file, interpolate_data
from strato_prediction.simulation import Balloon, get_bounding_square
from strato_prediction.display import plot_trajectories_2d, plot_trajectories_3d, show_on_map
import time
import numpy as np
#Permet de pouvoir afficher un nb illimité de ligne dans la console
np.set_printoptions(threshold=np.inf)

def main():
    args = {
        'start_pressure': 0,
        'start_altitude':0,
        'start_lat': 47.82980,
        'start_lon': 10.88130,
        'ascent_rate':[5],
        'burst_pression':0,
        'burst_altitude':[30000],
        'date': "20250127",
        'time_m':60428,
        'cycle': "12",
        'offset_time': 4,
    }

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
    #balloon.pressure = balloon.get_pressure_at_point(interpolated_data)
    trajectories = []
    hour = 0
    seconds = args['time_m']%3600
    current_time = seconds + balloon.time_flying
    previous_time = current_time
    start_time = time.time()
    for burst_altitude in args['burst_altitude']:
        for ascent_rate in args['ascent_rate']:
            balloon.w_speed = ascent_rate
            ## ASCENT ##
            print('ASSSSSSSSCENT')
            while balloon.altitude < burst_altitude:
                current_time = seconds + balloon.time_flying
                if (previous_time // 3600 != current_time // 3600):
                    hour+=1
                    geo_bounds = get_bounding_square(balloon.lat,balloon.lon)
                    current_file_path = next_file_path
                    next_file_path = download_next_grib_file(args['date'],
                                                            args['cycle'],
                                                            args['offset_time']+hour,
                                                            geo_bounds)
                    current_file_data, next_file_data, surface_data = load_grib_data(current_file_path, next_file_path)
                if (previous_time // 1800 != current_time // 1800):
                    interpolated_data = interpolate_data(current_file_data, 
                                                        next_file_data, 
                                                        surface_data,
                                                        current_time, 
                                                        balloon.lat, 
                                                        balloon.lon, 
                                                        balloon.pressure, 
                                                        hour)
                    balloon.prepare_interpolators(interpolated_data)
                balloon.get_next_point(interpolated_data, 0)
                previous_time = current_time

            ## DESCENT ##
            print('DESSSSSSSSSSSSSSSCENT')
            surface = balloon.get_surface_level_at_coords()
            balloon.prepare_air_density_interpolators(interpolated_data)
            while balloon.altitude > surface:
                current_time = seconds + balloon.time_flying
                if (previous_time // 3600 != current_time // 3600):
                    hour+=1
                    geo_bounds = get_bounding_square(balloon.lat,balloon.lon)
                    current_file_path = next_file_path
                    next_file_path = download_next_grib_file(args['date'],
                                                            args['cycle'],
                                                            args['offset_time']+hour,
                                                            geo_bounds)
                    current_file_data, next_file_data, surface_data = load_grib_data(current_file_path, next_file_path)
                if (previous_time // 1800 != current_time // 1800):
                    interpolated_data = interpolate_data(current_file_data, 
                                                        next_file_data, 
                                                        surface_data, 
                                                        current_time, 
                                                        balloon.lat, 
                                                        balloon.lon, 
                                                        balloon.pressure, 
                                                        hour)
                    balloon.prepare_interpolators(interpolated_data)
                    balloon.prepare_air_density_interpolators(interpolated_data)
                balloon.get_next_point(interpolated_data, 1)
                surface = balloon.get_surface_level_at_coords()
                previous_time = current_time


            trajectories.append(balloon.trajectory)
            
            current_file_path, next_file_path = reset_c_f_p, reset_n_f_p
            current_file_data, next_file_data, surface_data = load_grib_data(current_file_path, next_file_path)
            print('HEYOOOOOOOO')
            interpolated_data = interpolate_data(current_file_data, 
                                            next_file_data, 
                                            surface_data,
                                            seconds, 
                                            args['start_lat'], 
                                            args['start_lon'], 
                                            0,
                                            0)
            balloon.reset(interpolated_data, args['start_lon'], args['start_lat'], 0)
            balloon.pressure = balloon.get_pressure_at_point(interpolated_data)
            hour = 0
            current_time = seconds + balloon.time_flying
            previous_time = current_time
    print("--- %s seconds ---" % (time.time() - start_time))
    plot_trajectories_2d(trajectories, args['ascent_rate'], args['burst_altitude'])
    plot_trajectories_3d(trajectories, args['ascent_rate'], args['burst_altitude'])
    show_on_map(trajectories, args['ascent_rate'], args['burst_altitude'], args['start_lat'], args['start_lon'])        


if __name__ == "__main__":
    main()
