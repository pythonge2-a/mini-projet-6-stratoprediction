#ploting
import matplotlib.pyplot as plt
import folium as fm
from folium.plugins import AntPath, MiniMap, MeasureControl, MousePosition,MarkerCluster
import http.server
import socketserver

def plot_trajectory_2d(trajectory): 
    plt.figure(figsize=(10, 6))
    plt.plot(trajectory['times'], trajectory['altitudes'], label="Altitude", color="b")
    plt.xlabel("Temps (s)")
    plt.ylabel("Altitude (m)")
    plt.title("Évolution de l'altitude en fonction du temps")
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_trajectory_3d(trajectory):
    # Tracer la trajectoire en 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(trajectory['latitudes'], trajectory['longitudes'], trajectory['altitudes'], label='Trajectoire', color='b')
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Hauteur (m)')
    ax.set_title('Trajectoire du ballon YIPEEE')
    plt.show()

def plot_trajectories_3d(trajectories, speeds):
    # Tracer les trajectoires en 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colors = ["blue", "red", "green", "yellow", "purple"]
    for i, (trajectory, speed) in enumerate(zip(trajectories, speeds)):
        # Utiliser des couleurs différentes pour chaque vitesse
        ax.plot(trajectory['latitudes'], trajectory['longitudes'], trajectory['altitudes'], label=f'Vitesse ascensionnelle = {speed} m/s', color=colors[i])
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Hauteur (m)')
    ax.set_title('Trajectoire du ballon YIPEEE')
    ax.legend()
    plt.show()

def show_on_map(trajectories,speeds, alt_max, init_lat, init_lon):
    colors = ["blue", "red", "green", "yellow", "purple"]
    carte = fm.Map(location=[init_lat, init_lon], zoom_start=10)
    for i, (trajectory, speed) in enumerate(zip(trajectories, speeds)):
        # Création de la carte centrée sur un point
        latitudes = trajectory['latitudes']
        longitudes = trajectory['longitudes']
        altitudes = trajectory['altitudes']
        times = trajectory['times']
        marker_cluster = MarkerCluster().add_to(carte)
        # Trouver l'index où l'altitude dépasse alt_max
        threshold_index = next((i for i, alt in enumerate(altitudes) if alt > alt_max), len(altitudes))
        # Créer les coordonnées pour les deux segments
        coordinates_before = list(zip(latitudes[:threshold_index+1], longitudes[:threshold_index+1]))
        coordinates_after = list(zip(latitudes[threshold_index:], longitudes[threshold_index:]))
        # Ajout des marqueurs pour chaque point de la trajectoire
        for j, (lat, lon, alt, time) in enumerate(zip(latitudes, longitudes, altitudes, times)):
            popup_text = f"Lat: {round(lat,8)}°\nLon: {round(lon,8)}°\nAltitude: {round(alt,1)}m\nTemps de vol: {time}s\nVitesse d'ascension: {speed}m/s\nAltitude d'explosion:{alt_max}m"
            # Personnalisation des icônes selon l'altitude
            if j == 0:
                icon_url = "Miscellaneous/startflag.png"
                custom_icon = fm.CustomIcon(icon_url, icon_size=(120,120))
                fm.Marker(
                    location=[lat, lon],
                    popup=popup_text,
                    icon=custom_icon
                ).add_to(carte)
            elif alt >= alt_max:
                icon_url = "Miscellaneous/explosion.png"
                custom_icon = fm.CustomIcon(icon_url, icon_size=(60, 60))
                fm.Marker(
                    location=[lat, lon],
                    popup=popup_text,
                    icon=custom_icon
                ).add_to(carte)
            elif alt == trajectory['altitudes'][-1]:
                icon_url = "Miscellaneous/endflag.png"
                custom_icon = fm.CustomIcon(icon_url, icon_size=(100, 100))
                fm.Marker(
                    location=[lat, lon],
                    popup=popup_text,
                    icon=custom_icon
                ).add_to(carte)
            elif j%5 == 0:
                icon_url = "Miscellaneous/blackcircle.png"
                custom_icon = fm.CustomIcon(icon_url, icon_size=(7, 7))
                fm.Marker(
                    location=[lat, lon],
                    popup=popup_text,
                    icon=custom_icon
                ).add_to(marker_cluster)
        if coordinates_before:
            AntPath(
                locations=coordinates_before,
                dash_array=[20, 30],
                color=colors[i],  # Segment gris avant alt_max
                pulse_color="white",
                delay=500
            ).add_to(carte)
        if coordinates_after:
            AntPath(
                locations=coordinates_after,
                dash_array=[20, 30],
                color=colors[i],  # Segment rouge après alt_max
                pulse_color="black",
                delay=500
            ).add_to(carte)

    # Ajout des plugins à la carte
    fm.plugins.Fullscreen(
        position="topright",
        title="Expand me",
        title_cancel="Exit me",
        force_separate_button=True
    ).add_to(carte)

    MiniMap().add_to(carte)
    MeasureControl().add_to(carte)
    MousePosition().add_to(carte)

    # Sauvegarde de la carte dans un fichier HTML
    carte.save("carte_interactive.html")

    # Lancement du serveur HTTP local pour afficher la carte
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler

    print(f"Serving map at http://localhost:{PORT}/carte_interactive.html")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
    



# Valentin, tu peux aller regarder la gueule de trajectory dans simulation.simulation, dans la class Balloon