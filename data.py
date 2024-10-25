import psycopg2
from psycopg2 import sql
import random

# Connection details - replace with your actual details
DB_HOST = "pydb.cvcu6ymskoeq.us-east-1.rds.amazonaws.com"DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "KittuKrishna123"

# Sample data for insertion
names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hank", "Ivy", "Jack"]
emails = ["example@gmail.com", "sample@yahoo.com", "test@outlook.com", "info@mail.com", "admin@company.com"]
countries = ["USA", "Canada", "UK", "Germany", "Australia"]

try:
    # Establish a connection to the database
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS postgres_user (
            ID SERIAL PRIMARY KEY,
            Name VARCHAR(100),
            Email VARCHAR(100),
            Country VARCHAR(50)
        );
    """)
    conn.commit()

    insert_query = sql.SQL(
        "INSERT INTO postgres_user (Name, Email, Country) VALUES (%s, %s, %s)"
    )

    # Insert 100 records
    for _ in range(100):
        name = random.choice(names)
        email = f"{name.lower()}.{random.choice(emails)}"
        country = random.choice(countries)
        cur.execute(insert_query, (name, email, country))

    # Commit the transaction
    conn.commit()

    print("100 records inserted successfully.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close communication with the database
    if cur:
        cur.close()
    if conn:
        conn.close()
