#include <string>
#include <vector>
#include <algorithm>

using namespace std;

bool can_place(int i, int j, vector<vector<string>>& park,int mat) {
    int H = park.size();
    int W = park[0].size();
    if(i+mat > H || j+mat > W) return false;
    
    for(int p=i; p<i+mat; p++) {
        for(int q=j; q<j+mat; q++) {
            if(park[p][q] != "-1") return false;
        }
    }
    return true;
}

int solution(vector<int> mats, vector<vector<string>> park) {
    int H = park.size();
    int W = park[0].size();
    sort(mats.begin(), mats.end(), greater<int>());
    
    for(int mat : mats) {
        for(int i=0; i<H; i++) {
            for(int j=0; j<W; j++) {
                if(can_place(i, j, park, mat)) return mat;
            }
        }
    }
    
    return -1;
}