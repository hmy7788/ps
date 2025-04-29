#include <string>
#include <vector>
#include <iostream>
#include <algorithm>

using namespace std;

bool compare(int a, int b) {
    return a > b;
}

int targeting(vector<int>& cards, vector<int>& visited, int i) {
    int count = 0;
    while(visited[i] != 1) {
        visited[i] = 1;
        count++;
        i = cards[i];
    }
    return count;
}

int solution(vector<int> cards) {
    cards.insert(cards.begin(), 0);
    int n = cards.size();
    vector<int> visited(n, 0);
    vector<int> counts;
    
    for(int i=1; i<n; i++) {
        if(visited[i] != 1) {
            counts.push_back(targeting(cards, visited, i));
        }
    }
    
    if(counts.size() < 2) {
        return 0;
    }
    else {
        sort(counts.begin(), counts.end(), compare);
        return counts[0] * counts[1];
    }
}