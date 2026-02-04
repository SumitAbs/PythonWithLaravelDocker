import mysql.connector
from mysql.connector import Error

def connect_to_database():
    """
    Function to establish a connection to the MySQL database.
    """
    try:
        # Initializing connection with database credentials
        connection = mysql.connector.connect(
            host='localhost',
            database='my_laravel_db',
            user='root',
            password='password'
        )

        if connection.is_connected():
            print("Successfully connected to the database")
            
            # Fetching server information
            db_info = connection.get_server_info()
            print(f"MySQL Server version: {db_info}")

    except Error as e:
        # Handling connection errors gracefully
        print(f"Error while connecting to MySQL: {e}")

    finally:
        # Closing the connection to free up resources
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    connect_to_database()