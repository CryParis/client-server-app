import socket
import select
import sys


#this is because im working with Python3
from _thread import *

# server's IP address
ServerIP = "127.0.0.1"
ServerPORT = 1234 # port we want to use
Space = "<SPACE>" # I will use separate the client name & message


# initialize list/set of all connected client's sockets
List_Of_Clients = []


# create a TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# make the port as reusable port
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# bind the socket to the address we specified
server.bind((ServerIP, ServerPORT))

# listen for upcoming connections
server.listen(5)



print(f"Listening as {ServerIP}:{ServerPORT}")


#This function keep listening for a message from `Client Socket` socket
#Whenever a message is received, broadcast it to all other connected clients
def listen_for_client(cs):
	while True:
		try:
			# keep listening for a message from `cs` socket
			msg = cs.recv(2048).decode("utf-8")
		except Exception as e:
			# client no longer connected
			# remove it from the set
			print(f"[!] Error: {e}")
			List_Of_Clients.remove(cs)
		else:
			# if I received a message, replace the <SPACE> token with ": "
			msg = msg.replace(Space, ": ")
		# iterate over all connected sockets
		for client_socket in List_Of_Clients:
			# and send the message
			client_socket.send(msg.encode("utf-8"))


while True:
	# we keep listening for new connections all the time
	client_socket, client_address = server.accept()

	print(f"[+] {client_address} connected.")
	# add the new connected client to connected sockets

	List_Of_Clients.append(client_socket)

	start_new_thread(listen_for_client,(client_socket,))


# close client sockets
for cs in List_Of_Clients:
	cs.close()
# close server socket
server.close()