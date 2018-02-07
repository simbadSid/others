#!/bin/bash

#---------------------------------------
# User options
#---------------------------------------
OPTION_CIPHER="--cipher"
OPTION_DECIPHER="--decipher"

#---------------------------------------
# Global parameters
#---------------------------------------
PATH_BASE="papers"
PATH_CIPHERED="papers_ciphered"


#PASS="qwerty"

myEcho()
{
	 echo -e "\t>>>>"${1}
}


getPass()
{
	# password storage
	PASS=$(tempfile 2>/dev/null)

	# trap it
	trap "rm -f $PASS" 0 1 2 5 15

	# get password
	dialog	--title "Password" \
		--clear \
		--passwordbox "Enter your password" 10 30 2  > $PASS
ret=$?
echo "SSSSS"
#	clear
}

cipher()
{
	for file in `ls ${PATH_BASE}`;
	do
		echo "+++++++++++++++++++++"
		echo "ZIP: file ${file}"
                echo "+++++++++++++++++++++"
		zip -P ${PASS} -r ${file}.zip ${PATH_BASE}/${file}
                echo "+++++++++++++++++++++"
                echo "GPG: pass ${PASS}"
                echo "+++++++++++++++++++++"
		echo ${PASS} | gpg --passphrase-fd 0 --cipher-algo AES256 -c --output ${PATH_CIPHERED}/${file}.gpg ${file}.zip
		rm -f ${file}.zip
	done;
}


deleteClearFic()
{
	while true; do
		myEcho "Confirm suppression of \"${PATH_BASE}\" [Y/n]:"
		read answer
		if [ ${answer} == "Y" ] || [ ${answer} == "y" ]; then
			rm -rf ${DIR_NAME}
			myEcho "File \"${PATH_BASE}\" deleted"
		elif [ ${answer} == "N" ] || [ ${answer} == "n" ]; then
	                myEcho "File \"${PATH_BASE}\" not deleted (carefull when u commit)"
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


errorExit()
{
	 myEcho "Usage: ${0} [${OPTION_CIPHER} | ${OPTION_DECIPHER}]"
	exit
}

if [ $# -ne 1 ]; then
	errorExit
elif [ ${1} == ${OPTION_CIPHER} ]; then
	getPass
	cipher
	deleteClearFic
elif [ ${1} == ${OPTION_DECIPHER} ]; then
#	decipher ${PATH_BASE}
echo "AAAAAAAAAAAAAAAAAAAA"
else
#	errorExit
echo "XXXXXXXXXXXXXxxxxxxx"
fi


