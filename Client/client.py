import socket
import sys
import os
import struct

# Initialise socket stuff
TCP_IP = "127.0.0.1" # Only a local server
TCP_PORT = 1456 # Just a random choice
BUFFER_SIZE = 1024 # Standard chioce
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conn():
    # Connect to the server
    print ("Sending server request...")
    try:
        s.connect((TCP_IP, TCP_PORT))
        print ("Connection sucessful")
    except:
        print ("Connection unsucessful. Make sure the server is online.")

print ("\n\nWelcome to the FTP client."
       "\n\nPlease type one of the following functions :" 
       "\nCONN           : Connect to server"
       "\nUPLD file_path : Upload a file to the server folder"
       "\nLIST           : List all the files"
       "\nDWLD file_path : Download a file from the server"
       "\nDELF file_path : Delete a file"
       "\nQUIT           : Exit the program")
