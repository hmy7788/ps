#include <iostream>
#include <string>
#include <sstream>
#include <vector>

using namespace std;

int to_s(int m, int s) { return 60 * m + s; }

string to_m_s(int sec) {
    int m = sec / 60;
    int s = sec % 60;
    
    string m_str = (m < 10 ? "0" : "") + to_string(m);
    string s_str = (s < 10 ? "0" : "") + to_string(s);
    
    return m_str + ":" + s_str;
}

bool checking_opening(int pos_s, int op_start_s, int op_end_s) {
    if(op_start_s <= pos_s && pos_s <= op_end_s) return true;
    return false;
}

int next_cmd(int video_len_s, int pos_s) {
    if(video_len_s - pos_s < 10) return 0;
    return pos_s + 10;
}

int prev_cmd(int pos_s) {
    if(pos_s < 10) return 0;
    return pos_s - 10;
}

string solution(string video_len, string pos, string op_start, string op_end, vector<string> commands) {
    string mmss[] = {video_len, pos, op_start, op_end};
    int s[4];
    int i = 0;
    
    for(string t : mmss) {
        string mm_str, ss_str;
        
        stringstream ss(t);
        getline(ss, mm_str, ':');
        getline(ss, ss_str, ':');
        
        s[i++] = to_s(stoi(mm_str), stoi(ss_str));
    }
    
    for(string cmd : commands) {
        if(checking_opening(s[1], s[2], s[3])) s[1] = s[3];
        if(cmd == "next") {
            s[1] = next_cmd(s[0], s[1]);
        }
        else if(cmd == "prev") {
            s[1] = prev_cmd(s[1]);
        }
        if(checking_opening(s[1], s[2], s[3])) s[1] = s[3];
    }
    
    return to_m_s(s[1]);
}