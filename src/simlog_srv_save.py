# UDP server example
import socket
import xml.parsers.expat
import re
import os
import sys
import signal
import threading
import cPickle
import datetime
from optparse import OptionParser

all_receives = [];
all_owner_info = {};

def getset_owner_info():
	global all_owner_info;
	for line in os.popen('getent passwd', 'r'):
		match = line.split(r':');
		all_owner_info[match[0]] = (match[2], match[4]);

def save_me(file):
	global all_receives;
	try:
		output = open(file, 'wb');
		# Pickle dictionary using protocol 0.
		cPickle.dump(all_receives, output);
		print "Creating file ", file;
		output.close();
	except:
		print "Unexpected error:", sys.exc_info()[0]
		return;

def load_me(file):
	global all_receives;
	try:
		input = open(file, 'rb');
		# Pickle dictionary using protocol 0.
		all_receives = cPickle.load(input);
		input.close();
	except:
		print "Unexpected error:", sys.exc_info()[0]
		return;

re_save_me = re.compile(r'<save_me>(.*)<.save_me>');
re_quit = re.compile(r'<quit>(.*)<.quit>');
def listen_update():
	global all_receives;
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
	server_socket.bind(("", 9600));

	print "UDPServer Waiting for client on port 9600";

	finish = False;
	while not finish:
		##
		data, address = server_socket.recvfrom(256);
		try:
			m = re_save_me.search(data);
			mq = re_quit.search(data);
			if m:
				print "%s : Saving to %s" % (datetime.datetime.now(), m.group(1));
				save_me(obj["save_me"]);
				continue;
			elif mq:
				print "%s : quit" % (datetime.datetime.now());
				finish = True;
				continue;
		except:
			pass;
		## Not a debug communication
		print "Received data:", data;
		all_receives.append(data);

if "__main__" == __name__:
	parser = OptionParser();
	parser.add_option("-f", "--save_file", dest="filename",
		help="Save, restore state FILE", metavar="FILE");
	(options, args) = parser.parse_args();
	if options.filename and os.path.exists(options.filename):
		print "Presuming state from ", options.filename;
		load_me(options.filename);

	##
	getset_owner_info();
	listen_update();

