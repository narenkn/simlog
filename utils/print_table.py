# UDP client example

import socket
import optparse
import os

parser = optparse.OptionParser()
parser.add_option("-f", "--file", dest="filename", default="./usage.html",
                  help="write report to FILE", metavar="FILE")
parser.add_option("-p", "--prog", dest="program", default='.*',
                  help="Program to filter")
parser.add_option("-u", "--user", dest="user", default=None,
                  help="Username to filter")

(options, args) = parser.parse_args()

if options.program:
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	data = """<data><debug> </debug><print_html>%s</print_html><file>%s</file>""" % (options.program, options.filename);
	if options.user:
		data += "<user>%s</user>" % options.user;
	data += "</data>";
	if "SIMLOG_DEBUGON" in os.environ:
		client_socket.sendto(data, ("localhost",9600));
	else:
		client_socket.sendto(data, ("idcas003",9600));
	client_socket.close();
else:
	print "Skipping since missing -p/-u option";

