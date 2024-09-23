from application import app 
from flask import render_template, url_for, jsonify, request
import pandas as pd
import json
import plotly
import plotly_express as px
import plotly.graph_objects as go
import requests

# Google Drive API base URL for public access
GOOGLE_DRIVE_API_URL = 'https://www.googleapis.com/drive/v3/files'

#public folder ID (seaview data)
FOLDER_ID = '19wtpV2toakJXD40QcYYYgi1gESFSXdx9'

#Google API key
API_KEY = 'AIzaSyBLBpljoW3tkbkNhIUhw2ckQmrO_jYQC3o'

def get_file_names_from_folder(): # data folder in seaview2024data@gmail.com account (google drive)
    """
    Function to fetch file names from a public Google Drive folder
    """
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
    """
    Function to fetch file ID by matching file name from a public Google Drive folder.
    """
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

@app.route("/")
def index():
    file_names = get_file_names_from_folder()
    return render_template("index.html", fileNames=file_names, title = "Test")

@app.route("/plot", methods=["POST"])
def plot():
    selected_file = request.form.get("selected_file")
    selected_id = get_file_id_from_name(selected_file)
    # Fetch and read the selected CSV file from Google Drive (this part needs actual implementation)
    # For now, I'll assume you have some way to access the Google Drive CSV
    csv_url = f"https://drive.google.com/uc?export=download&id={selected_id}"
    
    try:
        pd.set_option('display.float_format', '{:.16f}'.format)
        df = pd.read_csv(csv_url)  # Assuming the URL points to a direct CSV link
        depth_data = df.groupby(['Latitude', 'Longitude'], as_index=False).agg({'Depth_in_Feet': 'mean'}) # grouping repeated x,y values based on 3rd column average
        
        x = depth_data['Latitude'].values
        y = depth_data['Longitude'].values
        z = depth_data['Depth_in_Feet'].values

        fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='markers')])
        fig.update_traces(marker=dict(size=5, color=z, colorscale='Viridis', opacity=0.8))

        fig.update_layout(title="3D scatterplot of " + selected_file,
                        scene=dict(xaxis_title='Longitude',
                                    yaxis_title='Latitude',
                                    zaxis_title='Depth in Feet'))
        
        # Plot the CSV data using Plotly Express
        # fig = px.line(merged_df, x="Latitude", y="Longitude", title=f"Plot for {selected_file}")
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return jsonify({"graphJSON": graphJSON})
    
    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify({"error": "Error processing file"}), 500