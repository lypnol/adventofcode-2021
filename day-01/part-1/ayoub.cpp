#include <iostream>
#include <string>
#include <ctime>

using namespace std;

int run(char* s) {
    int count = 0, curr = 0, prev = -1;
    size_t i = -1;
    while (s[++i]) {
        if (s[i] == '\n') {
            if (prev != -1 && curr > prev) count++;
            prev = curr;
            curr = 0;
        } else curr = curr*10 + (int)(s[i]-'0');
    }
    if (curr != 0 && prev != -1 && curr > prev) count++;

    return count;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    clock_t start = clock();
    int answer = run(argv[1]);
    
    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
