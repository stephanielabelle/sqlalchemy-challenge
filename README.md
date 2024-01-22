# Module 10 : SQLAlchemy Challenge
## Hawaii Climate Analysis

Objective: Utilize Python and SQLAlchemy to analyse precipitation and temperature data from 2010-2018 across various Hawaii weather stations.

### Part 1: SQLAlchemy in Jupyter Notebook  
The provided [hawaii.sqlite](Resources/hawaii.sqlite) file was reflected with SQLAlchemy in a [jupyter notebook](SurfsUp/climate_starter.ipynb).  Script file is located in the SurfsUp folder of this repository.  
Queries were utilized to find the following information:  
1. The most recent date in the dataset  
2. Precipitation data from the final 12 months  
3. Plotting of precipitation data  
4. Calculation of the number of weather stations  
5. Determination of the most active weather stations  
6. Summary statistics for the most active weather station  
7. Plotting of final 12 months of TOBS data of most active weather station  

### Part 2: Utilizing Flask for Design of Climate App  
The provided [hawaii.sqlite](Resources/hawaii.sqlite) file was reflected using SQLAlchemy in VSCode for utilization of Flask to create an [API](SurfsUp/app.py). Script file is located in the SurfsUp folder of this repository.  
The homepage shows all available routes:  
1. "/api/v1.0/precipitation" - dictionary of dates:precipitation for last 12 months of data  
2. "/api/v1.0/stations" - dictionary of station information  
3. "/api/v1.0/tobs" - temperature observations of most active weather station  
4. "/api/v1.0/<start>" - inputting a 'start' date returns summary statistics of temperature data for start date to end of dataset (input format = YYYY-MM-DD)  
5. /api/v1.0/<start>/<end>" - inputting a 'start' date and 'end' date returns summary statistics of temperature data for that date range (input format = YYYY-MM-DD)  
