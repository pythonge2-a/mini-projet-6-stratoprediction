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
points = ((0.8439, 2.5321, 4.2142), (3.532, 2.1024, 0.2314))

# Ajout des deux points
ax.scatter3D(points[0][0], points[0][1], points[0][2], color='red', label='point rouge')
ax.scatter3D(points[1][0], points[1][1], points[1][2], color = 'blue', label='point bleu')

# Ajout du segment entre les deux points
x = [points[0][0], points[1][0]]  # Coordonnées x des deux points
y = [points[0][1], points[1][1]]  # Coordonnées y des deux points
z = [points[0][2], points[1][2]]  # Coordonnées z des deux points
ax.plot3D(x, y, z, color='green', label='segment0')

# Ajout d'un titre et d'une légende
ax.set_title('Les petits poingues')
plt.show()


