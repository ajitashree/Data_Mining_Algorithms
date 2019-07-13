#include <iostream>
#include <vector>
#include <string.h>
#include <algorithm>
#include <map>

using namespace std;

long adjMatrix[1000][1000], adjMatrixT[1000][1000];
void printGraph(map <long, vector <long> > adjList, long N)
{

	cout << "The Graph is represented as : " << endl;
	for(long i = 1; i <= N; i++)
	{
		cout << i << " : ";
		for (auto j : adjList[i])
		{
			cout << j << " ";
		}
		cout << endl;
	}

	cout << "Adjacency Matrix and its transpose : " << endl;
	for(long n = 0; n < N; n++)
	{
		for(long m = 0; m < N; m++)
		{
			cout << adjMatrix[n][m] << " ";
		}
		cout << "		";
		for(long m = 0; m < N; m++)
		{
			cout << adjMatrixT[n][m] << " ";
		}
		cout << endl;
	}
}

void printVectors(vector <double> A, vector <double> H)
{
	for (auto a : A)
		cout << a << " ";
	cout << endl;
	for (auto h : H)
		cout << h << " ";
	cout << endl;
}

vector <double> mutiply(bool trans, vector <double> vec)
{
	double maxVal = -1;
	long N = vec.size();
	vector <double> res;

	for (long i = 0; i < N; i++)
	{
		double tmp = 0, op;
		for (long j = 0; j < N; j++)
		{
			op = (trans == 1) ? adjMatrixT[i][j] : adjMatrix[i][j];
			tmp += op*vec[j];
		}
		res.push_back(tmp);
		if (tmp > maxVal) maxVal = tmp;
	}

	for (long i = 0; i < res.size(); i++)
		res[i] = (res[i]/(double)maxVal);

	return res;
}

void transpose(long N)
{
	for (long i = 0; i < N; i++)
	{
		for(long j = 0; j < N; j++)
		{
			adjMatrixT[j][i] = adjMatrix[i][j];
		}
	}
}

double ab(double a)
{
	if (a < 0) return -1*a;
	return a;
}	

bool equal(vector <double> A, vector <double> _A)
{
	for (long i = 0; i < A.size(); i++)
	{
		if (A[i] != _A[i]) return false;
	}
	return true;
}

bool converged(vector <double> A, vector <double> _A, vector <double> H, vector <double> _H)
{
	if(equal(A, _A) && equal(H, _H)) return true;

	return false;
}

void printNodes(vector <double> A, vector <double> H)
{
	double maxA = *max_element(A.begin(), A.end());
	double maxH = *max_element(H.begin(), H.end());
	vector <long> hubNodes, authNodes;

	for (long a = 0; a < A.size(); a++)
	{
		if(A[a] == maxA) authNodes.push_back(a + 1);
	}
	for (long h = 0; h < H.size(); h++)
	{
		if(H[h] == maxH) hubNodes.push_back(h + 1);
	}
	cout << endl;
	cout << "Hub nodes are : ";
	for (auto h : hubNodes) cout << h << " ";
	cout << endl;
	cout << "Authority Nodes are : ";
	for (auto a : authNodes) cout << a << " ";
	cout << endl;
	cout << endl;
}

int main(int argc, char const *argv[])
{
	long N;
	cin >> N;

	memset(adjMatrix, 0, sizeof(adjMatrix));
	map <long, vector <long> > adjList;

	vector <double> A, H, _A, _H;
	adjList[1].push_back(2);
	adjMatrix[0][1] = 1;

	for (long i = 3; i <= N; i++)
	{
		adjMatrix[0][i - 1] = 1;
		adjMatrix[i - 1][1] = 1;
		adjList[1].push_back(i);
		adjList[i].push_back(2);
	}
	transpose(N);
	printGraph(adjList, N);

	for (long i = 1; i <= N; i++)
	{
		A.push_back(1.0);
		_A.push_back(0.0);
		_H.push_back(0.0);
	}

	H = mutiply(false, A);
	while(!converged(A, _A, H, _H))
	{
		//printVectors(H, A);
		_A = A;
		_H = H;
		A = mutiply(true, _H); // A transpose
		H = mutiply(false, _A); // A	
	}

	cout << "The Hub and Authority vectors is : " << endl;
	printVectors(H, A);
	printNodes(A, H);
	return 0;
}