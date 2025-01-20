from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

import folium as fm
from folium.plugins import AntPath, Fullscreen, MiniMap, MeasureControl, MousePosition,MarkerCluster
import http.server
import socketserver

import numpy as np
#Permet de pouvoir afficher un nb illimité de ligne dans la console
np.set_printoptions(threshold=np.inf)

fig = plt.figure() 

# Définir l'axe 3D
ax = plt.axes(projection='3d')
# Définir les limites pour que les axes partent de 0
ax.set_xlim3d(0, 5)
ax.set_ylim3d(0, 5)
ax.set_zlim3d(0, 5)
# Données des points 
points = ((0.8439, 2.5321, 4.2142), (3.532, 2.1024, 0.2314), (1.4, 4.6, 0.2), (1, 2, 3))
# Ajout des deux points
for i in points:
    ax.scatter3D(i[0], i[1], i[2], color='red', label='point rouge')
# Ajout du segment entre les points
for i in range(len(points) - 1):  # Parcourt jusqu'à l'avant-dernier point
    x = [points[i][0], points[i + 1][0]]
    y = [points[i][1], points[i + 1][1]]
    z = [points[i][2], points[i + 1][2]]
    ax.plot3D(x, y, z, color='green', label=f'segment{i}')
# Ajout d'un titre et d'une légende
ax.set_title('Les petits poingues')
plt.show()
alt_max = 32000
# Données de trajectoire
trajectory = {
    'longitudes': [6.2000, 6.2200, 6.2400, 6.2600, 6.2800, 6.3000, 6.3079, 6.3100, 6.3150, 6.3200, 6.3250, 6.3300, 6.3350, 6.3400, 6.3450],
    'latitudes': [46.4000, 46.4200, 46.4400, 46.4600, 46.4800, 46.5000, 46.5091, 46.5100, 46.5150, 46.5200, 46.5250, 46.5300, 46.5350, 46.5400, 46.5450],
    'altitudes': [100, 1000, 5000, 10000, 15000, 20000, 32001, 25000, 20000, 15000, 10000, 5000, 2000, 1000, 100],
    'times': [0, 60.0, 120.0, 180.0, 240.0, 300.0, 360.0, 420.0, 480.0, 540.0, 600.0, 660.0, 720.0, 780.0, 840.0]
}


# Initialisation de la carte centrée sur la première position
latitudes = trajectory['latitudes']
longitudes = trajectory['longitudes']
altitudes = trajectory['altitudes']
carte = fm.Map(location=[latitudes[0], longitudes[0]], zoom_start=10)
marker_cluster = MarkerCluster().add_to(carte)
# Trouver l'index où l'altitude dépasse alt_max
threshold_index = next((i for i, alt in enumerate(altitudes) if alt > alt_max), len(altitudes))

# Créer les coordonnées pour les deux segments
coordinates_before = list(zip(latitudes[:threshold_index+1], longitudes[:threshold_index+1]))
coordinates_after = list(zip(latitudes[threshold_index:], longitudes[threshold_index:]))


# Ajout des marqueurs pour chaque point de la trajectoire
for i, (lat, lon, alt) in enumerate(zip(latitudes, longitudes, altitudes)):
    popup_text = f"Lat: {lat}, Lon: {lon}, Altitude: {alt} m"
    
    # Personnalisation des icônes selon l'altitude
    if i == 0:
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
    else:
        icon_url = "Miscellaneous/blackcircle.png"
        custom_icon = fm.CustomIcon(icon_url, icon_size=(7, 7))
        fm.Marker(
            location=[lat, lon],
            popup=popup_text,
            icon=custom_icon
        ).add_to(marker_cluster)

threshold_index = next((i for i, alt in enumerate(altitudes) if alt > alt_max), len(altitudes))


if coordinates_before:
    AntPath(
        locations=coordinates_before,
        dash_array=[20, 30],
        color="gray",  # Segment gris avant alt_max
        pulse_color="white",
        delay=500
    ).add_to(carte)

if coordinates_after:
    AntPath(
        locations=coordinates_after,
        dash_array=[20, 30],
        color="red",  # Segment rouge après alt_max
        pulse_color="white",
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