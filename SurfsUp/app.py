# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt


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

# Route that returns a dictionary of precipitation data for last year of database with 'Date' as key
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= querydate).all()
    precip_list = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        precip_list.append(precip_dict)
    return jsonify(precip_list)

# Route that returns list of stations
@app.route("/api/v1.0/stations")
def stations_tab():
    stat = session.query(station.station, station.name, station.latitude, station.longitude, station.elevation).all()
    station_list = []
    for sta, nm, lat, lon, el in stat:
        station_dict = {}
        station_dict["Station"] = sta,
        station_dict["Name"] = nm,
        station_dict["Latitude"] = lat,
        station_dict["Longitude"] = lon,
        station_dict['Elevation'] = el
        station_list.append(station_dict)
    return jsonify(station_list)

# Route that returns temperature observations from last year of most active station 'USC00519281'
@app.route("/api/v1.0/tobs")
def tobs():
    activestation = session.query(measurement.tobs).\
    filter(measurement.station == 'USC00519281').\
    filter(measurement.date >= querydate).all()
    temp_list = list(np.ravel(activestation))
    return jsonify(temp_list)

# Route that returns summary statistics of temperature data with user defined start date
@app.route("/api/v1.0/<start>", methods=['GET'])
def startdate(start):
    sel = [ func.min(measurement.tobs),
            func.max(measurement.tobs),
            func.avg(measurement.tobs)]
    data = session.query(*sel).\
        filter(measurement.date >= start).all()
    for mi, mx, av in data:
        stats = {"Minimum Temperature":mi, "Maximum Temperature":mx, "Average Temperature":av}
    return jsonify(stats)

# Route that returns summary statistics of temperature data with user defined start and end date
@app.route("/api/v1.0/<start>/<end>", methods=['GET'])
def startend(start, end):
    sel = [ func.min(measurement.tobs),
            func.max(measurement.tobs),
            func.avg(measurement.tobs)]
    data = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()
    for mi, mx, av in data:
        stats = {"Minimum Temperature":mi, "Maximum Temperature":mx, "Average Temperature":av}
    return jsonify(stats)


if __name__ == '__main__':
    app.run(debug=True)