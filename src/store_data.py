import pymysql
import json
import os

# Database connection parameters
DB_CONFIG = {
    'host': '192.168.0.1',
    'port': 6603,
    'user': 'galeras',
    'passwd': 'galeras234',
    'db': 'galeras'
}

# Directory where the JSON file will be saved
OUTPUT_DIR = "/workspaces/galeras-benchmark/datasets/code_smells"  # Change this to your desired directory


def fetch_data():
    """
    Connects to the MySQL database, fetches all data from the 
    distinct_repo_code_dataset table, and returns the result as a list of dictionaries.
    """
    try:
        # Connect to the database
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            passwd=DB_CONFIG['passwd'],
            db=DB_CONFIG['db'],
            cursorclass=pymysql.cursors.DictCursor  # This ensures rows are returned as dictionaries
        )
        print("Database connection established.")

        with connection:
            with connection.cursor() as cursor:
                # Execute the query to fetch records with n_ast_errors = 0
                query = "SELECT * FROM distinct_repo_code_dataset WHERE n_ast_errors = 0"
                cursor.execute(query)
                results = cursor.fetchall()
                print(f"Fetched {len(results)} records with n_ast_errors = 0 from the database.")
                return results

    except Exception as e:
        print("An error occurred while fetching data:", e)
        return []


def save_to_json(data, directory, filename="distinct_repo_code_dataset.json"):
    """
    Saves the provided data to a JSON file in the specified directory.

    Args:
        data (list): The data to be saved (list of dictionaries).
        directory (str): The directory in which to save the file.
        filename (str): The name of the JSON file.
    """
    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")

    # Construct full file path
    file_path = os.path.join(directory, filename)
    
    try:
        # Write data to JSON file with pretty-printing
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Data successfully saved to '{file_path}'.")
    except Exception as e:
        print("An error occurred while saving data to JSON:", e)



data = fetch_data()
    
if data:
    # Save the fetched data to a JSON file
    save_to_json(data, OUTPUT_DIR)
else:
    print("No data to save.")