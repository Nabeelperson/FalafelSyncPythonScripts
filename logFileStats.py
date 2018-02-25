#Written by Nabeel Younis under Professor Trachtenberg, NISLab Boston University

#The following program generates statistics about the activity of a full node
#The statistics recorded are: ratio of cmpct to normal blocks, compactblock successrate,
#time needed for a successful cmpctblock and a failed cmpctblock

#Some of the statistics generated use sliding windows instead of agragate calucaltions


import array


#WindowSize = 2 hours, ~12 blocks
WS = 36

#Opening the log and activity files
fnLog = open('logNode001.txt', 'r')
#fnAct = open('incomingMessages.txt', 'r')

fnOut = open('OLD_NOsync_node001_results.txt', 'w')

fnOut.write("EXPERIMENT 0: FLUCTUATING NODES WITH NO SYNC - NODE001 STABLE \n")


#blockStatus - fail or success - 0/1
blockStatus = array.array('i')
#missingTx - number of missing tx from failed blocks ONLY, does not include 0's from success
missingTx = array.array('i')
#blockType - whether block is normal or cmpct  - 0/1
blockType = array.array('i')
#slidingWindowSuccessRate - the last WS blocks sucess rate
slidingWindowSuccessRate = array.array('d')
#slidingWindowMissingTx - average missing TX in last WS blocks
slidingWindowMissingTx = array.array('d')


sucCmpct = 0
failCmpct = 0
txMiss = 0
totalCmpct = 0

for line in fnLog:
	if line.find('FAILCMPCT') !=-1:
		blockStatus.append(0)
		totalCmpct = totalCmpct + 1
		failCmpct = failCmpct + 1
		#fnOut.write('%.4f	%.4f\n' %(sucCmpct/totalCmpct, txMiss/failCmpct))
	if line.find('SUCCESSCMPCT') !=-1:
		blockStatus.append(1)
		missingTx.append(0)
		totalCmpct = totalCmpct + 1
		sucCmpct = sucCmpct + 1
		#fnOut.write('%.4f	0\n' %(sucCmpct/totalCmpct))
	if line.find('REQSENT') !=-1:
		tx = int(line[line.find('missing') + 8:line.find(' tx')])
		missingTx.append(tx)
		txMiss = txMiss + tx

sucCount = 0
txCount = 0

for i in range(36, totalCmpct - 1):
	for j in range( i - WS, i):
		sucCount = sucCount + blockStatus[j]
	slidingWindowSuccessRate.append(sucCount / WS)
	sucCount = 0


for i in range(1, WS):
	fnOut.write('%d	%d	0	%d\n' %(i,blockStatus[i], missingTx[i]))

for i in range(WS + 1, totalCmpct - 2):
	fnOut.write('%d	%d	%.4f	%d\n' %(i, blockStatus[i], slidingWindowSuccessRate[i - WS], missingTx[i]))

