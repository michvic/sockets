## Michel Victor
import socket
import struct
Host = '127.0.0.1'
Port = 8886

print('nome do arquivo para download:') 
str = input('Entre com um String: ')

socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
origem = (Host,Port)

socketCliente.connect(origem)
socketCliente.sendall( str.encode())

response = socketCliente.recv(1024)

nome, tamanho = response.decode().split(',')
print(nome.split(':')[-1])
print(tamanho.split(':')[-1])

print(response)
aceitar = input('Baixar arquivo? (s) ou (n)')
socketCliente.send(aceitar.encode())
dados = socketCliente.recv(1024) 



print(dados)
serializar = struct.Struct("{}s {}s".format(
    len(nome.split(':')[-1]), 
    int(tamanho.split(':')[-1])))

nome, arquivo = serializar.unpack(dados)


with open("downloads/{}".format(nome.decode()), 'wb') as novo_arquivo:
    novo_arquivo.write(arquivo)
    print("Arquivo {} salvo em downloads.".format(nome.decode()))
