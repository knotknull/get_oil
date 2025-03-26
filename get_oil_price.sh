#!/bin/bash

# first backup the data file to todays data
#

chkdir=${HOME}/dev/get_oil_price

if [[ -f ${chkdir}/hist.txt && -f  ${chkdir}/get_oil_price.py ]]
then

	now=$(date '+%Y%m%d.%H%M%S')
	cp hist.txt hist.txt.${now}
	/usr/bin/python3 getpdo.py >> hist.txt
	exit $?
else
       	print "ERROR:  NOT FOUND ${chkdir}/hist.txt, ${chkdir}/get_oil_price.py" 
	exit 99	
fi
