# import necessary libraries
from sqlalchemy import create_engine, inspect, func

import numpy as np
import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///DataSets/belly_button_biodiversity.sqlite"

db = SQLAlchemy(app)

engine = create_engine("sqlite:///DataSets/belly_button_biodiversity.sqlite")
inspector = inspect(engine)

class otu(db.Model):
    __tablename__ = "otu"
    otu_id = db.Column(db.Integer, primary_key=True)
    lowest_taxonomic_unit_found = db.Column(db.Text)


#     SAMPLEID INTEGER
# EVENT TEXT
# ETHNICITY TEXT
# GENDER TEXT
# AGE INTEGER
# WFREQ INTEGER
# BBTYPE TEXT
# LOCATION TEXT
# COUNTRY012 TEXT
# ZIP012 INTEGER
# COUNTRY1319 TEXT
# ZIP1319 INTEGER
# DOG TEXT
# CAT TEXT
# IMPSURFACE013 INTEGER
# NPP013 FLOAT
# MMAXTEMP013 FLOAT
# PFC013 FLOAT
# IMPSURFACE1319 INTEGER
# NPP1319 FLOAT
# MMAXTEMP1319 FLOAT
# PFC1319 FLOAT


#################################################
# Flask Routes
#################################################

# Query the database and send the jsonified results
@app.route("/names")
def names():
    sampNames=[]
    for field in inspector.get_columns(table_name='samples'):
        sampNames.append(field["name"])
    return jsonify(sampNames)

@app.route("/otu")
def otuout():
    results = db.session.query(otu.lowest_taxonomic_unit_found).all()
    df = pd.DataFrame(results)
    return jsonify(df.to_dict(orient="records"))
   

# @app.route("/metadata/<sample>")
# def meta():
#     return "here is the meta data"

# @app.route("/wfreq/<sample>")
# def wfreq():
#     return "here is the wfreq data"

# @app.route("/sample/<sample>")
# def sample():
#     return "here is the sample data"

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
