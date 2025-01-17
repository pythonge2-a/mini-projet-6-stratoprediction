from strato_prediction.simulation import Balloon
from strato_prediction.GRIB import load_grib_data
from strato_prediction.display import plot_trajectory_3d, show_on_map
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import message_dialog, button_dialog, input_dialog, radiolist_dialog
from datetime import datetime, timedelta


def  is_valid_datetime_within_range(launch_date_str, current_datetime):
    """
    Valide que la date et l'heure de lancement sont au plus dans 10 jours
    par rapport à la date et heure actuelles.
    """
    try:
        # Convertir l'entrée utilisateur (format HH:MM:SS) en datetime
        launch_time = datetime.strptime(launch_date_str, "%Y-%m-%d %H:%M:%S")
        # Calculer la limite de 10 jours
        max_launch_time = current_datetime + timedelta(days=10)
        # Valider la contrainte
        return current_datetime <= launch_time <= max_launch_time
    except ValueError:
        return False
    
# Obtenir la date et l'heure actuelles
current_datetime = datetime.now()

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    
def is_valid_time(time_str):
    """Valide si une chaîne est au format HH:MM:SS."""
    try:
        hours, minutes, seconds = map(int, time_str.split(":"))
        return 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60
    except ValueError:
        return False  
    

    
while True:
    result = radiolist_dialog(
    title="Lancement simulateur",
    text="Quelle type de simulation voulez-vous lancer?",
    values=[
        ("sim1", "Trajet simple"),
        ("sim2", "Distance point d'attérissage minimisée"),
        ("sim3", "Aucune, fin de simulation")
    ] 
    ).run()
    if result == "sim2":
        print("Maximisation pas prête.")
        break
    elif result == "sim1":

        lon_str = input_dialog(
        title="Coordonnées initiales",
        text="Entrez la longitude au format float.",
        ).run()
        print(f"'{lon_str}'")
        while(not is_float(lon_str)) :
            print(f"'{lon_str}'")
            lon_str = input_dialog(
            title="Coordonnées initiales",
            text="Mauvais input. Entrez la longitude au format float.",
            ).run()

        lat_str = input_dialog(
        title="Coordonnées initiales",
        text="Entrez la latitude au format float.",
        ).run()
        while(not is_float(lat_str)) :
            lat_str = input_dialog(
            title="Coordonnées initiales",
            text="Mauvais input. Entrez la latitude au format float.",
            ).run()

        pressure_str = input_dialog(
        title="Coordonnées initiales",
        text="Entrez la pression au format float.",
        ).run()
        print(f"'{pressure_str}'")
        while(not is_float(pressure_str)) :
            pressure_str = input_dialog(
            title="Coordonnées initiales",
            text="Mauvais input. Entrez la pression au format float.",
            ).run()

        drag_coefficient = input_dialog(
        title="Coefficient de traînée",
        text="Entrez le coefficient de traînée au format float.",
        ).run()
        while(not is_float(drag_coefficient)) :
            pressure_str = input_dialog(
            title="Coordonnées initiales",
            text="Mauvais input. Entrez le coefficient de traînée au format float.",
            ).run()

        masse_str = input_dialog(
        title="Masse",
        text="Entrez la masse en grammes au format float.",
        ).run()
        while(not is_float(masse_str)) :
            masse_str = input_dialog(
            title="Masse",
            text="Mauvais input. Entrez la masse au format float.",
            ).run()

        launch_time_str = input_dialog(
            title="Heure de départ",
            text="Entrez l'heure de départ (YYYY-MM-DD HH:MM:SS, max. dans 10 jours) :",
        ).run()
        while not is_valid_datetime_within_range(launch_time_str, current_datetime):
            launch_time_str = input_dialog(
                title="Erreur",
                text="Date invalide. Entrez une heure de départ correcte (dans les 10 jours) YYYY-MM-DD HH:MM:SS :",
            ).run()


        lon_start = float(lon_str)
        lat_start = float(lat_str)
        pressure_start = float(pressure_str)
        drag_coefficient = float(drag_coefficient)
        masse = float(masse_str)



        message_dialog(
            title="Résumé de la simulation",
            text=(
                f"Simulation configurée avec :\n"
                f"Longitude : {lon_start},\n"
                f"Latitude : {lat_start},\n"
                f"Pression : {pressure_start},\n"
                f"Coefficient de traînée : {masse},\n"
                f"Masse : {drag_coefficient},\n"
                f"Heure de départ : {launch_time_str},\n"
            
            )
        ).run()
    else:
        break


