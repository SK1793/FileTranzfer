import socket
import tqdm
import os
import tkinter as tk
from tkinter import filedialog as fd
root=tk.Tk().withdraw()
# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 1793
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"


#1
# create the server socket
# TCP socket
s = socket.socket()

#2
# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))

#3
# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

#4
# accept connection if there is any
client_socket, address = s.accept() 
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")



#5
recvd=client_socket.recv(BUFFER_SIZE).decode()
filename,filesize=recvd.split(SEPARATOR)
filename=os.path.basename(filename)
filesize=int(filesize)

#6
# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

#popup directory selector

dir=fd.askdirectory()
with open(dir+"/"+filename, "wb") as f:
    for _ in progress:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

# close the client socket
client_socket.close()
# close the server socket
s.close()
break

