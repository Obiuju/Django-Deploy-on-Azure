import requests
import time
import psycopg2
from psycopg2 import sql

# PostgreSQL connection details
conn = psycopg2.connect(
    host="localhost",  # e.g., "localhost" or your remote host
    database="finalproject",  # Replace with your database name
    user="postgres",  # Replace with your PostgreSQL username
    password="Ujuobi93#"  # Replace with your PostgreSQL password
)
cur = conn.cursor()

# URL to fetch data
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data"

# Define the field names for each entry (based on the dataset documentation)
field_names = [
    "symboling", "normalized_losses", "make", "fuel_type", "aspiration", "num_doors",
    "body_style", "drive_wheels", "engine_location", "wheel_base", "length", "width",
    "height", "curb_weight", "engine_type", "num_cylinders", "engine_size", "fuel_system",
    "bore", "stroke", "compression_ratio", "horsepower", "peak_rpm", "city_mpg", "highway_mpg",
    "price"
]

# Create a table for the car data if it doesn't exist
create_table_query = sql.SQL("""
CREATE TABLE IF NOT EXISTS cars (
    id SERIAL PRIMARY KEY,
    symboling TEXT,
    normalized_losses TEXT,
    make TEXT,
    fuel_type TEXT,
    aspiration TEXT,
    num_doors TEXT,
    body_style TEXT,
    drive_wheels TEXT,
    engine_location TEXT,
    wheel_base TEXT,
    length TEXT,
    width TEXT,
    height TEXT,
    curb_weight TEXT,
    engine_type TEXT,
    num_cylinders TEXT,
    engine_size TEXT,
    fuel_system TEXT,
    bore TEXT,
    stroke TEXT,
    compression_ratio TEXT,
    horsepower TEXT,
    peak_rpm TEXT,
    city_mpg TEXT,
    highway_mpg TEXT,
    price TEXT
)
""")
cur.execute(create_table_query)
conn.commit()

while True:
    # Fetch data from the URL
    r = requests.get(url)
    
    if r.status_code == 200:
        data = r.text  # For plain text or CSV data
        
        # Split the data into lines
        lines = data.splitlines()
        
        # Iterate over each line and convert it into a dictionary
        for line in lines:
            values = line.split(',')
            
            # Insert the car data into the PostgreSQL table
            insert_query = sql.SQL("""
            INSERT INTO cars ({})
            VALUES ({})
            """).format(
                sql.SQL(', ').join(map(sql.Identifier, field_names)),
                sql.SQL(', ').join(sql.Placeholder() * len(field_names))
            )
            cur.execute(insert_query, values)
        
        conn.commit()
        
        # Sleep for 24 hours (24 hours * 60 minutes * 60 seconds)
        time.sleep(86400)
    else:
        print("Failed to fetch data, exiting...")
        exit()

cur.close()
conn.close()
