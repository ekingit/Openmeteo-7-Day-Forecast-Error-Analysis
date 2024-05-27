#calculate and save error in sql database

import pandas as pd
from sqlalchemy import create_engine
import my_functions as mf


connection = mf.connection

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
ds = pd.DataFrame(dataset)

engine = create_engine('postgresql://postgres:12345@localhost:5433/cities_api')

max_one_day_error = mf.error(ds_max,1)
min_one_day_error = mf.error(ds_min,1)
avg_one_day_error = mf.error(ds,1)

max_one_day_error.to_sql('max_one_day_error', engine, index=False)
min_one_day_error.to_sql('min_one_day_error', engine, index=False)
avg_one_day_error.to_sql('avg_one_day_error', engine, index=False)


max_two_day_error = mf.error(ds_max,2)
min_two_day_error = mf.error(ds_min,2)
avg_two_day_error = mf.error(ds,2)

max_two_day_error.to_sql('max_two_day_error', engine, index=False)
min_two_day_error.to_sql('min_two_day_error', engine, index=False)
avg_two_day_error.to_sql('avg_two_day_error', engine, index=False)

max_three_day_error = mf.error(ds_max,3)
min_three_day_error = mf.error(ds_min,3)
avg_three_day_error = mf.error(ds,3)

max_three_day_error.to_sql('max_three_day_error', engine, index=False)
min_three_day_error.to_sql('min_three_day_error', engine, index=False)
avg_three_day_error.to_sql('avg_three_day_error', engine, index=False)

max_four_day_error = mf.error(ds_max,4)
min_four_day_error = mf.error(ds_min,4)
avg_four_day_error = mf.error(ds,4)

max_four_day_error.to_sql('max_four_day_error', engine, index=False)
min_four_day_error.to_sql('min_four_day_error', engine, index=False)
avg_four_day_error.to_sql('avg_four_day_error', engine, index=False)

max_five_day_error = mf.error(ds_max,5)
min_five_day_error = mf.error(ds_min,5)
avg_five_day_error = mf.error(ds,5)

max_five_day_error.to_sql('max_five_day_error', engine, index=False)
min_five_day_error.to_sql('min_five_day_error', engine, index=False)
avg_five_day_error.to_sql('avg_five_day_error', engine, index=False)

max_six_day_error = mf.error(ds_max,6)
min_six_day_error = mf.error(ds_min,6)
avg_six_day_error = mf.error(ds,6)

max_six_day_error.to_sql('max_six_day_error', engine, index=False)
min_six_day_error.to_sql('min_six_day_error', engine, index=False)
avg_six_day_error.to_sql('avg_six_day_error', engine, index=False)