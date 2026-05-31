#include <iostream>
#include <string>

using namespace std;

int main(void) {
    string str;
    cin >> str;
    
    for(int i=0; i<=str.size()-1; i++) {
        char alpha = str[i];
        if(alpha >= 65 && alpha <=90) { // 대문자
            cout << (char)(alpha + 32);
        }
        else {  // 소문자
            cout << (char)(alpha - 32);
        }
    }
    
    return 0;
}