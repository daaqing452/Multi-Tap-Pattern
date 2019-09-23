#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <vector>
#include <map>
#define SQR(x) ((x)*(x))
using namespace std;

#define NORMALIZE
#define PRINT_SCORE
#define SHUFFLE
#define TAP_CHECK

typedef vector<pair<float,int> > Candidates;
const int N = 9999, S = 2, LMAX = 60, D = 3;
const int TAPS[] = {
	2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
	2, 2, 2, 2, 2, 2, 2, 2, 3, 3,
	3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
	3, 3
};

const int SP = LMAX;

float data[N][S][LMAX][D];
int label[N], aTrain[N], aTest[N], userSz[99];
int nTrain = 0, nTest = 0, L;
float f[LMAX][LMAX];
vector< pair<int,int> > resLabel;

vector<float> scoreTrue;
vector<float> scoreFalse;

float dtwDist(float a[], float b[]) {
	float d = 0;
	for (int i = 0; i < D; i++) d += fabs(a[i] - b[i]);
	//for (int i = 0; i < D; i++) d += SQR(a[i] - b[i]);
	//d = sqrt(d);
	return d;
}

float dtwOne(float a[][D], float b[][D]) {
	memset(f, 60, sizeof(f));
	for (int i = 0; i < L; i++)
		for (int j = max(0, i - SP); j < min(L, i + SP); j++) {
			float d = 1e20;
			if (i > 0) d = min(d, f[i - 1][j]);
			if (j > 0) d = min(d, f[i][j - 1]);
			if (i > 0 && j > 0) d = min(d, f[i - 1][j - 1]);
			if (i == 0 && j == 0) d = 0;
			f[i][j] = d + dtwDist(a[i], b[j]);
		}
	return f[L - 1][L - 1];
}

Candidates dtwAll(float a[][LMAX][D], int canMaxNum, int trueLabel) {
	Candidates can;
	can.push_back(make_pair(1e20, -1));
	for (int i = 0; i < nTrain; i++) {
		int x = aTrain[i];
#ifdef TAP_CHECK
		if (TAPS[trueLabel] != TAPS[label[x]]) continue;
#endif
		float scoreAcc = dtwOne(a[0], data[x][0]);
		float scoreGyr = dtwOne(a[1], data[x][1]);
		float score = 1.5 * scoreAcc + scoreGyr;
		//float score = scoreGyr;
		can.push_back(make_pair(score, label[x]));
		int j = can.size() - 1;
		while (j > 0 && can[j].first < can[j - 1].first) {
			swap(can[j], can[j - 1]);
			j--;
		}
		if (can.size() > canMaxNum) can.pop_back();
	}
	return can;
}

int main() {
	FILE *fin = fopen("plain.txt", "r");
	int n, n1, n2;
	fscanf(fin, "%d%d%d", &n, &n1, &n2);
	for (int i = 0; i < n; i++)
		for (int j = 0; j < n1; j++)
			for (int k = 0; k < n2; k++) {
				fscanf(fin, "%f", &data[i][j / 3][k][j % 3]);
				//data[i][j / 3][k][j % 3] = int(data[i][j / 3][k][j % 3] * 100) / 100.0;
			}
	for (int i = 0; i < n; i++)
		fscanf(fin, "%d", &label[i]);
	L = n2;
	printf("L=%d\n", L);
	int nUser;
	fscanf(fin, "%d", &nUser);
	userSz[0] = 0;
	for (int i = 1; i <= nUser; i++) {
		fscanf(fin, "%d", &userSz[i]);
		userSz[i] += userSz[i - 1];
	}
	fclose(fin);

#ifdef NORMALIZE
	for (int i = 0; i < n; i++)
		for (int j = 0; j < S; j++)
			for (int k = 0; k < D; k++) {
				float mean = 0, std = 0;
				for (int l = 0; l < L; l++)
					mean += data[i][j][l][k] / L;
				for (int l = 0; l < L; l++)
					std += pow(data[i][j][l][k] - mean, 2);
				std = sqrt(std / L);
				for (int l = 0; l < L; l++)
					data[i][j][l][k] = (data[i][j][l][k] - mean) / std;
			}
#endif

	double accAll = 0;
	for (int u = 0; u < nUser; u++) {
		nTrain = nTest = 0;
		for (int i = 0; i < n; i++)
			if (i >= userSz[u] && i < userSz[u + 1])
				aTest[nTest++] = i;
			else
				aTrain[nTrain++] = i;

		int N_CAN = 1, acc = 0;
		for (int i = 0; i < nTest; i++) {
			int x = aTest[i];
			Candidates can = dtwAll(data[x], N_CAN, label[x]);
			resLabel.push_back(make_pair(can[0].second, label[x]));
			
			// best
			if (can[0].second == label[x]) {
				acc++;
				scoreTrue.push_back(can[0].first);
			} else {
				scoreFalse.push_back(can[0].first);
			}

			// majority vote / knn
			// map<int,float> mv;
			// for (int j = 0; j < N_CAN; j++) {
			// 	if (mv.find(can[j].second) == mv.end()) mv[can[j].second] = 0;
			// 	mv[can[j].second] += 1 + (N_CAN - j) * 0.01;
			// }
			// map<int,float>::iterator best = mv.begin();
			// for (map<int,float>::iterator it = mv.begin(); it != mv.end(); it++) {
			// 	if (it->second > best->second) {
			// 		best = it;
			// 	}
			// }
			// if (best->first == label[x]) acc++;
		}
		printf("user %d: %lf\n", u, 100.0 * acc / nTest);
		accAll += 100.0 * acc / nTest;
	}
	printf("ave = %lf\n", accAll / nUser);

	FILE *fout = fopen("cm.txt", "w");
	fprintf(fout, "%lu\n", resLabel.size());
	for (int i = 0; i < resLabel.size(); i++)
		fprintf(fout, "%d %d\n", resLabel[i].first, resLabel[i].second);
	fclose(fout);

#ifdef PRINT_SCORE
	sort(scoreTrue.begin(), scoreTrue.end());
	sort(scoreFalse.begin(), scoreFalse.end());
	printf("\ntrue (%lu)\n", scoreTrue.size());
	for (int i = 0; i < scoreTrue.size(); i++) printf("%.3lf ", scoreTrue[i]);
	printf("\n\nfalse (%lu)\n", scoreFalse.size());
	for (int i = 0; i < scoreFalse.size(); i++) printf("%.3lf ", scoreFalse[i]);
	printf("\n");
#endif

	return 0;
}