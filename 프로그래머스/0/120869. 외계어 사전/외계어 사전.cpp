#include <string>
#include <vector>

using namespace std;

bool check_dic(vector<int>& check) {
    for(int i=0; i<check.size(); i++) {
        if(check[i] == 0) return false;
    }
    return true;
}

int solution(vector<string> spell, vector<string> dic) {
    for(int i=0; i<dic.size(); i++) {
        if(dic[i].size() > spell.size() || dic[i].size() < spell.size()) continue;
        string str = dic[i];
        vector<int> check(spell.size(), 0);
        for(int j=0; j<str.size(); j++) {
            string ch(1, str[j]);
            for(int k=0; k<spell.size(); k++) {
                if(spell[k] == ch) check[k] = 1;
            }
        }
        if(check_dic(check)) return 1;
    }
    return 2;
}