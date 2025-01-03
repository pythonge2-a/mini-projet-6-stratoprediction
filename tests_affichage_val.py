from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

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


