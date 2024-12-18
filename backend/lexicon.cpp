#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <unordered_map>
#include <string>
#include <fstream>

std::unordered_map<std::string, int> lexicon;

// Function to load the lexicon from a binary file
void load_lexicon(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    if (!file) {
        throw std::runtime_error("Error: Could not open file " + filename);
    }

    lexicon.clear();

    while (file.peek() != EOF) {
        uint8_t word_length;
        file.read(reinterpret_cast<char*>(&word_length), sizeof(word_length));
        if (file.eof()) break;

        std::vector<char> word_buffer(word_length);
        file.read(word_buffer.data(), word_length);
        if (file.eof()) break;
        std::string word(word_buffer.begin(), word_buffer.end());

        uint32_t word_id;
        file.read(reinterpret_cast<char*>(&word_id), sizeof(word_id));
        if (file.eof()) break;

        lexicon[word] = word_id;
    }

    file.close();
}

// Function to get the ID of a word
int get_word_id(const std::string& word) {
    auto it = lexicon.find(word);
    return (it != lexicon.end()) ? it->second : -1; // Return -1 if not found
}

// Function to get the word from an ID
std::string get_word(int word_id) {
    for (const auto& [word, id] : lexicon) {
        if (id == word_id) {
            return word;
        }
    }
    return ""; // Return empty string if not found
}

// Function to expose lexicon to Python
std::unordered_map<std::string, int> get_lexicon() {
    return lexicon;
}

namespace py = pybind11;

PYBIND11_MODULE(lexicon, m) {
    m.doc() = "Lexicon Hash Table Backend";
    m.def("load_lexicon", &load_lexicon, "Load the lexicon from a binary file");
    m.def("get_word_id", &get_word_id, "Get the ID of a word");
    m.def("get_word", &get_word, "Get the word from an ID");
    m.def("get_lexicon", &get_lexicon, "Get the entire lexicon as a dictionary");
}
