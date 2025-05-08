#include <string>
#include <vector>
#include <iostream>

using namespace std;

int solution(vector<vector<int>> board) {
    int n = board.size();
    for(int i=0; i<n; i++) {
        for(int j=0; j<n; j++) {
            if(board[i][j] == 1) {
                if((0 <= i-1 && i-1 < n) && (0 <= j-1 && j-1 < n) && board[i-1][j-1] != 1) {  // 좌상
                    board[i-1][j-1] = -1;
                }
                if((0 <= i-1 && i-1 < n) && (0 <= j && j < n) && board[i-1][j] != 1) {    // 상
                    board[i-1][j] = -1;
                }
                if((0 <= i-1 && i-1 < n) && (0 <= j+1 && j+1 < n) && board[i-1][j+1] != 1) {  // 우상
                    board[i-1][j+1] = -1;
                }
                if((0 <= i && i < n) && (0 <= j-1 && j-1 < n) && board[i][j-1] != 1) {    // 좌
                    board[i][j-1] = -1;
                }
                if((0 <= i && i < n) && (0 <= j+1 && j+1 < n) && board[i][j+1] != 1) {    // 우
                    board[i][j+1] = -1;
                }
                if((0 <= i+1 && i+1 < n) && (0 <= j-1 && j-1 < n) && board[i+1][j-1] != 1) {  // 좌하
                    board[i+1][j-1] = -1;
                }
                if((0 <= i+1 && i+1 < n) && (0 <= j && j < n) && board[i+1][j] != 1) {    // 하
                    board[i+1][j] = -1;
                }
                if((0 <= i+1 && i+1 < n) && (0 <= j+1 && j+1 < n) && board[i+1][j+1] != 1) {  // 우하
                    board[i+1][j+1] = -1;
                }
            }
        }
    }
    // for(auto& b : board) {
    //     for(int i : b) {
    //         cout << i << ' ';
    //     }
    //     cout << '\n';
    // }
    
    int cnt = 0;
    for(int i=0; i<n; i++) {
        for(int j=0; j<n; j++) {
            if(board[i][j] == 1 || board[i][j] == -1) cnt++;
        }
    }
    
    return n*n - cnt;
}