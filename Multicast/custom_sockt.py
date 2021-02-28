# UDP multicast
import socket
import struct


def send(data, port=50000, addr='224.0.0.1'):
  # Create the socket
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  # Make the socket multicast-aware, and set TTL.
  s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL,
                20)  # Change TTL (=20) to suit
  # Send the data
  s.sendto(data, (addr, port))

def sendto(data, port=50000, addr="224.0.0.1"):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  print(data)

  try:
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
  except AttributeError as e:
      print(e)
      pass 

  s.sendto(data, (addr, port))

def recvfrom(port=50000, addr='224.0.0.1', buf_size=1024):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  try:
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
  except AttributeError:
      pass 

  s.bind((addr, port))

  data, sender_addr = s.recvfrom(buf_size)

  # s.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton('0.0.0.0'))
  s.close()

  return data, sender_addr

def recv(port=50000, addr='224.0.0.1', buf_size=1024):
  # Create the socket
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  # Set some options to make it multicast-friendly
  try:
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
  except AttributeError:
      pass  # Some systems don't support SO_REUSEPORT

  # Bind to the port
  s.bind(("", port))

  # Set some more multicast options  
  intf = socket.gethostbyname('localhost')

  s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                socket.inet_aton(addr) + socket.inet_aton(intf))
  s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)

# Receive the data, then unregister multicast receive membership, then close the port

  data, sender_addr = s.recvfrom(buf_size)

  # s.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton('0.0.0.0'))
  s.close()
  return data, sender_addr


def load_file(name='public.key'):
  try:
    file = open('public.key', 'rb')
  except IOError:
    raise Exception('Error 404 fileNotFound')

  else:
    with file:
      file_data = file.read()

      # bytes_size = len(file_data)

      # serializar = struct.Struct("{}s {}s".format(len(name), bytes_size))
      # upload = serializar.pack(*[name.encode(), file_data])
      file.close()
      result = "{}|{}".format(name, file_data).encode()

      return result
