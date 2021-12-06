#include <iostream>
#include <string>
#include <chrono>
#include <array>

using namespace std;

array<int,81> MAGIX_MATRIXX = {252,  20, 210,  37, 120,  84,  45, 126,  11,
        56, 252,  20, 210,  37, 120,  84,  45, 126,
       210,  56, 252,  20, 210,  37, 120,  84,  45,
       165, 210,  56, 252,  20, 210,  37, 120,  84,
       121, 165, 210,  56, 252,  20, 210,  37, 120,
       330, 121, 165, 210,  56, 252,  20, 210,  37,
        57, 330, 121, 165, 210,  56, 252,  20, 210,
       210,  37, 120,  84,  45, 126,  11, 126,   9,
        20, 210,  37, 120,  84,  45, 126,  11, 126};

array<int, 9> parse_int(char* s) {
    array<int, 9> res = {0};
    while (*(s+1) != '\0') {
        res[*s - '0'] += 1;
        s+=2;
    }
    res[*s - '0'] += 1;
    return res;

}

int run(char* s) {
    auto input = parse_int(s);
    int sum = 0;
    for (int i(0); i < 9; i++) {
        for (int j(0); j < 9; j++) {
            sum += MAGIX_MATRIXX[i*9+j]*input[j];
        }
    }
    return sum;
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
