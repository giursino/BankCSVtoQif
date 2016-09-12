#!/bin/sh
INPUT=$1

Usage () {
	echo "Convert XLS to QIF"
	echo "usage: "
	echo " `basename $0` filename.xls"
}

if [ -z $INPUT ]; then 
	Usage
	exit 1
fi

if [ ! -f $INPUT ]; then 
	Usage
	exit 1
fi

if [ ! `which xls2csv` ]; then
	echo "ERROR: xls2csv is missing."
	echo "Try to install it: sudo apt-get install catdoc."
	exit 1
fi

if [ ! `which b2q` ]; then
	echo "ERROR: bankCSVtoQif is missing."
	echo "Try to install it: git clone https://github.com/giursino/BankCSVtoQif.git."
	exit 1
fi

TMPF=`tempfile`
echo "Converting to CSV..."
xls2csv -c ',' $INPUT > $TMPF
echo "Converting to QIF..."
b2q fineco $TMPF $1.qif
echo "Generated $1.qif."
#libreoffice --calc $TMPF
rm -f $TMPF
echo "Done."
