#############################
# Dependencies
#############################
# Import dependancies form Part 1 of HW
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime
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
        f"/api/v1.0/precipitation | Returns all precipitation data from all stations<br/>"
        f"/api/v1.0/stations | Returns the IDs and names/locations of all stations<br/>"
        f"/api/v1.0/tobs | Returns temperature observations from the most active station over the past year<br/>"
        f"/api/v1.0/start_date | Returns minimum, maximum, and average temperature for all data after your selected start date<br/>"
        f"/api/v1.0/start_date/end_date | Returns minimum, maximum, and average temperature for all data between your selected dates<br/>"
        f"For date queries, please use the format YYYY-MM-DD"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Return all precipitation data from all stations
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
    
    # Returns station ID and station name/location
    session = Session(engine)

    sel = [Measurement.station, Station.name]

    results = session.query(*sel).\
        filter(Measurement.station == Station.station).\
        group_by(Measurement.station).all()

    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
    # Returns all tobs within the past year from most active station
    session = Session(engine)

    # Finds most recent date in db
    most_recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date = list(np.ravel(most_recent))

    # Converts most recent date in db to datetime using 
    # strptime function from datetime. 
    most_recent_dt = datetime.strptime(most_recent_date[0], '%Y-%m-%d')

    # Finds date exactly 1 year ago
    one_year_back = most_recent_dt - dt.timedelta(days=365)

    sel = [Measurement.date, Measurement.tobs]
    results = session.query(*sel).\
        filter(Measurement.station == "USC00519281", Measurement.date >= one_year_back, Measurement.date <= most_recent_dt).\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()

    session.close()

    station_year = list(np.ravel(results))

    return jsonify(station_year)

@app.route("/api/v1.0/<start>")
def date_search1(start):
    
    # Returns tobs stats starting from user-selected start date
    session = Session(engine)

    # Convert entered date into datetime
    start_dt = datetime.strptime(start, '%Y-%m-%d')

    sel = [Measurement.station,
      func.min(Measurement.tobs),
      func.max(Measurement.tobs),
      func.avg(Measurement.tobs)]

    results = session.query(*sel).\
        filter(Measurement.date >= start_dt).all()

    session.close()

    tobs_stats1 = list(np.ravel(results))

    return jsonify(tobs_stats1)

@app.route("/api/v1.0/<start>/<end>")
def date_search2(start, end):
    
    # Returns tobs stats between user-selected start/end date
    session = Session(engine)

    # Convert entered dates into datetime
    start_dt = datetime.strptime(start, '%Y-%m-%d')
    end_dt = datetime.strptime(end, '%Y-%m-%d')

    sel = [Measurement.station,
      func.min(Measurement.tobs),
      func.max(Measurement.tobs),
      func.avg(Measurement.tobs)]

    results = session.query(*sel).\
        filter(Measurement.date >= start_dt, Measurement.date <= end_dt).all()

    session.close()

    tobs_stats2 = list(np.ravel(results))

    return jsonify(tobs_stats2)

if __name__ == '__main__':
    app.run(debug=True)


