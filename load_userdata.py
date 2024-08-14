import requests
import psycopg2
import time

# PostgreSQL connection parameters
conn = psycopg2.connect(
    host="localhost",  # e.g., "localhost" or your remote host
    database="group9",  # Replace with your database name
    user="postgres",  # Replace with your PostgreSQL username
    password="Ujuobi93#"  # Replace with your PostgreSQL password
)

cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_profile (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        username VARCHAR(50),
        password VARCHAR(100),
        email VARCHAR(100),
        phone VARCHAR(20),
        picture VARCHAR(255)
    )
''')
conn.commit()

def fetch_and_insert_data():
    # URL to request 12 random user datasets
    url = "https://randomuser.me/api/?results=12"

    # Make the API request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract the list of users
        users = data['results']

        for user in users:
            # Extract necessary fields
            first_name = user['name']['first'] if 'name' in user and 'first' in user['name'] else None
            last_name = user['name']['last'] if 'name' in user and 'last' in user['name'] else None
            username = user['login']['username'] if 'login' in user and 'username' in user['login'] else None
            password = user['login']['password'] if 'login' in user and 'password' in user['login'] else None
            email = user['email'] if 'email' in user else None
            phone = user['phone'] if 'phone' in user else None
            picture = user['picture']['large'] if 'picture' in user and 'large' in user['picture'] else None

            # Insert the data into PostgreSQL
            cursor.execute('''
                INSERT INTO user_profile (first_name, last_name, username, password, email, phone, picture)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (first_name, last_name, username, password, email, phone, picture))

        conn.commit()
        print("Data successfully uploaded to PostgreSQL.")
    else:
        print("Failed to retrieve data:", response.status_code)

# Fetch and insert data every 24 hours
while True:
    fetch_and_insert_data()
    time.sleep(86400)  # Sleep for 24 hours


