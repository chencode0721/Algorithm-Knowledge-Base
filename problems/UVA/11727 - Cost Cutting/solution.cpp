#include <bits/stdc++.h>
using namespace std;
int main () {
    int T;
    cin >> T;
    for (int i = 1; i <= T; i++) {
        vector<int>slsry(3);
        cin >> slsry[0] >> slsry[1] >> slsry[2];
        sort(slsry.begin(), slsry.end());
        cout << "Case " << i << ": " << slsry[1] << endl;
    }
}
