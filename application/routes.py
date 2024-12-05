from application import app 
from flask import render_template, url_for, jsonify, request
import requests
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
    csv_url = f"https://drive.google.com/uc?export=download&id={selected_id}"

    try:
        # Fetch the file contents from the Google Drive URL
        response = requests.get(csv_url)
        response.raise_for_status()  # Ensure the request was successful
        csv_content = response.text  # Get CSV content as text

        # Send the CSV content as JSON response
        return jsonify({"csv_content": csv_content}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500