#include <bits/stdc++.h>
using namespace std;
int main ()
{
    int N,M;
    cin >> N >> M;
    vector<int> a(N, 1);
    for (int i = 1;i<=M;i++)
    {
        for (int j=0;j<a.size();j++)
        {
            if ((j+1)%i==0)a[j]*=-1;
        }
    }
    vector<int>b;
    for (int i = 0;i<a.size();i++)
        if (a[i] == -1)b.push_back(i+1);
    for (int i = 0;i<b.size()-1;i++)
    {
        cout << b[i] << ",";
    }
    cout << b[b.size()-1];
}
