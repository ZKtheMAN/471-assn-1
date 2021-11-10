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
    print("Sending server request...")
    try:
        s.connect((TCP_IP, TCP_PORT))
        print ("Connection sucessful")
    except:
        print ("Connection unsucessful. Make sure the server is online.")


def list_files():
    # List the files avaliable on the file server
    # Called list_files(), not list() (as in the format of the others) to avoid the standard python function list()
    print ("Requesting files...\n")
    try:
        # Send list request
        s.send("LIST")
    except:
        print ("Couldn't make server request. Make sure a connection has bene established.")
        return
    try:
        # First get the number of files in the directory
        number_of_files = struct.unpack("i", s.recv(4))[0]
        # Then enter into a loop to recieve details of each, one by one
        for i in range(int(number_of_files)):
            # Get the file name size first to slightly lessen amount transferred over socket
            file_name_size = struct.unpack("i", s.recv(4))[0]
            file_name = s.recv(file_name_size)
            # Also get the file size for each item in the server
            file_size = struct.unpack("i", s.recv(4))[0]
            print ("\t{} - {}b".format(file_name, file_size))
            # Make sure that the client and server are syncronised
            s.send("1")
        # Get total size of directory
        total_directory_size = struct.unpack("i", s.recv(4))[0]
        print ("Size: {}b".format(total_directory_size))
    except:
        print ("No listing found")
        return
    try:
        # Final check
        s.send("1")
        return
    except:
        print ("No server confirmation")
        return


print ("\n\nWelcome to the FTP client."
       "\n\nPlease type one of the following functions :" 
       "\nCONN           : Connect to server"
       "\nUPLD file_path : Upload a file to the server folder"
       "\nLIST           : List all the files"
       "\nDWLD file_path : Download a file from the server"
       "\nDELF file_path : Delete a file"
       "\nQUIT           : Exit the program")
