#include <vector>
#include <iostream>
#include <sstream>
#include <string>
#include <ctime>

using namespace std;

int run(string s) {
    std::istringstream iss(s);
    string line;
    std::vector<int> depths;
    while (getline(iss, line, '\n'))
    {
        depths.push_back(stoi(line));
    }
    int answer = 0;
    int previous = -1;
    int current = 0;
    for (int i = 0; i < depths.size() - 2; i++)
    {
        current = depths[i] + depths[i+1] + depths[i+2];
        if (previous >= 0 && current > previous)
        {
            answer += 1;
        }
        previous = current;
        current = 0;
    }
    return answer;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    clock_t start = clock();
    int answer = run(string(argv[1]));

    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
