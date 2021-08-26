#############################
# Dependencies
#############################
# Import dependancies form Part 1 of HW
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc

# Import Flask
from flask import Flask, jsonify

############################
# Database Setup
# Copy/Pasted from Part 1
############################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

##########################
# Set Up Flask
##########################

app = Flask(__name__)

##########################
# API Routes
##########################

@app.route("/")
def index():
    return(
        f"Welcome to the Hawaii Climate API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    sel = [Measurement.date, Measurement.prcp]
    results = session.query(*sel).\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()
    
    session.close()

    prcp_data = list(np.ravel(results))

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    sel = [Measurement.station, Station.name]

    # Joins the two tables together on Station ID, also
    # groups by station ID, and counts rows containing a specific ID. 
    results= session.query(*sel).\
        filter(Measurement.station == Station.station).\
        group_by(Measurement.station).all()

    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    most_recent_date = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()
    

    session.close()


if __name__ == '__main__':
    app.run(debug=True)


