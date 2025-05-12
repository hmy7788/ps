#include <iostream>
#include <vector>

using namespace std;

int solution(vector<int> numbers, int k) {
    int p = 1;
    for(int i=1; i<k; i++) {
        cout << p << "->";
        p += 2;
        if(p > numbers.size()) {
            p -= numbers.size();
        }
    }
    
    return p;
}