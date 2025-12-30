from Crypto.Cipher import AES

# AES como cifra de bloco (ECB)
def aes_encrypt_block(key, block):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(block)

def aes_decrypt_block(key, block):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(block)
