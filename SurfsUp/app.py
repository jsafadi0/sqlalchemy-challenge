# Import the dependencies.
import numpy as np
import re
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,func
from flask import Flask,jsonify





#################################################
# Database Setup
#################################################
engine=create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base=automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement=Base.classes.measurement
station=Base.classes.station


# Create our session (link) from Python to the DB

#################################################
# Flask Setup
#################################################
apps=Flask(__name__)




#################################################
# Flask Routes
#################################################
@apps.route("/")
def homepage():
    """all available routes."""
    return(
        f"Welcome to Hawaii Climate Analysis Homepage. The Available Routes:<br/>"
        f"<br/>"
        f"Precipitation Data for One Year:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"List of Active Weather Stations:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Temperature Observations of the Most-Active Station for One Year:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"The Average, Maximum, and Minimum Temperature for a specified Start Date(Format:yyyy-mm-dd):<br/>"
        f"/api/v1.0/<start><br/>"
        f"<br/>"
        f"The Average, Maximum, and Minimum Temperature for a specified Start and End Date(Format:yyyy-mm-dd/yyyy-mm-dd):<br/>"
        f"/api/v1.0/<start><br/>"
    )

@apps.route("/api/v1.0/precipitation")
def precipitation():
    session=Session(engine)
    date_ago=dt.date(2017,8,23)-dt.timedelta(days=365)
    result=session.query(measurement.date,measurement.prcp).filter(measurement.date>=date_ago).all()
    session.close()
    prcp_data=[]
    for date,prcp in result:
        prcp_dict={}
        prcp_dict[date]=prcp
        prcp_data.append(prcp_dict)
    return jsonify(prcp_data)

@apps.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    station1=session.query(station.name,station.station,station.elevation,station.latitude,station.longitude).all()
    session.close()
    station_data=[]
    for name,station,elevation,latitude,longitude in station1:
        station_dict={}
        station_dict["Name"]=name
        station_dict["Station ID"]=station
        station_dict["Elevation"]=elevation
        station_dict["Latitude"]=latitude
        station_dict["Longitude"]=longitude
        station_data.append(station_dict)
    return jsonify(station_data)



@apps.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    date_ago=dt.date(2017,8,23)-dt.timedelta(days=365)
    active_stations=session.query(measurement.date,measurement.tobs).filter(measurement.station=='USC00519281').filter(measurement.date>=date_ago).all()
    session.close()
    most_active=[]
    for date,temp in active_stations:
        active_dict={}
        active_dict[date]=temp
        most_active.append(active_dict)
    return jsonify(most_active)


@apps.route("/api/v1.0/<start>")
def start(start):
    session=Session(engine)
    query_result=session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date>=start).all()
    session.close()
    start_date=[]
    for min,max,avg in query_result:
        start_dict={}
        start_dict["Minimum Temperature"]=min
        start_dict["Maximum Temperature"]=max
        start_dict["Average Temperature"]=avg
        start_date.append(start_dict)
    return jsonify(start_date)

@apps.route("/aou.v1.0/<start>/<end>")
def range_date(start,end):
    session=Session(engine)
    query_results=session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tob)).filter(measurement.date>=start).filter(measurement.date<=end).all()
    session.close()
    range_date=[]
    for min,max,avg in query_results:
        range_dict={}
        range_dict["Minimum Temperature"]=min
        range_dict["Maximum Temperature"]=max
        range_dict["Average Temperature"]=avg
        range_date.append(range_dict)
        return jsonify(range_date)
if __name__=='__main__':
    apps.run(debug=True)




    
