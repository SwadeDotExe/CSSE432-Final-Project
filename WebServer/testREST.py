#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import mysql.connector
import audio_metadata
import os
import json
from pygame import mixer

# Initialize mixer
mixer.init()

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(S, self).end_headers()

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
            self.wfile.write("{}".format(getSongQueue()).encode('utf-8'))
            return
        
        # API Request - Play
        if str(self.path).startswith('/api/play'):
            print("API Request -- Play")
            self.wfile.write("{}".format("gonna play now").encode('utf-8'))
            playSong()
            return
    
        # API Request - Pause
        if str(self.path).startswith('/api/pause'):
            print("API Request -- Play")
            self.wfile.write("{}".format("gonna stop now").encode('utf-8'))
            pauseSong()
            return
        
        # API Request - Resume
        if str(self.path).startswith('/api/resume'):
            print("API Request -- Play")
            self.wfile.write("{}".format("gonna keep going now").encode('utf-8'))
            resumeSong()
            return
        
        # API Request - Stop
        if str(self.path).startswith('/api/stop'):
            print("API Request -- Play")
            self.wfile.write("{}".format("gonna stop for good now").encode('utf-8'))
            stopSong()
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

def run(server_class=HTTPServer, handler_class=S, port=9000):
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

    # Query data from table
    cursor.execute("SELECT Song_Name,Song_ID,Artist_Name FROM Song_Library")

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

        # Find index of first number in row
        index = 0
        for i in range(len(row)):
            if row[i].isdigit():
                index = i
                break
        
        # Replace char at index -1 with underscore
        row = row[:index-1] + "_" + row[index-1+1:]

        # Find index of last number in row
        index = 0
        for i in range(len(row)):
            if row[i].isdigit():
                index = i

        # Replace char at index + 1 with underscore
        row = row[:index+1] + "_" + row[index+1+1:]

        # Add each row to r
        r.append(row)

    # Convert r to JSON
    r = json.dumps(r)

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
    newPath = "../AudioFiles/" + str(newID) + ".mp3"
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

def getSongQueue():

    # Connect to database
    ourDB = mysql.connector.connect(
        user='william', 
        password='changeme',
        host='swadeslab.rose-hulman.edu',
        database='SpandoraDB')
    cursor = ourDB.cursor()

    # Query data from table
    cursor.execute("SELECT Song_ID FROM Queue")

    # Get songs in queue
    songQueue = []
    for row in cursor:
            
        # Remove commas from row
        row = str(row).replace(',', '')

        # Remove parentheses from row
        row = str(row).replace('(', '')
        row = str(row).replace(')', '')

        # Remove apostrophes from row
        row = str(row).replace('\'', '')

        # Add each row to r
        songQueue.append(row)

    # Close connection
    cursor.close()
    ourDB.close()

    print(songQueue)
    return songQueue

def playSong():

    # Get songs in queue
    songsInQueue = getSongQueue()

    # Get first song in queue
    songID = songsInQueue[0]

    # Create song path
    songPath = "../AudioFiles/" + str(songID) + ".mp3"
    mixer.music.load(songPath)
    mixer.music.set_volume(0.5)
    mixer.music.play()

    # Remove song from queue
    removeSongfromQueue(songID)

def pauseSong():
    mixer.music.pause()

def resumeSong():
    mixer.music.unpause()

def stopSong():
    mixer.music.stop()

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()