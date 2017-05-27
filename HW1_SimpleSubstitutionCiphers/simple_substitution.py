# python2.7

import sys
import string
import argparse

# Define Command-Line arguments
parser = argparse.ArgumentParser(description='Encrypt or Decrypt Messages in Ceasar or Keyword Ciphers.')
parser.add_argument('method', choices=['c','k'], help='encryption method')
parser.add_argument('action', choices=['enc','dec'], help='encrypt or decrypt')
parser.add_argument('key', help='encryption key or offset')
args = parser.parse_args()

# Generate Keylist for Selected Cipher
if args.method == 'c': # Caesar Cipher
    if args.key.isdigit() and int(args.key) <= 26:
        args.key = -1*int(args.key)
        key = string.ascii_uppercase[args.key:]+string.ascii_uppercase[:args.key]
    else:
        raise ValueError('Caesar cipher key must be a positive integer no larger than '+str(len(string.ascii_uppercase)))
elif args.method == 'k': # Keyword Cipher
    if args.key.isalpha() and len(set(args.key)) == len(args.key):
        args.key = args.key.upper()
        key = args.key + string.ascii_uppercase.translate(None, args.key)
    else:
        raise ValueError('Keywork cipher key must be alphabetical with no repeated characters')

# Set ClearList and CipherList for selected Method
if args.action == 'enc': # Encryption
    clear = string.ascii_uppercase
    cipher = key
    out_file = "ciphertext.txt"
elif args.action == 'dec': # Decryption
    cipher = string.ascii_uppercase
    clear = key
    out_file = "plaintext.txt"

#Read-in text and create output string holder
msg = list(sys.stdin.read().upper())
out = ''

#En/De-crypt msg
for char in msg:
    if char in clear:
        out += cipher[clear.index(char)]
    else:
        out += char

# In via stdin, but out via file. What logic is this?????
#print out
out_file = open(out_file, "w")
out_file.write(out)
out_file.close()
