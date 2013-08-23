# UDP client example
import socket
from datetime import date
import os

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
today = date.today();
data = """<data><debug> </debug><save_me>./save_file_%02d%02d%04d.pkl</save_me></data>""" % (today.day, today.month, today.year);
if "SIMLOG_DEBUGON" in os.environ:
	client_socket.sendto(data, ("localhost",9600));
else:
	client_socket.sendto(data, ("idcas003",9600));
client_socket.close();

