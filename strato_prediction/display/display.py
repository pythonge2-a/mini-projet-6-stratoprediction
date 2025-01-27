#ploting
import matplotlib.pyplot as plt
import folium as fm
from folium.plugins import AntPath, MiniMap, MeasureControl, MousePosition,MarkerCluster
import http.server
import socketserver

def plot_trajectories_2d(trajectories, speeds, burst_altitudes):
    """
    Trace les trajectoires 2D des altitudes en fonction du temps pour différentes vitesses initiales et altitudes d'explosion.
    """
    plt.figure(num = '2D_Trajectories',figsize=(12, 8))
    colors = ["blue", "red", "green", "yellow", "purple", "orange", "cyan", "magenta"]
    color_count = len(colors)
    
    num_altitudes = len(burst_altitudes)
    num_speeds = len(speeds)
    
    for alt_idx in range(num_altitudes):
        for speed_idx in range(num_speeds):
            traj_idx = alt_idx * num_speeds + speed_idx
            trajectory = trajectories[traj_idx]
            color = colors[traj_idx % color_count]
            label = f'Vitesse = {speeds[speed_idx]} m/s, Alt. Explosion = {burst_altitudes[alt_idx]} m'
            plt.plot(
                trajectory['times'], 
                trajectory['altitudes'], 
                label=label, 
                color=color)
    
    plt.xlabel("Temps (s)")
    plt.ylabel("Altitude (m)")
    plt.title("Évolution des altitudes en fonction du temps")
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_trajectories_3d(trajectories, speeds, burst_altitudes):
    """
    Trace les trajectoires 3D des altitudes en fonction des couples (latitude, longitude) pour différentes vitesses initiales et altitudes d'explosion.
    """
    fig = plt.figure(num = '3D_Trajectories',figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    colors = ["blue", "red", "green", "yellow", "purple", "orange", "cyan", "magenta"]
    color_count = len(colors)
    
    # Parcourir les trajectoires en fonction des indices des altitudes et vitesses
    num_altitudes = len(burst_altitudes)
    num_speeds = len(speeds)
    
    for alt_idx in range(num_altitudes):
        for speed_idx in range(num_speeds):
            traj_idx = alt_idx * num_speeds + speed_idx
            trajectory = trajectories[traj_idx]
            color = colors[traj_idx % color_count]
            label = f'Vitesse = {speeds[speed_idx]} m/s, Alt. Explosion = {burst_altitudes[alt_idx]} m'
            ax.plot(
                trajectory['latitudes'], 
                trajectory['longitudes'], 
                trajectory['altitudes'], 
                label=label, 
                color=color)
    
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Hauteur (m)')
    ax.set_title('Trajectoires du ballon')
    ax.legend()
    plt.show()

def show_on_map(trajectories, speeds, burst_altitudes, init_lat, init_lon):
    """
    Trace les trajectoires 2D des altitudes en fonction des couples (latitude, longitude) pour différentes vitesses initiales et altitudes d'explosion sur
    une map interactive.
    """
    colors = ["blue", "red", "green", "yellow", "purple", "orange", "cyan", "magenta"]
    color_count = len(colors)
    carte = fm.Map(location=[init_lat, init_lon], zoom_start=10)
    
    num_altitudes = len(burst_altitudes)
    num_speeds = len(speeds)
    
    # Parcourir les combinaisons d'altitudes et de vitesses
    for alt_idx in range(num_altitudes):
        for speed_idx in range(num_speeds):
            traj_idx = alt_idx * num_speeds + speed_idx
            trajectory = trajectories[traj_idx]
            burst_altitude = burst_altitudes[alt_idx]
            speed = speeds[speed_idx]
            color = colors[traj_idx % color_count]
            
            latitudes = trajectory['latitudes']
            longitudes = trajectory['longitudes']
            altitudes = trajectory['altitudes']
            times = trajectory['times']
            marker_cluster = MarkerCluster().add_to(carte)
            
            # Trouver l'index où l'altitude dépasse burst_altitude
            threshold_index = next((j for j, alt in enumerate(altitudes) if alt > burst_altitude), len(altitudes))
            
            # Créer les coordonnées pour les deux segments
            coordinates_before = list(zip(latitudes[:threshold_index + 1], longitudes[:threshold_index + 1]))
            coordinates_after = list(zip(latitudes[threshold_index:], longitudes[threshold_index:]))
            
            # Ajout des marqueurs pour chaque point de la trajectoire
            for j, (lat, lon, alt, time) in enumerate(zip(latitudes, longitudes, altitudes, times)):
                popup_text = (
                    f"Lat: {round(lat, 8)}°\nLon: {round(lon, 8)}°\n"
                    f"Altitude: {round(alt, 1)}m\nTemps de vol: {time}s\n"
                    f"Vitesse d'ascension: {speed}m/s\nAltitude d'explosion: {burst_altitude}m"
                )
                # Personnalisation des icônes selon l'altitude
                if j == 0:  # Point de départ
                    icon_url = "Miscellaneous/startflag.png"
                    custom_icon = fm.CustomIcon(icon_url, icon_size=(120, 120))
                    fm.Marker(location=[lat, lon], popup=popup_text, icon=custom_icon).add_to(carte)
                elif alt >= burst_altitude:  # Point d'explosion
                    icon_url = "Miscellaneous/explosion.png"
                    custom_icon = fm.CustomIcon(icon_url, icon_size=(60, 60))
                    fm.Marker(location=[lat, lon], popup=popup_text, icon=custom_icon).add_to(carte)
                elif alt == altitudes[-1]:  # Point final
                    icon_url = "Miscellaneous/endflag.png"
                    custom_icon = fm.CustomIcon(icon_url, icon_size=(100, 100))
                    fm.Marker(location=[lat, lon], popup=popup_text, icon=custom_icon).add_to(carte)
                elif j % 5 == 0:  # Points intermédiaires
                    icon_url = "Miscellaneous/blackcircle.png"
                    custom_icon = fm.CustomIcon(icon_url, icon_size=(7, 7))
                    fm.Marker(location=[lat, lon], popup=popup_text, icon=custom_icon).add_to(marker_cluster)
            
            # Ajouter les segments avant et après burst_altitude
            if coordinates_before:
                AntPath(
                    locations=coordinates_before,
                    dash_array=[20, 30],
                    color=color,
                    pulse_color="white",
                    delay=500,
                ).add_to(carte)
            if coordinates_after:
                AntPath(
                    locations=coordinates_after,
                    dash_array=[20, 30],
                    color=color,
                    pulse_color="black",
                    delay=500,
                ).add_to(carte)
    
    # Ajout des plugins à la carte
    fm.plugins.Fullscreen(
        position="topright",
        title="Expand me",
        title_cancel="Exit me",
        force_separate_button=True,
    ).add_to(carte)
    MiniMap().add_to(carte)
    MeasureControl().add_to(carte)
    MousePosition().add_to(carte)
    
    # Sauvegarde de la carte dans un fichier HTML
    carte.save("carte_interactive.html")
    
    # Lancer un serveur HTTP local pour afficher la carte
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    
    print(f"Serving map at http://localhost:{PORT}/carte_interactive.html")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
