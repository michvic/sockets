import custom_sockt as cs

try:
  cs.send(cs.load_file())
  while True:
    data, sender_addr = cs.recv()
    
    try:
      name_file, file = data.decode().split("|")

      if name_file == 'public.key':
        with open(sender_addr[0]+'_public.key', 'wb') as public_key:
          public_key.write(file.encode())
          public_key.close()
        
        print(sender_addr[0]+'_public.key has been successfully saved!')
    except ValueError:
        print(data)
      

except KeyboardInterrupt:
  cs.send('Disconnect!'.encode())
  pass

