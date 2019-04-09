i="1"

timestamp() {
	
	date +"%s"
}

while true ; do

	number=$((( RANDOM % 10 ) + 1))

	while [ $i -le $number ]; do

		responseTime=$RANDOM
		echo "$(timestamp),$responseTime,Look at Product,200,,Thread-Gruppe 1-2,text,true,,93753,760,10,10,http://localhost:30080/tools.descartes.teastore.webui/product?id=233,63,0,0" >> mylogfile.log
		i=$[$i+1]

	done

	i=1
	sleep 1

done