import os
from crypto.aes_block import aes_encrypt_block

BLOCK_SIZE = 16


def encrypt(key, plaintext):
    """
    Criptografa dados usando AES no modo CTR.
    """
    nonce = os.urandom(8)
    counter = 0
    ciphertext = b''

    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i+BLOCK_SIZE]
        counter_bytes = counter.to_bytes(8, "big")
        keystream = aes_encrypt_block(key, nonce + counter_bytes)
        ciphertext += bytes(x ^ y for x, y in zip(block, keystream))
        counter += 1

    return nonce + ciphertext


def decrypt(key, ciphertext):
    """
    Descriptografa dados usando AES no modo CTR.
    """
    nonce = ciphertext[:8]
    data = ciphertext[8:]
    counter = 0
    plaintext = b''

    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i+BLOCK_SIZE]
        counter_bytes = counter.to_bytes(8, "big")
        keystream = aes_encrypt_block(key, nonce + counter_bytes)
        plaintext += bytes(x ^ y for x, y in zip(block, keystream))
        counter += 1

    return plaintext
