# Gustave Michel III
# 05/03/2017
# Encrypt and Decrypt file using AES with 16, 24, or 32 Byte Keys.
# Also checks Key Hashes to ensure right Key is being supplied to Decrypt

import sys
import os
import argparse
import re

import hashlib
from Crypto.Cipher import AES

def input_file(x):
    """'Type' for argparse - checks that file exists and opens read-only."""
    if not os.path.exists(x):
        raise argparse.ArgumentTypeError("{0} does not exist".format(x))
    return open(x,'r')

parser = argparse.ArgumentParser(description='')
parser.add_argument('action', choices=['enc','dec'], help='Encrypt or Decrypt')
parser.add_argument('key', help='Encryption/Decryption Key')
parser.add_argument('filename', type=input_file, help='File to Encrypt/Decrypt')
args = parser.parse_args()

# The block size for cipher object; must be 16 bytes (128 bit) for AES.
BLOCK_SIZE = 16

# Pad at the end, so all blocks, including the last one, are 128 bit long.
PAD_WITH = '#'

# Valid Key Lengths (Bytes)
KEY_LENGTHS = [16,24,32]

# Appends 'PAD_WITH' to end of plaintext to make it fully fill all blocks.
def pad(plaintext):
    return plaintext + (BLOCK_SIZE - len(plaintext) % BLOCK_SIZE) * PAD_WITH

# Encrypts 'plaintext' using 'cipher' object.
def encrypt(cipher, plaintext):
    return cipher.encrypt(pad(plaintext))

# Decrypts 'ciphertext' using 'cipher' object.
def decrypt(cipher, ciphertext):
    return  cipher.decrypt(ciphertext).rstrip(PAD_WITH)

# Create a 'cipher' object and generate the 'key hash' using 'key'
cipher = AES.new(args.key)
key_hash = hashlib.sha256(args.key).digest()

# Filename Regex Groups
filename = re.search('(^.+?)(_enc|_dec)?(\..+$)',args.filename.name)
input_text = args.filename.read()

# Encryption
if args.action == 'enc': # Encryption
    output_text = key_hash+encrypt(cipher, input_text)
# Key Hash Validation and Decryption
elif args.action == 'dec': # Decryption
    ciphertext, ciphertext_hash = [input_text[32:],input_text[:32]]
    if key_hash != ciphertext_hash:
        raise ValueError('File\'s Key Hash does not match provided Key\'s Hash')
    output_text = decrypt(cipher, ciphertext)

out_file = open(filename.group(1)+"_"+args.action+filename.group(3),'w')
out_file.write(output_text)
out_file.close()
args.filename.close()
