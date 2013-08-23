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

class MyParser:
	re_dotslash = re.compile(r'[.\/]');
	# prepare for parsing
	def __init__(self):
		self.Parser = xml.parsers.expat.ParserCreate();
		self.Parser.CharacterDataHandler = self.handleCharData;
		self.Parser.StartElementHandler = self.handleStartElement;
		self.Parser.EndElementHandler = self.handleEndElement;
		self.tag = None;
		self.Parser.Parse("<root>", False);

	def __del__(self):
		self.Parser.Parse("</root>", True);

	def check_format_info(self, info):
		global all_owner_info;
		if "debug" in info:
			return;
		assert("user" in info);
		assert("owner" in info);
		assert("date" in info);
		assert(info["owner"] in all_owner_info);
		## Create date format
		spl = info["date"].split(r':');
		if '0' == spl[1][0]:
			spl[1] = spl[1][1];
		info["clsdate"] = "%s%s%s" % (spl[0], spl[1], spl[2]);
		## Format script path
		tmp = info["program"];
		tmp = self.re_dotslash.sub("_", tmp);
		info["clsprogram"] = tmp;

	# parse the XML file
	def parse(self, xml_string):
		self.obj = {};
		try:
			self.Parser.Parse(xml_string, False);
		except:
			print "ERROR: While parsing XML!";
			return None;
		self.check_format_info(self.obj);
		self.tag = None;
		return self.obj;

	# 3 handler functions
	def handleStartElement(self, name, attrs): self.tag = name;
	def handleEndElement(self, name): pass
	def handleCharData(self, data):
		if self.tag and self.tag not in self.obj:
			self.obj[self.tag] = data;

ignore_list = ["clsdate", "clsprogram", "user", "date", "program", "root", "data"];

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

def listen_update():
	global all_receives;
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
	server_socket.bind(("", 9600));

	print "UDPServer Waiting for client on port 9600";
	p = MyParser();

	finish = False;
	while not finish:
		##
		data, address = server_socket.recvfrom(256);
		try:
			obj = p.parse(data);
		except e:
			pass;
		## Not a debug communication
		if "save_me" in obj:
			print "%s : Saving to %s" % (datetime.datetime.now(), obj["save_me"]);
			save_me(obj["save_me"]);
		elif "quit" in obj:
			print "%s : quit" % (datetime.datetime.now());
			finish = True;
		else:
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

