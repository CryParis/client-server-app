import socket
import random
import sys
import select
from datetime import datetime
from colorama import Fore, init, Back

# init colors
init()

# Array with colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.RED, Fore.YELLOW]

# Random choose a color for client
client_color = random.choice(colors)

ServerIP = "127.0.0.1"
ServerPORT = 1234 # server's port
SPACE = "<SPACE>" # we will use this to separate the client name & message


# Get clients name
name = input("Enter your name: ")


# START TCP socket
socks = socket.socket()
print(f"\n\tConnecting to {ServerIP}:{ServerPORT}")

# Connect to the server and display message
socks.connect((ServerIP, ServerPORT))
print(f"\t\nWellcome to the chat {name}!\n")


while True:

	# maintains a list of possible input streams
	#sys.stdin can be used to get input from the command line directly. 
	#It used is for standard input
	sockets_list = [sys.stdin, socks] 

	read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])

	for each_sock in read_sockets:
		if each_sock == socks:
			#Message that i will receive
			message = each_sock.recv(2048).decode("utf-8")
			print("\n" + message)
		else:
			# Message that i will send to the server
			message_send =  input()
			# If i want to exit...
			if message_send == 'exit':
				print("\n\n\tAdios!\n\n")
				socks.shutdown()
				
			# add the datetime, name & the color of the sender
			date_now = datetime.now().strftime('%H:%M:%S') #%Y-%m-%d %H:%M:%S
			message_send = f"{client_color}[{date_now}] {name}{SPACE}{message_send}{Fore.RESET}"
			# Send the message to the server
			socks.send(message_send.encode("utf-8"))

# close the socket
socks.close()

