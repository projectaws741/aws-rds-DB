from flask import Flask, render_template, request
import psycopg2
import boto3
from botocore.exceptions import BotoCoreError, ClientError

app = Flask(__name__)

# Function to get parameter from AWS Parameter Store
def get_parameter(name):
    try:
        client = boto3.client('ssm')
        parameter = client.get_parameter(Name=name, WithDecryption=True)
        return parameter['Parameter']['Value']
    except (BotoCoreError, ClientError) as e:
        print(f"Error fetching parameter {name}: {e}")
        return None

# Fetch database configuration from AWS Parameter Store
db_host = get_parameter('RDS_ENDPOINT')
db_port = '5432'  # Assuming the port is constant
db_user = get_parameter('RDS_USERNAME')
db_password = get_parameter('RDS_PASSWORD')
db_name = 'postgres'  # Assuming the database name is constant
table_name = 'postgres_user'

# Connect to the database
def get_db_connection():
    try:
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )
        return connection
    except psycopg2.Error as e:
        print("Connection to the database failed:", str(e))
        return None

# Create the 'user_info' table if it doesn't exist
def create_table():
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS {table_name} ("
                    "id SERIAL PRIMARY KEY,"
                    "name VARCHAR(255) NOT NULL,"
                    "email VARCHAR(255) NOT NULL,"
                    "country VARCHAR(255) NOT NULL"
                    ")"
                )
                connection.commit()
            print("Table created successfully!")
        except psycopg2.Error as e:
            print("Error while creating table:", str(e))
        finally:
            connection.close()
    else:
        print("Failed to connect to the database")

# Retrieve all records from the database
def get_all_records():
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table_name}")
                records = cursor.fetchall()
            return records
        except psycopg2.Error as e:
            print("Error while executing SQL query:", str(e))
        finally:
            connection.close()
    else:
        print("Failed to connect to the database")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    country = request.form['country']

    create_table()

    # Insert the data into the database
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = f"INSERT INTO {table_name} (name, email, country) VALUES (%s, %s, %s)"
                cursor.execute(sql, (name, email, country))
                connection.commit()
            return "Data stored successfully!"
        except psycopg2.Error as e:
            print("Error while executing SQL query:", str(e))
        finally:
            connection.close()
    else:
        return "Failed to connect to the database"

@app.route('/getdata')
def get_data():
    records = get_all_records()
    return render_template('data.html', records=records)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
