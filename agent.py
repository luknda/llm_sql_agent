import sqlite3
import pandas as pd
import yaml
from llm_handler_factory import LLMHandlerFactory

# Load configuration from YAML file
try:
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
except FileNotFoundError:
    print("Error: The configuration file 'config.yaml' was not found.")
    exit(1)
except yaml.YAMLError as e:
    print(f"Error: An issue occurred while loading the YAML configuration: {e}")
    exit(1)

# Initialize SQLite Database
conn = sqlite3.connect('AAPL_daily.db')
cursor = conn.cursor()

# Initialize the LLM handler
try:
    llm_handler = LLMHandlerFactory.create_handler(config)
except ValueError as e:
    print(f"Error: {e}")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred during LLM handler initialization: {e}")
    exit(1)

# Set Pandas display options to show all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Define the database schema
schema = """
    Table: AAPL_daily
    Columns:
    - Date (text): The date of the record.
    - Time (text): The time of the record.
    - Open (double precision): The opening price of the stock.
    - High (double precision): The highest price of the stock.
    - Low (double precision): The lowest price of the stock.
    - Close (double precision): The closing price of the stock.
    - Volume (bigint): The volume of stock traded.
    """

# Function to handle SQL queries and return results as a DataFrame
def execute_sql_query(query):
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except sqlite3.Error as e:
        return f"SQL or database error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Function to export DataFrame to CSV
def export_to_csv(df, file_path):
    try:
        df.to_csv(file_path, index=False)
        print(f"Data exported successfully to {file_path}")
    except Exception as e:
        print(f"Failed to export data: {e}")

# Main function to process user queries
def process_query(nl_query, dates, export=False, file_path=None):
    sql_query = llm_handler.generate_sql_query(nl_query, schema, dates)
    if sql_query is None:
        print("Query handling failed due to invalid input.")
        return
    
    # print(f"Generated SQL Query: {sql_query}") # Uncomment this line to see the generated SQL query
    result = execute_sql_query(sql_query)
    
    # Display or export the result
    if isinstance(result, pd.DataFrame):
        if export and file_path:
            export_to_csv(result, file_path)
        else:
            print(result)
    else:
        print(result)

if __name__ == "__main__":
    # Main loop to interact with the user
    while True:
        try:
            print('''First, input your desired query in natural language. 
            Next step, indicate what date range you want to consider.
            Then, an option to save as csv will appear.
            Finally, an option to predict the stock value over the next three days will become available.
            CTRL+C to exit anytime.''') 
            user_query = input("Enter your query: ")
            dates = input("Enter the date range (if using very specific dates, remember to follow YYYY-MM-DD): ")
            
            export = input("Do you want to export the result to a CSV file? (yes/no): ").strip().lower() == 'yes'
            file_path = None
            if export:
                file_path = input("Enter the full path and file name for the CSV file (e.g., /path/to/file.csv): ").strip()
                if not file_path:
                    print("No file path provided. Skipping export.")
                    export = False

            process_query(user_query, dates, export, file_path)

            predict = input("Do you want predictions for the next three days? (yes/no): ").strip().lower() == 'yes'
            if predict:
                prediction_response = llm_handler.mock_price_prediction()
                print(prediction_response)
            
            print("Done! Feel free to continue or exit the program by pressing CTRL+C.\n")

        except KeyboardInterrupt:
            print("\n Exiting...")
            break