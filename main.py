import mysql.connector
from local_settings import *

my_db = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

my_cursor = my_db.cursor()

my_cursor.execute("""CREATE TABLE person (
id int ,
first_name varchar (16) NOT NULL,
lastname varchar (16) NOT NULL,
age int NOT NULL,
PRIMARY KEY (id),
CHECK (age >= 18)
)""")

result = my_cursor.fetchall()

for res in result:
    print(res)
