#include <iostream>
#include <string>
#include <ctime>

#define WINDOW_SIZE 4

using namespace std;

int run(char* s) {
    int count = 0, curr = 0;
    int window[WINDOW_SIZE] = {0};
    int window_sum = 0;
    size_t i = -1, lines_count = 1, k = 0;
    while (s[++i]) {
        if (s[i] == '\n') {
            window[k] = curr; k = (k+1)%WINDOW_SIZE;
            // cout << lines_count << " " << curr;
            if (lines_count > WINDOW_SIZE-1) {
                // cout << " window=[";
                // for (size_t j = 0; j < WINDOW_SIZE-1; j++) cout << window[(k+j)%WINDOW_SIZE] << ",";
                // cout << window[(k+WINDOW_SIZE-1)%WINDOW_SIZE] << "]";
                // cout << " prev=" << window_sum << " next=" << window_sum - window[k%WINDOW_SIZE] + curr << "\n";
                if ((window_sum - window[k%WINDOW_SIZE] + curr) > window_sum) count++;
                window_sum = window_sum - window[k%WINDOW_SIZE] + curr;
            } else {
                // cout << " " << window_sum << " summing\n";
                window_sum += curr;                
            }
            curr = 0;
            lines_count++;
        } else curr = curr*10 + (int)(s[i]-'0');
    }
    if (curr != 0 && ((window_sum - window[k%WINDOW_SIZE] + curr) > window_sum)) count++;

    return count;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    clock_t start = clock();
    int answer = run(argv[1]);
    
    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
