from strato_prediction import init_project
from strato_prediction.analyse import AnalyserGRIB
from strato_prediction.display import afficher_resultats

def main():
    # Initialiser le projet
    init_project()
    analyser = AnalyserGRIB()
    # Tester l'analyse et l'affichage des résultats
    file_path = "assets/gfs.t06z.pgrb2.0p25.f000"  # Utilisez un chemin de fichier de test
    data = analyser.analyser_grib(file_path)

    # Afficher les résultats
    afficher_resultats(data)

if __name__ == "__main__":
    main()
