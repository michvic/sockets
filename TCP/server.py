## Michel Victor
import socket
import threading
import os.path
import struct
Host = '127.0.0.1'
Port = 8886

def download(conexao, cliente):
    with conexao:
        print ('Concetado por', cliente)
        dado = conexao.recv(1024)

        if not dado: return 

        nome_arquivo = dado.decode()
        print(cliente, " >>> ", dado.decode())

        try:
            arq = open('repositorio/{}'.format(nome_arquivo), 'rb')
        except IOError:                         
            print('Error 404 fileNotFound')
            conexao.sendall(b'Error 404 fileNotFound\r\n')
            
        else :
            with arq:
                dados_arquivo = arq.read()
                
                serializar = struct.Struct("{}s {}s".format(len(nome_arquivo), len(dados_arquivo)))
                dados_upload = serializar.pack(*[nome_arquivo.encode(), dados_arquivo])

                conexao.send("Arquivo:{}, bytes:{}".format(
                    nome_arquivo, len(dados_arquivo)).encode()) 

                ouvir = conexao.recv(1024) 
                
                if ouvir.decode() == 's':
                    conexao.send(dados_upload)
                else:
                    conexao.send('Operação cancelada!'.encode())



        print('Finalizando conexao do cliente', cliente)
        conexao.close()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
origem = (Host,Port)

tcp.bind(origem)
tcp.listen(5)

while True:
    print("...Esperando conexões!")
    conexao, cliente = tcp.accept()

    t = threading.Thread(target=download, args=(conexao,cliente))
    t.start()
