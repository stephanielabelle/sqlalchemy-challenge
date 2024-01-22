
# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from statistics import mean

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite", echo=True)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)
print(f' The tables are named {Base.classes.keys()}')

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
querydate = dt.date(2017,8,23) - dt.timedelta(days=365)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available routes"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= querydate).all()
    precip_list = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        precip_list.append(precip_dict)
    return jsonify(precip_list)

@app.route("/api/v1.0/stations")
def stations_tab():
    station_list = session.query(station.station).all()
    station_names = list(np.ravel(station_list))
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    activestation = session.query(measurement.tobs).\
    filter(measurement.station == 'USC00519281').\
    filter(measurement.date >= querydate).all()
    temp_list = list(np.ravel(activestation))
    return jsonify(temp_list)


@app.route("/datecheck/<date>", methods=['GET'])
def datecheck(date):
    data = session.query(measurement.tobs).\
    filter(measurement.date >= date).all()
    tobs_list = list(np.ravel(data))
    min_temp = min(tobs_list)
    max_temp = max(tobs_list)
    avg_temp = mean(tobs_list)
    temp_dict = {"min_temp":min_temp, "max_temp":max_temp, "avg_temp":avg_temp}
    return temp_dict


@app.route("/api/v1.0/<start>", methods=['GET'])
def startdate(start):
    data = session.query(measurement.tobs).filter(measurement.date >= start).all()
    tobs_list = list(np.ravel(data))
    min_temp = min(tobs_list)
    max_temp = max(tobs_list)
    avg_temp = mean(tobs_list)
    temp_dict = {"min_temp":min_temp, "max_temp":max_temp, "avg_temp":avg_temp}
    return jsonify(temp_dict)

@app.route("/api/v1.0/<start>/<end>", methods=['GET'])
def startend(start, end):
    data = session.query(measurement.tobs).\
    filter(measurement.date >= start).\
    filter(measurement.date <= end).all()
    tobs_list = list(np.ravel(data))
    min_temp = min(tobs_list)
    max_temp = max(tobs_list)
    avg_temp = mean(tobs_list)
    temp_dict = {"min_temp":min_temp, "max_temp":max_temp, "avg_temp":avg_temp}
    return jsonify(temp_dict)


if __name__ == '__main__':
    app.run(debug=True)