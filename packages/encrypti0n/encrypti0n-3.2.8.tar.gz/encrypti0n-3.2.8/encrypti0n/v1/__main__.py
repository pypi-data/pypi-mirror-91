#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# insert the package for universal imports.
import os, sys, pathlib

# functions.
def __get_file_path_base__(path, back=1):
	path = path.replace('//','/')
	if path[len(path)-1] == "/": path = path[:-1]
	string, items, c = "", path.split("/"), 0
	for item in items:
		if c == len(items)-(1+back):
			string += "/"+item
			break
		else:
			string += "/"+item
		c += 1
	return string+"/"

# settings.
SOURCE_NAME = "ssht00ls"
VERSION = "v1"
SOURCE_PATH = __get_file_path_base__(__file__, back=2)
BASE = __get_file_path_base__(SOURCE_PATH)
sys.path.insert(1, BASE)

# imports.
from encrypti0n.v1.classes.config import *
from encrypti0n.v1.classes import utils
#from encrypti0n.v1.classes.rsa import RSA,EncryptedDictionary
from encrypti0n.v1.classes.aes import AssymetricAES


# the cli object class.
class CLI(cl1.CLI):
	def __init__(self):
		
		# cli.
		cl1.CLI.__init__(self,
			modes={
				"--generate-keys":"Generate a key pair.",
				"--encrypt /path/to/file":"Encrypt the provided file path.",
				"--decrypt /path/to/file":"Decrypt the provided file path.",
				"-h / --help":"Show the documentation.",
			},
			options={
				"--key /path/to/directory/":"Specify the path to the key's directory.",
				"--public-key /path/to/directory/public_key":"Specify the path to the public key.",
				"--private-key /path/to/directory/private_key":"Specify the path to the private key.",
				"-p / --passphrase 'Passphrase123!'":"Specify the key's passphrase.",
			},
			executable=__file__,
			alias=ALIAS,)

		#
	def start(self):
		
		# help.
		if self.argument_present('-h') or self.argument_present('--help'):
			print(self.documentation)

		# encrypt.
		elif self.argument_present('--encrypt'):
			file = self.get_argument('--encrypt')
			encryption = self.get_encryption()
			encryption.load_public_key()
			#if os.path.isdir(file): 
			response = encryption.encrypt(file, layers=layers, recursive=True)
			#else: encryption.encrypt_file(file, layers=layers)
			r3sponse.log(response=response)

		# decrypt.
		elif self.argument_present('--decrypt'):
			file = self.get_argument('--decrypt')
			file = self.get_argument('--encrypt')
			encryption = self.get_encryption()
			encryption.load_private_key()
			#if os.path.isdir(file): 
			response = encryption.decrypt(file, layers=layers, recursive=True)
			#else: encryption.decrypt_file(file, layers=layers)
			r3sponse.log(response=response)

		# generate-keys.
		elif self.argument_present('--generate-keys'):
			encryption = self.get_encryption()
			response = encryption.generate_keys()
			r3sponse.log(response=response)

		# invalid.
		else: 
			print(self.documentation)
			print("Selected an invalid mode.")

		#
	def get_encryption(self):
		# key.
		public_key = self.get_argument('--public-key', required=False)
		private_key = self.get_argument('--private-key', required=False)
		if public_key == None and private_key == None:
			key = self.get_argument('--key', required=True)
			public_key = f"{key}/public_key"
			private_key = f"{key}/private_key"
		# passphrase.
		passphrase = self.get_argument('-p', required=False)
		if passphrase == None:
			passphrase = self.get_argument('--passphrase', required=False)
		if passphrase == None:
			passprase = utils.__prompt_password__("Enter the key's passphrase (leave blank to use no passphrase):")
		if passprase in ["", "none", "null"]: passprase = None
		# encryption.
		encryption = AssymetricAES(
			public_key=public_key,
			private_key=private_key,
			passphrase=passphrase,)
		return encryption
	
# main.
if __name__ == "__main__":
	cli = CLI()
	cli.start()
