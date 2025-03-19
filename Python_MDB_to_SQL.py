
import pyodbc, os, shutil
from datetime import datetime
import configparser

# Read configuration from config.ini
def get_db_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    db_config = {
        'server': config.get('database', 'server'),
        'database': config.get('database', 'database'),
        'username': config.get('database', 'username'),
        'password': config.get('database', 'password')
    }
    return db_config
test_no_track = ''
def db_connection():
    db_config = get_db_config()
    conn = pyodbc.connect(
        r'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={db_config["server"]};'
        f'DATABASE={db_config["database"]};'
        f'UID={db_config["username"]};'
        f'PWD={db_config["password"]}'
    )

    return conn

def  get_last_check_sql():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT TOP(1) [ID] FROM [dbo].[Test_MDB] order by timestamp desc")
    last_check = cursor.fetchall()
    try:
        last_check = int(last_check[0][0])
    except Exception as e:
        last_check = 0

    print(last_check)
    return last_check

def fetch_from_mdb(filepath,next_testid):
    #con = pyodbc.connect(f"DRIVER=Microsoft Access Driver (*.mdb, *.accdb); UID=admin; UserCommitSync=Yes; Threads=3; SafeTransactions=0; PageTimeout=5; MaxScanRows=8; MaxBufferSize=2048; FIL=MS Access; DriverId=25; DBQ={filepath}")
    access_conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            f'DBQ={os.path.abspath(filepath)};'
        )
    test_no_track = "next_testid- " + str(next_testid)
    con = pyodbc.connect(access_conn_str)
    
    cur = con.cursor()
    print(next_testid)
    sql = f"SELECT field.ID, field.Field1, field_data.Field_data1, field.Field2, field_data.Field_data2,field.Field3, field_data.Field_data3 FROM field RIGHT JOIN field_data ON field.ID = field_data.ID WHERE field.ID > {next_testid}"
    result = cur.execute(sql)
    rows = result.fetchall()
    rows = list(rows)
    cur.close()
    con.close()
    return rows

def push_to_sql(rows):
    conn = db_connection()
    cursor = conn.cursor()

    for row in rows:
        try:
            field_ID = row[0]
            field_Field1 =  row[1]
            field_data_Field_data1 =  row[2]
            field_Field2 =  row[3]
            field_data_Field_data2 =  row[4]
            field_Field3 =  row[5]
            field_data_Field_data3 =  row[6]
            
            #print(row[0] , date)
            cursor.execute('''INSERT INTO [dbo].[Test_MDB]
                                ([field_ID]  ,[field_Field1] ,[field_data_Field_data1] ,[field_Field2] ,[field_data_Field_data2] ,[field_Field3] ,[field_data_Field_data3], timestamp)
                           VALUES (  ?,          ?,               ?,                           ?,               ?,                       ?,            ?,            getdate())'''.format(length='multi-line', ordinal='second'),
                                    field_ID  ,field_Field1 ,field_data_Field_data1 ,field_Field2 ,field_data_Field_data2 ,field_Field3 ,field_data_Field_data3)
        except Exception as e:
            log_report(e)
            continue

    log_report("success")
    conn.commit()   # sql connection closed
    conn.close()

def log_report(e):
    # log_file = 'log.txt'
    log_file = r".\log_file.txt"
    with open(log_file, 'a') as log:
        log.write(f"{datetime.now()} + ' | ' +  {test_no_track} + ' | ' +  {e} \n")

if __name__ == "__main__":
    filepath = r".\Test.mdb"
    next_testid = get_last_check_sql()
    rows = fetch_from_mdb(filepath, next_testid)
    push_to_sql(rows)
    print("Datan Inserted in db Successfully.")  

