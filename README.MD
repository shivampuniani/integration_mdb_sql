# Python Database Integration Project

This project connects to a Microsoft Access database, retrieves data, and inserts it into a SQL Server database. It demonstrates how to use Python to work with SQL and Access databases using `pyodbc`.

## Requirements

- Python 3.x
- `pyodbc` for database connection

## Setup

1. Clone the repository:
	git clone https://github.com/shivampuniani/integration_mdb_sql

2. Install the required Python dependencies:
	pip install -r requirements.txt

3. Configure the database connection:

Update the connection strings (if required in main.py) and config.ini for both SQL Server and Access databases.
SQL Server connection: Update the SERVER, DATABASE, UID, and PWD placeholders in config.ini file.
Access database file: Ensure the path to your .mdb file is correct.
Run the script:

python main.py
  
MDB-SQL-Integration-project/  
│  
├── main.py               # Your main Python program  
├── requirements.txt      # Python dependencies  
├── README.md             # Project documentation  
├── config.ini            # config file to store and configure sql server and file data   
├── .gitignore            # Git ignore rules  
└── log_file.txt          # Log file (will be generated when running the program)  
