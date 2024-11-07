from application import app 
from flask import render_template, url_for, jsonify, request
import pandas as pd
import json
import plotly
import plotly_express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from application.files_drive import get_file_id_from_name, get_file_names_from_folder

@app.route("/")
def home():
    file_names = get_file_names_from_folder()
    return render_template("home.html", fileNames=file_names, title = "Home")

@app.route("/about")
def about():
    return render_template("about.html", title = "About")

@app.route("/documentation")
def documentation():
    return render_template("documentation.html", title = "Documentation")

@app.route("/graph")
def graph():
    file_names = get_file_names_from_folder()
    return render_template("index.html", fileNames=file_names, title = "Graph")

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

        # Create a subplot with two columns
        fig = make_subplots(
            rows=1, cols=2,
            column_widths=[0.5, 0.5],  # Adjusted column widths to make them closer
            subplot_titles=("3D Scatterplot", "Data Table"),
            specs=[[{'type': 'scatter3d'}, {'type': 'table'}]]
        )

        # Add the 3D scatterplot to the first column
        fig.add_trace(
            go.Scatter3d(x=x, y=y, z=z, mode='markers', 
                 marker=dict(size=5, color=z, colorscale='Viridis', opacity=0.8)),
            row=1, col=1
        )

        # Add the table to the second column
        fig.add_trace(
            go.Table(
                header=dict(
                    values=list(df.columns),
                    fill_color='rgb(127, 255, 212)',
                    align='left',
                    font=dict(size=12, color='black')
                ),
                cells=dict(
                    values=[df[col] for col in df.columns],
                    fill_color='lavender',
                    align='left',
                    font=dict(size=11, color='black')
                )
            ),
            row=1, col=2
        )

        # Update layout
        fig.update_layout(
            title="3D Scatterplot and Data Table for " + selected_file,
            width=1100,
            height=620
        )

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return jsonify({"graphJSON": graphJSON})
    
    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify({"error": "Error processing file"}), 500