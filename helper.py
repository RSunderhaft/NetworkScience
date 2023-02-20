import numpy as np
import pickle
import networkx as nx
import pandas as pd
import sys

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

#pulls the map from metis_map, converts to list where index = Metis_NodeID and value = Snap_NodeID
def get_map(name):
    mmap = pickle.load(open("MetisAlgo/" + name + "_map.obj", "rb"))
    mlist = [ele for ele in mmap]
    return mmap, mlist

#given (name and type) -> fname, load clustering and convert to list of communities (each community is its own list)
def get_clustering(name, type):
	mmap, mlist = get_map(name)

    #get fname
	if type == "mcl":
		clustering = np.loadtxt('output/' + name + '.metis.c1000.i2.0.b0.5', dtype = int)
	elif type == "metis":
		clustering = np.loadtxt('output/' + name + '.metis.part.100', dtype = int)
	elif type == "community":
		clustering = np.loadtxt('output/' + name + '_community.txt', dtype = int)

		clusters = [[] for i in range(len(np.unique(clustering[:,1])))]
    	# Iterates through file output and puts them in clusters
		for node in clustering:
			clusterID = node[1]
			nodeID= node[0]
			clusters[clusterID].append(nodeID)
		
		return clusters

	clusters = [[] for i in range(len(np.unique(clustering)))] #group by cluster
	for i in range(len(clustering)):
		clusters[clustering[i]].append(mlist[i])
	return clusters

#hopefully print results, modularity only works for wikiG (so setting it to zero)
def print_results(G, name, type):

	clusters = get_clustering(name, type)
	results = []
	V = set(G.nodes) #does not change
	modularity = nx.algorithms.community.modularity(G, clusters) #does not change
	for i in range(len(clusters)):
		#values
		C = set(clusters[i])
		C_bar = V - C
		numer = nx.cut_size(G, C, C_bar)
		denom = nx.cut_size(G, C, V)
		alt_denom = nx.cut_size(G, C_bar, V)
		
		#metrics
		ncut = numer / denom
		conductance = numer / min(denom, alt_denom)
		results.append({"Modularity": modularity, "n-cut": ncut, "Conductance": conductance})
	return pd.DataFrame(results)