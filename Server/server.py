import socket
import sys
import time
import os
import struct

print("\nWelcome to our FTP server Server Example.\n\nTo get started, connect a client by opening a second terminal and running the client.py file.")


TCP_IP = "127.0.0.1"
TCP_PORT = 1456
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()

print("\nConnected to the server sucessful...".format(addr))

def list_files():
    print("Listing files:")
    listing = os.listdir(os.getcwd())
    conn.send(struct.pack("i", len(listing)))
    total_directory_size = 0
    for i in listing:
        conn.send(struct.pack("i", sys.getsizeof(i)))
        conn.send(i)
        conn.send(struct.pack("i", os.path.getsize(i)))
        total_directory_size += os.path.getsize(i)
        conn.recv(BUFFER_SIZE)
    conn.send(struct.pack("i", total_directory_size))
    conn.recv(BUFFER_SIZE)
    print("The Files have been successfully Listed!")
    return

def put():
    conn.send("1")
    file_name_size = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_size)
    conn.send("1")
    file_size = struct.unpack("i", conn.recv(4))[0]
    start_time = time.time()
    output_file = open(file_name, "wb")
    bytes_recieved = 0
    print("\nRecieving the file...")
    while bytes_recieved < file_size:
        l = conn.recv(BUFFER_SIZE)
        output_file.write(l)
        bytes_recieved += BUFFER_SIZE
    output_file.close()
    print("\nFile Recieved: {}".format(file_name))
    conn.send(struct.pack("f", time.time() - start_time))
    conn.send(struct.pack("i", file_size))
    return

def dwld():
    conn.send("1")
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    print (file_name_length)
    file_name = conn.recv(file_name_length)
    print (file_name)
    if os.path.isfile(file_name):
        conn.send(struct.pack("i", os.path.getsize(file_name)))
    else:
        print ("File name not valid")
        conn.send(struct.pack("i", -1))
        return
    conn.recv(BUFFER_SIZE)
    start_time = time.time()
    print ("Sending file...")
    content = open(file_name, "rb")
    l = content.read(BUFFER_SIZE)
    while l:
        conn.send(l)
        l = content.read(BUFFER_SIZE)
    content.close()
    conn.recv(BUFFER_SIZE)
    conn.send(struct.pack("f", time.time() - start_time))
    return

def delf():
    conn.send("1")
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_length)
    if os.path.isfile(file_name):
        conn.send(struct.pack("i", 1))
    else:
        conn.send(struct.pack("i", -1))
    confirm_delete = conn.recv(BUFFER_SIZE)
    if confirm_delete == "Y":
        try:
            os.remove(file_name)
            conn.send(struct.pack("i", 1))
        except:
            print ("Failed to delete {}".format(file_name))
            conn.send(struct.pack("i", -1))
    else:
        print ("Delete not completed: User error")
        return


def quit():
    conn.send("1")
    conn.close()
    s.close()
    os.execl(sys.executable, sys.executable, *sys.argv)


while True:
    print ("\n\nWaiting for instruction")
    data = conn.recv(BUFFER_SIZE)
    print ("\nRecieved instruction: {}".format(data))
    if data == "UPLD":
        put()
    elif data == "LIST":
        list_files()
    elif data == "DWLD":
        dwld()
    elif data == "DELF":
        delf()
    elif data == "QUIT":
        quit()
    data = None
