# services/import_data.py

import os
import csv
from db.connections import get_connection

def import_data(folder_name: str) -> bool:
    conn = None
    cursor = None

    # Define correct FK-safe import order
    IMPORT_ORDER = [
        "User.csv",
        "AgentCreator.csv",
        "AgentClient.csv",
        "BaseModel.csv",
        "CustomizedModel.csv",
        "Configuration.csv",
        "InternetService.csv",
        "LLMService.csv",
        "DataStorage.csv",
        "ModelServices.csv",
        "ModelConfigurations.csv"
    ]

    try:
        conn = get_connection()
        cursor = conn.cursor()

        print("Executing schema.sql...")

        # Load schema
        schema_path = os.path.join("ddl", "schema.sql")
        with open(schema_path, "r") as f:
            schema_sql = f.read()

        for result in cursor.execute(schema_sql, multi=True):
            pass

        print("Schema loaded successfully.\n")

        folder_path = os.path.join(folder_name)

        # Import CSVs in the exact required order
        for filename in IMPORT_ORDER:
            file_path = os.path.join(folder_path, filename)

            if not os.path.exists(file_path):
                print(f"WARNING: {filename} not found, skipping.")
                continue

            table_name = filename[:-4]  # strip .csv

            print(f"--- Importing {filename} into {table_name} ---")

            with open(file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)  # skip header

                line_number = 1

                for row in reader:
                    line_number += 1
                    try:
                        placeholders = ", ".join(["%s"] * len(row))
                        sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
                        cursor.execute(sql, row)
                    except Exception as row_error:
                        print("\nERROR while inserting row:")
                        print(f"  Table:      {table_name}")
                        print(f"  Line:       {line_number}")
                        print(f"  Row data:   {row}")
                        print(f"  MySQL Error: {row_error}")
                        raise row_error

        conn.commit()
        print("\nAll data imported successfully!")
        return True

    except Exception as e:
        print("\nIMPORT FAILED:", e)
        if conn:
            conn.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
