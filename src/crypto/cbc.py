import os
from crypto.aes_block import aes_encrypt_block, aes_decrypt_block

BLOCK_SIZE = 16


def xor(a, b):
    """
    Aplica XOR byte a byte entre dois blocos.
    """
    return bytes(x ^ y for x, y in zip(a, b))


def pad(data):
    """
    Aplica padding PKCS#7 ao texto plano.
    """
    pad_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([pad_len] * pad_len)


def unpad(data):
    """
    Remove o padding PKCS#7 do texto plano.
    """
    return data[:-data[-1]]


def encrypt(key, plaintext):
    """
    Criptografa dados usando AES no modo CBC.
    """
    iv = os.urandom(BLOCK_SIZE)
    plaintext = pad(plaintext)

    blocks = []
    prev = iv

    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i+BLOCK_SIZE]
        x = xor(block, prev)
        c = aes_encrypt_block(key, x)
        blocks.append(c)
        prev = c

    return iv + b''.join(blocks)


def decrypt(key, ciphertext):
    """
    Descriptografa dados usando AES no modo CBC.
    """
    iv = ciphertext[:BLOCK_SIZE]
    data = ciphertext[BLOCK_SIZE:]

    prev = iv
    plaintext = b''

    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i+BLOCK_SIZE]
        x = aes_decrypt_block(key, block)
        plaintext += xor(x, prev)
        prev = block

    return unpad(plaintext)
