#!/bin/sh
INPUT=$1
BANK_TYPE="fineco"

usage () {
	echo "Convert XLS to QIF"
	echo "usage: "
	echo " `basename $0` [-h] [-t BANK_TYPE] filename.xls"
	echo "options:"
	echo "  -h  this help"
	echo "  -t  bank type to pass to b2q (fineco/fineco_comune)"
	echo ""
}

## PARSE OPTIONS
while getopts 'ht:' OPTION
do
	case $OPTION in
	t)
		BANK_TYPE="$OPTARG"
		;;
	h|?)
		usage
		exit 2
		;;
	esac
done
shift $(($OPTIND - 1))

if [ ! "$#" -eq 1 ]; then
	usage
	exit 1
fi

if [ -z $INPUT ]; then 
	usage
	exit 1
fi

if [ ! -f $INPUT ]; then 
	usage
	exit 1
fi

if [ ! `which libreoffice` ]; then
	echo "ERROR: libreoffice is missing."
	echo "Try to install it: sudo apt-get install libreoffice."
	exit 1
fi

if [ ! `which b2q` ]; then
	echo "ERROR: bankCSVtoQif is missing."
	echo "Try to install it: git clone https://github.com/giursino/BankCSVtoQif.git."
	exit 1
fi

TMPF=`tempfile`
echo "Converting to CSV..."
# Converting using libreoffice because previous program "xls2csv" don't parse correct the excel data value
# Excel store data value as number of days from 1 Gen 1900
# To setup the filter to export CSV in libreoffice see:
# https://wiki.openoffice.org/wiki/Documentation/DevGuide/Spreadsheets/Filter_Options#Filter_Options_for_the_CSV_Filter
# I decide to use ';' as separator to avoid problem with decimal character separator which in Italy is ',' (44)
#  Field separator: ';' (59)
#  Text delimiter: '"' (34)
#  Numeric format: system locale (it_IT)
# Note: It is also possibile to change locale export prefixing the command with LC_ALL=es_US but I don't like the date format.
libreoffice --headless --convert-to csv:"Text - txt - csv (StarCalc)":59,34,,, $INPUT > $TMPF
echo "Converting to QIF..."
b2q $BANK_TYPE $TMPF $1.qif
echo "Generated $1.qif."
rm -f $TMPF
echo "Done."
