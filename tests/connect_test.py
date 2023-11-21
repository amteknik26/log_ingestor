import psycopg2
from psycopg2 import OperationalError

# Replace with your actual DATABASE_URL
DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"

def test_connection(database_url):
    try:
        # Connect to the PostgreSQL server
        connection = psycopg2.connect(database_url)
        print("Connection to the PostgreSQL server successful")

        # Execute a simple query
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            print("PostgreSQL version:")
            print(cursor.fetchone())

    except OperationalError as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()
            print("Connection closed")

# Call the function with the specified DATABASE_URL

if __name__ == "__main__":
    test_connection(DATABASE_URL)