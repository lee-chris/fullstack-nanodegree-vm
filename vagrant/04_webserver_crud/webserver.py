from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant

class WebServerHandler(BaseHTTPRequestHandler):

    engine = create_engine("sqlite:///restaurantmenu.db")
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    
    def do_GET(self):
        if self.path.endswith("/restaurants"):

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            message = ""
            message += "<html><body>"

            session = self.DBSession()
            for restaurant in session.query(Restaurant).all():
                message += """
  <div>
    <h1>{0}</h1>
    <a href="/restaurant/{1}/edit">Edit</a>
    <a href="/restaurant/{1}/delete">Delete</a>
  </div>""".format(restaurant.name, restaurant.id)

            message += "</body></html>"
            
            self.wfile.write(message)
            print message
            return

        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ""
            self.wfile.write(output)
            print output
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
