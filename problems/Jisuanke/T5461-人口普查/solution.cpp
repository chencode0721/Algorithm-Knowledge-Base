#include <bits/stdc++.h>
using namespace std;
int main ()
{
    int A[26] = {0};
    string s;
    int n,m;
    cin >> n >> m;
    cin >> s;
    for (int i = 0;i<n;i++)
        A[s[i]-'a']+=1;
    for (int i = 0;i<26;i++)
        if (A[i]>m)cout << char(i+97) << endl;
}
