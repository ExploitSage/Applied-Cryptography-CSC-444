# Gustave Michel III
# 03/30/2017
# Encrypts an image with a randomly generated key using AND, OR, or XOR.
# Stores encrypted image and key to disk.
import sys
import os
import random
import operator
import argparse
from PIL import Image

def image_file(x):
    """'Type' for argparse - checks that image file exists and opens with PIL Image."""
    if not os.path.exists(x):
        raise argparse.ArgumentTypeError("{0} does not exist".format(x))
    return Image.open(x)

def random_byte():
    """Generate random integer value between 0 and 255."""
    return random.randint(0,255)

parser = argparse.ArgumentParser(description='Encrypt image with randomly generated key using AND, OR, or XOR.')
parser.add_argument('method', choices=['and','or','xor'], help='Encryption Method.')
parser.add_argument('image', type=image_file, help='Image File to Encrypt.')
args = parser.parse_args()

key_out = open('key_'+args.method+'.txt','w')
methods = {'and': operator.and_,'or': operator.or_,'xor': operator.xor}
pix = args.image.load()
rows, cols = args.image.size

for row in range(0,rows):
    for col in range(0,cols):
        key = tuple([random_byte() for rgb in range(0,3)])
        pix[row, col] = tuple(map(methods[args.method], pix[row,col], key))
        key_out.write("%d\n%d\n%d\n" % key)

args.image.save('encrypted_'+args.method+'.png')
key_out.close()
