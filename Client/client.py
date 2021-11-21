import socket
import sys
import os
import struct


TCP_IP = "127.0.0.1"
TCP_PORT = 1456
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conn():
    print("Sending server request...")
    try:
        s.connect((TCP_IP, TCP_PORT))
        print("Connection successful")
    except Exception as e:
        print(e)
        print("Connection unsuccessful. Make sure the server is online.")

def list_files():
    print("Requesting files...\n")
    try:
        s.send(b"LIST")
    except Exception as e:
        print(e)
        print("Connection unsuccessful. Make sure the server is online.")
        return
    try:
        number_of_files = struct.unpack("i", s.recv(4))[0]
        for i in range(int(number_of_files)):
            file_name_size = struct.unpack("i", s.recv(4))[0]
            file_name = s.recv(file_name_size)
            file_size = struct.unpack("i", s.recv(4))[0]
            print("\t{} - {}b".format(file_name, file_size))
            s.send(b"1")
        total_directory_size = struct.unpack("i", s.recv(4))[0]
        print("Size: {}b".format(total_directory_size))
    except Exception as e:
        print(e)
        print("No listing found")
        return
    try:
        s.send(b"1")
        return
    except Exception as e:
        print(e)
        print("No server confirmation")
        return

def upld(file_name):
    print ("\nUploading the file to the server: {}...".format(file_name))
    try:
        content = open(file_name, "rb")
    except Exception as e:
        print(e)
        print ("Couldn't open file. Make sure the file name was spelled correctly.")
        return
    try:
        s.send(b"UPLD")
    except Exception as e:
        print(e)
        print("Couldn't make server request. Make sure the server is running.")
        return
    try:
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode("UTF8"))
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("i", os.path.getsize(file_name)))
    except Exception as e:
        print(e)
        print("Error: Cannot send file details")
    try:
        l = content.read(BUFFER_SIZE)
        print("\nSending...")
        while l:
            s.send(l)
            l = content.read(BUFFER_SIZE)
        content.close()
        upload_time = struct.unpack("f", s.recv(4))[0]
        upload_size = struct.unpack("i", s.recv(4))[0]
        print("\nSent file: {}\nTime taken: {}s\nFile size: {}b".format(file_name, upload_time, upload_size))
    except Exception as e:
        print(e)
        print("Error sending file")
        return
    return


def dwld(file_name):
    print ("Downloading file: {}".format(file_name))
    try:
        s.send(b"DWLD")
    except Exception as e:
        print(e)
        print ("Couldn't make server request. Make sure the server is running.")
        return
    try:
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode('UTF8'))
        file_size = struct.unpack("i", s.recv(4))[0]
        if file_size == -1:
            print ("Couldn't open file. Make sure the file name was spelled correctly")
            return
    except Exception as e:
        print(e)
        print ("Error checking file")
    try:
        s.send(b"1")
        output_file = open(file_name, "wb")
        bytes_recieved = 0
        print ("\nDownloading...")
        while bytes_recieved < file_size:
            l = s.recv(BUFFER_SIZE)
            output_file.write(l)
            bytes_recieved += BUFFER_SIZE
        output_file.close()
        print ("Successfully downloaded {}".format(file_name))
        s.send(b"1")
        time_elapsed = struct.unpack("f", s.recv(4))[0]
        print ("Time elapsed: {}s\nFile size: {}b".format(time_elapsed, file_size))
    except Exception as e:
        print(e)
        print ("Error downloading file")
        return
    return


def delf(file_name):
    print ("Deleting file: {}...".format(file_name))
    try:
        s.send(b"DELF")
        s.recv(BUFFER_SIZE)
    except Exception as e:
        print(e)
        print ("Couldn't make server request. Make sure the server is running.")
        return
    try:
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode("UTF8"))
    except Exception as e:
        print(e)
        print ("Couldn't send file details")
        return
    try:
        file_exists = struct.unpack("i", s.recv(4))[0]
        if file_exists == -1:
            print ("The file does not exist on server")
            return
    except Exception as e:
        print(e)
        print ("Couldn't find file.")
        return
    try:
        confirm_delete = input("Are you sure you want to delete {}? (Y/N)\n".format(file_name)).upper()
        while confirm_delete != "Y" and confirm_delete != "N" and confirm_delete != "YES" and confirm_delete != "NO":
            print("Command not recognised, try again")
            confirm_delete = input("Are you sure you want to delete {}? (Y/N)\n".format(file_name)).upper()
    except Exception as e:
        print(e)
        print("Couldn't confirm deletion status")
        return
    try:
        if confirm_delete == "Y" or confirm_delete == "YES":
            s.send(b"Y")
            delete_status = struct.unpack("i", s.recv(4))[0]
            if delete_status == 1:
                print("File successfully deleted")
                return
            else:
                print("File failed to delete")
                return
        else:
            s.send(b"N")
            print("Delete not completed: User error")
            return
    except Exception as e:
        print(e)
        print("Couldn't delete file")
        return

def quit():
    s.send(b"QUIT")
    s.recv(BUFFER_SIZE)
    s.close()
    print("Server connection ended")
    return


#print("\n\nWelcome to the FTP client."
       #"\n\nPlease type one of the following functions :"
       #"\nCONN           : Connect to server"
       #"\nUPLD file_path : Upload a file to the server folder"
       #"\nLIST           : List all the files"
       #"\nDWLD file_path : Download a file from the server"
       #"\nDELF file_path : Delete a file"
       #"\nQUIT           : Exit the program")


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
        original_input = input('FTP CLIENT> ').split(' ')
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
                file_path = ''.join([s if s!= '' else ' ' for s in original_input[1:]])
                upld(file_path)
            except IndexError:
                print("Error: Command incomplete!")
        elif user_input[0].upper() == "LIST":
            list_files()
            pass
        elif user_input[0].upper() == "DWLD":
            try:
                file_path = ''.join([s if s!= '' else ' ' for s in original_input[1:]])
                dwld(file_path)
            except IndexError:
                print("Error: Command incomplete!")
        elif user_input[0].upper() == "DELF":
            try:
                file_path = ''.join([s if s!= '' else ' ' for s in original_input[1:]])
                delf(file_path)
            except IndexError:
                print("Error: Command incomplete!")
        elif user_input[0].upper() == "QUIT":
            quit()
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