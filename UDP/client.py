## Michel Victor
import socket

Host = '127.0.0.1'
Port = 8886 


socketCliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (Host,Port)

socketCliente.connect(server_address)

try:
    caderno = open('caderno', 'r')

    with caderno:
        dados_do_arquivo = caderno.read()
        socketCliente.send(dados_do_arquivo.encode())
        resultado = socketCliente.recv(1024)
    
finally:
    print('closing socket')
    socketCliente.close()
