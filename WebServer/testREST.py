#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import mysql.connector
import audio_metadata
import os

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):

        self._set_response()

        # API Request - Songlist
        if str(self.path).startswith('/api/songlist'):
            print("API Request -- Songlist")
            self.wfile.write("{}".format(getSongList(self)).encode('utf-8'))
            return
        
        # API Request - Queue
        if str(self.path).startswith('/api/queue'):
            print("API Request -- Queue")
            self.wfile.write("{}".format(getSongList(self)).encode('utf-8'))
            return
        

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self._set_response()

        # API Request - Create new Song
        if str(self.path).startswith('/api/create'):
            print("API Request -- Create")
            self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

            # Add the song to the database
            addSongtoDB(post_data)
            return
        
        # API Request - Insert to Queue
        if str(self.path).startswith('/api/insert'):
            print("API Request -- Create")
            self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

            # Parse data
            post_data = post_data.decode('utf-8')

            # Add the song to queue
            addSongtoQueue(post_data) # Expecting songID
            return
        

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

# Function to handle mySQL database requests
def getSongList(self):

    # Connect to database
    ourDB = mysql.connector.connect(
        user='william', 
        password='changeme',
        host='swadeslab.rose-hulman.edu',
        database='SpandoraDB')
    cursor = ourDB.cursor()

    # # Insert data into Song_Library table
    # cursor.execute("INSERT INTO Song_Library (Song_Name, Artist_Name, Album_Name, Genre, Song_Length, Song_Path, Song_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)", ("Song1", "Artist1", "Album1", "Genre1", "1:00", "Path1", "69696969"))
    # ourDB.commit()

    # Query data from table
    cursor.execute("SELECT Song_Name FROM Song_Library")

    # Make JSON containing all rows for response
    r = []

    # Loop through each row in cursor
    for row in cursor:

        # Remove commas from row
        row = str(row).replace(',', '')

        # Remove parentheses from row
        row = str(row).replace('(', '')
        row = str(row).replace(')', '')

        # Remove apostrophes from row
        row = str(row).replace('\'', '')

        # Add each row to r
        r.append(row)

    # Close connection
    cursor.close()
    ourDB.close()

    # Print r
    print(r)

    # Return JSON response
    return r

# Function to add song to database
def addSongtoDB(songData):

    # Save the file to a temp file
    f = open("../AudioFiles/temp.mp3", "wb")
    f.write(songData)
    f.close()

    # Read metadata from temp file
    metadata = audio_metadata.load("../AudioFiles/temp.mp3")

    # Save metadata to variables
    artist = metadata['tags']['artist'][0]
    album = metadata['tags']['album'][0]
    title = metadata['tags']['title'][0]
    duration = metadata['streaminfo']['duration']
    genre = metadata['tags']['genre'][0]

    # Connect to database
    ourDB = mysql.connector.connect(
        user='william', 
        password='changeme',
        host='swadeslab.rose-hulman.edu',
        database='SpandoraDB')
    cursor = ourDB.cursor()

    # Get the next song ID
    cursor.execute("SELECT MAX(Song_ID) FROM Song_Library")
    for row in cursor:

        # Remove commas from row
        row = str(row).replace(',', '')

        # Remove parentheses from row
        row = str(row).replace('(', '')
        row = str(row).replace(')', '')
        
        # Remove apostrophes from row
        row = str(row).replace('\'', '')
        
        # Add 1 to old max ID
        newID = int(row) + 1

    # Rename temp file to actual title
    newPath = "../AudioFiles/" + str(newID) + "_" + title + ".mp3"
    os.rename("../AudioFiles/temp.mp3", newPath)

    # Add song to database
    cursor.execute("INSERT INTO Song_Library (Song_Name, Artist_Name, Album_Name, Genre, Song_Length, Song_Path, Song_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)", (title, artist, album, genre, duration, newPath, newID))
    ourDB.commit()

    # Close connection
    cursor.close()
    ourDB.close()

    return

# Function to add song to queue
def addSongtoQueue(songID):

    # Connect to database
    ourDB = mysql.connector.connect(
        user='william', 
        password='changeme',
        host='swadeslab.rose-hulman.edu',
        database='SpandoraDB')
    cursor = ourDB.cursor()

    # Add song to queue
    cursor.execute("INSERT INTO Queue (Song_ID) VALUES (%s)", (songID,))
    ourDB.commit()

    # Close connection
    cursor.close()
    ourDB.close()

    return

# Function to remove song from queue
def removeSongfromQueue(songID):

    # Connect to database
    ourDB = mysql.connector.connect(
        user='william', 
        password='changeme',
        host='swadeslab.rose-hulman.edu',
        database='SpandoraDB')
    cursor = ourDB.cursor()

    # Add song to queue
    cursor.execute("DELETE FROM Queue WHERE Song_ID = %s", (songID,))
    ourDB.commit()

    # Close connection
    cursor.close()
    ourDB.close()

    return

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()