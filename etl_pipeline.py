# import pandas as pd
# from sqlalchemy import create_engine

# print("--- STARTING DATA PIPELINE IN VS CODE ---")

# # 1. Create sample DataFrame to simulate data extraction
# data = {
#     'employee_id': [1, 2, 3, 4],
#     'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
#     'department': ['Engineering', 'Marketing', 'Sales', 'Engineering'],
#     'salary': [75000, 60000, 55000, 80000]
# }

# df = pd.DataFrame(data)
# print("\nOriginal Data:")
# print(df)

# # 2. Data Cleaning & Transformation (Give Engineering a 10% raise)
# df.loc[df['department'] == 'Engineering', 'salary'] *= 1.10

# print("\nTransformed Data (After 10% Engineering Raise):")
# print(df)

# # 3. Write to a local SQLite database file to test SQL integration
# engine = create_engine('sqlite:///company_test.db')
# df.to_sql('employees', con=engine, if_exists='replace', index=False)

# # 4. Read it back from the database to verify the load step
# verify_df = pd.read_sql("SELECT * FROM employees;", con=engine)
# print("\nData successfully loaded and read back from SQL database:")
# print(verify_df)

# print("\n--- PIPELINE COMPLETED SUCCESSFULLY ---")



# import pandas as pd

# # Sample data
# data = {
#     'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
#     'department': ['Engineering', 'Marketing', 'Sales', 'Engineering'],
#     'salary': [75000, 60000, 55000, 80000]
# }

# df = pd.DataFrame(data)

# # Here is how you solve it:
# filtered_df = df[(df['department'] == 'Sales') & (df['salary'] < 80000)]

# print(filtered_df)

import requests
import pandas as pd
import sqlite3
from datetime import datetime

def extract_weather_data(city="London"):
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {city}. Status code: {response.status_code}")
        return None

def transform_weather_data(raw_data, city="London"):
    print("Transforming data...")
    current_condition = raw_data['current_condition'][0]
    
    # Adding a timestamp for when our pipeline ran (crucial for Data Engineering!)
    extracted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    transformed_dict = {
        "City": [city],
        "Temperature_C": [int(current_condition['temp_C'])],
        "Humidity_Percent": [int(current_condition['humidity'])],
        "Condition": [current_condition['weatherDesc'][0]['value']],
        "Observation_Time": [current_condition['observation_time']],
        "Extracted_At": [extracted_at]
    }
    
    df = pd.DataFrame(transformed_dict)
    print("Data transformed successfully!")
    return df

def load_weather_data(df, db_name="weather_data.db"):
    print("Loading data into SQLite database...")
    
    # Connect to (or create) the SQLite database file
    conn = sqlite3.connect(db_name)
    
    # Write the DataFrame to a SQL table named 'weather_logs'
    # if_exists='append' ensures new runs add rows rather than overwriting old ones!
    df.to_sql("weather_logs", conn, if_exists="append", index=False)
    
    # Let's verify by running a quick SQL query to read the data back!
    query_result = pd.read_sql("SELECT * FROM weather_logs", conn)
    
    conn.close()
    print("Data loaded successfully! Here is what is currently stored in your SQL database:")
    print(query_result)

# --- RUN THE FULL ETL PIPELINE ---
if __name__ == "__main__":
    target_city = "London" # You can change this to any city, like "Mumbai" or "New York"!
    
    raw_data = extract_weather_data(target_city)
    if raw_data:
        df_clean = transform_weather_data(raw_data, target_city)
        load_weather_data(df_clean)