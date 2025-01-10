from strato_prediction.simulation import Balloon
from strato_prediction.GRIB import load_grib_data
from strato_prediction.display import plot_trajectory_3d, show_on_map
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import message_dialog, button_dialog, input_dialog, radiolist_dialog

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
            text="Mauvaise input. Entrez la longitude au format float.",
            ).run()
        lat_str = input_dialog(
        title="Coordonnées initiales",
        text="Entrez la latitude au format float.",
        ).run()
        while(not is_float(lat_str)) :
            lat_str = input_dialog(
            title="Coordonnées initiales",
            text="Mauvaise input. Entrez la latitude au format float.",
            ).run()
        pressure_str = input_dialog(
        title="Coordonnées initiales",
        text="Entrez la pression au format float.",
        ).run()
        print(f"'{pressure_str}'")
        while(not is_float(pressure_str)) :
            pressure_str = input_dialog(
            title="Coordonnées initiales",
            text="Mauvaise input. Entrez la pression au format float.",
            ).run()

        drag_coefficient = input_dialog(
        title="Coefficient de traînée",
        text="Entrez le coefficient de traînée au format float.",
        ).run()
        while(not is_float(drag_coefficient)) :
            pressure_str = input_dialog(
            title="Coordonnées initiales",
            text="Mauvaise input. Entrez le coefficient de traînée au format float.",
            ).run()

        launch_time = input_dialog(
        title="Heure de départ",
        text="Entrez l'heure de départ au format (HH:MM:SS)",
        ).run()
        while(not is_valid_time(launch_time)) :
            launch_time = input_dialog(
            title="heure de départ",
            text="Mauvaise input. Entrez l'heure de départ au format HH:MM:SS.",
            ).run()


        lon_start=float(lon_str)
        lat_start=float(lat_str)
        pressure_start=float(pressure_str)
        message_dialog(
            text="Simulation avec longitude: {lon_start}, latitude: {lat_start} et pression: {pressure_start}."
        )
        print("executer code ici")
    else:
        break
