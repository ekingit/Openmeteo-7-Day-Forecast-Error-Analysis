import math
import datetime
import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry
import psycopg2


#Connect to a PostgreSQL database
connection = psycopg2.connect(
    database = "cities_api",
    user = "postgres",
    password = "12345",
    host = "localhost",
    port = "5433"
)


#Select capitals of all countries within the database
def dataset():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM cities_table WHERE capital='primary'")
    return cursor.fetchall()

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)
URL = "https://api.open-meteo.com/v1/forecast"


#sth here
def forecast(x, y): #Coordinates -> dataframe
    """Returns """
    params = {"latitude": x, "longitude": y,"daily": ["temperature_2m_max", "temperature_2m_min"]}
    responses = openmeteo.weather_api(URL, params=params)
    response = responses[0]
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    daily_data["max"] = daily_temperature_2m_max
    daily_data["min"] = daily_temperature_2m_min
    daily_dataframe = pd.DataFrame(data = daily_data)
    daily_dataframe['date']=(pd.to_datetime(daily_dataframe["date"])).dt.date
    return daily_dataframe

today=datetime.date.today()
start_date=datetime.date(2024,4,24)
diff=(today-start_date).days

#Daily update
def update(ds,dfl):
    cursor=connection.cursor()
    cursor.execute('ALTER TABLE max_forecast ADD COLUMN "%s" FLOAT', (diff+6,))
    cursor.execute('ALTER TABLE min_forecast ADD COLUMN "%s" FLOAT', (diff+6,))
    cursor.execute('ALTER TABLE avg_forecast ADD COLUMN "%s" FLOAT', (diff+6,))
    connection.commit()
    cursor = connection.cursor()
    for i in range(0,len(dfl)):
        cursor.execute('''INSERT INTO max_forecast (id, exec_date, "%s", "%s", "%s", "%s", "%s", "%s", "%s") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                       (diff, diff+1, diff+2, diff+3, diff+4, diff+5, diff+6,
                        ds[i][0], dfl[i].iloc[0,0], dfl[i].iloc[0,1].item(),dfl[i].iloc[1,1].item(),dfl[i].iloc[2,1].item(),dfl[i].iloc[3,1].item(),dfl[i].iloc[4,1].item(),dfl[i].iloc[5,1].item(),dfl[i].iloc[6,1].item(),))
        cursor.execute('''INSERT INTO min_forecast (id, exec_date, "%s", "%s", "%s", "%s", "%s", "%s", "%s") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                       (diff, diff+1, diff+2, diff+3, diff+4, diff+5, diff+6,
                        ds[i][0], dfl[i].iloc[0,0], dfl[i].iloc[0,2].item(),dfl[i].iloc[1,2].item(),dfl[i].iloc[2,2].item(),dfl[i].iloc[3,2].item(),dfl[i].iloc[4,2].item(),dfl[i].iloc[5,2].item(),dfl[i].iloc[6,2].item(),))
        cursor.execute('''INSERT INTO avg_forecast (id, exec_date, "%s", "%s", "%s", "%s", "%s", "%s", "%s") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                       (diff, diff+1, diff+2, diff+3, diff+4, diff+5, diff+6,
                        ds[i][0], dfl[0].iloc[0,0], (dfl[i].iloc[0,1].item()+dfl[i].iloc[0,2].item())/2,(dfl[i].iloc[1,1].item()+dfl[i].iloc[1,2].item())/2,(dfl[i].iloc[2,1].item()+dfl[i].iloc[2,2].item())/2,(dfl[i].iloc[3,1].item()+dfl[i].iloc[3,2].item())/2,(dfl[i].iloc[4,1].item()+dfl[i].iloc[4,2].item())/2,(dfl[i].iloc[5,1].item()+dfl[i].iloc[5,2].item())/2,(dfl[i].iloc[6,1].item()+dfl[i].iloc[6,2].item())/2,))
    connection.commit()

#k-days error
def error(ds,k):
    start_date = datetime.date(2024,4,24)
    k_day_error = pd.DataFrame()
    index=0
    for i in range(k, len(ds)):
        exec_date = ds.loc[i,1]
        diff = (exec_date - start_date).days
        if ds.iloc[i,0] == ds.iloc[i-k,0]: #id
            k_day_error.loc[index,0] = ds.iloc[i,0] #id
            k_day_error.loc[index,diff] = [ds.iloc[i-k,2+diff] - ds.iloc[i,2+diff]] #1-day forecast - exec_date's temp.
        else:
            index=index+1
    return k_day_error


#k-day mean error
def mean(k_day_error):
    k_day_mean=pd.DataFrame()
    num=len(k_day_error.loc[0])
    for i in range(0,len(k_day_error)):
        mean=0
        for j in range(1,num):
            if k_day_error.iloc[i,j] < 100:
                mean = mean+k_day_error.iloc[i,j]
        k_day_mean.loc[i,0] = k_day_error.iloc[i,0]
        k_day_mean.loc[i,1] = mean/(num-1)
    return k_day_mean


#k-day absolute mean error, returns a matrix whose rows are capitals, columns are index, k^th day.
def abs_mean(k_day_error):
    k_day_mean=pd.DataFrame()
    num=len(k_day_error.loc[0])
    for i in range(0,len(k_day_error)):
        mean=0
        for j in range(1,num):
            if k_day_error.iloc[i,j] < 100:
                mean = mean+abs(k_day_error.iloc[i,j])
        k_day_mean.loc[i,0] = k_day_error.iloc[i,0]
        k_day_mean.loc[i,1] = mean/(num-1)
    return k_day_mean


def avg_mean(k_day_mean):
    num = len(k_day_mean)
    sum=0
    for i in range(0,num):
        sum = sum+k_day_mean.iloc[i,1]
    return sum/num 

def std_dev(k_day_error):
    col_num = len(k_day_error.loc[0])
    row_num = len(k_day_error)
    dev_res = 0
    for i in range(0,row_num):
        for j in range(1,col_num):
            if k_day_error.iloc[i,j] < 100:
                dev_res = dev_res + (k_day_error.iloc[i,j])**2
    dev_res = math.sqrt(dev_res/((col_num-1)*row_num))
    return dev_res
