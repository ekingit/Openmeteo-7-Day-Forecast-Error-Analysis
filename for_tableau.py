import datetime
import pandas as pd
from sqlalchemy import create_engine
import my_functions as mf


connection = mf.connection

#forecast table for tableau

cursor = connection.cursor()
cursor.execute("SELECT ct.country, ct.city, mf.* FROM max_forecast as mf LEFT JOIN cities_table as ct ON mf.id = ct.id ORDER BY (mf.id, mf.exec_date)")
dataset_max = cursor.fetchall()
cursor.execute("SELECT ct.country, ct.city, mf.* FROM min_forecast as mf LEFT JOIN cities_table as ct ON mf.id = ct.id ORDER BY (mf.id, mf.exec_date)")
dataset_min = cursor.fetchall()
cursor.execute("SELECT ct.country, ct.city, mf.* FROM avg_forecast as mf LEFT JOIN cities_table as ct ON mf.id = ct.id ORDER BY (mf.id, mf.exec_date)")

dataset = cursor.fetchall()
connection.commit()
cursor.close()

ds_max=pd.DataFrame(dataset_max)
ds_min = pd.DataFrame(dataset_min)
ds_avg = pd.DataFrame(dataset)


ds = pd.DataFrame()
start_date = datetime.date(2024,4,24)
for i in range(0,len(ds_max)):
    ds.loc[i,0] = ds_max.iloc[i,0]
    ds.loc[i,1] = ds_max.iloc[i,1]
    ds.loc[i,2] = ds_max.iloc[i,3]
    ds.loc[i,3] = 'max'
    exec_date = ds.loc[i,2]
    diff = (exec_date - start_date).days
    for j in range(0,7):
        ds.loc[i,4+j] = ds_max.iloc[i,4+diff+j]

for i in range(0,len(ds_min)):
    ds.loc[3514+i,0] = ds_min.iloc[i,0]
    ds.loc[3514+i,1] = ds_min.iloc[i,1]
    ds.loc[3514+i,2] = ds_min.iloc[i,3]
    ds.loc[3514+i,3] = 'min'
    exec_date = ds.loc[3514+i,2]
    diff = (exec_date - start_date).days
    for j in range(0,7):
        ds.loc[3514+i,4+j] = ds_min.iloc[i,4+diff+j]

for i in range(0,len(ds_avg)):
    ds.loc[7028+i,0] = ds_avg.iloc[i,0]
    ds.loc[7028+i,1] = ds_avg.iloc[i,1]
    ds.loc[7028+i,2] = ds_avg.iloc[i,3]
    ds.loc[7028+i,3] = 'avg'
    exec_date = ds.loc[7028+i,2]
    diff = (exec_date - start_date).days
    for j in range(0,7):
        ds.loc[7028+i,4+j] = ds_avg.iloc[i,4+diff+j]
        

ds.to_csv('forecast_db_tableau.csv', index=False)
engine = create_engine('postgresql://postgres:12345@localhost:5433/cities_api')
ds.to_sql('forecast_tableau', engine, index=False)


#error for tableau

cursor = connection.cursor()
cursor.execute("SELECT * FROM max_forecast ORDER BY (id, exec_date)")
dataset_max = cursor.fetchall()
cursor.execute("SELECT * FROM min_forecast ORDER BY (id, exec_date)")
dataset_min = cursor.fetchall()
cursor.execute("SELECT * FROM avg_forecast ORDER BY (id, exec_date)")
dataset = cursor.fetchall()
connection.commit()
cursor.close()

ds_max=pd.DataFrame(dataset_max)
ds_min = pd.DataFrame(dataset_min)
ds_avg = pd.DataFrame(dataset)


num=0
ds = pd.DataFrame()
for k in range(1,7):
    df_max = mf.error(ds_max,k)
    df_min = mf.error(ds_min,k)
    df_avg = mf.error(ds_avg,k)

    mean_max = mf.mean(df_max)
    mean_min = mf.mean(df_min)
    mean_avg = mf.mean(df_avg)
    abs_mean_max = mf.abs_mean(df_max)
    abs_mean_min = mf.abs_mean(df_min)
    abs_mean_avg = mf.abs_mean(df_avg)

    k_day_max = mf.avg_mean(mean_max)
    k_day_min = mf.avg_mean(mean_min)
    k_day_avg = mf.avg_mean(mean_avg)
    abs_k_day_max = mf.avg_mean(abs_mean_max)
    abs_k_day_min = mf.avg_mean(abs_mean_min)
    abs_k_day_avg = mf.avg_mean(abs_mean_avg)
    std_dev_k_day_max = mf.std_dev(mean_max)
    std_dev_k_day_min = mf.std_dev(mean_min)
    std_dev_k_day_avg = mf.std_dev(mean_avg)
    for i in range(0,len((df_max))):
        num=num+1
        ds.loc[num,0] = df_max.iloc[i,0]
        ds.loc[num,1] = 'max'
        ds.loc[num,2] = k
        ds.loc[num,3] = mean_max.iloc[i,1]
        ds.loc[num,4] = abs_mean_max.iloc[i,1]
        ds.loc[num,5] = k_day_max
        ds.loc[num,6] = abs_k_day_max
        ds.loc[num,7] = std_dev_k_day_max
        for j in range(k,14):
            ds.loc[num,7+j] = df_max.iloc[i,1+j-k]
    for i in range(0,len(df_min)):
        num=num+1
        ds.loc[num,0] = df_min.iloc[i,0]
        ds.loc[num,1] = 'min'
        ds.loc[num,2] = k
        ds.loc[num,3] = mean_min.iloc[i,1]
        ds.loc[num,4] = abs_mean_min.iloc[i,1]
        ds.loc[num,5] = k_day_min
        ds.loc[num,6] = abs_k_day_min
        ds.loc[num,7] = std_dev_k_day_min
        for j in range(k,14):
            ds.loc[num,7+j] = df_min.iloc[i,1+j-k]
    for i in range(0,len(df_avg)):
        num=num+1
        ds.loc[num,0] = df_avg.iloc[i,0]
        ds.loc[num,1] = 'avg'
        ds.loc[num,2] = k
        ds.loc[num,3] = mean_avg.iloc[i,1]
        ds.loc[num,4] = abs_mean_avg.iloc[i,1]
        ds.loc[num,5] = k_day_avg
        ds.loc[num,6] = abs_k_day_avg
        ds.loc[num,7] = std_dev_k_day_avg
        for j in range(k,14):
            ds.loc[num,7+j] = df_avg.iloc[i,1+j-k]


ds.to_csv('error_db.csv', index=False)
engine = create_engine('postgresql://postgres:12345@localhost:5433/cities_api')
ds.to_sql('error_tableau', engine, index=False)

cursor.close()
cursor = connection.cursor()
cursor.execute('SELECT ct.country, ct.city, et.* FROM error_tableau as et LEFT JOIN cities_table as ct ON et."0" = ct.id')
dst = cursor.fetchall()
dst=pd.DataFrame(dst)
dst.to_csv('error_db1.csv', index=False)




