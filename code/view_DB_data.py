#view data in the Postgresql DB

import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="weather_data",
    user="postgres",
    password="password"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM weather_data WHERE max_temp = -999.9")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
