#import sys
from flask import Flask, Response
application = Flask(__name__)

#def application(environ, start_response):
#	start_response('200 OK', [('Content-Type', 'text/plain')])
#	v = sys.version_info
#	str = 'hello world from %d.%d.%d!\n' % (v.major, v.minor, v.micro)
#	return [bytes(str, 'UTF-8')]

@application.route("/")
def hello():
	return "Hello World!"

if __name__ == "__main__":
	application.run()
