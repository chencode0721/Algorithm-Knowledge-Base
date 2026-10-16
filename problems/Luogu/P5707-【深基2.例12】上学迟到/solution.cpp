#include <bits/stdc++.h>
using namespace std;

int main()
{
    int s, v;
    cin >> s >> v;
    int t=(s+v-1)/v;
    int yyy = 470-t;

    if (yyy >= 0)
    {
        printf("%02d:%02d", yyy / 60, yyy % 60);
    }
    else
    {   
        yyy = yyy+1440;
        printf("%02d:%02d", yyy / 60, yyy % 60);
    }

    
}
