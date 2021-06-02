
import socket
import tqdm
import os
from tkinter import filedialog as fd
import tkinter as tk
#1
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step
#2
# the ip address or hostname of the server, the receiver
host = "192.168.43.1"
# the port, let's use 5001
port = 1793
root=tk.Tk().withdraw()
# the name of file we want to send, make sure it exists
dir1 = fd.askopenfilename()
filename=dir1.split('/')[-1]
# get the file size
filesize = os.path.getsize(dir1)

#3
# create the client socket
s = socket.socket()

#4
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

#5
# send the filename and filesize
s.send(f"{dir1}{SEPARATOR}{filesize}".encode())

#6
# start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(dir1, "rb") as f:
    for _ in progress:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            
            break
        # we use sendall to assure transimission in 
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
# close the socket
s.close()