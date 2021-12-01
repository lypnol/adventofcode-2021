#include <vector>
#include <iostream>
#include <string>
#include <ctime>

// Optimizin quentin's solutions

using namespace std;

int run(char* s) {
    short int occurences = 0;
    short int previous[3] = {-1,-1,-1};
    short int moduloCount = 0;
    short int current = 0;

    while(*s != '\0') {
        moduloCount = moduloCount % 3;
        if (*s == '\n') {
            if (previous[moduloCount] >= 0 && current > previous[moduloCount])
            {
                occurences += 1;
            }
            previous[moduloCount] = current;
            moduloCount++;
            current = 0;
        }
        else {
            current = current * 10 + *s - '0';
        }
        s++;
    }
    if (current > previous[moduloCount])
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
    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    int answer = run(argv[1]);

    cout << answer << "\n";
    return 0;
}
