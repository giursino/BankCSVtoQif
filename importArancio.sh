#!/bin/sh
INPUT=$1

file $INPUT --mime-type | grep -q 'application/vnd.ms-office'
if [ ! $? = 0 ]; then
	echo "ATTENZIONE: per utilizzare il file XLS scaricato dal sito di ING Direct Conto Arancio, si deve prima aprire con Libre Office e poi salvarlo nuovamente in formato XLS Excel in quanto il formato scaricato è in HTML"
	exit 1
fi

importBankXls.sh -t "arancio" "$INPUT"
