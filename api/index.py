from http.server import BaseHTTPRequestHandler

from consumer.src.consumer import start_rabbitmq_consumer

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        start_rabbitmq_consumer()
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write('Init'.encode('utf-8'))
        return
