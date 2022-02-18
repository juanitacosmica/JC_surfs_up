# let's get our dependencies imported. The first thing we'll need to import is datetime, NumPy, and Pandas. 
# We assign each of these an alias so we can easily reference them later
import datetime as dt
import numpy as np
import pandas as pd
# Add the SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
# add the code to import the dependencies that we need for Flask
from flask import Flask, jsonify
# set up our database engine for the Flask application
engine = create_engine("sqlite:///hawaii.sqlite")
# let's reflect the database into our classes
Base = automap_base()
# to reflect the db
Base.prepare(engine, reflect=True)
# create variables
Measurement = Base.classes.measurement
Station = Base.classes.station
# create a session link from Python to our database
session = Session(engine)
# set up Flask
app = Flask(__name__)
# define the welcome route
@app.route("/")
# create a function welcome() with a return statement
def welcome():
    return(
        '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
# run the code
#flask run
# next route to build is for the precipitation analysis
@app.route("/api/v1.0/precipitation")
# we will create the precipitation() function
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)
# stations route
@app.route("/api/v1.0/stations")
# stations functions and jsonfy
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
# temperature route
@app.route("/api/v1.0/tobs")
# temperature function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
#test the code to see if it runs
#flask run
# Statistics Route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# Statistics Function
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
#test the code to see if it runs
#flask run
# 6. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)