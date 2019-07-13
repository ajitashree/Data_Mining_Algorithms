import sys 
import pandas as pd
import numpy as np
from numpy import linalg as LA

def findDistance(distance, documents):
	for i in range(len(documents)):
		for j in range(i + 1, len(documents)):
			distance[i][j] = LA.norm(np.subtract(documents[i],documents[j]) )** 2
			distance[j][i] = distance[i][j]

def findClusters(documents, clusters, distance):

	Ci = clusters[0]
	Cj = clusters[1]

	minDist = distance[clusters[0][1]][clusters[1][1]]

	for i in range(1, len(clusters)):
		for j in range(i + 1, len(clusters)):

			dist = distance[clusters[i][1]][clusters[i][1]]
			if (minDist > dist):
				minDist = dist
				Ci = clusters[i]
				Cj = clusters[j]

	return (Ci, Cj)

def printwords(clusters, documents, words, level):
	for c, c1 in clusters:
		print c
		print ""
		if (level <= 3):
			print "Words present in the documents of this clusters are"
			L = np.zeros(len(words)) + 1
			for i in c:
				L = [L[j] or documents[i][j] for j in range(len(words))]

			wrds = []
			for i in range(len(L)):
				if (L[i] == 1):
					wrds.append(words[i])
			print wrds

if __name__ == '__main__':

	with open ('./dataset2.txt', 'r') as f:
		read_data = f.readlines()

	with open('./vocab.txt', 'r') as fwords:
		data = fwords.readlines()

	words = []
	for w in data:
		words.append(w.strip())

	NoOfDoc = int(read_data[0].strip());
	NoOfWords = int(read_data[1].strip());
	totalWords = int(read_data[2].strip());
	documents = np.zeros((NoOfDoc, NoOfWords));
	distance = np.zeros((NoOfDoc, NoOfWords));

	for r in read_data[3:]:
		l = r.strip().split(' ')
		documents[int(l[0]) - 1][int(l[1]) - 1] = int(l[2])

	clusters = [([x], x) for x in range(NoOfDoc)]
	findDistance(distance, documents)

	itr = 1;
	while(len(clusters) > 1):
		print "Level ", itr
		(Ci, Cj) = findClusters(documents, clusters, distance)
		clusters.remove(Ci)
		clusters.remove(Cj)
		clus = list(set(Ci[0] + Cj[0]))
		clusDis = max(Ci[1], Cj[1])
		clusters += [(clus, clusDis)]	

		for i in  range(NoOfWords):
			documents[clusDis][i] = min(documents[Ci[1]][i], documents[Ci[1]][i])

		printwords(clusters, documents, words, itr)
		itr += 1


