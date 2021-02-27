from Crypto.PublicKey import RSA 

def generate_RSA(bits=2048):
    new_key = RSA.generate(bits, e=65537) 
    public_key = new_key.publickey().exportKey("PEM") 
    private_key = new_key.exportKey("PEM") 
    return private_key, public_key

key_priv, key_pub = generate_RSA()

with open('private.key', 'wb') as key:
  key.write(key_priv)
  key.close()

with open('public.key', 'wb') as key:
  key.write(key_pub)
  key.close()