import sys
import pickle

def metis_map(inFile_name, objFile_name):
	if(len(sys.argv) < 3):
		print("./Snap2Metis.py input-file output-file [current version works only on unweighted graph.]")
		sys.exit(0)
	inFile = open(inFile_name, "r")

	#check if directed
	line = inFile.readline()
	directed = False #not "Undirected" in line
	if(directed):
		print("The graph is directed.")
	else:
		print("The graph is undirected.")

	dic = dict()
	nodeNum = 4039
	edgeNum = 88234
	for line in inFile:
		if("#" in line):
			if("Nodes" in line):
				strSplit = line.strip().split()
				nodeNum = int(strSplit[2])
				edgeNum = int(strSplit[4])
				print(nodeNum,edgeNum)
			continue
		strSplit = [int(ele) for ele in line.strip().split()]
		if(strSplit[0] == strSplit[1]):
			continue
		if(strSplit[0] in dic):
			dic[strSplit[0]].append(strSplit[1])
		else:
			dic[strSplit[0]] = []
			dic[strSplit[0]].append(strSplit[1])
		if(directed == False):
			if(strSplit[1] in dic):
				dic[strSplit[1]].append(strSplit[0])
			else:
				dic[strSplit[1]] = []
				dic[strSplit[1]].append(strSplit[0])
	
	count = 1 # new ids start from 1...
	idMap = dict() #discrete 2 continuous; Or original 2 new. 
	keySet = [ele for ele in dic]
	for ele in keySet:
		idMap[ele] = count
		count += 1

	inFile.close()
	objFile = open(objFile_name, "wb")
	pickle.dump(idMap, objFile)
	objFile.close()