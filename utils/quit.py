# UDP client example
import socket
import os
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = """ <data> <debug> </debug> <quit> </quit> </data> """;
if "SIMLOG_DEBUGON" in os.environ:
	client_socket.sendto(data, ("localhost",9600));
else:
	client_socket.sendto(data, ("idcas003",9600));
client_socket.close();

