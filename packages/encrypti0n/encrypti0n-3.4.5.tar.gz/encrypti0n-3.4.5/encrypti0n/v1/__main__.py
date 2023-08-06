#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# insert the package for universal imports.
import os, sys, syst3m

# settings.
SOURCE_PATH = syst3m.defaults.get_source_path(__file__, back=2)
BASE = syst3m.defaults.get_source_path(SOURCE_PATH)
OS = syst3m.defaults.check_operating_system(supported=["linux", "osx"])
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
				"--encrypt /path/to/file":"Encrypt the provided file path.",
				"--decrypt /path/to/file":"Decrypt the provided file path.",
				"--generate-keys":"Generate a key pair.",
				"--generate-passphrase --length 32":"Generate a passphrase.",
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
			response = encryption.load_public_key()
			r3sponse.log(response=response)
			if not r3sponse.success(response): sys.exit(1)
			if os.path.isdir(file): 
				raise ValueError("COMING SOON.")
				response = encryption.encrypt_directory(file)
			else: 
				response = encryption.encrypt_file(file)
			r3sponse.log(response=response)

		# decrypt.
		elif self.argument_present('--decrypt'):
			file = self.get_argument('--decrypt')
			file = self.get_argument('--encrypt')
			encryption = self.get_encryption()
			response = encryption.load_private_key()
			r3sponse.log(response=response)
			if not r3sponse.success(response): sys.exit(1)
			if os.path.isdir(file): 
				raise ValueError("COMING SOON.")
				response = encryption.decrypt_directory(file)
			else: 
				response = encryption.decrypt_file(file)
			r3sponse.log(response=response)

		# generate-keys.
		elif self.argument_present('--generate-keys'):
			encryption = self.get_encryption(check_passphrase=True)
			response = encryption.generate_keys()
			r3sponse.log(response=response)

		# generate passphrase.
		elif self.argument_present('--generate-passphrase'):
			length = int(self.get_argument('--length', required=False, empty=32))
			print("Generated passphrase:",Formats.String("").generate(length=length, capitalize=True, digits=True))

		# invalid.
		else: 
			print(self.documentation)
			print("Selected an invalid mode.")

		#
	def get_encryption(self, check_passphrase=False):
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
			passphrase = utils.__prompt_password__("Enter the key's passphrase (leave blank to use no passphrase):")
			if check_passphrase and passphrase != utils.__prompt_password__("Enter the same passphrase:"):
				print("Error: passphrases do not match.")
				sys.exit(1)
		if passphrase in ["", "none", "null"]: passphrase = None
		# encryption.
		return AssymetricAES(
			public_key=public_key,
			private_key=private_key,
			passphrase=passphrase,)
	
# main.
if __name__ == "__main__":
	cli = CLI()
	cli.start()
