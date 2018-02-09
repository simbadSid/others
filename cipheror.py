import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


DEFAULT_ENCODE_MODE	= False 


class Cipheror:
	# -----------------------------
	# Builder
	# -----------------------------
	def __init__(self, key):
		self._key	= SHA256.new(key).digest()		# use SHA-256 over our key to get a proper-sized AES key
		self._IV	= Random.new().read(AES.block_size)	# generate initialisation vector
		self._encryptor	= AES.new(self._key, AES.MODE_CBC, self._IV)


	# -----------------------------
	# Local methods
	# -----------------------------
	def cipher(self, text, encode=DEFAULT_ENCODE_MODE):
		padding	= (AES.block_size - len(text)) % AES.block_size	# calculate needed padding
		text	+= chr(padding) * padding			#Python 3.X:    text  += bytes([padding]) * padding
		data	= self._IV + self._encryptor.encrypt(text)	# store the IV at the beginning and encrypt
		return base64.b64encode(data).decode("latin-1") if encode else data


	def decipher(self, text, encode=DEFAULT_ENCODE_MODE):
		if decode:
			text = base64.b64decode(text.encode("latin-1"))
		data	= self._encryptor.decrypt(text[AES.block_size:])# decrypt
		padding	= ord(data[-1])					# pick the padding value from the end; Python 3.x: data[-1]
		if data[-padding:] != chr(padding) * padding:		# Python 3.x: bytes([padding]) * padding
			raise ValueError("Invalid padding...")
		return data[:-padding] 
