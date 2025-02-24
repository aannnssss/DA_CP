#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <sstream>

using namespace std;

vector<int> compress(const string &text) {
    unordered_map<string, int> dictionary;
    vector<int> output;

    for (char c = 'a'; c <= 'z'; ++c) {
        dictionary[string(1, c)] = c - 'a';
    }
    dictionary["EOF"] = 26;

    string current = "";
    int code = 27;

    for (char c : text) {
        string currentWithChar = current + c;
        if (dictionary.find(currentWithChar) != dictionary.end()) {
            current = currentWithChar;
        } else {
            output.push_back(dictionary[current]);
            dictionary[currentWithChar] = code++;
            current = string(1, c);
        }
    }

    if (!current.empty()) {
        output.push_back(dictionary[current]);
    }

    output.push_back(dictionary["EOF"]);

    return output;
}

string decompress(const vector<int> &codes) {
    unordered_map<int, string> dictionary;
    string output;

    for (char c = 'a'; c <= 'z'; ++c) {
        dictionary[c - 'a'] = string(1, c);
    }

    string current = "";
    int code = 27;
    string previous = dictionary[codes[0]];
    output += previous;

    for (size_t i = 1; i < codes.size() - 1; ++i) {
        int currentCode = codes[i];

        if (dictionary.find(currentCode) != dictionary.end()) {
            current = dictionary[currentCode];
        } else {
            current = previous + previous[0];
        }

        output += current;
        dictionary[code++] = previous + current[0];
        previous = current;
    }

    return output;
}

int main() {
    
    string command;
    getline(cin, command);
    
    if (command == "compress") {
        string text;
        getline(cin, text);

        vector<int> compressedCodes = compress(text);
        for (int code : compressedCodes) {
            cout << code << " ";
        }
        cout << endl;
    } else if (command == "decompress") {
        string codesInput;
        getline(cin, codesInput);
        
        vector<int> codes;
        stringstream codeStream(codesInput);
        int code;

        while (codeStream >> code) {
            codes.push_back(code);
        }

        string decompressedText = decompress(codes);
        cout << decompressedText << endl;
    }

    return 0;
}