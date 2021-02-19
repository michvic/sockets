""" 
    Python 2 ou 3
    Michel Victor
"""
import socket

Host = '127.0.0.1'
Port = 8886 


socketCliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (Host,Port)

try:
    caderno = open('caderno', 'rb')

    with caderno:
        dados_do_arquivo = caderno.read()
        socketCliente.sendto(dados_do_arquivo, server_address)
        resultado, server = socketCliente.recvfrom(1024)

    print(resultado)
    
finally:
    print('closing socket')
    socketCliente.close()
