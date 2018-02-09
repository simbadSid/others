import Tkinter, tkSimpleDialog 
import base64
import gzip
import shutil
import os

from cipheror import Cipheror


STR_TITLE_PASS		= "Password"
STR_LABEL_PASS		= "Please enter password:"
STR_LABEL_PASS2		= "Please re-enter the same password:"

EXTENSION_COMPRESSED	= '.gz'
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


def compressFile(fileName_in, fileName_out):
	myPrint('Compress \"' + fileName_in + '\"  =>  \"' + fileName_out)
	if (os.path.isdir(fileName_in)):				# Compress a directory
		shutil.make_archive(fileName_out, 'zip', fileName_in)
	else:								# Compress a regular file
		with open(fileName_in, 'rb') as f_in, gzip.open(fileName_out, 'wb') as f_out:
			shutil.copyfileobj(f_in, f_out)


def cipherFile(PASS, fileName_in, fileName_out, chunkSize=64*1024):
        myPrint('Cipher   file \"' + fileName_in + '\"  =>  \"' + fileName_out)


if __name__ == '__main__':
	myPrint('---------------------', preNewLine=True)
        myPrint('Get user password')
        myPrint('---------------------')
	PASS	= getPass()
	if (PASS == None):
		myPrint('Abort')
		exit (0)
	cipheror= Cipheror(PASS)

        myPrint('---------------------', preNewLine=True)
        myPrint('Scan directory \"' + PATH_TO_COMPRESS + '\"')
        myPrint('---------------------')
	for fileName_in in os.listdir(PATH_TO_COMPRESS):
		fileName_compressed	= PATH_RESULT + fileName_in + EXTENSION_COMPRESSED
		fileName_ciphered	= PATH_RESULT + fileName_in + EXTENSION_CIPHERED
		compressFile	(	PATH_TO_COMPRESS +	fileName_in,		fileName_compressed)
		cipherFile	(PASS,				fileName_compressed,	fileName_ciphered)


