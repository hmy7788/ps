#include <iostream>

using namespace std;

int solution(int n, int a, int b) {
    int cnt = 0;
    while(1) {
        if(a == b) {
            return cnt;
        }
        if(a % 2 == 0) {    // a 짝수
            a /= 2;
        }
        else if(a % 2 != 0) {  // a 홀수
            a = (a+1) / 2;
        }
        if(b % 2 == 0) {
            b /= 2;
        }
        else if(b % 2 != 0) {
            b = (b+1) / 2;
        }
        cnt++;
    }
}