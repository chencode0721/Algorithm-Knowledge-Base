#include <bits/stdc++.h>
using namespace std;
int main() {
    char c;
    bool X = false;
    while (cin.get(c)) {
        if (c == '"') {
            if (X == false) {
                X = true;
                cout << "``";
            }
            else {
                X = false;
                cout << "''";
            }
        }
        else {
            cout << c;
        }
    }
}
