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

class metadata(db.Model):
    __tablename__="samples_metadata"
    sample_id = db.Column(db.Integer, primary_key=True) 
    event = db.Column(db.Text)
    ethnicity = db.Column(db.Text)
    gender = db.Column(db.Text)
    age = db.Column(db.Integer)
    wfreq = db.Column(db.Integer)
    bbtype = db.Column(db.Text)
    location = db.Column(db.Text)
    country012 = db.Column(db.Text)
    zip012 = db.Column(db.Integer)
    country1319 = db.Column(db.Text)
    zip1319 = db.Column(db.Integer)
    dog = db.Column(db.Text)
    cat = db.Column(db.Text)
    impsurface013 = db.Column(db.Integer)
    npp013 = db.Column(db.Float)
    mmaxtemp013 = db.Column(db.Float)
    pfc013 = db.Column(db.Float)
    impsurface1319 = db.Column(db.Integer)
    npp1319 = db.Column(db.Float)
    mmaxtemp1319 = db.Column(db.Float)
    pfc1319 = db.Column(db.Float)


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
   

@app.route('/metadata/<sample>')
@app.route("/metadata")
def metadataout():
    results = db.session.query(metadata.bbtype, metadata.ethnicity, metadata.gender, metadata.location).all()
    df = pd.DataFrame(results)
    return jsonify(df.to_dict(orient="records"))
#  I am having issues with age and id(metadata.age, metadata.bbtype, metadata.ethnicity, metadata.gender, metadata.location, metadata.sample_id).all():

@app.route("/wfreq/<sample>")
@app.route("/wfreq")
def wfreq():
    results = db.session.query(metadata.wfreq).all()
    df = pd.DataFrame(results)
    return jsonify(df.to_dict(orient="records"))


# @app.route("/sample/<sample>")
# @app.route("/sample)
# def sample():
#     return "here is the sample data"

# create route that renders index.html template

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
