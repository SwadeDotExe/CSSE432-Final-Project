import http.server
import socketserver
import mysql.connector
import audio_metadata
from os import path as path
import os



my_host_name = 'localhost'
my_port = 8080
#my_html_folder_path = '/Users/swade/Library/CloudStorage/GoogleDrive-swade@swadesdesigns.com/My Drive/College/Classes/CSSE432/FinalProject/WebServer'
my_html_folder_path = '/home/fosswe/csse432/CSSE432-Final-Project/WebServer'

my_home_page_file_path = 'index.html'


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    extensions_map = {
        '': 'application/octet-stream',
        '.manifest': 'text/cache-manifest',
        '.html': 'text/html',
        '.png': 'image/png',
        '.jpg': 'image/jpg',
        '.svg':    'image/svg+xml',
        '.css':    'text/css',
        '.js':'application/x-javascript',
        '.wasm': 'application/wasm',
        '.json': 'application/json',
        '.xml': 'application/xml',
    }

    def _set_headers(self):
        self.send_response(200)
        # Check if sending CSS File
        if self.path.endswith('.css'):
            self.send_header('Content-Type', 'text/css')
        else:
            self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', path.getsize(self.getPath()))
        self.end_headers()

    def getPath(self):

        # API Request - Songlist
        if str(self.path).startswith('/api/songlist'):

            print("API Request -- Songlist")

            songList = getSongList(self)

            # Respond to API request
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Data', songList)
            self.send_header('Content-Length', len(songList))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            # Set requested path to homepage for simplicity
            self.path = '/'

        if self.path == '/':
            content_path = path.join(
                my_html_folder_path, my_home_page_file_path)
        else:
            content_path = path.join(my_html_folder_path, str(self.path).split('?')[0][1:])
        return content_path
    


    def getContent(self, content_path):
        with open(content_path, mode='rb') as f:
            content = f.read()
        return bytes(content)

    def do_GET(self):
        self._set_headers()
        # Print URL requested
        print("URL requested: %s" % self.path)
        self.wfile.write(self.getContent(self.getPath()))

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

        

if __name__ == "__main__":   

    httpd = socketserver.TCPServer(("", my_port), MyHttpRequestHandler)
    httpd.allow_reuse_address = True
    print("Http Server Serving at port", my_port)     
    
    # # List files in http server directory
    # print("Files in %s:" % my_html_folder_path)
    # for f in os.listdir(my_html_folder_path):
    #     print(f)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print("Server stopped.")
