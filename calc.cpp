#include<bits/stdc++.h>
using namespace std;
const int n = 80;

char st[100];
double p[n], s[n], b[n];

const double eps = 1e-5;

void pr() {
    memset(s, 0, sizeof(s));
    memset(b, 0, sizeof(b));
    for(int i = 0; i < n; i++) 
        p[i] = (double)(i + 5) / 100.0;
    p[0] = 0.0;
    p[n - 1] = 1000.0;
}

int main() {
    freopen("example.txt", "r", stdin);
    pr();
    while(scanf("%s", st) != EOF) {
        assert(st[0] == 's' || st[0] == 'b');
        string x;
        for(int i = 1; i < size(st); i++) {
            x = x + st[i];
        }       
        int num;
        num = stoi(x);
        if(st[0] == 's') {
            scanf("%lf", &s[num]);
        } else if (st[0] == 'b') {
            scanf("%lf", &b[num]);
        } else assert(0);
    }

    double check1 = 0, check2 = 0;
    for(int i = 0; i < n; i++) check1 += s[i];
    for(int i = 0; i < n; i++) check2 += b[i];

    //Check if it is a valid distrbution
    assert(fabs(check1 - 1) <= eps); assert(fabs(check2 - 1) <= eps);

    double opt = 0, EB = 0, ES = 0;
    for(int i = 0; i < n; i++) for(int j = 0; j < n; j++) opt += max(p[i], p[j]) * s[i] * b[j];
    for(int i = 0; i < n; i++) EB += p[i] * b[i];
    for(int i = 0; i < n; i++) ES += p[i] * s[i];
    double bestratio = 0, bestwelfare = 0;
    for(int k = 0; k < n; k++) {
        double res = 0, prob = 0;
        for(int i = 0; i < n; i++) res += p[i] * s[i];
        for(int i = 0; i <= k; i++) for(int j = k + 1; j < n; j++) res += (p[j] - p[i]) * s[i] * b[j];
        
        bestratio = max(bestratio, res / opt);
        bestwelfare = max(bestwelfare, res);
    }
    cout << "Best Ratop:" << bestratio << endl;
    cout << "Welfare of Optimal Fixed-Price Mechanism:" << bestwelfare << endl;
    cout << "Optimal Welfare" << opt << endl;
    // cout << check1 << ' ' << check2 << ' ' << opt << endl;
// for k in range(n):
//     expr = gp.QuadExpr()
//     for i in range(n):
//         for j in range(n):
//             if C[k][i][j] != 0:
//                 if (i > k or j < k):
//                     print("Error")
//                     exit(0)
//                 expr += C[k][i][j] * s[i] * b[j]
    
// for k in range(n):
//     for i in range(k + 1):
//         for j in range(k + 1, n):
//             C[k][i][j] = p[j] - p[i]

    
//     m.addConstr(expr <= r, "Ratio" + str(k))
}