# Gustave Michel III
# 03/30/2017
# Decrypts an image with provided key using AND, OR, or XOR.
# Stores decrypted image to disk.
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

def input_file(x):
    """'Type' for argparse - checks that file exists and opens read-only."""
    if not os.path.exists(x):
        raise argparse.ArgumentTypeError("{0} does not exist".format(x))
    return open(x,'r')

parser = argparse.ArgumentParser(description='Encrypt image with provided key using AND, OR, or XOR.')
parser.add_argument('method', choices=['and','or','xor'], help='Decryption Method.')
parser.add_argument('image', type=image_file, help='Image File to Decrypt.')
parser.add_argument('key', type=input_file, help='Text File containing Key.')
args = parser.parse_args()

methods = {'and': operator.and_,'or': operator.or_,'xor': operator.xor}
pix = args.image.load()
rows, cols = args.image.size

for row in range(0,rows):
    for col in range(0,cols):
        key = tuple([int(args.key.readline().strip()) for rgb in range(0,3)])
        pix[row, col] = tuple(map(methods[args.method], pix[row,col], key))

args.image.save('decrypted_'+args.method+'.png')
args.key.close()
