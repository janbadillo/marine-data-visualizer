from application import app 
from flask import render_template, url_for, jsonify, request
import pandas as pd
import json
import plotly
import plotly_express as px
import plotly.graph_objects as go

from application.files_drive import get_file_id_from_name, get_file_names_from_folder

@app.route("/")
def index():
    file_names = get_file_names_from_folder()
    return render_template("index.html", fileNames=file_names, title = "Home")

@app.route("/about")
def about():
    return render_template("about.html", title = "About")

@app.route("/documentation")
def documentation():
    return render_template("documentation.html", title = "Documentation")

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