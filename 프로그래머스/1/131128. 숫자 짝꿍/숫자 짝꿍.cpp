#include <string>
#include <vector>

using namespace std;

string solution(string X, string Y) {
    vector<int> countX(10, 0);
    vector<int> countY(10, 0);
    string answer;
    
    for(char c : X) {
        countX[int(c) - '0'] += 1;
    }
    for(char c : Y) {
        countY[int(c) - '0'] += 1;
    }
    
    for(int i=9; i>=0; i--) {
        int count = min(countX[i], countY[i]);
        answer += string(count, i + '0');
    }
    
    if(answer.size() == 0) return "-1";
    if(answer[0] == '0') return "0";
    else return answer;
}