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
        print("Connection successful")
    except:
        print("Connection unsuccessful. Make sure the server is online.")


def list_files():
    # List the files avaliable on the file server
    # Called list_files(), not list() (as in the format of the others) to avoid the standard python function list()
    print("Requesting files...\n")
    try:
        # Send list request
        s.send("LIST")
    except:
        print("Couldn't make server request. Make sure a connection has bene established.")
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
            print("\t{} - {}b".format(file_name, file_size))
            # Make sure that the client and server are synchronized
            s.send("1")
        # Get total size of directory
        total_directory_size = struct.unpack("i", s.recv(4))[0]
        print("Size: {}b".format(total_directory_size))
    except:
        print("No listing found")
        return
    try:
        # Final check
        s.send("1")
        return
    except:
        print("No server confirmation")
        return

def upld(file_name):
    # Upload a file
    print ("\nUploading the file to the server: {}...".format(file_name))
    try:
        # Check the file exists
        content = open(file_name, "rb")
    except:
        print ("Couldn't open file. Make sure the file name was spelled correctly.")
        return
    try:
        # Make upload request
        s.send("UPLD")
    except:
        print("Couldn't make server request. Make sure the server is running.")
        return
    try:
        # Wait for server acknowledgement then send file details
        # Wait for server ok
        s.recv(BUFFER_SIZE)
        # Send file name size and file name
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name)
        # Wait for server ok then send file size
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("i", os.path.getsize(file_name)))
    except:
        print("Error: Cannot send file details")
    try:
        # Send the file in chunks defined by BUFFER_SIZE
        # Doing it this way allows for unlimited potential file sizes to be sent
        l = content.read(BUFFER_SIZE)
        print("\nSending...")
        while l:
            s.send(l)
            l = content.read(BUFFER_SIZE)
        content.close()
        # Get upload performance details
        upload_time = struct.unpack("f", s.recv(4))[0]
        upload_size = struct.unpack("i", s.recv(4))[0]
        print("\nSent file: {}\nTime taken: {}s\nFile size: {}b".format(file_name, upload_time, upload_size))
    except:
        print("Error sending file")
        return
    return

def quit_client():
    print("Qutting.")


def download(path):
    print("Downloading " + path)


def delete_file(path):
    print("Deleting" + path)

def main():
    running = True
    print ("\n\nWelcome to the FTP client."
        "\n\nPlease type one of the following functions :" 
        "\nCONN ipv4 port : Connect to server"
        "\nUPLD file_path : Upload a file to the server folder"
        "\nLIST           : List all the files"
        "\nDWLD file_path : Download a file from the server"
        "\nDELF file_path : Delete a file"
        "\nQUIT           : Exit the program")
    while running:
        original_input = raw_input('FTP CLIENT> ').split(' ')
        user_input = original_input
        if user_input[0].upper() == "CONN":
            user_input = [s for s in user_input if s != '']
            # IP Address Validation
            # From: https://stackoverflow.com/a/319298/2923706
            try:
                socket.inet_pton(socket.AF_INET, user_input[1])
                if isinstance(int(user_input[2]),int):
                    TCP_IP = user_input[1]
                    TCP_PORT = user_input[2]
                    conn()
            except socket.error:
                print("Error: Invalid IPV4 address \"" + user_input[1] + "\"")
            except ValueError:
                print("Error: Invalid port number \"" + user_input[2] + "\"")
            except IndexError:
                print("Error: Command incomplete!")
        elif user_input[0].upper() == "UPLD":
            try:
                file_path = [s if s!= '' else ' ' for s in original_input[1:]].join()
                upld(file_path)
            except IndexError:
                print("Error: Command incomplete!")
        elif user_input[0].upper() == "LIST":
            list_files()
            pass
        elif user_input[0].upper() == "DWLD":
            try:
                file_path = [s if s!= '' else ' ' for s in original_input[1:]].join()
                download(file_path)
            except IndexError:
                print("Error: Command incomplete!")
        elif user_input[0].upper() == "DELF":
            try:
                file_path = [s if s!= '' else ' ' for s in original_input[1:]].join()
                delete_file(file_path)
            except IndexError:
                print("Error: Command incomplete!")
        elif user_input[0].upper() == "QUIT":
            quit_client()
            running = False
        else:
            print("ERROR: Invalid function!")
            print("Please type one of the following functions :" 
                "\nCONN ip port   : Connect to server"
                "\nUPLD file_path : Upload a file to the server folder"
                "\nLIST           : List all the files"
                "\nDWLD file_path : Download a file from the server"
                "\nDELF file_path : Delete a file"
                "\nQUIT           : Exit the program")

        print(user_input)


main()