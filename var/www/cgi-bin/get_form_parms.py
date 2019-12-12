#!/usr/bin/python3

import cgi
import cgitb
cgitb.enable(display=0, logdir="/logs")


def application(environ, start_response):
    params = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

    word = params.getfirst('word', default=None)

    #output = ("<h2>Hello %s %s</h2>" + (word))
    output = "<h2>Hallo " + word +  "</h2>"

    #print("Content-type:text/html\r\n\r\n")
    #print("<html>")
    #print("<head>")
    #print("<title>Hello - Second CGI Program</title>")
    #print("</head>")
    #print("<body>")
    #print("<h2>Hello %s %s</h2>" % (word))
    #print("</body>")
    #print("</html>")

    status = "200 OK"
    output = output.encode()
    response_headers = [("Content-type", "text/html; charset=UTF-8"),
                        ("Content-Length", str(len(output)))]
    start_response(status, response_headers)
    return [output]
