
##################### Eclat algorithm ##############################################

import sys
import pandas as pd

def intersect(l1, l2):
	ans = []
	for l in l1:
		if l in l2:
			ans += [l]
	return list(set(ans))

def issubset(l, m):
	for i in l:
		if i not in m:
			return False
	return True

def Eclat(P, minsupport, F, FrequentSets):

	if (len(P) == 1):
		FrequentSets += [P[0]]

	for i in range(len(P)):
		F += [P[i]]
		Pa = []

		for j in range(i + 1, len(P)):

			Xab = list(set(P[i][0] + P[j][0]));
			Tab = intersect(P[i][1], P[j][1])

			if len(Tab) >= minsupport:
				Pa += [(Xab, Tab, len(Xab))]	
		

		if(Pa):
			Eclat(Pa, minsupport, F, FrequentSets)
		else:
			if (len(P) != 1):
				FrequentSets += [P[i]]


# returns l1 - l2			
def diff(l1, l2):
	ans = []
	for l in l1:
		if l not in l2:
			ans += [l]
	return ans

def DeEclat(Q, minsupport, IF, InFrequentSets):

	if (len(Q) == 1):
		InFrequentSets += [Q[0]]

	for i in range(len(Q)):
		IF += [Q[i]]
		Qa = []

		for j in range(i + 1, len(Q)):

			Xab = list(set(Q[i][0] + Q[j][0])); 
			Dab = diff(Q[j][2], Q[i][2])
			Sab = Q[i][1] - len(Dab)

			if Sab >= minsupport:
				Qa += [(Xab, Sab, Dab, len(Xab))]

		if (Qa):
			DeEclat(Qa, minsupport, IF, InFrequentSets)
		else:
			if (len(Q) != 1):
				InFrequentSets += [Q[i]]


if __name__ == '__main__':

	F = []
	IF = []
	P = []
	Q = []

	print ""
	minsupport = input('Enter minsupport: ')
	itemsets = ["TID"]
	FrequentSets = []
	InFrequentSets = []
	diffIndex = []

	database = pd.read_csv('./db.csv', header = None)
	#database = pd.read_csv('./db1.csv', header = None)
	#database = pd.read_csv('./dataset1.csv', header = None);

	for i in range(1, len(database.columns)):
		itemsets += [("i" + str(i))]

	database.columns = itemsets
	rowCount = database["TID"].count()
	del database["TID"]
	itemsets.remove("TID")
	
	print ""
	print "Itemsets", itemsets

	
	T = [i + 1 for i in range(rowCount)]
	
	for colName in itemsets:

		tmp = [index + 1 for index in range(rowCount) if database[colName][index] == 1]
		diffIndex = diff(T, tmp)

		if (len(tmp) >= minsupport):
			P += [(colName,tmp, 1)]
			Q += [(colName, len(tmp), diffIndex, 1)]


    ########################### PRINTING VALUES ECLAT ALGORITHM ###############################
	print " "
	print "     ECLAT Algorihtm   "
	Eclat(P, minsupport, F, FrequentSets)

	print "Freq Isets || Trans id's where pr"
	FrequentSets = sorted(FrequentSets, key = lambda x: x[2] ,reverse = True)

	for a,b,c in FrequentSets:
		print ''.join(a), "=>", b

	MFSeclat = []

	for f in FrequentSets:
		flag = True

		for m in MFSeclat:
			if (issubset(f[0], m[0])):
				flag = False

		if (flag):
			MFSeclat += [f]


	print " "
	print "MAximal Frequent set || Trans id's where pr"
	for a,b,c in MFSeclat:
		print ''.join(a), "=>", b

	
	############################ PRINTING VALUES DECLAT ALGORIHTM ###########################
	print " "
	print "     DEclat  Algorithm   "
	DeEclat(Q, minsupport, IF, InFrequentSets)

	MFSeclat = []
	print "Freq Isets || support of itemsets"

	InFrequentSets = sorted(InFrequentSets, key = lambda x: x[3] ,reverse = True)
	for a,b,c,d in InFrequentSets:
		print ''.join(a), "=>", b

	for f in InFrequentSets:
		flag = True

		for m in MFSeclat:
			if (issubset(f[0], m[0])):
				flag = False

		if (flag):
			MFSeclat += [f]

	print " "
	print "MAximal Frequent set || Trans id's where pr"
	for a,b,c,d in MFSeclat:
		print ''.join(a), "=>", b
	