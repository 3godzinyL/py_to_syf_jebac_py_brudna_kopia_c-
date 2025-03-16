#include <iostream>
#include <vector>
#include <algorithm>

void printNumbers(const std::vector<int>& numbers) {
    std::cout << "Liczby: ";
    for (int num : numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
}

int main() {
    std::vector<int> numbers;
    int n;

    std::cout << "Ile liczb chcesz wprowadzić? ";
    std::cin >> n;

    for (int i = 0; i < n; ++i) {
        int num;
        std::cout << "Podaj liczbę " << i + 1 << ": ";
        std::cin >> num;
        numbers.push_back(num);
    }

    printNumbers(numbers);

    std::sort(numbers.begin(), numbers.end());
    std::cout << "Liczby posortowane: ";
    printNumbers(numbers);

    int suma = 0;
    for (int num : numbers) {
        suma += num;
    }
    std::cout << "Suma liczb: " << suma << std::endl;

    double srednia = static_cast<double>(suma) / numbers.size();
    std::cout << "Średnia liczb: " << srednia << std::endl;

    if (!numbers.empty()) {
        std::cout << "Najmniejsza liczba: " << numbers.front() << std::endl;
        std::cout << "Największa liczba: " << numbers.back() << std::endl;
    }

    return 0;
}