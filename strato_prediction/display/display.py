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

def afficher_resultats(trajectory,data):
    # step = 2
    fig = plt.figure()
    ax = fig.add_subplot(111,projection = '3d')
    ax.plot(trajectory["latitudes"], trajectory["longitudes"], trajectory["altitudes"], color='r')
    
    # # Récupérer les données des grilles
    # latitudes = trajectory["latitudes"]
    # longitudes = trajectory["longitudes"]
    # altitudes = trajectory["altitudes"]

    # # Parcourir chaque niveau d'altitude pour afficher les vecteurs
    # for alt_index, altitude in enumerate(altitudes):
    #     # Échantillonnage pour alléger la visualisation
    #     lat_sample = latitudes[step]
    #     lon_sample = longitudes[step]
    #     U_sample = data["u_wind"][alt_index, ::step, ::step]
    #     V_sample = data["v_wind"][alt_index, ::step, ::step]

    #     # Créer des grilles de coordonnées
    #     lat_grid, lon_grid = np.meshgrid(lat_sample, lon_sample, indexing='ij')

    #     # Tracer les vecteurs sur le plan correspondant à l'altitude
    #     ax.quiver(lat_grid, lon_grid, altitude, U_sample, V_sample, np.zeros_like(U_sample),
    #               length=0.1, normalize=True, color='blue')
    
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
    
    