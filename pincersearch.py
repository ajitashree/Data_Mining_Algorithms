
#########################implementation of pincer search#################################

import sys
from sets import Set
import pandas as pd
import itertools
from pprint import pprint

def unique(s):
	ans = []
	for i in s:
		if i not in ans:
			ans.append(i)
	return sorted(ans)

def union(s1, s2):
	return unique(s1 + s2)

def difference(s1, s2):
	ans = []
	for i in s1:
		if i not in s2:
			ans.append(i)

	return ans

def issubset(l, m):
	for i in l:
		if i not in m:
			return False
	return True


#checks if mset is subset of any set of MFCS
def notsubset(mset, MFCS):

	for m in MFCS:
		if issubset(mset, m):
			return False
	return True

# output new MFCS
def MFCS_gen(MFCS, S):

	for s in S:
		for m in MFCS:

			if issubset(s, m):
				MFCS = difference(MFCS, [m])
				for e in s:
	
					mset = difference(m, [e])   
					if (notsubset(mset, MFCS)):
						MFCS = union(MFCS, [mset])
		
	return MFCS


def findsubsets(S, m):
	l = list(itertools.combinations(S, m))
	return [sorted(list(i)) for i in l]

def prune(L, MFS, C, k):
	
	for c in C:

		flag = False
		for m in MFS:
			if issubset(c, m):
				flag = True
				C.remove(c)
				break

		if(not flag):
			sets = findsubsets(c, k)
			for s in sets:
				if s not in L:
					C.remove(c)
					break

	return C

def common(s1, s2):
	ans = 0
	for i in s1:
		if i in s2:
			ans += 1
	return ans

def recovery(C, L, MFS, k):

	for l in L:
		for m in MFS:

			if (common(l, m) == k-1):

				mlistAfter = difference(m, l)

				for lst in mlistAfter:
					C = union(C, [union(l, [lst])])

	return C



# output candidate set for next pass
def join(L, k):

	C = []
	for i in range(len(L)):
		for j in range(i+1,len(L)):

			if (common(L[i], L[j]) == k-1):
				C = union(C, [union(L[i], L[j])])
			#else: 
			#	break
	return C

def support(c, database):
	return sum([all(x) for x in zip(*[database[i]==1 for i in c])])


def pincersearch(database, minsupport, itemsets, threshold):

	L = []
	MFS = []
	MFCS = [list(itemsets)]
	k = 1
	C = [[item] for item in list(itemsets)] 

	while(C):

		L = []
		freqMFCS = []
		S = []

		for c in C:
			if (support(c, database) >= minsupport):
				L = union(L, [c])
			if (support(c, database) <= threshold):
				S = union(S, [c])

		for m in MFCS:
			if (support(m, database) >= minsupport):
				freqMFCS = union(freqMFCS, [m])

		for m in freqMFCS:
			MFS = union(MFS, [m])

		for l in L:
			for m in MFS:
				if issubset(l, m):
					L.remove(l)
					break

		for l in L:
			MFS += [l];

		Cnew = join(L, k)
		
		for l in L:
			for m in MFS:
				if issubset(l, m):
					Cnew = recovery(Cnew, L, MFS, k)
					break

		
		Cnew = prune(L, MFS, Cnew, k)

		MFCS = MFCS_gen(MFCS, S)
		C = Cnew
		k += 1


		print "Iteration", k-1
		print "MFCS:", MFCS
		print "MFS:", MFS
		print "L:", L
		print "S:", S
	
		print ""

	MFS.sort(lambda x,y: cmp(len(x), len(y)), reverse = True)
	MFSpincer = []
	print "Maximal Frequent set :"
	for f in MFS:
		flag = True

		for m in MFSpincer:
			if (issubset(f, m)):
				flag = False

		if (flag):
			MFSpincer += [f]
	
	print MFSpincer

#Bread,Diaper,Milk,Egg,Beer,Cola = Data set

if __name__ == '__main__':

	database = pd.read_csv('./db1.csv', header = None)
	#database = pd.read_csv('./db.csv', header = None)
	#database = pd.read_csv('./dataset1.csv', header = None)
	itemsets = ["TID"]

	for i in range(1, len(database.columns)):
		itemsets += [("i" + str(i))]


	database.columns = itemsets
	print ""
	minsupport = input('Enter minsupport: ')
	threshold = minsupport - 1

	del database["TID"]
	itemsets = database.keys()
	print " "
	pincersearch(database, minsupport, itemsets, threshold)
