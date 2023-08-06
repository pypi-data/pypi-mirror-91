#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from encrypti0n.v1.classes.config import *
from encrypti0n.v1.classes import utils, rsa

# imports.
import base64, string, random
from Crypto.Cipher import AES as _AES_
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2

# the symetric aes 254 object class.
class AES(object):
	def __init__(self, passphrase="MyPassphrase123!"):
		self.block_size = 16
		self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr(self.block_size - len(s) % self.block_size)
		self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]
		self.passphrase = passphrase
	def encrypt(self, raw):
		if raw in ["", b"", None, False]:
			return r3sponse.error_response("Can not encrypt null data.")
		response = self.get_key()
		if not r3sponse.success(response): return response
		key = response["key"]
		salt = response["salt"]
		if isinstance(raw, bytes):
			raw = raw.decode()
		raw = self.pad(raw)
		iv = Random.new().read(_AES_.block_size)
		cipher = _AES_.new(key, _AES_.MODE_CBC, iv)
		encrypted = base64.b64encode(iv + salt + cipher.encrypt(raw.encode()))
		if raw != b"" and encrypted == b"":
			return r3sponse.error_response("Failed to encrypt the specified data with the current passphrase / salt.")
		return r3sponse.success_response("Successfully encrypted the specified data.", {
			"encrypted":encrypted,
		})
	def decrypt(self, enc):
		if enc in ["", b"", None, False]:
			return r3sponse.error_response("Can not decrypt null data.")
		if isinstance(enc, str):
			enc = enc.encode()
		enc = base64.b64decode(enc)
		iv_salt = enc[:32]
		iv = iv_salt[:16]
		salt = iv_salt[16:]
		response = self.get_key(salt=salt)
		if not r3sponse.success(response): return response
		key = response["key"]
		cipher = _AES_.new(key, _AES_.MODE_CBC, iv)
		decrypted = self.unpad(cipher.decrypt(enc[32:]))
		if enc != b"" and decrypted == b"":
			return r3sponse.error_response("Failed to decrypt the specified data with the current passphrase / salt.")
		return r3sponse.success_response("Successfully decrypted the specified data.", {
			"decrypted":decrypted,
		})
	def get_key(self, salt=None):
		if salt == None:
			salt = self.generate_salt()["salt"]
		if isinstance(salt, str):
			salt = salt.encode()
		kdf = PBKDF2(self.passphrase, salt, 64, 1000)
		key = kdf[:32]
		return r3sponse.success_response("Successfully loaded the aes key.", {
			"key":key,
			"salt":salt,
		})
	def generate_salt(self):
		length=16
		chars = ''.join([string.ascii_uppercase, string.ascii_lowercase, string.digits])
		salt = ''.join(random.choice(chars) for x in range(length))
		return r3sponse.success_response("Successfully generated a salt.", {
			"salt":salt,
		})

# the assymetric aes 254 object class.
class AssymetricAES(object):
	def __init__(self,
		# the public key (str).
		public_key=None,
		# the private key (str).
		private_key=None,
		# the key passphrase (str / null).
		passphrase=None,
	):
		self.rsa = rsa.RSA(public_key=public_key, private_key=private_key, passphrase=passphrase)
	def generate_keys(self):
		return self.rsa.generate_keys()
	def load_keys(self):
		return self.rsa.load_keys()
	def load_private_key(self):
		return self.rsa.load_private_key()
	def load_public_key(self):
		return self.rsa.load_public_key()
	def encrypt(self, string):
		if isinstance(string, bytes):
			string = string.decode()
		
		# encrypt data with aes.
		passphrase = utils.__generate_shell_string__(characters=64, numerical_characters=True)
		aes = AES(passphrase=passphrase)
		response = aes.encrypt(string)
		if not r3sponse.success(response): return response
		aes_encrypted = response["encrypted"]
		if b" " in aes_encrypted:
			return r3sponse.error_response("AES encrypt data contains invalid ' ' character(s).")

		# encrypt aes key with rsa.
		response = self.rsa.encrypt_string(passphrase)
		if not r3sponse.success(response): return response
		rsa_encrypted = response["encrypted"]

		# pack encrypted.
		encrypted = rsa_encrypted+b" "+aes_encrypted

		# success.
		return r3sponse.success_response("Successfully encrypted the specified data.", {
			"encrypted":encrypted
		})

		#
	def decrypt(self, string):

		# split encrypted aes key.
		if isinstance(string, bytes):
			string = string.decode()
		try:
			key,encrypted = string.split(" ")
		#except:
		except KeyboardInterrupt:
			return r3sponse.error_response("Unable to unpack the encrypted data.")

		# decypt key with rsa.
		response = self.rsa.decrypt_string(key)
		if not r3sponse.success(response): return response
		passphrase = response["decrypted"].decode()

		# decrypt with aes.
		aes = AES(passphrase=passphrase)
		response = aes.decrypt(encrypted)
		if not r3sponse.success(response): return response
		decrypted = response["decrypted"]

		# success.
		return r3sponse.success_response("Successfully decrypted the specified data.", {
			"decrypted":decrypted
		})

		#

# initialize. 
"""
aes = AES(password="Mic60623!C")
aes.salt
 
# encrypt message
encrypted = aes.encrypt("This is a secret message".encode())
print(encrypted)
 
# decrypt using password
decrypted = aes.decrypt(encrypted)
print(decrypted)
"""