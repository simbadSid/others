import Tkinter, tkSimpleDialog 
import base64
import gzip
import shutil
import os
from subprocess import call
from cipheror import Cipheror


STR_TITLE_PASS		= "Password"
STR_LABEL_PASS		= "Please enter password:"
STR_LABEL_PASS2		= "Please re-enter the same password:"

EXTENSION_COMPRESSED	= '.zip'
EXTENSION_CIPHERED	= '.gpg'
PATH_TO_COMPRESS	= 'papers/'
PATH_RESULT		= 'rowData/'



def myPrint(msg, preNewLine=False, header="\t>>>>"):
	if (preNewLine):
		print("")
	print(header + msg)


def getPass(nbTry=1):
	root	= Tkinter.Tk()						# dialog needs a root window, or will create an "ugly" one for you
	root.withdraw()							# hide the root window
	PASS	= tkSimpleDialog.askstring(STR_TITLE_PASS, STR_LABEL_PASS, show='*', parent=root)
	if (PASS == None):
		return None
	for i in range(nbTry):
		PASS2	= tkSimpleDialog.askstring(STR_TITLE_PASS, STR_LABEL_PASS2,show='*', parent=root)
		if (PASS2 == None):
			return None
	root.destroy()							# clean up after yourself!
	if ((nbTry > 1) and (PASS != PASS2)):
		raise ValueError("Password mismatch!")
	return PASS 


def compressFile(PASS, fileCompressed, fileDecompressed):
	myPrint('Compress \"' + fileCompressed + '\"  =>  \"' + fileDecompressed)
	call(["zip", "-P", PASS, "-r", fileDecompressed, fileCompressed])


def decompressFile(PASS, fileCompressed, fileDecompressed):
	myPrint('DeCompress \"' + fileCompressed + '\"  =>  \"' + fileName_out)
	call(["unzip", "-P", PASS, "-r", fileDecompressed, fileCompressed])


def cipherFile(cipheror, fileCiphered, fileDeciphered, chunkSize=64*1024):
	myPrint('Cipher file \"' + fileCiphered + '\"  =>  \"' + fileDeciphered)
	fileSize = os.path.getsize(fileCiphered)

	with open(fileCiphered, 'rb') as infile:
		with open(fileDeciphered, 'wb') as outfile:
			while True:
				chunk = infile.read(chunkSize)
				if len(chunk) == 0:
					break
				outfile.write(cipheror.cipher(chunk))


def decipherFile(cipheror, fileCiphered, fileDeciphered, chunkSize=64*1024):
	myPrint('Decipher file \"' + fileDeciphered + '\"  =>  \"' + fileCiphered)
	fileSize = os.path.getsize(fileDeiphered)

	with open(fileCiphered, 'rb') as infile:
		with open(fileDeciphered, 'wb') as outfile:
			while True:
				chunk = infile.read(chunkSize)
				if len(chunk) == 0:
					break
				outfile.write(cipheror.cipher(chunk))


def cipher(PASS, cipheror):
	myPrint('---------------------', preNewLine=True)
	myPrint('Scan directory \"' + PATH_TO_COMPRESS + '\"')
	myPrint('---------------------')
	for fileName_in in os.listdir(PATH_TO_COMPRESS):
		fileName_compressed     = PATH_RESULT + fileName_in + EXTENSION_COMPRESSED
		fileName_ciphered       = PATH_RESULT + fileName_in + EXTENSION_CIPHERED
		compressFile		(PASS, PATH_TO_COMPRESS +       fileName_in,            fileName_compressed)
		cipherFile      (cipheror, fileName_compressed,     fileName_ciphered)
		call(["rm", fileName_compressed])


def decipher(PASS, cipheror):
	myPrint('---------------------', preNewLine=True)
	myPrint('Scan directory \"' + PATH_TO_COMPRESS + '\"')
	myPrint('---------------------')
	for fileName_in in os.listdir(PATH_TO_COMPRESS):
		fileName_compressed     = PATH_RESULT + fileName_in + EXTENSION_COMPRESSED
		fileName_ciphered       = PATH_RESULT + fileName_in + EXTENSION_CIPHERED
		decipherFile      (cipheror, fileName_compressed,     fileName_ciphered)
#		decompressFile		(PASS, PATH_TO_COMPRESS +       fileName_in,            fileName_compressed)
#		call(["rm", fileName_compressed])


if __name__ == '__main__':
	myPrint('---------------------', preNewLine=True)
        myPrint('Get user password')
        myPrint('---------------------')
#	PASS	= getPass()
	PASS = "XXXXXXXXXX"
	if (PASS == None):
		myPrint('Abort')
		exit (0)
	cipheror= Cipheror(PASS)
	
	cipher(PASS, cipheror)
#	decipher(PASS, cipheror)


