#Imports
from strato_prediction.CLI import args_retrieval
from strato_prediction.GRIB import download_grib_file, load_grib_data,download_next_grib_file
from strato_prediction.simulation import Balloon, get_bounding_square
from scipy.interpolate import interp1d
from strato_prediction.display import plot_trajectory_3d

import numpy as np
#Permet de pouvoir afficher un nb illimité de ligne dans la console
np.set_printoptions(threshold=np.inf)

def main():
    args = args_retrieval()
    top_lat,btm_lat,right_lon,left_lon = get_bounding_square(args['init_latitude'],args['init_longitude'])
    file_path_current,file_path_next = download_grib_file(args['date'],args['cycle'],args['offset_time'],top_lat,left_lon,right_lon,btm_lat)
    interpolated_data = load_grib_data(file_path_current,file_path_next,args['time']%3600,args['init_latitude'],args['init_longitude'])
    print(args['time']%3600)
    # interpolated_data = interpolate_data(data,args['time']%3600)
    # print(interpolated_data)
    balloon = Balloon(interpolated_data, args['init_longitude'], args['init_latitude'], args['start_pressure'])
    balloon.altitude = balloon.get_surface_level_at_coords()
    balloon.pressure = balloon.get_pressure_at_point(interpolated_data)
    trajectories = []
    i = 0
    for ascent_rate in args['ascent_rate']:
        balloon.w_speed = ascent_rate
        while balloon.altitude < args['burst_altitude']:
            if (args['time']+balloon.time_flying % 3600) == 0:
                i+=1
                top_lat,btm_lat,right_lon,left_lon = get_bounding_square(balloon.lat,balloon.lon)
                file_path_current = file_path_next
                print(args['offset_time']+i)
                file_path_next = download_next_grib_file(args['date'],args['cycle'],args['offset_time']+i,top_lat,left_lon,right_lon,btm_lat)
            interpolated_data = load_grib_data(file_path_current,file_path_next,(args['time']%3600)+balloon.time_flying,args['init_latitude'],args['init_longitude'],i)
            # interpolated_data = interpolate_data(data,(args['time']%3600)+balloon.time_flying)
            balloon.prepare_interpolators(interpolated_data)
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            balloon.get_next_point(interpolated_data, 0)
        surface = balloon.get_surface_level_at_coords()
        while balloon.altitude > surface:
            if (args['time']+balloon.time_flying % 3600) == 0:
                i+=1
                top_lat,btm_lat,right_lon,left_lon = get_bounding_square(balloon.lat,balloon.lon)
                file_path_current = file_path_next
                file_path_next = download_next_grib_file(args['date'],args['cycle'],args['offset_time']+i,top_lat,left_lon,right_lon,btm_lat)
            interpolated_data = load_grib_data(file_path_current,file_path_next,(args['time']%3600)+balloon.time_flying,args['init_latitude'],args['init_longitude'],i)
            # interpolated_data = interpolate_data(data,(args['time']%3600)+balloon.time_flying)
            balloon.prepare_interpolators(interpolated_data)
            balloon.get_next_point(interpolated_data, 1)
        trajectories.append(balloon.trajectory)
        balloon.reset(args['init_longitude'], args['init_latitude'], args['init_pressure'])
    plot_trajectory_3d(trajectories[0])            
            
        

if __name__ == "__main__":
    main()
