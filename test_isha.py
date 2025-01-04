from strato_prediction.simulation import Balloon
from strato_prediction.GRIB import load_grib_data
from strato_prediction.display import plot_trajectories_3d, show_on_map, plot_trajectory_2d

file_path = "assets/gfs.t06z.pgrb2.0p25.f024"
data = load_grib_data(file_path)
# Définir les coordonnées de départ 
lon_start = 7.1  # Longitude de départ
lat_start = 47.1  # Latitude de départ
pressure_start = 960.4 # Pression de départ
altitude_max = 32000
speeds = [5]
trajectories = []
balloon = Balloon(data, lon_start, lat_start, pressure_start)
# Préparer les interpolateurs
balloon.prepare_interpolators(data)
for speed in speeds:
    down = 0
    balloon.w_speed = speed
    while balloon.altitude < altitude_max:
        balloon.get_next_point(data, down)
    down = 1
    # balloon.time_step = .2
    surface = balloon.get_surface_level_at_coords()
    while balloon.altitude > surface:
        balloon.get_next_point(data, down) 
        surface = balloon.get_surface_level_at_coords()
    trajectories.append(balloon.trajectory)
    balloon.reset(lon_start, lat_start, pressure_start)

# Afficher le trajet sur carte géo
show_on_map(trajectories[0])

plot_trajectory_2d(trajectories[0])
# Afficher les trajets en 3D
plot_trajectories_3d(trajectories, speeds)