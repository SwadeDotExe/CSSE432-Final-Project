# Setup file for mySQL database testing

import mysql.connector
from mysql.connector import errorcode

# Connect to database
try:
    cnx = mysql.connector.connect(
        user='server', 
        password='thisisnotagoodpassword',
        host='swadeslab.rose-hulman.edu',
        database='spandora')
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your username or password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist.")
    else:
        print(err)

# Create table
TABLES = {}
TABLES['test'] = (
    "CREATE TABLE `test` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(14) NOT NULL,"
    "  `age` int(3) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

# Insert data into table
cursor.execute("INSERT INTO test (name, age) VALUES (%s, %s)", ('John Smith', 25))

# Query data from table
cursor.execute("SELECT * FROM test")
for row in cursor:
    print(row)

# Close connection
cursor.close()
cnx.close()

if __name__ == "__main__":
    print("Hello World")
    