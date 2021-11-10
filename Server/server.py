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

def list_files():
    print ("Listing files:")
    # Get list of files in directory
    listing = os.listdir(os.getcwd())
    # Send over the number of files, so the client knows what to expect (and avoid some errors)
    conn.send(struct.pack("i", len(listing)))
    total_directory_size = 0
    # Send over the file names and sizes whilst totaling the directory size
    for i in listing:
        # File name size
        conn.send(struct.pack("i", sys.getsizeof(i)))
        # File name
        conn.send(i)
        # File content size
        conn.send(struct.pack("i", os.path.getsize(i)))
        total_directory_size += os.path.getsize(i)
        # Make sure that the client and server are syncronised
        conn.recv(BUFFER_SIZE)
    # Sum of file sizes in directory
    conn.send(struct.pack("i", total_directory_size))
    #Final check
    conn.recv(BUFFER_SIZE)
    print ("The Files have been successfully Listed!")
    return
