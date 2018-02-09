import Tkinter, tkSimpleDialog 
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


STR_TITLE_PASS	= "Password"
STR_LABEL_PASS	= "Please enter password:"
STR_LABEL_PASS2	= "Please re-enter the same password:"

def myPrint(msg, header="\t>>>>"):
	print(header + msg)


def getPass():
	root	= Tkinter.Tk()					# dialog needs a root window, or will create an "ugly" one for you
	root.withdraw()						# hide the root window
	PASS	= tkSimpleDialog.askstring(STR_TITLE_PASS, STR_LABEL_PASS, show='*', parent=root)
	PASS2	= tkSimpleDialog.askstring(STR_TITLE_PASS, STR_LABEL_PASS2,show='*', parent=root)
	root.destroy()						# clean up after yourself!
	if (PASS != PASS2):
		raise ValueError("Password mismatch!")
	return password


def cipher(key, source, encode=True):
	key		= SHA256.new(key).digest()				# use SHA-256 over our key to get a proper-sized AES key
	IV		= Random.new().read(AES.block_size)			# generate IV
	encryptor	= AES.new(key, AES.MODE_CBC, IV)
	padding		= (AES.block_size - len(source)) % AES.block_size	# calculate needed padding
	source		+= chr(padding) * padding				#Python 3.X:    source	+= bytes([padding]) * padding
	data		= IV + encryptor.encrypt(source)			# store the IV at the beginning and encrypt
	return base64.b64encode(data).decode("latin-1") if encode else data

def decipher(key, source, decode=True):
	if decode:
		source = base64.b64decode(source.encode("latin-1"))
	key		= SHA256.new(key).digest()			# use SHA-256 over our key to get a proper-sized AES key
	IV		= source[:AES.block_size]			# extract the IV from the beginning
	decryptor	= AES.new(key, AES.MODE_CBC, IV)
	data		= decryptor.decrypt(source[AES.block_size:])	# decrypt
	padding		= ord(data[-1])					# pick the padding value from the end; Python 3.x: data[-1]
	if data[-padding:] != chr(padding) * padding:			# Python 3.x: bytes([padding]) * padding
		raise ValueError("Invalid padding...")
	return data[:-padding]						# remove the padding


def cipher(password):
	myPrint("Cipher file \"" + password + "\"")


if __name__ == '__main__':
	password = getPass()
	
