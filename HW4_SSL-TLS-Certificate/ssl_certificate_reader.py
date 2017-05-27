# Gustave Michel III
# 05/10/2017
# Extract SSl/TLS Certificate and Cipher Information and print to Stdout
# Bonus Complete: Prints Public Key, extracted from certificate, requires pyOpenSSL

import argparse
import socket
import ssl
import OpenSSL

parser = argparse.ArgumentParser(description='Extract SSL/TLS Certificate and Cipher information for given Hostname. Bonus: Extracts Public Key')
parser.add_argument('hostname', help='Domain/IP of server to connect to')
parser.add_argument('port', type=int, help='Port to connect to server')
args = parser.parse_args()

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = False
context.load_default_certs()

# Setup Socket, and Wrap with SSL Context
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
wrappedSocket = context.wrap_socket(sock)

# Try to connect, add www. to beginning if it doesn't work.
# Good Going LaTech...
try:
    wrappedSocket.connect((args.hostname, args.port))
except ssl.SSLError:
    wrappedSocket.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wrappedSocket = context.wrap_socket(sock)
    wrappedSocket.connect(('www.'+args.hostname, args.port))

# Cert and Cipher Info
cert = wrappedSocket.getpeercert()
cipher = wrappedSocket.cipher()

# Bonus, Get Public Key!
der_cert = wrappedSocket.getpeercert(binary_form=True)
x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, der_cert)
pub_key = OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, x509.get_pubkey())

wrappedSocket.close()

# Print all the things!
print "Domain names:\t%s" % ", ".join([domain[1] for domain in cert['subjectAltName']])
print "Issue Date:\t%s" % cert['notBefore']
print "Expiry Date:\t%s" % cert['notAfter']
print "Issuer\'s CN:\t%s" % ", ".join([issuer_attr[0][1] for issuer_attr in cert['issuer'] if issuer_attr[0][0] == "commonName"])
print "CA Issuers:\t%s" % cert['caIssuers'][0]
print "OCSP:\t\t%s" % cert['OCSP'][0]
print "Cipher:\t\t%s" % cipher[0]
print "SSL Version:\t%s" % cipher[1]
print "Secret Bits:\t%s" % cipher[2]
print ""
print pub_key
