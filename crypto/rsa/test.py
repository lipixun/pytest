#!/usr/bin/env python
# encoding=utf8
# The RSA test

"""The RSA test
"""

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import base64

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5

def generate(length, pubfile, privfile):
    """Generate the RSA key pair
    """
    key = RSA.generate(length)
    with open(pubfile, 'wb') as fd:
        print >>fd, key.publickey().exportKey()
    with open(privfile, 'wb') as fd:
        print >>fd, key.exportKey()

def sign(keyfile, text):
    """Sign the text by key
    """
    with open(keyfile, 'rb') as fd:
        key = fd.read()
    key = RSA.importKey(key)
    h = SHA.new(text)
    signer = PKCS1_v1_5.new(key)
    return signer.sign(h)

def verify(keyfile, sig, text):
    """Verify the sign
    """
    with open(keyfile, 'rb') as fd:
        key = fd.read()
    key = RSA.importKey(key)
    h = SHA.new(text)
    verifier = PKCS1_v1_5.new(key)
    return verifier.verify(h, sig)

if __name__ == '__main__':

    from argparse import ArgumentParser

    def getArguments():
        """Get arguments
        """
        parser = ArgumentParser(description = 'RSA test tool')
        subParser = parser.add_subparsers(dest = 'type')
        # Generate
        genParser = subParser.add_parser('gen')
        genParser.add_argument('-l', '--length', dest = 'length', default = 2048, type = int, help = 'The length of the key')
        genParser.add_argument('--pub', dest = 'pub', required = True, help = 'The public key file')
        genParser.add_argument('--priv', dest = 'priv', required = True, help = 'The private key file')
        # Sign
        signParser = subParser.add_parser('sign')
        signParser.add_argument('--key', dest = 'key', required = True, help = 'The key file')
        signParser.add_argument('text', nargs = 1, help = 'The text')
        # Verify
        verifyParser = subParser.add_parser('verify')
        verifyParser.add_argument('--key', dest = 'key', required = True, help = 'The key file')
        verifyParser.add_argument('--sig', dest = 'sig', required = True, help = 'The signature')
        verifyParser.add_argument('text', nargs = 1, help = 'The text')
        # Done
        return parser.parse_args()

    def main():
        """The main entry
        """
        args = getArguments()
        if args.type == 'gen':
            # Generate key pair
            generate(args.length, args.pub, args.priv)
        elif args.type == 'sign':
            # Sign
            print base64.b64encode(sign(args.key, args.text[0]))
        else:
            # Verify
            print verify(args.key, base64.b64decode(args.sig), args.text[0])

    main()
