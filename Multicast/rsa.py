from Crypto.PublicKey import RSA
import os

def generate_RSA(bits=2048):
  new_key = RSA.generate(bits, e=65537)
  public_key = new_key.publickey().exportKey("PEM")
  private_key = new_key.exportKey("PEM")
  return private_key, public_key

  key_priv, key_pub = generate_RSA()

  with open('private.key', 'wb') as private_key:
      private_key.write(key_priv)
      private_key.close()

  with open('public.key', 'wb') as public_key:
      public_key.write(key_pub)
      public_key.close()


def generate_public_private_key(user_name):
  key = RSA.generate(2048)
  dir_path = os.path.join('keys', user_name)

  try:
    os.mkdir(dir_path)
  except OSError:
    print('Pasta já existe, sobrescrevendo arquivo...')

  private_fname = "rsa_private.pem"
  public_fname = "rsa_public.pem"

  private_key = key.export_key()
  file_out = open(os.path.join(dir_path, private_fname), "wb")
  file_out.write(private_key)
  file_out.close()

  public_key = key.public_key().export_key()
  file_out = open(os.path.join(dir_path, public_fname), "wb")
  file_out.write(public_key)
  file_out.close()

  return "{}|{}".format(private_fname, private_key.decode()), "{}|{}".format(public_fname, public_key.decode())
