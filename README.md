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
The accuracy assessment reveals that the OpenMeteo API achieves 99.7% accuracy within a range of 
* +/-0.951 for 1-day,
* +/-1.505 for 2-day,
* +/-2.102 for 3-day,
* +/-2.409 for 4-day,
* +/-2.789 for 5-day,
* and +/-3.690 for 6-day

Detailed analysis of results are showcased in a [tableau dashborad](https://public.tableau.com/views/OpenMeteo7-DayForecastDashboardErrorAnalysis/OpenMeteo7-DayForecastDashboardErrorAnalysis?:language=en-US&:sid=&:display_count=n&:origin=viz_share_link).

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
1 - **Download Data:** Obtain .csv file of [worldcities](https://simplemaps.com/data/world-cities). It consists of city, country names, coordinates, administrative status.

2 - **Run `database.py`:** Execute this script to extract capital cities and their coordinates from the downloaded data, clean it and load it into PostgreSQL (PSQL) database.

3 - **Run `forecast_daily_run.py`:** This script serves as a simple Extract, Transform, Load (ETL) pipeline. It creates a table in PSQL server, adds necessary columns and updates the table with 7-day weather forecasts retrieved from the OpenMeteo API. It must be run daily. I used Windows Task Schedular to automate this as it was sufficient for my purpose. One can use modern tools such as Apache Airflow.

4 - **Run `error_to_sql.py`:** This script calculates the mean, absolute mean, average mean, and standard deviation of forecast errors. The results are saved to the PostgreSQL database for further analysis.

5 - **Run `for_tableau.py`:** This script prepares the error data with appropriate JOIN operations and saves it as a .csv file suitable for analysis.

6 - **Visualize results with Tableau:** Finally, utilize Tableau to create visualizations and analyze the forecast accuracy.





