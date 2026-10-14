#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    while (cin >> n) {
        vector<long long> a(n);
        for (auto &v : a) cin >> v;
        vector<bool> seen(n, false);
        bool jolly = true;
        for (int i = 1; i < n; ++i) {
            long long diff = llabs(a[i] - a[i - 1]);
            if (diff < 1 || diff >= n || seen[static_cast<size_t>(diff)]) {
                jolly = false;
            } else {
                seen[static_cast<size_t>(diff)] = true;
            }
        }
        cout << (jolly ? "Jolly" : "Not jolly") << '\n';
    }
}
