import socket
import sys
import time
import os
import struct

print ("\nWelcome to our FTP server Server Example.\n\nTo get started, connect a client by opening a second terminal and running the client.py file.")

# Initialise socket stuff
TCP_IP = "127.0.0.1" # Only a local server
TCP_PORT = 1456 # Just a random choice
BUFFER_SIZE = 1024 # Standard size
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()

print ("\nConnected to the server sucessful...".format(addr))