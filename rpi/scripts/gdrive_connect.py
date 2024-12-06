import json
import requests

import pydrive


from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive



#Basic Google Drive connection template. Can be run on raspberry pi via 4G connection to upload any file. 

SERVICE_ACCOUNT_CREDENTIALS = "seaview-436305-5779f6d64074.json"
FOLDER_ID = "19wtpV2toakJXD40QcYYYgi1gESFSXdx9" # SeaView Folder ID


def main():
    gauth = GoogleAuth()
    gauth.auth_method = 'service'
    gauth.settings['service_config'] = {
        "client_user_email": "admin-343@seaview-436305.iam.gserviceaccount.com",
        "client_json_file_path": SERVICE_ACCOUNT_CREDENTIALS
    }
    gauth.ServiceAuth()

    drive = GoogleDrive(gauth)

    # Create and upload a file
    file1 = drive.CreateFile({'title': "Hi.txt", 'parents': [{'id': FOLDER_ID}]})
    string = "Hello, I am born anew!"
    print(string)
    file1.SetContentString(string)
    file1.Upload()

    print("File uploaded successfully!")


    
















if __name__ == "__main__":
    main()