
import csv
import numpy as np
import os

from datetime import date
from time import sleep, time

# Devices
import bluerobotics_navigator as navigator
from brping import Ping1D
import ms5837

#Placeholder for GPS
import random


import pydrive

# Google Drive
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive




SERVICE_ACCOUNT_CREDENTIALS = "seaview-436305-5779f6d64074.json"
FOLDER_ID = "19wtpV2toakJXD40QcYYYgi1gESFSXdx9" # SeaView Folder ID
SERVICE_ACCOUNT_EMAIL = "" # Can't push this to github for security purposes.



def main() -> None:
    print("Navigator initialization...")
    navigator.init()
    print("Navigator initialized")
    navigator.set_led(navigator.UserLed.Led1, True)
    
    #Echosounder, connected to Serial 3 Port, at a 1200 BAUDRATE
    myPing = Ping1D()
    myPing.connect_serial("/dev/ttyAMA1", 1200)

    if myPing.initialize() is False:
        print("Failed to initialize Ping!")
        exit(1)

    
    sensor = ms5837.MS5837_30BA(6) # Default I2C bus is 1 (Raspberry Pi 3), For this project, it is 6. 


    print("Trying to authenticate")
    gauth = GoogleAuth()
    gauth.auth_method = 'service'
    gauth.settings['service_config'] = {
        "client_user_email": "",
        "client_json_file_path": SERVICE_ACCOUNT_CREDENTIALS
    }
    gauth.ServiceAuth()

    drive = GoogleDrive(gauth)

    print("Authenticated.")

    if not sensor.init():
        print("Temperature/Pressure Sensor could not be initialized")
        exit(1)

    # Initialize data lists
    lat = np.array([])
    lon = np.array([])
    topo = np.array([])
    pres = np.array([])
    temp = np.array([])
    today = date.today().strftime("%b-%d-%Y")

    # Create and initialize csv file
    csvfile = open(os.getcwd() + "/Data/navigator/" + today + ".csv", "w")
    writer = csv.writer(csvfile)
    _header = ["Latitude", "Longitude", "Depth_in_Feet", "Temperature_in_C", "Pressure_in_psi"]
    writer.writerow(_header)


    row = [None, None, None, None, None]
    GDriveCount = 0 # After 50 rows we will upload to GDrive. 
    try:
        while True:

            # Fire Echosounder

            data = myPing.get_distance()
            if data:
                print("Distance: %s\tConfidence: %s%%" % (data["distance"]/304.8, data["confidence"]))
                topo = np.append(topo, float(data["distance"]/304.8))
                row[2] = float(data["distance"]/304.8) # Convert to feet, no clue why default is milimeters.
            else:
                print("Failed to get distance data")
            
            # Fire GPS (Placeholder):
            lat = np.append(lat, random.uniform(17.92, 17.97))
            row[0] = random.uniform(17.92, 17.97)
            lon = np.append(lon, random.uniform(-66.73, -66.63))
            row[1] = random.uniform(-66.73, -66.63)


            # Fire Temperature and pressure:

            if sensor.read():
                print(("P: %0.1f mbar  %0.3f psi\tT: %0.2f C  %0.2f F") % (
                sensor.pressure(), # Default is mbar (no arguments)
                sensor.pressure(ms5837.UNITS_psi), # Request psi
                sensor.temperature(), # Default is degrees C (no arguments)
                sensor.temperature(ms5837.UNITS_Farenheit))) # Request Farenheit

                temp = np.append(temp, float(sensor.temperature()))
                row[3] = float(sensor.temperature())
                pres = np.append(pres, float(sensor.pressure(ms5837.UNITS_psi)))
                row[4] = float(sensor.pressure(ms5837.UNITS_psi))

            else:
                print("Sensor read failed!")
                exit(1)
            
            if all(row):
                print("WRITING TO CSV")
                writer.writerow(row)
                csvfile.flush()
                row = [None, None, None, None, None]
                GDriveCount+=1
                if GDriveCount >= 50:
                    query = f"title='{today}' and '{FOLDER_ID}' in parents and trashed=false"
                    file_list = drive.ListFile({'q': query}).GetList()
                    print(file_list)
                    if file_list:
                        print("File found, updating.")
                        gfile = file_list[0]  # Get the first match
                        gfile.SetContentFile(os.getcwd() + "/Data/navigator/" + today + ".csv")
                        gfile.Upload()
                        print(f"File '{today}' updated successfully on Google Drive!")
                        GDriveCount=0
                    

                    else:
                        print("File not found in cloud")
                        print("Uploading to google drive...")
                        file1 = drive.CreateFile({'title': today, 'parents': [{'id': FOLDER_ID}]})
                        file1.SetContentFile(os.getcwd() + "/Data/navigator/" + today + ".csv")
                        file1.Upload()
                        print("Uploaded!")
                        GDriveCount = 0



                sleep(0.5)

                # Here we update if we have a mission, for now we can't we have no GPS.
                # isVehicleActive = vehicle.active
    except KeyboardInterrupt:
        print("Saving CSV...")
        csvfile.flush()
        csvfile.close()
        print("Stopping program due to user input...")
        print("Goodbye.")

    








        

if __name__ == "__main__":
    main()