
import csv
import numpy as np
import os

from datetime import date
from time import sleep, time

import bluerobotics_navigator as navigator


# The google drive functionality requires additional setup from the user. The user must place their client_secrets.json
# obtained from their google cloud account (no payment or credit card required) and place it in the same folder as this script. 
# this will allow the csv to be automatically uploaded to the uer's google drive account, and be viewed on the dashboard. 




def missionStart(ready):
    # Initialize data lists
    lat = np.array([])
    lon = np.array([])
    topo = np.array([])
    today = date.today().strftime("%b-%d-%Y")

    # Create and initialize csv file
    csvfile = open(os.getcwd() + "/Data/navigator/" + today + ".csv", "w")
    writer = csv.writer(csvfile)
    _header = ["Latitude", "Longitude", "Depth_in_Feet"]
    writer.writerow(_header)
    #TODO 

    # Each sensor fires, once row is filled, write to CSV 

    #Flush CSV after each write, to save data if something were to happen to system. 

    # After x amount of rows written, upload to Google drive account, user will be able to see the updated CSV through the dashboard

    # Update ready variable, check if mission has ended. IF so, finally close the writer, and prepare to exit script. 


def main() -> None:
    print("Navigator initialization...")
    navigator.init()
    print("Navigator initialized")
    navigator.set_led(navigator.UserLed.Led1, True)
    print("Testing sensors...")
    if navigator.self_test():
        print("Sensors responding as expected!")
    else:
        print("Sensors did not respond as expected. Are they connected properly?")
        exit()
    # get vehicle status, ready variable
    ready = False
    missionStart(ready)




if __name__ == "__main__":
    main()