import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Google Drive API base URL for public access
GOOGLE_DRIVE_API_URL = os.getenv("GOOGLE_DRIVE_API_URL")
# Public folder ID (seaview data)
FOLDER_ID = os.getenv("FOLDER_ID")
# Google API key
API_KEY = os.getenv("API_KEY")

def get_file_names_from_folder(): 
    # data folder in seaview2024data@gmail.com account (google drive)
    # Function to fetch file names from a public Google Drive folder
    try:
        # Define the parameters for the Google Drive API request
        params = {
            'q': f"'{FOLDER_ID}' in parents and trashed = false",
            'fields': 'files(id, name)',
            'key': API_KEY,
        }

        # Perform the GET request to the Google Drive API
        response = requests.get(GOOGLE_DRIVE_API_URL, params=params)

        # Check if the response is successful
        if response.status_code == 200:
            files = response.json().get('files', [])
            # Extract and return the file names
            file_names = [file['name'] for file in files]
            return file_names
        else:
            return []

    except Exception as e:
        print(f"Error fetching files: {e}")
        return []
    
def get_file_id_from_name(file_name):
    # Function to fetch file ID by matching file name from a public Google Drive folder.
    try:
        # Define the parameters for the Google Drive API request
        params = {
            'q': f"'{FOLDER_ID}' in parents and trashed = false",
            'fields': 'files(id, name)',
            'key': API_KEY,
        }

        # Perform the GET request to the Google Drive API
        response = requests.get(GOOGLE_DRIVE_API_URL, params=params)

        # Check if the response is successful
        if response.status_code == 200:
            files = response.json().get('files', [])
                
            # Iterate through the list of files and return the ID if the name matches
            for file in files:
                if file['name'] == file_name:
                    return file['id']
                
            # If no match is found, return None or an error message
            return None
        else:
            return None

    except Exception as e:
        print(f"Error fetching file ID: {e}")
        return None