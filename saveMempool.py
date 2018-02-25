#This program periodically saves the mempool of a bitcoin node

import time
import os

#array used to store the mempool after 10sec, 10min, 15m, 30m, 45m and 60m in seconds 
timearray = [600, 1800, 3600]

fn = None
command = None
logfn = open('logNode001FINAL.txt','w')
iterations = 10000
dutyCycleOn = 0.9

def timeString():
	curTime = time.localtime(time.time())
	return str(curTime.tm_year) + str(curTime.tm_mon) + str(curTime.tm_mday)+ ' - ' + str(curTime.tm_hour) + ':' + str(curTime.tm_min) + ':' + str(curTime.tm_sec) + ' : '


logfn.write(timeString() + 'STARTING EXPERIMENT NODE001: 100 percent duty cycle, 2 hour resync period\n')
logfn.write(timeString() + 'STARTING EXPERIMENT NODE001: times tested in sec: 10, 600, 900, 1800, 2700, 3600\n\n')
logfn.close()

for timeSEC in timearray:
	logfn = open('logNode001FINAL.txt','a')
	logfn.write(timeString() + 'STARTING: ' + str(timeSEC) + ' second intervals\n')
	logfn.close()
	for inc in range(iterations):
		time.sleep(timeSEC)
		logfn = open('logNode001FINAL.txt','a')
		#BUILD STRING --- WORKS
		fn = str(timeSEC) + '_' + str(inc + 1) + '.txt'
		#save mempool to that file_name		
		command = 'bitcoin-cli getrawmempool > ' + fn
		os.system(command)
		command = 'bitcoin-cli getmempoolinfo >> ' + fn
		os.system(command)
		logfn.write(timeString() + fn + ' created\n')
		logfn.close()
	#Allow for soft reset of the two bitcoin mempools
	logfn = open('logNode001FINAL.txt','a')	
	logfn.write(timeString() + 'ENDING: ' + str(timeSEC) + ' second intervals\n')
	logfn.write(timeString() + 'RESYNCING NODES\n')
	logfn.close()
	time.sleep(3600*2)


logfn = open('logNode001FINAL.txt','a')
logfn.write(timeString() + '--------END EXPERIMENT NODE001--------\n')
logfn.close()
