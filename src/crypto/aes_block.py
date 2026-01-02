from Crypto.Cipher import AES


def aes_encrypt_block(key, block):
    """
    Criptografa um bloco usando AES no modo ECB.
    """
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(block)


def aes_decrypt_block(key, block):
    """
    Descriptografa um bloco usando AES no modo ECB.
    """
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(block)
