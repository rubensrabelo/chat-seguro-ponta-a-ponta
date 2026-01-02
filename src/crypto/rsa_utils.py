from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def generate_keys():
    """
    Gera um par de chaves RSA (privada e pública).
    """
    key = RSA.generate(2048)
    return key.export_key(), key.publickey().export_key()


def encrypt_with_public_key(public_key_bytes, data):
    """
    Criptografa dados usando a chave pública RSA.
    """
    pub = RSA.import_key(public_key_bytes)
    cipher = PKCS1_OAEP.new(pub)
    return cipher.encrypt(data)


def decrypt_with_private_key(private_key_bytes, data):
    """
    Descriptografa dados usando a chave privada RSA.
    """
    priv = RSA.import_key(private_key_bytes)
    cipher = PKCS1_OAEP.new(priv)
    return cipher.decrypt(data)
