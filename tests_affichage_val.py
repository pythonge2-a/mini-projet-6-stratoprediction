from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure() 

if(0):
    # syntax for 3-D projection
    ax = plt.axes(projection ='3d')
    
    # defining all 3 axis
    z = np.linspace(0, 1, 100)
    x = z * np.sin(25 * z)
    y = z * np.cos(25 * z)
    
    # plotting
    ax.plot3D(x, y, z, 'green')
    ax.set_title('spirale du swagg')
    plt.show()

if(1):
    # syntax for 3-D projection
    ax = plt.axes(projection='3d')

    # Définir les limites pour que les axes partent de 0
    ax.set_xlim3d(0, 5)
    ax.set_ylim3d(0, 5)
    ax.set_zlim3d(0, 5)

    # Ajout du point (1, 2, 3)
    ax.scatter3D(1, 2, 3, color='red', label='Point (1, 2, 3)')

    # Ajout d'un titre et d'une légende
    ax.set_title('Petit Poingue')
    plt.show()


