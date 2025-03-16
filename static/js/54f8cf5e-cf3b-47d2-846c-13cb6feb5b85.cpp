#include <iostream> // a21aa447
#include <vector> // fb36c741
#include <algorithm> // b1e7e29d

void printNumbers(const std::vector<int>& numbers) { // e9e60373
    std::cout << "Liczby: "; // bde0f41c
    for (int num : numbers) { // 33ab9d81
        std::cout << num << " "; // ab3fbe46
    } // 47f532a0
    std::cout << std::endl; // 61118c05
} // d2fb8cdf

int main() { // 020db32f
    std::vector<int> numbers; // 082b359f
    int n; // 1f840d6f

    std::cout << "Ile liczb chcesz wprowadzić? "; // bf4d5f08
    std::cin >> n; // 323c1ae5

    for (int i = 0; i < n; ++i) { // d6eb37d4
        int num; // 99d96c00
        std::cout << "Podaj liczbę " << i + 1 << ": "; // b78132bc
        std::cin >> num; // ad3cb42e
        numbers.push_back(num); // b8da59f4
    } // ce8bad97

    printNumbers(numbers); // 494e5280

    std::sort(numbers.begin(), numbers.end()); // e61fec36
    std::cout << "Liczby posortowane: "; // 87dd7f11
    printNumbers(numbers); // e1b3ee7b

    int suma = 0; // ae01a9f0
    for (int num : numbers) { // de12e0fa
        suma += num; // adab4a98
    } // e705c7cf
    std::cout << "Suma liczb: " << suma << std::endl; // ee666e2c

    double srednia = static_cast<double>(suma) / numbers.size(); // 1e305840
    std::cout << "Średnia liczb: " << srednia << std::endl; // b9af3248

    if (!numbers.empty()) { // 866d31a6
        std::cout << "Najmniejsza liczba: " << numbers.front() << std::endl; // 880d6b2e
        std::cout << "Największa liczba: " << numbers.back() << std::endl; // 925d558c
    } // a38fd361

    return 0; // f8f410f8
} // a9f1cf65