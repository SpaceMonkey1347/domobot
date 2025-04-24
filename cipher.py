import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


allowed_chars = []
for i in range(26):
    letter = chr(ord('A') + i)
    allowed_chars.append(letter)
allowed_chars.extend((' ',))


def nykro_cipher(message: str, encipher: bool):
    message = message.upper()
    output = ''
    incr = 1
    if not encipher:
        incr = -1

    for char in message:
        if char not in allowed_chars:
            output += char
            continue

        val = allowed_chars.index(char)
        val = val + incr
        while val < 0:
            val = val + len(allowed_chars)
        outchar = allowed_chars[val % len(allowed_chars)]
        output += outchar

        if incr < 0:
            incr = incr * -1 + 1
        else:
            incr = incr * -1 - 1
    return output


words_by_len = []



def domo_encrypt(message: str, key: str):
    pass
