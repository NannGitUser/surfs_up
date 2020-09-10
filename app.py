# dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# flask
from flask import Flask, jsonify

# set up database
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect databases
Base = automap_base()
Base.prepare(engine, reflect=True)

#create classes and link to DB
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#flask set to run on name of file
app = Flask(__name__)

# set up flask routes
@app.route("/")

#set up welcome message and base info
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

#create sub route (rainfall)
@app.route("/api/v1.0/precipitation")
#def precipitation():
#   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
#   precipitation = session.query(Measurement.date, Measurement.prcp).\
#      filter(Measurement.date >= prev_year).all()
#   return

#use jsonify to make data presentable
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

#create sub route (stations)
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#create sub route (temperature)
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#create subroute (statistics)
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

    if not end: 
       results = session.query(*sel).\
    filter(Measurement.date <= start).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

    results = session.query(*sel).\
           filter(Measurement.date >= start).\
         filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

