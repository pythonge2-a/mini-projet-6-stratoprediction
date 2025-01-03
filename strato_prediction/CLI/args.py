def args_retrieval():
    while True:
        validation = input("Voulez-vous entrer des coordonnées de départ? [YES/NO] [Y/N]\n").strip().upper()
        if validation in ["YES", "Y", "NO", "N"]:
            break
        else:
            print("Entrez YES/Y ou NO/N")
            
    if validation in ["YES","Y"]:
        while True:
            start_lat = input("""Entrez une latitude de départ (DMS:[--° --' --"]):""")
            if len(start_lat) >= 8 and len(start_lat) <= 11:
                break
            else:
                print("Format incorrect")

        while True:
            start_long = input("""Entrez une longitude de départ (DMS:[--° --' --"]):""")
            if len(start_long) >= 8 and len(start_lat) <= 11:
                break
            else:
                print("Format incorrect")  

        start_alt = input(f"""Entrez une altitude de départ [----]:""")
        print(f"Les coordonnées de départ sont:\n - Latitude: {start_lat}\n - Longitude: {start_long}\n - Altitude: {start_alt}")
    
        while True:
            validation = input("Valider ? [YES/NO] [Y/N]\n").strip().upper()
            if validation in ["YES", "Y", "NO", "N"]:
                break
            else:
                print("Entrez YES/Y ou NO/N")

        if validation in ["YES","Y"]:
            print("continue")
        elif validation in ["NO","N"]:
            print("Recommencer") 
    elif validation in ["NO","N"]:
        print("Coordonnées initiales") 
    #return start_lat
                
#start_lat = args_retrieval()
#print(f"Il a comme latitude : {start_lat}")

# On veut un return avec lat_start (float), lon_start (float), altitude [m](float)