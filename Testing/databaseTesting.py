# Setup file for mySQL database testing

import mysql.connector

# Connect to database
ourDB = mysql.connector.connect(
    user='william', 
    password='changeme',
    host='swadeslab.rose-hulman.edu',
    database='SpandoraDB')
cursor = ourDB.cursor()

# Insert data into Song_Library table
# cursor.execute("INSERT INTO Song_Library (Song_Name, Artist_Name, Album_Name, Genre, Song_Length, Song_Path, Song_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)", ("Song1", "Artist1", "Album1", "Genre1", "1:00", "Path1", "69696969"))

# Query data from table
cursor.execute("SELECT * FROM Song_Library")
for row in cursor:
    print(row)

cursor.execute("SELECT MAX(Song_ID) FROM Song_Library")
for row in cursor:
    # Remove commas from row
    row = str(row).replace(',', '')

    # Remove parentheses from row
    row = str(row).replace('(', '')
    row = str(row).replace(')', '')
    
    # Remove apostrophes from row
    row = str(row).replace('\'', '')
    
    print(row)

# Close connection
cursor.close()
ourDB.close()

if __name__ == "__main__":
    print("Hello World")
    