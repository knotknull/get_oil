#!/bin/bash

# 20240131,3.429


for i in $(cat hist.csv )
do
	## Get the columns first
	dt=$(echo $i  | cut -f1 -d, )
	prc=$(echo $i | cut -f2 -d, )

	yr=$(echo $dt | cut -c1-4 )
	mon=$(echo $dt | cut -c5-6 )
	day=$(echo $dt | cut -c7-8 )
	qry="insert into pdo_prices (date, price, tmstmp) values ('${yr}-${mon}-${day}', $prc, current_localtimestamp());"
	echo ${qry}
	qry="insert into test_prices (date, price, tmstmp) values ('${yr}-${mon}-${day}', $prc, current_localtimestamp());"
	echo ${qry}

done
