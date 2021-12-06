#include <iostream>
#include <string>
#include <chrono>
#include <array>

using namespace std;

array<uint64_t,81> MAGIX_MATRIXX = { 655568076,  496266131,  589731885,  399865906,  491122368,
357868865,  378763547,  339582910,  280698774,
659462321,  655568076,  496266131,  589731885,  399865906,
491122368,  357868865,  378763547,  339582910,
697451775,  659462321,  655568076,  496266131,  589731885,
399865906,  491122368,  357868865,  378763547,
869885915,  697451775,  659462321,  655568076,  496266131,
589731885,  399865906,  491122368,  357868865,
757734771,  869885915,  697451775,  659462321,  655568076,
496266131,  589731885,  399865906,  491122368,
1080854253,  757734771,  869885915,  697451775,  659462321,
655568076,  496266131,  589731885,  399865906,
896132037, 1080854253,  757734771,  869885915,  697451775,
659462321,  655568076,  496266131,  589731885,
589731885,  399865906,  491122368,  357868865,  378763547,
339582910,  280698774,  315985166,  215567357,
496266131,  589731885,  399865906,  491122368,  357868865,
378763547,  339582910,  280698774,  315985166};

array<uint64_t, 9> parse_int(char* s) {
    array<uint64_t, 9> res = {0, 0, 0, 0, 0 ,0, 0, 0,0};
    while (*(s+1) != '\0') {
        res[*s - '0'] += 1;
        s+=2;
    }
    res[*s - '0'] += 1;
    return res;

}

uint64_t run(char* s) {
    auto input = parse_int(s);
    uint64_t sum = 0;
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
