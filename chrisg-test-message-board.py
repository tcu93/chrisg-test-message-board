#!/usr/bin/env python3
#
# An HTTP server that's a message board.

# GET form
# POST to form
# GET what you just posted back
# GET-POST-GET

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import os

memory = []

form = '''<!DOCTYPE html>
  <title>Message Board</title>
  <form method="POST">
    <textarea name="message"></textarea>
    <br>
    <button type="submit">Post it!</button>
  </form>
  <pre>
{}
  </pre>
'''

class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-length', 0))
        data = self.rfile.read(length).decode()
        message2 = parse_qs(data)["message"][0] # message = HTML message
        message2 = message2.replace("<", "&lt;")
        memory.append(message2)
        self.send_response(303)  # redirect via GET
        self.send_header('Location', '/') # routes client back to root pg
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        mesg = form.format("\n".join(memory))
        self.wfile.write(mesg.encode())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))   # Use PORT 8000 if it's there.
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, Shortener)
    httpd.serve_forever()
