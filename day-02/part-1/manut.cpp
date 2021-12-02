#include <iostream>
#include <string>
#include <ctime>

using namespace std;

int parse_int(char* s) {
  int res = 0;
  while (*s != '\n' && *s != '\0') {
    res = res*10 + *s - '0';
    s++;
  }
  return res;

}
int run(char* s) {
    int x_pos = 0;
    int depth = 0;
    while(*s != '\0') {
        switch (*s) {
          case 'f':
            s =  s+8;
            x_pos += parse_int(s);
            break;
          case 'd':
            s =  s+5;
            depth += parse_int(s);
            break;
          case 'u':
            s =  s+3;
            depth -= parse_int(s);
            break;
        }
        s++;
    }
    return x_pos * depth;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    clock_t start = clock();
    auto answer = run(argv[1]);

    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
