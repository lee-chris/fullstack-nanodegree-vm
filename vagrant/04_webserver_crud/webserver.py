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
  </div>
""".format(restaurant.name, restaurant.id)

            message += "</body></html>"
            
            self.wfile.write(message)
            print message
            return

        elif self.path.endswith("/restaurants/new"):

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            message = """
<html>
  <body>
    <form method="post" action="/restaurants/new" enctype="multipart/form-data">
      Restaurant Name: <input type="text" name="name"/> <input type="submit" value="Add"/>
    </form>
  </body>
</html>
"""

            self.wfile.write(message)
            print message
            return

        elif self.path.endswith("/edit"):

            restaurant_id = self.path.split("/")[2]

            session = self.DBSession()
            restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            message = """
<html>
  <body>
    <form method="post" enctype="multipart/form-data">
      Restaurant Name: <input type="text" name="name" value="{0}"/> <input type="submit" value="Update"/>
    </form>
  </body>
</html>
""".format(restaurant.name)

            self.wfile.write(message)
            print message
            return

        elif self.path.endswith("/delete"):

            restaurant_id = self.path.split("/")[2]

            session = self.DBSession()
            restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            message = """
<html>
  <body>
    <form method="post" enctype="multipart/form-data">
      Are you sure you want to delete {0}? <input type="submit" value="Delete"/>
    </form>
  </body>
</html>
""".format(restaurant.name)

            self.wfile.write(message)
            print message
            return
        
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):

        if self.path.endswith("/restaurants/new"):
            
            restaurant_name = None
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                restaurant_name = fields.get('name')[0]

            # create new Restaurant record
            session = self.DBSession()
            session.add(Restaurant(name=restaurant_name))
            session.commit()

            self.send_response(302)
            self.send_header('Location', '/restaurants')
            self.end_headers()

        elif self.path.endswith("/edit"):

            restaurant_name = None
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                restaurant_name = fields.get('name')[0]
                
            restaurant_id = self.path.split("/")[2]

            session = self.DBSession()
            restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

            restaurant.name = restaurant_name

            session.add(restaurant)
            session.commit()

            self.send_response(302)
            self.send_header('Location', '/restaurants')
            self.end_headers()
            
        elif self.path.endswith("/delete"):

            restaurant_id = self.path.split("/")[2]

            session = self.DBSession()
            restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

            session.delete(restaurant)
            session.commit()

            self.send_response(302)
            self.send_header('Location', '/restaurants')
            self.end_headers()
            
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

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
