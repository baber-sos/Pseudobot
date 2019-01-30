from urlparse import urlparse
import SimpleHTTPServer
import SocketServer
import urllib2


class requestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            query = urlparse(self.path).query
            query_components = dict(qc.split("=") for qc in query.split("&"))
            if "query" in query_components:
                actualQuery = query_components["query"]
                actualQuery = urllib2.unquote(actualQuery)
            elif "idtoken":
                idtoken = query_components["idtoken"]
                token = urllib2.unquote(token)
            #send code 200 response
            self.send_header('Access-Control-Allow-Origin','*')
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.send_response(200)

            #send header first

            # query = 
            print token
            # response = chatbot.get_response(actualQuery)
            #send file content to client
            self.wfile.write(response)

            # self.wfile.write('Blah')
            return
        except:
            self.wfile.write("");
            pass

Handler = requestHandler
PORT = 8000


server = SocketServer.TCPServer(("", PORT), Handler)

server.serve_forever()
