import xarray as xr
import numpy as np
#Permet de pouvoir afficher un nb illimité de ligne dans la console
np.set_printoptions(threshold=np.inf)

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
        self.latitude = None
        self.longitude = None

    def analyser_grib(self, file_path):
        # Utilise cfgrib comme moteur pour ouvrir le fichier GRIB
        #Filtre permettant de trier le fichier par pression en PA
        filter_keys = {'typeOfLevel': "isobaricInhPa"}
        #Ouverture du fichier
        ds = xr.open_dataset(file_path, engine='cfgrib', filter_by_keys=filter_keys)
        
        #print(f"\nVariables disponibles:{sorted(ds.variables)}\n")
        #print(f"\nisobaricInhPa: {ds.variables['isobaricInhPa']}")
        #print(f"\nlatitude: {ds.variables['latitude']}")
        #print(f"\nlongitude: {ds.variables['longitude']}")
        #print(f"\nstep: {ds.variables['step']}")
        #print(f"\ntime: {ds.variables['time']}")
        #print(f"\nu: {ds.variables['u']}")
        #print(f"\nv: {ds.variables['v']}")
        #print(f"\nvalid_time: {ds.variables['valid_time']}")
        
        varLon = ds.variables['longitude']
        varLat = ds.variables['latitude']
        varv = ds.variables['v']
        varu = ds.variables['u']
        varIs = ds.variables['isobaricInhPa']
        
        print(f"V:{varv.data}")
        print(f"U:{varu}")

        liste1= [] 
        liste1 = varv.data[0][0]
        liste2= [] 
        liste2 = varu.data[0][0]
        #print(f"longitude:{varLon.data[0]}")
        #print(f"latitude:{varLat.data[0]}")
        #print(f"V:{varv.data[0]}")
        #print(f"U:{varu.data[0]}")
        print(f"liste1:{liste1}")
        print(f"liste2:{liste2}")
        print(f"ziping:{next(zip(liste1,liste2))}")
        print(f"len lat:{len(varLat.data)}")
        print(f"len lon:{len(varLon.data)}")
        print(f"len alt:{len(varu.data)}")
        print(f"len alt:{len(varIs.data)}")
        #print(f"len alt:{len(varst.data)}")
        #print(f"len alt:{len(vart.data)}")
        #print(f"len alt:{len(varvt.data)}")
        
        for alt in range(len(varIs.data)):
            self.pressure = varIs.data[alt]
            print(f"alt:{self.pressure}lat:{self.latitude}lon:{self.longitude}")
            for lat in range(len(varLat.data)):
                print(f"alt:{self.pressure}lat:{self.latitude}lon:{self.longitude}")
                """
                for lon in range(len(varLon.data)):
                    self.longitude = varLat.data[lon]"""
        
                    
        """
        for lat in range(len(varLat.data)):
            print(lat)
            print(f"longitude:{varLat.data[lat]}")
            for lon in range(len(varLon.data)):
                for alt in range(len(varIs.data)):
                    print(f"longitude:{varLon.data[lon]}")
                    #print(f"U:{varu.data[lat][lon]}")
                    #print(f"V:{varv.data[lat][lon]}")"""
            


