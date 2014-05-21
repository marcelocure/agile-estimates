from Crypto import Random
from Crypto.Cipher import AES
import base64

bs = 32

def pad(s):
	return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

key = '1234567890abcdef'

def unpad(s):
	return s[:-ord(s[len(s)-1:])]

def encrypt(raw):
	raw = pad(raw)
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	print key
	return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt(enc):
	enc = base64.b64decode(enc)
	iv = enc[:AES.block_size]
	cipher = AES.new(key, AES.MODE_CBC, iv)
	return unpad(cipher.decrypt(enc[AES.block_size:]))
