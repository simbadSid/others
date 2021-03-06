#!/bin/bash


OPTION_CIPHER="--cipher"
OPTION_DECIPHER="--decipher"

DIR_NAME="papers"
COMPRESS_NAME="${DIR_NAME}.zip"
CIPHERED_NAME="${COMPRESS_NAME}.gpg"

myEcho()
{
	 echo -e "\t>>>>"${1}
}


cipher()
{
	zip -er ${COMPRESS_NAME} ${DIR_NAME}
	gpg --cipher-algo AES256 -c ${COMPRESS_NAME}
	rm -f ${COMPRESS_NAME}

	while true; do
		myEcho "Confirm suppression of \"${DIR_NAME}\" [Y/n]:"
		read answer
		if [ ${answer} == "Y" ] || [ ${answer} == "y" ]; then
			rm -rf ${DIR_NAME}
			myEcho "File \"${DIR_NAME}\" deleted"
		elif [ ${answer} == "N" ] || [ ${answer} == "n" ]; then
	                myEcho "File \"${DIR_NAME}\" not deleted (carefull when u commit)"
		else
			continue
		fi
		break
	done
}

decipher()
{
	gpg ${CIPHERED_NAME}
	unzip ${COMPRESS_NAME}
	rm -f ${COMPRESS_NAME}
}



if [ ${1} == ${OPTION_CIPHER} ]; then
	cipher
elif [ ${1} == ${OPTION_DECIPHER} ]; then
	decipher
else
	myEcho "Usage: ${0} [${OPTION_CIPHER} | ${OPTION_DECIPHER}]"
fi
