#ploting
import matplotlib.pyplot as plt
import folium as fm

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
    colors = ["blue", "red", "green"]
    for i, (trajectory, speed) in enumerate(zip(trajectories, speeds)):
        # Utiliser des couleurs différentes pour chaque vitesse
        ax.plot(trajectory['latitudes'], trajectory['longitudes'], trajectory['altitudes'], label=f'Vitesse ascensionnelle = {speed} m/s', color=colors[i])
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Hauteur (m)')
    ax.set_title('Trajectoire du ballon YIPEEE')
    ax.legend()
    plt.show()

def show_on_map(trajectory):
    # Création de la carte centrée sur un point
    carte = fm.Map(location=[30.0, 10.1], zoom_start=4)

    latitudes = trajectory['latitudes']
    longitudes = trajectory['longitudes']
    altitudes = trajectory['altitudes']

    # Ajout des points avec les pressions
    for lat, lon, pres in zip(latitudes, longitudes, altitudes): #change altitudes in pressures!!!!!!!!!!!
        popup_text = f"Lat: {lat}, Lon: {lon}, Pressure: {pres} hPa"
        fm.Marker(
            location=[lat, lon],
            popup=popup_text,
            icon=fm.Icon(color="blue", icon="circle", icon_size=(10, 10))
        ).add_to(carte)

    # Ajout de la ligne reliant les points
    coordinates = list(zip(latitudes, longitudes))  # Création d'une liste de tuples (lat, lon)
    fm.PolyLine(
        locations=coordinates,
        color="red",
        weight=2.5,  # Épaisseur de la ligne
        opacity=0.8
    ).add_to(carte)
    # Sauvegarde de la carte dans un fichier HTML
    carte.save("carte_interactive.html")
    print("Carte générée!")

# Valentin, tu peux aller regarder la gueule de trajectory dans simulation.simulation, dans la class Balloon