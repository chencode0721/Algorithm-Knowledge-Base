#include <bits/stdc++.h>
using namespace std;
int main() {
    char c;
    vector<char> v;
    while (cin.get(c)) {
            if (c==' '||c=='\n') {
                for (int i = v.size()-1; i >= 0 ; i--)
                    cout << v[i];
                if (c == ' ' || c == '\n')cout << c;
                v.clear();
            }
            else
            {
                v.push_back(c);
            }
    }
    for (int i = v.size()-1; i >= 0 ; i--)
        cout << v[i];
}
