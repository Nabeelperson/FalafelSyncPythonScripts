#This program controls two nodes. One that fluctuates and the other is online continously
#We want to test the txmempool sync protocol by flcutuating one node on/off and seeing if the 
#mempool sync messages have any impact on the prefromance of compact blocks on fluctuating ndoes


import time
import os

timeSEC = 600 #10 mins

fn = None
command = None
iterations = 432
dutyCycleOn = 0.9

def timeString():
	curTime = time.localtime(time.time())
	return str(curTime.tm_year) + str(curTime.tm_mon) + str(curTime.tm_mday)+ ' - ' + str(curTime.tm_hour) + ':' + str(curTime.tm_min) + ':' + str(curTime.tm_sec) + ' : '

logfn = open('/home/node003/.bitcoin/expLogFiles/logNode003PY.txt','w')
logfn.write(timeString() + 'STARTING EXPERIMENT NODE003: 90 percent duty cycle\n')
logfn.close()

#time.sleep(3600 * 2) #two hours to allow nodes to sync up sightly

for inc in range(iterations):
	os.system('echo Nislab003 | sudo -S ifconfig enp0s25 up')
	os.system('bitcoin-cli addnode \"128.197.128.218\" \"add\"')
	logfn = open('/home/node003/.bitcoin/expLogFiles/logNode003PY.txt','a')
	logfn.write(timeString() + 'node ethernet network switched on\n')
	logfn.close()
	#Allow node to run before taking it down
	time.sleep(timeSEC * dutyCycleOn)
	logfn = open('/home/node003/.bitcoin/expLogFiles/logNode003PY.txt','a')
	os.system('echo Nislab003 | sudo -S ifconfig enp0s25 down')
	logfn.write(timeString() + 'node ethernet network switched off\n')
	logfn.close()
	time.sleep(timeSEC * (1-dutyCycleOn))
	
	
logfn = open('/home/node003/.bitcoin/expLogFiles/logNode003PY.txt','a')
logfn.write(timeString() + '--------END EXPERIMENT NODE003--------\n')
logfn.close()
os.system('echo Nislab003 | sudo -S ifconfig enp0s25 up')
