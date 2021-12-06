#include <iostream>
#include <vector>
#include <string>
#include <cstring>
#include <chrono>
#include <cmath>

using namespace std;

int run(char* s) {
    int gammaRate = 0;
    int epsilonRate = 0;
    int lineLength = 13; // includes \n
    int inputLength = strlen(s);
    for (int i = 0; i < (lineLength - 1); i++)
    {
        int ones = 0;
        for (int j = 0; j < inputLength / lineLength; j++) {
            char* current = s + i + j * lineLength;
            if (*current == '1') {
                ones += 1;
            }
        }
        if (ones > inputLength / (2 * lineLength)) {
            // 1 is most common
            gammaRate += pow(2,lineLength - 2 - i);
        } else {
            epsilonRate += pow(2,lineLength - 2 - i);
        }
    }
    return gammaRate * epsilonRate;
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
