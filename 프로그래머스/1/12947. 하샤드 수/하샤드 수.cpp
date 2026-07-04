#include <string>
#include <vector>
#include <iostream>

using namespace std;

bool solution(int x) {
    int sum = 0;
    bool check;
    int y = x;
    while(x != 0) {
        sum += x % 10;
        x /= 10;
    }
    
    if(y % sum == 0) {
        check = true;
    }
    else {
        check = false;
    }
    
    cout << sum << '\n';
    cout << boolalpha << check;
    
    return check;
}