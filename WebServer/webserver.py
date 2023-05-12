import http.server
import socketserver
from os import path as path
import os



my_host_name = 'localhost'
my_port = 8080
my_html_folder_path = '/Users/swade/Library/CloudStorage/GoogleDrive-swade@swadesdesigns.com/My Drive/College/Classes/CSSE432/FinalProject/WebServer'

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
        self.wfile.write(self.getContent(self.getPath()))
        

if __name__ == "__main__":   

    httpd = socketserver.TCPServer(("", my_port), MyHttpRequestHandler)
    print("Http Server Serving at port", my_port)     
    
    # List files in http server directory
    print("Files in %s:" % my_html_folder_path)
    for f in os.listdir(my_html_folder_path):
        print(f)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print("Server stopped.")