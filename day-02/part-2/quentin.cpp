#include <sstream>
#include <iostream>
#include <string>
#include <ctime>

using namespace std;

int run(string s) {
    int horizontalPosition = 0;
    int depth = 0;
    int aim = 0;
    istringstream iss = istringstream(s);
    string line;
    while (getline(iss, line, '\n')) {
        auto pos = line.find(" ");
        string command = line.substr(0, pos);
        if (command == "forward") {
            int forwardValue = stoi(line.substr(pos + 1, line.length()));
            horizontalPosition += forwardValue;
            depth += aim * forwardValue;
        }
        if (command == "up") {
            aim -= stoi(line.substr(pos + 1, line.length()));
        }
        if (command == "down") {
            aim += stoi(line.substr(pos + 1, line.length()));
        }
    }
    return horizontalPosition * depth;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    clock_t start = clock();
    auto answer = run(string(argv[1]));

    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
