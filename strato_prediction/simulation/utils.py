import numpy as np

def get_bounding_square(lat,lon):
    """
    Crée un carré de coordonnées pour limiter la taille des fichiers téléchargés
    """
    d_max = 3
    geo_bounds = {
        'top_lat': round(lat,1) + d_max,
        'btm_lat' :round(lat,1) - d_max,
        'right_lon' : round(lon,1) + d_max,
        'left_lon' : round(lon,1) - d_max
    }
    print(geo_bounds)
    return geo_bounds

def calculate_air_density(pressure, temp, humidity):
    """
    Retourne la dentisté de l'air en fonction de la pression, la température et l'humidité.
    Attention: pressure est en hPa
    """
    # Constantes
    R_d = 287.05  # Constante spécifique pour l'air sec (J/(kg·K))
    R_v = 461.5   # Constante spécifique pour la vapeur d'eau (J/(kg·K))

    # Calcul de la pression de vapeur saturante (en Pa) par la formule de Tetens
    e_s = 6.112 * np.exp((17.67 * (temp - 273.15)) / ((temp - 273.15) + 243.5)) * 100  # e_s en Pa
    
    # Pression partielle de la vapeur d'eau
    P_v = humidity * e_s  # P_v en Pa
    
    # Pression partielle de l'air sec
    P_d = pressure*100 - P_v  # P_d en Pa
    
    # Densité de l'air humide
    rho = (P_d / (R_d * temp)) + (P_v / (R_v * temp))
    return rho