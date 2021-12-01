#include <iostream>
#include <string>
#include <ctime>
#include <sstream>

using namespace std;

int run(string s) {
    int count = 0;
    int n = s.length();
    int i = 0;
    int j = 1;
    int j_starts[3] = {0,0,0};
    while (s[j] != '\n') {
        j++;
    }
    j++;
    j_starts[0] = j;
    while (s[j] != '\n') {
        j++;
    }
    j++;
    j_starts[1] = j;
    while (s[j] != '\n') {
        j++;
    }
    j++;
    j_starts[2] = j;
    int increasing = 0;
    int start_index = 0;
    while (j < n) {
        char i_char = s[i];
        char j_char = s[j];
        start_index = start_index %3;
        if (i_char == '\n') {
            if (j_char != '\n') {
                count++;
                increasing = 0;
                i = j_starts[start_index];
                do {
                    j++;
                } while(s[j] != '\n');
                j++;
                j_starts[start_index] = j;
                start_index++;
            } else {
                if (increasing == 1) {
                    count++;
                }
                increasing = 0;
                i = j_starts[start_index];
                j++;
                j_starts[start_index] = j;
                start_index++;
            }
        } else {
            if (j_char != '\n') {
                if (i_char < j_char) {
                    if (increasing == 0) {
                        increasing = 1;
                    }
                } else if (i_char > j_char) {
                    if (increasing == 0) {
                        increasing = -1;
                    }
                }
                i++;
                j++;
            } else {
                increasing = 0;
                i = j_starts[start_index];
                j++;
                j_starts[start_index] = j;
                start_index++;
            }
        }
    }
    if (s[i] == '\n' && increasing == 1) {
        count++;
    }

    return count;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    clock_t start = clock();
    auto answer = run(string(argv[1]));

    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
