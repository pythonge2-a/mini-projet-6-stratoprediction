import pygrib

def analyser_grib(file_path):
    try:
        grbs = pygrib.open(file_path)
        for grb in grbs:
            print(grb)
            print(f"description:{grb.name}\n")
    except Exception as e:
        print(f"Erreur lors de l'analyse du fichier GRIB : {e}")
    return "Données analysées"  