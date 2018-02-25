#This program periodically disables network connection for time specified in timeSec
#	network up for timeSec/2 seconds
#	get mempool data
#	network down for timeSec/2 seconds
# 	loop back
#This is a 50 percent uptime node senario, another time interval to test is 90 percent uptime
#Hypothesis: As the time interval increases, the size (in B) of the mempool differances will increase exponentially
import time
import os

#array used to store the mempool after 10sec, 10min, 15m, 30m, 45m and 60m in seconds 
timearray = [600, 1800, 3600]
fn = None
command = None
iterations = 10000
dutyCycleOn = 0.9


def timeString():
	curTime = time.localtime(time.time())
	return str(curTime.tm_year) + '-' + str(curTime.tm_mon) + '-' + str(curTime.tm_mday)+ ' - ' + str(curTime.tm_hour) + ':' + str(curTime.tm_min) + ':' + str(curTime.tm_sec) + ' : '

logfn = open('logNode003FINAL.txt','w')
logfn.write(timeString() + 'STARTING EXPERIMENT NODE002: %f duty cycle, 2 hour resync period\n' % dutyCycleOn)
logfn.write(timeString() + 'STARTING EXPERIMENT NODE002: times tested in seconds: 10, 600, 900, 1800, 2700, 3600\n\n')
logfn.close()


for timeSEC in timearray:
	logfn = open('logNode003FINAL.txt','a')
	logfn.write(timeString() + 'STARTING: ' + str(timeSEC) + ' second intervals\n')
	for inc in range(iterations):
		#Make sure the network is on
		os.system('echo Nislab003 | sudo -S ifconfig enp0s25 up')
		logfn = open('logNode002.txt','a')
		logfn.write(timeString() + 'node ethernet network switched on\n')
		logfn.close()
		#Allow node to run before taking it down
		time.sleep(timeSEC * dutyCycleOn)
		logfn = open('logNode003FINAL.txt','a')
		#Build file name
		fn = str(timeSEC) + '_' + str(inc + 1) + '_up.txt'
		#save mempool to that file_name
		command = 'bitcoin-cli getrawmempool > ' + fn
		os.system(command)
		#Append the current mempool's metadata to the end of the file
		command = 'bitcoin-cli getmempoolinfo >> ' + fn
		os.system(command)
		
		logfn.write(timeString() + fn + ' created\n')
		
		#switch off ethernet network, easier than switching off bitcoin core
		os.system('echo Nislab003 | sudo -S ifconfig enp0s25 down')
		logfn.write(timeString() + 'node ethernet network switched off\n')
		logfn.close()
		#Downtime
		time.sleep(timeSEC * (1-dutyCycleOn))
		logfn = open('logNode003FINAL.txt','a')
		#Build file name
		fn = str(timeSEC) + '_' + str(inc + 1) + '_down.txt'
		#save mempool to that file_name
		command = 'bitcoin-cli getrawmempool > ' + fn
		os.system(command)
		#Append the current mempool's metadata to the end of the file
		command = 'bitcoin-cli getmempoolinfo >> ' + fn
		os.system(command)
		logfn.write(timeString() + fn + ' created\n')
		logfn.close()
	#2 hour sleep between the different time intervals to allow the nodes to sync up enough
	logfn = open('logNode003FINAL.txt','a')
	logfn.write(timeString() + 'ENDING: ' + str(timeSEC) + ' second intervals\n')
	os.system('sudo ifconfig enp0s25 up')
	logfn.write(timeString() + 'node ethernet network switched on\n')
	logfn.write(timeString() + 'RESYNCING NODES\n')
	logfn.close()
	time.sleep(3600*2)

logfn = open('logNode003FINAL.txt','a')
logfn.write(timeString() + '--------END EXPERIMENT NODE002--------\n')
logfn.close()

