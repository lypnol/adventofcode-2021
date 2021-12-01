#include <iostream>
#include <string>
#include <ctime>

using namespace std;

int run(string s) {
    int occurences = 0;
    int previous = -1;
    int current = 0;
    for (int i = 0; i < s.length(); i++) {
        if (s[i] == '\n') {
            if (previous >= 0 && current > previous)
            {
                occurences += 1;
            }
            previous = current;
            current = 0;
        }
        else {
            current = current * 10 + s[i] - '0';
        }
    }
    if (current > previous)
    {
        occurences += 1;
    }
    return occurences;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    clock_t start = clock();
    int answer = run(string(argv[1]));

    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
