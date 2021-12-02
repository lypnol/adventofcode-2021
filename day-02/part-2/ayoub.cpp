#include <iostream>
#include <ctime>

using namespace std;

uint64_t run(char* s) {
    size_t i = -1;
    uint64_t curr = 0;
    uint64_t h = 0, d = 0, a = 0;

    while (s[++i]) {
        if (s[i] == '\n') continue;
        if (s[i] == 'f') {
            i += 7;
            curr = 0; while (s[++i] != '\n' && s[i]) curr = curr*10ULL + (uint64_t)(s[i]-'0');
            h += curr;
            d += a*curr;
        } else if (s[i] == 'u') {
            i += 2;
            curr = 0; while (s[++i] != '\n' && s[i]) curr = curr*10ULL + (uint64_t)(s[i]-'0');
            a -= curr;
        } else if (s[i] == 'd') {
            i += 4;
            curr = 0; while (s[++i] != '\n' && s[i]) curr = curr*10ULL + (uint64_t)(s[i]-'0');
            a += curr;
        }
    }

    return d*h;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    clock_t start = clock();
    uint64_t answer = run(argv[1]);
    
    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
