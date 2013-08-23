import StringIO
import operator
import os
import sys
import re
import socket

## 
def decrypt_simlog():
	if not os.path.exists("simlog.exml"): return "";
	f = open("simlog.exml", "rb") # binary required
	str2 = f.read()
	f.close()
	# create two streams in memory the size of the string str2
	# one stream to read from and the other to write the XOR crypted character to
	sr = StringIO.StringIO(str2)
	sw = StringIO.StringIO(str2)
	# make sure we start both streams at position zero (beginning)
	sr.seek(0)
	sw.seek(0)
	#str3 = "" # test
	for k in range(len(str2)):
		# read one character from stream sr
		c = sr.read(1)
		b = ord(c)
		# xor byte with password byte
		t = operator.xor(b, 42)
		z = chr(t)
		# advance position to k in stream sw then write one character
		sw.seek(k)
		sw.write(z)
	# reset stream sw to beginning
	sw.seek(0)
	return sw.read();

def read_sim_results():
	if not os.path.exists("sim_results.xml"): return "";
	re_data = re.compile("data>");
	re_sim_results = re.compile("sim_results>");
	f = open("sim_results.xml", "r");
	str = "";
	for l in f:
		if re_data.search(l): continue;
		if re_sim_results.search(l): continue;
		str += l;
	f.close();
	return str;

if "__main__" == __name__:
	data = " <data> <user>%s</user> " % os.getlogin();
	data += "<program>%s</program> " % sys.argv[1];
	for ui in range(2, len(sys.argv), 2):
		data += "<%s>%s</%s> " % (sys.argv[ui], sys.argv[ui+1], sys.argv[ui]);
	if "s_chipsim" == sys.argv[1]:
		data += decrypt_simlog();
		data += read_sim_results();
	if not re.search("pwd>", data):
		data += "<pwd>%s</pwd> " % os.getcwd();
	if not re.search("REPO_PATH>", data):
		data += "<REPO_PATH>%s</REPO_PATH> " % os.environ["REPO_PATH"];
	data += "</data> ";

	if (not re.match("/tmp/", os.getcwd())) and ("SIMLOG_RUNLOG" in os.environ):
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		if "SIMLOG_DEBUGON" in os.environ:
			print data;
			client_socket.sendto(data, ("localhost",9600));
		else:
			client_socket.sendto(data, ("idcas003",9600));
		client_socket.close();

