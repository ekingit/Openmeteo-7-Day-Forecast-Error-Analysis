# Openmeteo: 7-Day Forecast & Error Analysis

## Overview
This project aims to evaluate the accuracy of weather forecasts provided by the OpenMeteo API for capital cities around the world. By collecting and analyzing weather forecast data over a two-week period, I assess the reliability of this widely-used weather service using basic statistical measures such as mean absolute error and standard deviation.

## Data Collection
I utilized the OpenMeteo API to gather 7-day weather forecasts for the capital cities of various countries. This process was repeated daily for two weeks to ensure a comprehensive dataset for analysis. 

## Analysis
Statistical methods were employed to evaluate the accuracy of the OpenMeteo forecasts. Mean absolute error and standard deviation were calculated to quantify the disparities between the forecasted weather conditions and the actual observations over the two-week period.

## Dashboard
The results of the accuracy analysis are showcased through an interactive Tableau dashboard. This dashboard provides visualizations and summaries of the performance of the OpenMeteo API across different capital cities and weather parameters. Viewers can gain insights into the reliability of the forecasts through intuitive visualizations and informative summaries.

## Results
Openmeteo API is correct with %99.7 in the range of for 1-day forecast +/-0.951, 2-days +/-1.505, 3-days +/-2.102, 4-days +/-2.409, 5-days +/-2.789, 6 days +/-3.690. Detailed analysis of results are showcased in a [tableau dashborad](https://public.tableau.com/views/OpenMeteo7-DayForecastDashboardErrorAnalysis/OpenMeteo7-DayForecastDashboardErrorAnalysis?:language=en-US&:sid=&:display_count=n&:origin=viz_share_link)

## Installation and Usage

pip install -r requirements.txt
# Requirements
 - Data handling
numpy
pandas
 - Data collection
openmeteo_requests
requests_cache
retry_requests
 - Postgre SQL connection
psycopg2
sqlalchemy
# Usage
1 - Download .csv file of [worldcities](https://simplemaps.com/data/world-cities).
We use this data to extract capital cities and their coordinates.
2 - Run database.py 
Extract capital cities and their coordinates, clean and load it into PSQL database.
3 - Run forecast_daily_run everyday. 
This is a simple ETL pipeline which creates a PSQL table, updates it with columns and updates the table with 7-days weather forecasts.
I used Windows Task Schedular to automate this as it was sufficient for my purpose. One can use modern automation tools such as Apache Spark or Apache Airflow
4 - error_to_sql.py calculates mean, absolute mean, avarage mean and standard deviation and saves it to PSQL.
5 - for_tableau.py saves the error by couple of JOIN's as a .csv file appropriate for analysis.
6 - Finally, I use tableau to visualize the results.


Extract data from a database and an API.
Transform it (data cleaning).
Create a data structure and load the data to the database. 
Visualize. 


