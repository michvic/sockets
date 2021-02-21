## Michel Victor
import socket
import struct
from errors import NotAllowed

Host = '127.0.0.1'
Port = 8886
socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
origem = (Host,Port)

socketCliente.connect(origem)

try:
    str = input('nome do arquivo para download: ')
    socketCliente.send( str.encode())

    response = socketCliente.recv(1024)
    nome, tamanho = response.decode().split(',')

    print(response)
    aceitar = input('Baixar arquivo? (s) ou (n)')
    socketCliente.send(aceitar.encode())
    dados = socketCliente.recv(1024) 

    if aceitar == 'n': raise NotAllowed()

    serializar = struct.Struct("{}s {}s".format(
        len(nome.split(':')[-1]), 
        int(tamanho.split(':')[-1])))

    nome, arquivo = serializar.unpack(dados)

    with open("downloads/{}".format(nome.decode()), 'wb') as novo_arquivo:
        novo_arquivo.write(arquivo)
        print(arquivo)
        novo_arquivo.close()
        print("Arquivo {} salvo em downloads.".format(nome.decode()))


except ValueError:
    print('Error 404 fileNotFound')
except NotAllowed:
    print('Usuario cancelou a opeação')
