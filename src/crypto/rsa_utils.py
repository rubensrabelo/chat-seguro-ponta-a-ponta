from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Gera par de chaves RSA
def generate_keys():
    key = RSA.generate(2048)
    return key.export_key(), key.publickey().export_key()

def encrypt_with_public_key(public_key_bytes, data):
    pub = RSA.import_key(public_key_bytes)
    cipher = PKCS1_OAEP.new(pub)
    return cipher.encrypt(data)

def decrypt_with_private_key(private_key_bytes, data):
    priv = RSA.import_key(private_key_bytes)
    cipher = PKCS1_OAEP.new(priv)
    return cipher.decrypt(data)
