import readchar
def args_retrieval():
    args = {
            'start_pressure': 0,
            'start_altitude':0,
            'start_lat': 0,
            'start_lon': 0,
            'ascent_rate':0,
            'burst_pression':0,
            'burst_altitude':0,
            'date': "",
            'time':"",
            'cycle': "",
            'offset_time': "",
        }
    
    while True:
        validation = input("Voulez-vous entrer des coordonnées de départ? [YES/NO] [Y/N]\n").strip().upper()
        if validation in ["YES", "Y", "NO", "N"]:
            break
        else:
            print("Entrez YES/Y ou NO/N")
            
    if validation in ["YES","Y"]:
        while True:
            args['start_lat']=input_coordinates("latitude")
            args['start_lon'] = input_coordinates("longitude")
            args['start_pressure'], args['start_altitude']= input_altitude()
            args['ascent_rate'] = input_ascent_rate()
            args['burst_pression'], args['burst_altitude'] = input_burst_altitude(args['start_altitude'], args['start_pressure'])
            args['date'] = input_launch_date()
            args['offset_time']= input_launch_time()

            print(f"Les coordonnées de départ sont:\n - Latitude: {args['start_lat']}\n - Longitude: {args['start_lon']}\n - Altitude: {args['start_altitude']}\n - Pressure: {args['start_pressure']}\n")
            print(f"La date de départ est:\n - Date: {args['date']}\n - Heure {args['date']}\n")
            print(f"Les paramètres de départ sont:\n - Vitesse d'ascension: {args['ascent_rate']}\n - Altitude d'explosion: {['burst_altitude']}\n - Pression d'explosion: {args['burst_pression']}\n")
            

            while True:
                validation = input("Valider ? [YES/NO] [Y/N]\n").strip().upper()
                if validation in ["YES", "Y", "NO", "N"]:
                    break
                else:
                    print("Entrez YES/Y ou NO/N")

            if validation in ["YES","Y"]:
                break
            elif validation in ["NO","N"]:
                pass
    elif validation in ["NO","N"]:
        print("Coordonnées initiales") 
        args['start_lat'] = 22
        args['start_lon'] = 12
        args['start_pressure'] = 700
        args['ascent_rate'] = [5]
        args['burst_altitude'] = 2000
        args['date'] = "20250111"
        args['time'] = 32350
        
        args['cycle'] = "12"
        args['offset_time']= 20
        
    
    return args

def input_coordinates(type_coordinates):
    resultat = ""
    separateurs = ['°', "'", '"']  # Liste des séparateurs
    index_separateur = 0  # Index pour suivre quel séparateur utiliser
    
    print(f"Entrez une {type_coordinates} de départ (DMS:[--° --' --\"]): ", end='', flush=True)
    
    while True:
        # Compte les chiffres uniquement (pas les séparateurs)
        nb_chiffres = len(resultat.replace('°', '').replace("'", '').replace('"', ''))
        
        # Lit un caractère
        char = readchar.readchar()
        
        # Si Enter est pressé
        if char in ('\r', '\n'):  # Nouvelle ligne (Enter)
            return resultat  # Retourne la valeur entrée
        
        # Si c'est un chiffre et qu'on est en dessous de la limite
        elif char.isdigit() and nb_chiffres < 6:
            # Ajouter le chiffre au résultat
            resultat += char
            print(char, end='', flush=True)
            
            # Ajouter le séparateur après chaque paire de chiffres
            if len(resultat.replace('°', '').replace("'", '').replace('"', '')) % 2 == 0:
                if index_separateur < len(separateurs):
                    resultat += separateurs[index_separateur]
                    print(separateurs[index_separateur], end='', flush=True)
                    index_separateur += 1
        
        # Si c'est backspace (différents codes possibles)
        elif char in ('\x7f', '\x08') and len(resultat) > 0:
            # Supprime le dernier caractère
            if resultat[-1] in separateurs:
                index_separateur -= 1  # Reculer l'index si on supprime un séparateur
            resultat = resultat[:-1]
            print('\b \b', end='', flush=True)
            
def input_altitude():
    altitude = None
    pressure = None
    
    while True:
        choice = input("Voulez-vous rentrer une altitude ([m]) ou une pression ([hpa])? [Altitude/Pression] [A/P]: ").strip().upper()
        if choice in ["ALTITUDE", "A", "PRESSION", "P"]:
            break
        else:
            print("Entrez [Altitude/Pression] ou [A/P].")
    
    while True:
        if choice in ["ALTITUDE", "A"]:
            # Pose la question et lit la réponse sur la même ligne
            altitude = input("Entrez une altitude de départ ([m]): ").strip()
            if altitude.isdigit() and 0 < int(altitude) < 8848:
                break
            else:
                print("Entrez une altitude valide.")
        
        if choice in ["PRESSION", "P"]:
            # Pose la question et lit la réponse sur la même ligne
            pressure = input("Entrez une pression de départ ([hpa]): ").strip()
            if pressure.isdigit() and 0.1 < float(pressure) < 1013.15:
                break
            else:
                print("Entrez une pression valide.")
    
    print(f"Pression : {pressure}" if pressure else f"Altitude : {altitude}")
    return pressure, altitude


def input_ascent_rate():  
    while True: 
        # Pose la question et lit la réponse sur la même ligne
        ascent_rate = input("Entrez une vitesse d'ascension ([m/s]): ").strip()
        if ascent_rate.isdigit() and int(ascent_rate) > 0:
            return ascent_rate  # Retourne la vitesse d'ascension valide
        else:
            print("Entrez une vitesse d'ascension valide.")


def input_burst_altitude(launch_altitude, launch_pression):  
    burst_altitude = None
    burst_pressure = None
    
    while True:
        choice = input("Voulez-vous rentrer une altitude ([m]) ou une pression ([hpa]) d'explosion? [Altitude/Pression] [A/P]: ").strip().upper()
        if choice in ["ALTITUDE", "A", "PRESSION", "P"]:
            break
        else:
            print("Entrez [Altitude/Pression] ou [A/P]")
    while True:
        if choice in ["ALTITUDE", "A"]:
        
            burst_altitude = input("Entrez une altitude d'explosion ([m]): ") 
            if burst_altitude.isdigit() and int(burst_altitude) > int(launch_altitude):
                break
            else:
                print("Entrez une altitude valide")
        if choice in ["PRESSION", "P"]:
        
            burst_pressure = input("Entrez une pression d'explosion ([hpa]): ") 
            if burst_pressure.isdigit() and int(burst_pressure) > int(launch_pression):
                break
            else:
                print("Entrez une pression valide")    
    return burst_pressure, burst_altitude 

def input_launch_time():
    while True:
        resultat = ""
        separateurs = ['h', 'm', 's']
        index_separateur = 0
        position = 0
        
        print(f"Entrez un temps de départ (--h--m--s): ", end='', flush=True)
        
        while True:
            char = readchar.readchar()
            
            if char in ('\r', '\n'):
                if len(resultat.replace('h', '').replace('m', '').replace('s', '')) == 6:
                    try:
                        hours = int(resultat[:2])
                        minutes = int(resultat[3:5])
                        seconds = int(resultat[6:8])
                        
                        if 0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59:
                            return resultat
                        else:
                            print("\nErreur : Heure, minute ou seconde invalide. Les heures doivent être entre 00 et 23, les minutes et secondes entre 00 et 59. Réessayez.")
                            break
                    except ValueError:
                        print("\nErreur de format. Réessayez.")
                        break
                else:
                    print("\nFormat incomplet. Réessayez.")
                    break
            
            elif char in ('\x7f', '\x08') and len(resultat) > 0:
                last_char = resultat[-1]
                resultat = resultat[:-1]
                print('\b \b', end='', flush=True)
                
                if last_char in separateurs:
                    index_separateur -= 1
                else:
                    position -= 1
                    
            elif char.isdigit():
                position = len(resultat.replace('h', '').replace('m', '').replace('s', ''))
                
                if position < 6:
                    valid_input = True
                    
                    if position < 2:
                        tentative = int(resultat + char if position == 1 else char)
                        valid_input = tentative <= 23
                        if not valid_input:
                            print("\nErreur : Heure invalide. Les heures doivent être entre 00 et 23. Réessayez.")
                            break
                            
                    elif position < 4:
                        tentative = int(resultat.split('h')[1] + char if 'h' in resultat and len(resultat.split('h')[1]) == 1 else char)
                        valid_input = tentative <= 59
                        if not valid_input:
                            print("\nErreur : Minute invalide. Les minutes doivent être entre 00 et 59. Réessayez.")
                            break
                            
                    elif position < 6:
                        tentative = int(resultat.split('m')[1] + char if 'm' in resultat and len(resultat.split('m')[1]) == 1 else char)
                        valid_input = tentative <= 59
                        if not valid_input:
                            print("\nErreur : Seconde invalide. Les secondes doivent être entre 00 et 59. Réessayez.")
                            break
                    
                    if valid_input:
                        resultat += char
                        print(char, end='', flush=True)
                        
                        if position in [1, 3, 5] and index_separateur < len(separateurs):
                            resultat += separateurs[index_separateur]
                            print(separateurs[index_separateur], end='', flush=True)
                            index_separateur += 1

def input_launch_date():
    while True:
        resultat = ""
        separateurs = ['.', '.']
        index_separateur = 0
        position = 0
        
        print(f"Entrez une date (dd.mm.yyyy): ", end='', flush=True)
        
        while True:
            char = readchar.readchar()
            
            if char in ('\r', '\n'):
                if len(resultat.replace('.', '')) == 8:
                    try:
                        day = int(resultat[:2])
                        month = int(resultat[3:5])
                        year = int(resultat[6:])
                        
                        # Vérifier si le mois est valide
                        if not (1 <= month <= 12):
                            print("\nErreur : Mois invalide. Le mois doit être entre 01 et 12. Réessayez.")
                            break
                            
                        # Déterminer le nombre de jours dans le mois
                        jours_par_mois = [31, 29 if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0 else 28, 
                                        31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                        
                        if not (1 <= day <= jours_par_mois[month-1]):
                            print(f"\nErreur : Jour invalide pour le mois {month:02d}. Réessayez.")
                            break
                            
                        if not (2000 <= year <= 2100):
                            print("\nErreur : L'année doit être entre 2000 et 2100. Réessayez.")
                            break
                            
                        return resultat
                    except ValueError:
                        print("\nErreur de format. Réessayez.")
                        break
                else:
                    print("\nFormat incomplet. Réessayez.")
                    break
                    
            elif char in ('\x7f', '\x08') and len(resultat) > 0:
                last_char = resultat[-1]
                resultat = resultat[:-1]
                print('\b \b', end='', flush=True)
                
                if last_char in separateurs:
                    index_separateur -= 1
                else:
                    position -= 1
                    
            elif char.isdigit():
                position = len(resultat.replace('.', ''))
                
                if position < 8:
                    valid_input = True
                    
                    # Validation du jour
                    if position < 2:
                        tentative = int(resultat + char if position == 1 else char)
                        valid_input = tentative <= 31
                        if not valid_input:
                            print("\nErreur : Jour invalide. Le jour doit être entre 01 et 31. Réessayez.")
                            break
                            
                    # Validation du mois
                    elif position < 4:
                        tentative = int(resultat.split('.')[1] + char if '.' in resultat and len(resultat.split('.')[1]) == 1 else char)
                        valid_input = tentative <= 12
                        if not valid_input:
                            print("\nErreur : Mois invalide. Le mois doit être entre 01 et 12. Réessayez.")
                            break
                            
                    # Validation de l'année
                    elif position < 8:
                        if position == 4:
                            valid_input = char in ['2']
                        elif position == 5:
                            valid_input = char in ['0']
                        elif position == 6:
                            valid_input = char in ['0', '1']
                        else:
                            valid_input = char.isdigit()
                            
                        if not valid_input:
                            print("\nErreur : L'année doit être entre 2000 et 2100. Réessayez.")
                            break
                            
                    if valid_input:
                        resultat += char
                        print(char, end='', flush=True)
                        
                        if position in [1, 3] and index_separateur < len(separateurs):
                            resultat += separateurs[index_separateur]
                            print(separateurs[index_separateur], end='', flush=True)
                            index_separateur += 1
                

                
#start_lat = args_retrieval()
#print(f"Il a comme latitude : {start_lat}")

# On veut un return avec lat_start (float), lon_start (float), altitude [m](float)