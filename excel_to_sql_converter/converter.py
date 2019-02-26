import json
from modules.extract_excel_data import ExtractExcelData
import modules.write_to_sql as write_to_sql


def main():
    # open settings file
    with open("settings.json") as f:
        settings = json.load(f)
    excel_file_name = settings["excl_path"] + settings["excl_fname"]
    exceldata = ExtractExcelData(excel_file_name)
    exceldata.exctract_data()

    db_file_name = settings["db_path"] + settings["db_fname"]
    sql_data_base = write_to_sql.SQLiteDataBase(db_file_name)
    sql_data_base.open_connection()
    sql_data_base.write_data(exceldata)
    sql_data_base.commit_changes()
    sql_data_base.close_connection()


if __name__ == "__main__":
    main()