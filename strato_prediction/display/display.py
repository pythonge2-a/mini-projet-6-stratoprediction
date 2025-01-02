import matplotlib 
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import folium

def afficher_resultats(trajectory,trajectoryGP,data):
    # step = 2
    fig = plt.figure()
    ax = fig.add_subplot(111,projection = '3d')
    ax.plot(trajectory["latitudes"], trajectory["longitudes"], trajectory["altitudes"], color='b',label='Trajectory')
    ax.plot(trajectoryGP["latitudes"], trajectoryGP["longitudes"], trajectoryGP["altitudes"], color='r',label='Trajectory GP')
    #print(trajectory)
    print(trajectory)
    ax.set_xlabel('LAT')
    ax.set_ylabel('LON')
    ax.set_zlabel('ALT')
    ax.set_title('Graphique 3D avec des coordonnées')
    # Afficher le graphique
    plt.show()
    
    # map_route = folium.Map(location=[trajectory["latitudes"][0], trajectory["longitudes"][0]], zoom_start=10)

    # # Add first trajectory
    # coordinates = list(zip(trajectory["latitudes"], trajectory["longitudes"]))
    # folium.PolyLine(
    #     locations=coordinates,
    #     color="blue",
    #     weight=5,
    #     opacity=0.8,
    #     tooltip="Trajet"
    # ).add_to(map_route)

    # print(f"lat:{trajectoryGP["latitudes"]},lon:{trajectoryGP["longitudes"]}alt:{trajectory["altitudes"]}")
    # # Add second trajectory (GP)
    # coordinates_gp = list(zip(trajectoryGP["latitudes"], trajectoryGP["longitudes"]))
    # folium.PolyLine(
    #     locations=coordinates_gp,
    #     color="red",
    #     weight=5,
    #     opacity=0.8,
    #     tooltip="Trajet GP"
    # ).add_to(map_route)

    # # Add markers for both trajectories
    # for lat, lon, alt in zip(trajectory["latitudes"], trajectory["longitudes"], trajectory["altitudes"]):
    #     folium.Marker(
    #         location=[lat, lon],
    #         popup=f"Altitude: {alt} m\n, Latitude: {lat}°\n, Longitude {lon}°\n",
    #         tooltip="Point"
    #     ).add_to(map_route)

    # map_route.save("trajet_map.html")
    
    