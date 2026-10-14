#include <bits/stdc++.h>
using namespace std;
int main ()
{
    double n;
    double m = 0;
    double mtime = 0, uptime  = 0,downtime = 0;
    cin >> n;
    while (n--)
    {
        double x1,y1;
        cin >> x1 >> y1;
        m += sqrt(pow(x1,2)+pow(y1,2))*(double)2;
        int r;
        cin >> r;
        uptime += r;
        downtime += (double)r*0.5;
    }
    mtime = (double)m/50;
    if(mtime + uptime + downtime > (int)(mtime + uptime + downtime))
        cout << (int)(mtime + uptime + downtime)+1;
    else
        cout << (int)(mtime + uptime + downtime);
}
