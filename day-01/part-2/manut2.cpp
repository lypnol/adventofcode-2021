#include <vector>
#include <iostream>
#include <string>
#include <chrono>

// Optimizin quentin's solutions

using namespace std;

int run(char* s) {
    int occurences = 0;
    int previous[3];
    int moduloCount = 0;
    int current = 0;
    while (moduloCount < 3) {
        if (*s == '\n') {
            previous[moduloCount++] = current;
            current = 0;
        }
        else {
            current = current * 10 + *s - '0';
        }
        s++;
    }
    moduloCount = 0;

    while(*s != '\0') {
        if (*s == '\n') {
            occurences += (current > previous[moduloCount]);
            previous[moduloCount] = current;
            moduloCount++;
            current = 0;
            if (moduloCount == 3) {
                moduloCount = 0;
            }
        }
        else {
            current = current * 10 + *s - 48;
        }
        s++;
    }
    occurences += (current > previous[moduloCount]);
    return occurences;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    auto start_cpp = std::chrono::high_resolution_clock::now();
    auto answer = run(argv[1]);
    auto end_cpp = std::chrono::high_resolution_clock::now();

    cout << "_duration:"<< float(std::chrono::duration_cast<std::chrono::microseconds>(end_cpp-start_cpp).count()) /1000.0 << "\n";

    cout << answer << "\n";
    return 0;
}
