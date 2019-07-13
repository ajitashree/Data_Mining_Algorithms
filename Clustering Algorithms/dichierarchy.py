import sys
import numpy as np
import random
import copy
from numpy import linalg as LA
from scipy.cluster.hierarchy import linkage
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from scipy.cluster import hierarchy

def expectationStep(clus, documents, mean, C):

	L1 = []
	L2 = []
	for c in range(len(clus)):
		m1 = LA.norm(np.subtract(documents[clus[c]],mean[0]))
		m2 = LA.norm(np.subtract(documents[clus[c]],mean[1]))
		if m2 > m1 :
			C[c] = 0
			L1.append(clus[c])
		else:
			C[c] = 1;
			L2.append(clus[c])

	return (L1, L2)


def maximizationStep(clus, documents, mean, C):

	denoms = np.asarray([0, 0])
	mean.fill(0)

	for c in range(len(clus)):
		mean[C[c]] += documents[clus[c]]
		denoms[C[c]] += 1

	for i in range(len(denoms)):
		if(denoms[i] is not 0):
			mean[i] /= denoms[i]

def kmeans(clus, documents, NoOfWords):

	l = len(clus)
	if l == 1:
		return (False, [clus])
	mean = np.zeros((2, NoOfWords))
	mean[0] = documents[clus[0]]
	mean[1] = documents[clus[l/2]]

	C = np.zeros(l, dtype=np.int64)
	Cprev = np.zeros(l, dtype=np.int64) - 1

	while(True):

		if (np.all(C == Cprev)):
			break
		Cprev = np.asarray(C)
		(L1, L2) = expectationStep(clus, documents, mean, C)
		maximizationStep(clus, documents, mean, C)

	if len(L1) == 0 or len(L2) == 0:
		return (False, [clus])
	else:
		return (True, [L1] + [L2])

def printwords(clusters, documents, words, level):
	for c in clusters:
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



def clustering(documents, clusters, NoOfWords, words):

	level = 1
	while(True):

		print "Level", level
		flag = False
		newClusters = []

		printwords(clusters, documents, words, level)
		for c in clusters:
			(f, nc) = kmeans(c, documents, NoOfWords) 
			newClusters += nc
			flag = (flag  or f)

		level += 1
		clusters = list(newClusters)

		if (not flag):
			break

	return clusters

if __name__ == '__main__':

	with open('dataset2.txt', 'r') as f:
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

	clusters = [[x for x in range(NoOfDoc)]]
	clusters = clustering(documents, clusters, NoOfWords, words)

	#for c in clusters:
	#	print c

	sys.setrecursionlimit(1500)
	Z = hierarchy.linkage(documents, 'single')
	plt.figure(2, figsize=(20, 10))
	dn = hierarchy.dendrogram(Z, 3, truncate_mode = 'level')
	plt.show()
