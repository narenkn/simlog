process=`ps -aef | grep simlog_srv_save.py | grep -w python | wc -l`
if ((0 == process)) ; then
	/usr/bin/python ../src/simlog_srv_save.py -f `date +./save_file_%d%m%Y.pkl` 2>&1 | tee -a simlog_`date '+%d_%m_%Y'`.log > /dev/null &
fi

