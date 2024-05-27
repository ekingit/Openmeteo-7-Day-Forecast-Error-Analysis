import numpy as np
import pandas as pd
import psycopg2

#Save the data as a pd dataframe and clean
df = pd.read_csv(r"C:\Users\PC\forecast_error\data\worldcities.csv")
df = df.drop(columns = {"id", "city", "iso3", "admin_name"})
df = df.rename(columns={"city_ascii":"city"})
df["population"]=df["population"].replace({np.nan: 0})
df["population"]=df["population"].astype(int)

#Connect to a PostgreSQL database
connection = psycopg2.connect(
    database = "cities_api",
    user = "postgres",
    password = "12345",
    host = "localhost",
    port = "5433")

cursor = connection.cursor()
cursor.execute('CREATE TABLE max_forecast (id INT,  exec_date DATE)')
cursor.execute('CREATE TABLE min_forecast (id INT,  exec_date DATE)')
cursor.execute('CREATE TABLE avg_forecast (id INT,  exec_date DATE)')
connection.commit()

# start_date+i is labeled by i
cursor = connection.cursor()
for i in range(0,6):#range(0,6)
    cursor.execute('ALTER TABLE max_forecast ADD COLUMN "%s" FLOAT', (i,))
    cursor.execute('ALTER TABLE min_forecast ADD COLUMN "%s" FLOAT', (i,))
    cursor.execute('ALTER TABLE avg_forecast ADD COLUMN "%s" FLOAT', (i,))
connection.commit()
cursor.close()