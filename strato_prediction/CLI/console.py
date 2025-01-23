from strato_prediction.simulation import Balloon
from strato_prediction.GRIB import load_grib_data
from strato_prediction.display import plot_trajectory_3d, show_on_map
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import message_dialog, button_dialog, input_dialog, radiolist_dialog
from datetime import datetime, timedelta
import math
import calendar

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def validate_date_format(date_str):
    if len(date_str) != 10 or date_str[4] != '-' or date_str[7] != '-':
        return False
    try:
        year = int(date_str[0:4])
        month = int(date_str[5:7])
        day = int(date_str[8:10])
        return True
    except ValueError:
        return False

def validate_time_format(time_str):
    if len(time_str) != 8 or time_str[2] != ':' or time_str[5] != ':':
        return False
    try:
        hours = int(time_str[0:2])
        minutes = int(time_str[3:5])
        seconds = int(time_str[6:8])
        return True
    except ValueError:
        return False

def validate_date_range(date_str):
    try:
        # Convertir la chaîne de date en objet datetime (sans l'heure)
        date_input = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Obtenir la date actuelle (sans l'heure ni les microsecondes)
        now = datetime.now().date()
        
        # Calculer la limite supérieure (date actuelle + 10 jours max)
        max_date = now + timedelta(days=10)  # Calcul effectué avec un objet `date`, ce qui est correct
        
        # Vérifier que la date est dans l'intervalle [now, now + 10 jours]
        if not (now <= date_input <= max_date):
            return f"La date doit être comprise entre {now.strftime('%Y-%m-%d')} et {max_date.strftime('%Y-%m-%d')}."
        
        # Si la date est valide
        return None
    
    except ValueError:
        return "La date fournie est invalide. Assurez-vous qu'elle est au format YYYY-MM-DD."


def validate_time_range(time_str):
    try:
        # Convertit l'heure saisie en un objet datetime.time
        time_input = datetime.strptime(time_str, "%H:%M:%S").time()
       
        # Obtenir l'heure actuelle
        now = datetime.now()
        now_time = now.time()
       
        # Calculer la limite supérieure (10 jours après maintenant)
        max_datetime = now + timedelta(days=10)
        max_time = max_datetime.time()
       
        # Comparer uniquement si l'heure saisie est pour aujourd'hui
        if now.date() == max_datetime.date():
            if not (now_time <= time_input <= max_time):
                return f"L'heure doit être entre {now_time.strftime('%H:%M:%S')} aujourd'hui et {max_time.strftime('%H:%M:%S')} dans 10 jours."
       
        # Si la plage de validation doit inclure les jours complets
        if not (time_input >= now_time or time_input <= max_time):
            return "L'heure n'est pas dans les limites."
 
        return None  # L'heure est valide
    except ValueError:
        return "L'heure fournie est invalide. Assurez-vous qu'elle est au format HH:MM:SS."
    
def get_date_input():
    while True:
        date_str = input_dialog(
            title="Date initiale",
            text="Entrez la date au format YYYY-MM-DD."
        ).run()
        
        if not validate_date_format(date_str):
            while(not validate_date_format(date_str)):
                date_str = input_dialog(
                    title="Erreur!",
                    text="Format incorrect. Utilisez YYYY-MM-DD."
                ).run()
        
        error_msg = validate_date_range(date_str)
        if error_msg:
            message_dialog(
            title="Erreur!",
            text=(f"{error_msg}")
            ).run()
            continue
        
        return date_str
    
def get_time_input():
    while True:
        time_str = input_dialog(
            title="Heure initiale",
            text="Entrez l'heure au format HH:MM:SS."
        ).run()

        if not validate_time_format(time_str):
            while(not validate_time_format(time_str)):
                time_str = input_dialog(
                title="Erreur!",
                text="Aucune heure saisie. Veuillez entrer une heure."
                ).run()

        error_msg = validate_time_range(time_str)
        if error_msg:
            message_dialog(
            title="Erreur!",
            text=(f"{error_msg}")
            ).run()
            continue

        return time_str  

def console():
    args = {
            'start_lat': 0,
            'start_lon': 0,
            'ascent_rate':0,
            'burst_altitude':0,
            'date': 00000000,
            'time':000000,
            'cycle': 00,
            'offset_time': 00,
            'diameter_str': 0,
            'surface_area':0,
            'drag_coefficient':0,
            'masse_str':0
        }
    
    simulation = radiolist_dialog(
    title="Lancement simulateur",
    text="Quelle type de simulation voulez-vous lancer?",
    values=[
        ("sim1", "Trajet simple"),
        ("sim2", "Différentes altitudes d'explosion"),
        ("sim3", "Différentes vitesses d'ascension")]).run()
    
    lat_str = input_dialog(
        title="Coordonnées initiales",
        text="Entrez la latitude de lancement. ([-90,90][°])").run()
    while((not is_float(lat_str)) or not (-90 <= float(lat_str) <= 90)) :
        lat_str = input_dialog(
        title="Coordonnées initiales",
        text="Mauvais input. Entrez la latitude de lancementau format float. ([-90,90][°])").run()
    args['start_lat'] = lat_str
    
    lon_str = input_dialog(
        title="Coordonnées initiales",
        text="Entrez la longitude de lancement. ([0,360][°])").run()
    while((not is_float(lon_str)) or not (0 <= float(lon_str) <= 360)) :
        lon_str = input_dialog(
            title="Coordonnées initiales",
            text="Mauvais input. Entrez la longitude de lancement au format float. ([0,360][°])").run()
    args['start_lon'] = lon_str
    
    args['date'] = get_date_input()
    args['time'] = get_time_input()
    
    drag_coefficient = input_dialog(
        title="Coefficient de traînée",
        text="Entrez le coefficient de traînée (]0,5] [-])").run()
    while(not is_float(drag_coefficient)or not (0 < float(drag_coefficient) <= 5)):
        drag_coefficient = input_dialog(
            title="Coordonnées initiales",
            text="Mauvais input. Entrez le coefficient de traînée au format float.(]0,5] [-])").run()
    args['drag_coefficient'] = drag_coefficient
    
    masse_str = input_dialog(
        title="Masse",
        text="Entrez la masse (]0,100000] [g])").run()
    while(not is_float(masse_str)or not (0 < float(masse_str) <= 100000)) :
        masse_str = input_dialog(
            title="Masse",
            text="Mauvais input. Entrez la masse au format float.(]0,100000] [g])").run()
    args['masse_str'] = masse_str
        
    diametre_str = input_dialog(
        title="Diamètre du ballon",
        text="Entrez le diamètre en mètre. (]0,100] [m])").run()
    while(not is_float(diametre_str)or not (0 < float(diametre_str) <= 100)):
        diametre_str = input_dialog(
            title="Diamètre du ballon",
            text="Mauvais input. Entrez le diamètre au format float.(]0,100] [m])").run()
    args['diametre_str'] = diametre_str
    
    if simulation == "sim1":    
        burst_altitude = input_dialog(
            title="Altitude d'explosion",
            text="Entrez l'altitude d'explosion. ([0,40000][m])").run()
        while(not is_float(burst_altitude)or not (0 <= float(burst_altitude) <= 40000)) :
            if burst_altitude < 10000:
                text = "Mauvais input. L'altitude d'explosion doit être > 10000m."
            else:
                text="Mauvais input. Entrez l'altitude d'explosion au format float. ([0,40000][m])"
            burst_altitude = input_dialog(
                title="Altitude d'explosion",
                text = text).run()
        args['burst_altitude'] = burst_altitude
    
        ascent_rate = input_dialog(
            title="Vitesses d'ascension",
            text="Entrez la vitesse d'ascension. (]0,100][m/s])").run()
        while(not is_float(burst_altitude)or not (0 < float(ascent_rate) <= 100)) :
            if (0 < float(ascent_rate) <= 100):
                text = "Mauvais input. L'altitude d'explosion doit être (]0,100][m/s])"
            else:
                text="Mauvais input. Entrez l'altitude d'explosion au format float. (]0,100][m/s])"
            ascent_rate = input_dialog(
                title="Vitesses d'ascension",
                text = text).run()
        args['ascent_rate'] = ascent_rate

    elif simulation == "sim2":
        ascent_rate = input_dialog(
            title="Vitesses d'ascension",
            text="Entrez la vitesse d'ascension. (]0,100][m/s])").run()
        while(not is_float(burst_altitude)or not (0 < float(ascent_rate) <= 100)) :
            if (0 < float(ascent_rate) <= 100):
                text = "Mauvais input. L'altitude d'explosion doit être (]0,100][m/s])"
            else:
                text="Mauvais input. Entrez l'altitude d'explosion au format float. (]0,100][m/s])"
            ascent_rate = input_dialog(
                title="Vitesses d'ascension",
                text = text).run()
        args['ascent_rate'] = ascent_rate
        message_dialog(
            title="Altitudes d'explosions",
            text="Les altitudes d'explosion sont 25,26,27,...,35 [km]").run()
        args['burst_altitude'] = [25000,26000,27000,28000,29000,30000,31000,32000,33000,34000,35000]
                
    elif simulation == "sim3":
        burst_altitude = input_dialog(
            title="Altitude d'explosion",
            text="Entrez l'altitude d'explosion. ([0,40000][m])").run()
        while(not is_float(burst_altitude)or not (0 <= float(burst_altitude) <= 40000)) :
            if burst_altitude < 10000:
                text = "Mauvais input. L'altitude d'explosion doit être > 10000m."
            else:
                text="Mauvais input. Entrez l'altitude d'explosion au format float. ([0,40000][m])"
            burst_altitude = input_dialog(
                title="Altitude d'explosion",
                text = text).run()
        args['burst_altitude'] = burst_altitude
        message_dialog(
            title="Vitesses d'ascension",
            text="Les vitesses d'ascension sont 4,4.5,5,5.5,6 [m/s]").run()
        args['ascent_rate'] = [4,4.5,5,5.5,6]
        
    args['surface_area'] = math.pi*(float(args['diametre_str'])/2)**2

    # Obtenir l'heure actuelle
    now = datetime.now()
    hour = now.hour

    # Déterminer la tranche horaire pour ajuster le cycle
    if 0 <= hour < 6:
        cycle = "00"
    elif 6 <= hour < 12:
        cycle = "06"
    elif 12 <= hour < 18:
        cycle = "12"
    elif 18 <= hour < 24:
        cycle = "18"

    # Conversion du cycle en entier
    args['cycle'] = int(cycle)

    # Convertir l'heure de lancement future en datetime.time()
    launch_time = datetime.strptime(args['time'], "%H:%M:%S").time()

    # Convertir la chaîne de date du lancement en objet datetime.date()
    launch_date = datetime.strptime(args['date'], "%Y-%m-%d").date()

    # Vérifier si la date de lancement est aujourd'hui ou dans le futur
    if launch_date > now.date() or (launch_date == now.date() and launch_time > now.time()):
        # Si la date du lancement est dans le futur, combiner avec l'heure de lancement pour obtenir datetime
        future_datetime = datetime.combine(launch_date, launch_time)
    else:
        # Si l'heure de lancement est dans le passé pour aujourd'hui, passer au jour suivant
        future_datetime = datetime.combine(now.date() + timedelta(days=1), launch_time)

    # Calculer la différence de temps entre l'heure actuelle et l'heure future
    time_diff = future_datetime - now

    # Convertir la différence en heures
    hours_diff = time_diff.total_seconds() // 3600  # Total des secondes divisé par 3600 pour obtenir des heures

    # Soustraire le cycle au résultat
    adjusted_time = hours_diff - args['cycle']

    # Enregistrer le résultat dans args
    args['offset_time'] = adjusted_time

    print(f"Offset time : {args['offset_time']} heures")

    message_dialog(
        title="Résumé de la simulation",
        text=(
            f"Simulation configurée avec :\n"
            f"Latitude : {args['start_lat']},\n"
            f"Longitude : {args['start_lon']},\n"
            f"Altitude d'explosion : {args['burst_altitude']},\n"
            f"Coefficient de traînée : {args['drag_coefficient']},\n"
            f"Masse : {args['masse_str']}g,\n"
            f"Aire du parachute : {args['surface_area']}m,\n"
            f"Date de départ : {args['date']},\n"
            f"Heure de départ : {args['time']},\n"
            f"Cycle : {args['cycle']},\n"
            f"Offset: {args['offset_time']},\n"
        )).run()
    return args
console()
