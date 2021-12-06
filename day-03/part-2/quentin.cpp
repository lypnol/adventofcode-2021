#include <iostream>
#include <vector>
#include <set>
#include <string>
#include <cstring>
#include <chrono>
#include <cmath>

using namespace std;

int search(char* s, bool mostCommon) {
    int lineLength = 13; // includes \n
    int inputLength = strlen(s);

    int numberOfLine = (inputLength + 1)/lineLength;
    set<int> remainingLines = set<int>();
    for (int i = 0; i < numberOfLine; ++i) {
        remainingLines.insert(i);
    }

    for (int i = 0; i < (lineLength - 1); i++)
    {
        int ones = 0;
        int zeros = 0;
        for (auto it = remainingLines.begin(); it != remainingLines.end(); it++) {
            char* current = s + i + *it * lineLength;
            if (*current == '1') {
                ones += 1;
            } else {
                zeros += 1;
            }
        }
        char bit = '0';
        if ((ones >= zeros && mostCommon) || (ones < zeros && !mostCommon)) {
            bit = '1';
        }
        for (int j = 0; j < numberOfLine; j++) {
            char* current = s + i + j * lineLength;
            if (*current != bit) {
                remainingLines.erase(j);
            }
        }
        if (remainingLines.size() == 1)
        {
            break;
        }
    }
    int result = 0;
    for (int i = 0; i < (lineLength - 1); i++) {
        char* current = s + i + *remainingLines.begin() * lineLength;
        if (*current == '1') {
            result += pow(2,lineLength - 2 - i);
        }
    }
    return result;
}

int run(char* s) {
    int oxygen = search(s, true);
    int co2 = search(s, false);
    return oxygen * co2;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    auto start = std::chrono::high_resolution_clock::now();
    auto answer = run(argv[1]);
    auto end = std::chrono::high_resolution_clock::now();

    cout << "_duration:"<< float(std::chrono::duration_cast<std::chrono::microseconds>(end-start).count()) / 1000.0 << "\n";
    
    cout << answer << "\n";
    return 0;
}
