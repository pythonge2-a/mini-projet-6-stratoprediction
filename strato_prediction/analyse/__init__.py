import pygrib
class AnalyserGRIB:
    def __init__(self):
        self.uWind = None
        self.vWind = None
        self.level = None
        self.date = None
        self.time = None
        self.temperature = None
        self.pressure = None
        self.altitude = None

    def analyser_grib(self, file_path):
        #filtre zone coordonnées:
        zlatmin = 46.4008333
        zlatmax = 46.8072222
        zlonmin = 6.211111111111111
        zlonmax = 6.9991666666666665

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
            data, lats, lons = grb.data(lat1=zlatmin,lat2=zlatmax,lon1=zlonmin,lon2=zlonmax)
            print(f"data:{data}")
            print(f"lats:{lats}")
            print(f"lons:{lons}")
            print(f"dataDate:{self.date}")
            print(f"dataTime:{self.time}")
            print(f"datashape:{data.shape}")
        except Exception as e:
            print(f"Erreur lors de l'analyse du fichier GRIB : {e}")
        return "Données analysées"  