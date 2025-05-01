#include <string>
#include <vector>
#include <iostream>
#include <map>

using namespace std;

vector<int> solution(int n, vector<string> words) {
    map<string, int> m;
    vector<int> answer(2);
    int id = 1;       // 사람 번호
    int count = 1;    // 몇 번째 턴

    m[words[0]] = 1; // 첫 단어 등록

    for(int i=1; i<words.size(); i++) {
        string prev = words[i-1];
        string now = words[i];

        id++;
        if(id == n+1) { // n명 다 끝나면
            id = 1;
            count++;
        }

        if(prev.back() != now.front() || m.find(now) != m.end()) {
            answer[0] = id;
            answer[1] = count;
            return answer;
        }

        m[now] = 1;
    }
    return {0, 0};
}
