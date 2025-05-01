#include <string>
#include <vector>
#include <iostream>

using namespace std;

int solution(int n, int w, int num) {
    int floor;
    int box = 1;
    
    if(n % w != 0) floor = n/w + 1;
    else floor = n/w;
    
    vector<vector<int>> v(floor+1);
    for (int i = 1; i <= floor; ++i) {
        v[i] = vector<int>(w, 0);
    }
    
    for(int i=1; i<=floor; i++) {
        if(i % 2 == 0) {    // 역방향
            int j;
            int row = w-1;
            for(j=box; j<box+w; j++) {
                if(j > n) continue;
                v[i][row--] = j;
            }
            box = j;
        }
        else {  // 순방향
            int j;
            int row = 0;
            for(j=box; j<=box+w-1; j++) {
                if(j == n+1) break;
                v[i][row++] = j;
            }
            box = j;
        }
    }
    
    for(auto& a : v) {
        for(int aa : a) {
            cout << aa << " ";
        }
        cout << "\n";
    }
    
    int num_i, num_j;
    int top_i;
    
    for(int i=1; i<v.size(); i++) {
        for(int j=0; j<v[i].size(); j++) {
            if(v[i][j] == num) {
                num_i = i;
                num_j = j;
            }
            if(num_j == j && j < v.size() && v[i][j] != 0) {
                top_i = i;
            }
            
        }
    }
    
    cout << top_i - num_i + 1;
    
    return top_i - num_i + 1;
}