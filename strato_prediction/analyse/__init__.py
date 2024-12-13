import pygrib
class AnalyserGRIB:
    def __init__(self):
        self.uWind = None
        self.vWind = None
        self.level = None
        self.date = None
        self.time = None

    def analyser_grib(self, file_path):
        try:
            grbs = pygrib.open(file_path)
            for grb in grbs:
                print(grb)
                print(grb.name)
                if "U component of wind" in grb.name:         
                    self.uWind = 2          
                    
                if "V component of wind" in grb.name:
                    self.vWind = 1 

                self.level = grb.level         
                self.date = grb.dataDate           
                self.time = grb.dataTime
                print(f"vWind: {self.vWind}")
                print(f"uWind: {self.uWind}")
                print(f"Level: {self.level}")
                print(f"Date: {self.date}")
                print(f"Time: {self.time}")
            print(dir(grb))
            print(grb.data(lat1=45.20,lat2=45.3,lon1=8.2,lon2=8.3))
        except Exception as e:
            print(f"Erreur lors de l'analyse du fichier GRIB : {e}")
        return "Données analysées"  