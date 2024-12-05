import json
import requests

import pydrive


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive



# Basic Google Drive connection template. Can be run on raspberry pi via 4G connection to upload any file. 



def main():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    file1 = drive.CreateFile({'title': 'Hello.txt'})

    file1.SetContentString('Hello World!')

    file1.Upload()


    
















if __name__ == "__main__":
    main()