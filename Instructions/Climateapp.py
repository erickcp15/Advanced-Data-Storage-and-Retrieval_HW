from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start-date/<start_date><br/>"
        f"/api/v1.0/start-date/<start_date>/end-date/<end_date><br/>"
    )

@app.route("/api/v1.0/precipitation")
def prec():
    
    query_12M = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date<='2017-08-23').\
    filter(Measurement.date>='2016-08-23').all()

    Date_Precip =[]
    for date, precip in query_12M:
        Date_Precip_dict = {}
        Date_Precip_dict["date"] = date
        Date_Precip_dict["prcp"] = precip
        Date_Precip.append(Date_Precip_dict)
    return jsonify(Date_Precip)

@app.route("/api/v1.0/stations")
def stations():

    The_stations = session.query(Station.station, Station.name).all()

    Stations_list = []
    for stations, names in  The_stations:
        Station_dict = {}
        Station_dict["Station"] = stations
        Station_dict["Names"] = names
        Stations_list.append(Station_dict)
    return jsonify(Stations_list)

@app.route("/api/v1.0/tobs")
def temp():

    query_hist = session.query(Measurement.date, Measurement.tobs).group_by(Measurement.date).\
    filter(Measurement.date <= '2017-08-23').filter(Measurement.date >='2016-08-23').all()

    Tobs_list = []
    for date, tobs in query_hist:
        Tobs_dict = {}
        Tobs_dict["date"] = date
        Tobs_dict["tobs"] = tobs
        Tobs_list.append(Tobs_dict)
    return jsonify(Tobs_list)

@app.route("/api/v1.0/start-date/<start_date>")
def start(start_date):

    start_date_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).group_by(Measurement.date).all()

    Start_date_list = []
    for Min, Avg, Max in start_date_query:
        start_date_dict = {}
        start_date_dict["min"] = Min
        start_date_dict["avg"] = Avg
        start_date_dict["max"] = Max
        Start_date_list.append(start_date_dict)
    return jsonify(Start_date_list)

@app.route("/api/v1.0/start-date/<start_date>/end-date/<end_date>")
def start_end(start_date, end_date):

    start_end_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).group_by(Measurement.date).all()

    Start_end_list = []
    for Min2, Avg2, Max2 in start_end_query:
        start_end_dict = {}
        start_end_dict["min"] = Min2
        start_end_dict["avg"] = Avg2
        start_end_dict["max"] = Max2
        Start_end_list.append(start_end_dict)
    return jsonify(Start_end_list)

if __name__ == '__main__':
    app.run(debug=True)
    