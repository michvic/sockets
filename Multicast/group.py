import custom_sockt as cs
import socket
from rsa import generate_public_private_key
from threading import Thread
import random
import time

BUFFER_SIZE = 1024

class ClientThread(Thread):
    def __init__(self, ip, port, sock, file):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        self.file = file
        print("New thread started for "+ip+":"+str(port))

    def run(self):        
        try:
          while True:
              l = self.file.read(BUFFER_SIZE)
              while (l):
                  self.sock.send(l)
                  #print('Sent ',repr(l))
                  l = self.file.read(BUFFER_SIZE)
              if not l:
                  self.file.close()
                  self.sock.close()
                  break
        except:
          self.sock.close()

def listen(username=""):
  while True:
      data, sender_addr = cs.recv()

      try:
        data = data.decode()

        if "public_key=" in data:
          # Removendo as partes desnecessárias da chave pública
          rcv_public_key = data.replace("public_key=", "")

          print(rcv_public_key)

        elif "file_request=" in data:
          file_name = data.replace("file_request=", "")

          print("Arquivo de nome {} requisitado por {}:{}".format(file_name, sender_addr[0], sender_addr[1]))
          
          try: 
            f = open("repository/{}/{}" .format(username, file_name), "rb")
            TCP_IP = 'localhost'
            TCP_PORT = random.randrange(8000, 9999)

            time.sleep(2)

            cs.send(bytes("file_exists=YES|{}|{}|{}".format(TCP_IP, TCP_PORT, file_name), "utf-8"))

            tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tcpsock.bind((TCP_IP, TCP_PORT))
            cthreads = []

            tcpsock.listen(5)
            tcpsock.settimeout(5)
            print("Waiting for incoming connections...")
            (conn, (ip, port)) = tcpsock.accept()
            print('Got connection from ', (ip, port))
            newthread = ClientThread(ip, port, conn, f)
            newthread.start()
            cthreads.append(newthread)
          
          except IOError:
            print("Arquivo não existente")
            cs.send("file_exists=NO".encode())
        
        elif "file_exists=" in data:
          file_exists = data.replace("file_exists=", "")
          print(data)

          if "YES" in file_exists:
            _ , ip, port, file_name = data.split("|")

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, int(port)))


            recived_f = 'received_{}.{}' .format(str(time.time()).split('.')[0], file_name.split('.')[-1])

            with open(recived_f, 'wb') as f:
              while True:
                  fdata = s.recv(BUFFER_SIZE)
                  print('fdata=%s', (fdata))
                  if not fdata:
                      f.close()
                      break
                  f.write(fdata)

              print('Download do arquivo finalizado')
              s.close()

          else:
            print("File not exists")

      except ValueError:
        print(data)
      except KeyboardInterrupt:
        cs.send('Disconnect!'.encode())
        pass
      except Exception as e:
        print(e)

if __name__ == "__main__":
  threads = []

  try:
    name = input('Digite o seu nome: ')

    private_key, public_key = generate_public_private_key("_".join(name.split(" ")))

    cs.send(bytes("public_key="+public_key.split("|")[1], "utf-8"))

    t = Thread(target=listen, args=(name, ))
    threads.append(t)
    t.start()

    should_request_file = input("Deseja solicitar um arquivo? (YES/NO) ")
    print(should_request_file)

    if should_request_file == "YES":
      request_file_name = input("Digite o nome do arquivo: ")
      cs.send(bytes("file_request={}".format(request_file_name), "utf-8"))

  except KeyboardInterrupt:
    cs.send(('{} disconnected!'.format(name)).encode())
    pass
