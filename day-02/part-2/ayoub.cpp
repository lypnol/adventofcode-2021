#include <iostream>
#include <ctime>
#include <cstdint>

using namespace std;

int64_t run(char* s) {
    size_t i = -1;
    int64_t h = 0, d = 0, a = 0, x;

    while (s[++i]) {
        if (s[i] == '\n') continue;
        if (s[i] == 'f') {
            i += 8;
            x = (int64_t)(s[i]-'0');
            h += x;
            d += a*x;
            i++;
        } else if (s[i] == 'u') {
            i += 3;
            x = (int64_t)(s[i]-'0');
            a -= x;
            i++;
        } else if (s[i] == 'd') {
            i += 5;
            x = (int64_t)(s[i]-'0');
            a += x;
            i++;
        }
    }

    return d*h;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    cout << "sizeof: int=" << sizeof(int) << " int32_t=" << sizeof(int32_t) << " int64_t=" << sizeof(int64_t) << "\n";

    clock_t start = clock();
    int64_t answer = run(argv[1]);
    
    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
