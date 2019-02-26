import json
from modules.extract_excel_data import ExtractExcelData
import modules.write_to_sql as write_to_sql


def main():
    """Convert excel file into sqlite
    
    1) open settings file "settings.json" 
        "excl_path" -- path to the excel file
        "excl_fname"-- name of the excel file
        "db_path":  -- path to the data base file
        "db_fname": -- name of the data base file
    2) Extract data from the excel file into 'excel_data'
        attributes of excel_data correspond to SQL tables:
        - artists
        - locations
        - techniques
        - paintings
        - categories
        - subcategories
    3) Create new database, and connect to it
    4) write each excel_data field into corresponding table in DB
    5) commit changes and close DB
    """

    # open settings
    with open("settings.json") as f:
        settings = json.load(f)
    
    # Extract data from excel file
    excel_file_name = settings["excel_path"] + settings["excel_file_name"]  # full path to the excel file
    excel_data = ExtractExcelData(excel_file_name)  # Initialise ExtractExcelData instance
    excel_data.read_excel_data()  # open excel file and read all information from it
    excel_data.structure_data()  # structure all data

    # Insert data into the database
    db_file_name = settings["db_path"] + settings["db_file_name"]
    sql_data_base = write_to_sql.SQLiteDataBase(db_file_name)
    sql_data_base.open_connection()
    sql_data_base.write_data(excel_data)
    sql_data_base.commit_changes()
    sql_data_base.close_connection()


if __name__ == "__main__":
    main()
