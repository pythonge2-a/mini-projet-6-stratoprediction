from strato_prediction.simulation import Balloon, get_bounding_square
from strato_prediction.GRIB import load_grib_data, download_grib_file
from strato_prediction.display import plot_trajectories_3d, show_on_map
from strato_prediction.CLI import args_retrieval

# # Définir les coordonnées de départ 
# lon_start = 6.1  # Longitude de départ
# lat_start = 47.1  # Latitude de départ
# pressure_start = 960.4 # Pression de départ
altitude_max = 32000
speeds = [4.5,5,5.5]
trajectories = []
pressure_start,lat_start,lon_start,date,cycle,offset_time = args_retrieval()

top_lat,btm_lat,right_lon,left_lon = get_bounding_square(lat_start,lon_start)
file_path = download_grib_file(date, cycle, offset_time, top_lat, left_lon, right_lon, btm_lat)
#file_path = "assets/d20241226c12o014bl43.22607977003234tl49.69392022996766ll1.6854083484919276rl11.074591651508072"
data = load_grib_data(file_path)
    
balloon = Balloon(data, lon_start, lat_start, pressure_start)
    
# Préparer les interpolateurs
balloon.prepare_interpolators(data)
for speed in speeds:
    balloon.ascension_speed = speed
    while balloon.altitude < altitude_max:
        balloon.get_next_point(data)
    balloon.ascension_speed = -speed
    surface = balloon.get_surface_level_at_coords()
    while balloon.altitude > surface:
        balloon.get_next_point(data) 
        surface = balloon.get_surface_level_at_coords()
    trajectories.append(balloon.trajectory)
    balloon.reset(lon_start, lat_start, pressure_start)

# Afficher le trajet sur carte géo
show_on_map(trajectories[0])

# Afficher les trajets en 3D
#plot_trajectories_3d(trajectories, speeds)