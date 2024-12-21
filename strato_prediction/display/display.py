# #ploting
# def plot_trajectory_2d(trajectory):
#     pass
# def plot_trajectory_3d(trajectory):
#     pass
# def show_on_map(trajectory):
#     pass



import matplotlib 
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import folium

def afficher_resultats(trajectory):
    fig = plt.figure()
    ax = fig.add_subplot(111,projection = '3d')
    ax.plot(trajectory["latitudes"], trajectory["longitudes"], trajectory["altitudes"], color='r')
    ax.set_xlabel('LAT')
    ax.set_ylabel('LON')
    ax.set_zlabel('ALT')
    ax.set_title('Graphique 3D avec des coordonnées')
    # Afficher le graphique
    plt.show()
    
    map_route = folium.Map(location=[trajectory["latitudes"][0], trajectory["longitudes"][0]], zoom_start=10)
    
    # Ajouter le trajet à la carte
    coordinates = list(zip(trajectory["latitudes"], trajectory["longitudes"]))
    folium.PolyLine(
        locations=coordinates,
        color="blue",
        weight=5,
        opacity=0.8,
        tooltip="Trajet"
    ).add_to(map_route)

    # Ajouter des marqueurs pour chaque point
    for lat, lon, alt in zip(trajectory["latitudes"], trajectory["longitudes"], trajectory["altitudes"]):
        folium.Marker(
            location=[lat, lon],
            popup=f"Altitude: {alt} m",
            tooltip="Point"
        ).add_to(map_route)

    # Sauvegarder et afficher la carte
    map_route.save("trajet_map.html")
    
    