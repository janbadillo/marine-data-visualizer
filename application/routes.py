from application import app 
from flask import render_template, url_for
import pandas as pd
import json
import plotly
import plotly_express as px

@app.route("/")
def index():
    
    #1st Graph to render
    df = px.data.medals_wide()
    figl = px.bar(df, x = "nation", y = ['gold','silver', 'bronze'],
                  title = 'Wide=Form Input')
    
    graph1JSON = json.dumps(figl, cls = plotly.utils.PlotlyJSONEncoder)
    
    #2nd Graph
    df = px.data.iris()
    fig2 = px.scatter_3d(df, x = "sepal_length", y = "sepal_width", z = "petal_width", 
                         color = "species", title = "Iris Dataset")
    
    graph2JSON = json.dumps(fig2, cls = plotly.utils.PlotlyJSONEncoder)
    
    return render_template("index.html", title = "Test",
                           graph1JSON = graph1JSON,
                           graph2JSON = graph2JSON)
