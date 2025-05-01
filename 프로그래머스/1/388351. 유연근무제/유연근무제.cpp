#include <string>
#include <vector>

using namespace std;

int solution(vector<int> schedules, vector<vector<int>> timelogs, int startday) {
    int n = schedules.size();
    vector<int> count(n, 1);
    int sum = 0;
    
    for(int i=0; i<n; i++) {
        schedules[i] += 10;
        int hour = schedules[i] / 100;
        int minute = schedules[i] % 100;
        int add_hour = minute / 60;
        int add_minute = minute % 60;
        
        schedules[i] = hour * 100 + add_hour * 100 + add_minute;
        
        vector<int> log = timelogs[i];
        int day = startday;
        for(int j=0; j<7; j++) {
            if(day == 6 || day == 7) {
                day++;
                if(day == 8) day = 1;
            }
            else {
                if(log[j] > schedules[i]) {
                    count[i] = 0;
                    break;
                }
                day++;
            }
        }
    }
    
    for(int c : count) sum += c;
    
    return sum;
}