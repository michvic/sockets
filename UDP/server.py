## Michel Victor
import socket
import _thread
import os.path
import struct
Host = '127.0.0.1'
Port = 8886

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
origem = (Host,Port)

sock.bind(origem)
sock.listen(5)

while True:

    
