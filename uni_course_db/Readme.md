# University course database CRUD implementation

## Tech stack

- Python
    - Streamlit
    - Mysqlclient
    - Pandas
- MySql


## Setup

### Setup the database
- Connect to mysql
    ```
    mysql -u username -p
    ```
- Create a new database
    ```mysql
    CREATE DATABASE uni_course_db;
    ```
- Run the db/schema.sql file to create the tables
    ```mysql
    source /path/to/db/schema.sql;
    ```

### Create .streamlit/secrets.toml file

_.streamlit/secrets.toml_
```toml
[connections.mysql]
dialect = "mysql"
driver = "mysqldb"
host = "localhost"
port = 3306
database = "uni_course_db"
username = "your_usename"
password = "your_password"
```

### Create a virtual environment and activate it

In windows
```
python -m venv .venv
.venv\Scripts\activate.bat
```

In linux/mac
```
python3 -m venv .venv
source .venv/bin/activate
```

### Download the required packages

```
pip install -r requirements.txt
```


## Run the app

```
streamlit run app.py
```