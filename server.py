from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import urllib.parse
import requests

API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
if not API_KEY:
    raise RuntimeError('請先設置 GOOGLE_MAPS_API_KEY 環境變數')

class ProxyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        url = urllib.parse.urlparse(self.path)

        if url.path == '/' or url.path == '':
            self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)

        if url.path == '/directions':
            query = urllib.parse.parse_qs(url.query)
            origin = query.get('origin', [''])[0]
            destination = query.get('destination', [''])[0]
            if not origin or not destination:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'origin/destination required')
                return

            gmaps_url = ('https://maps.googleapis.com/maps/api/directions/json?' +
                        f'origin={urllib.parse.quote(origin)}&destination={urllib.parse.quote(destination)}' +
                        '&mode=transit&transit_mode=subway&departure_time=now&key=' + API_KEY)
            resp = requests.get(gmaps_url, timeout=10)
            self.send_response(resp.status_code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(resp.content)
            return

        # serve static files for any other GET request
        self.path = url.path
        SimpleHTTPRequestHandler.do_GET(self)

    def do_HEAD(self):
        # allow browser or curl HEAD checks
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        return SimpleHTTPRequestHandler.do_HEAD(self)

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, ProxyHandler)
    print('Server running at http://localhost:8000')
    print('Open this URL in your browser or on your iPhone (if on same network)')
    print('Use /directions to get Google Directions data (proxied)')
    httpd.serve_forever()