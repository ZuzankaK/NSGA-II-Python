Projekt: Algorytm genetyczny NSGA-II (Python)
Opis projektu

Program implementuje algorytm genetyczny NSGA-II (Non-dominated Sorting Genetic Algorithm II), który służy do rozwiązywania problemów optymalizacji wielokryterialnej.
Zaimplementowano pięć klasycznych funkcji testowych z rodziny ZDT1–ZDT6, służących do oceny jakości algorytmu.
Wyniki są prezentowane w formie wykresów frontu Pareto oraz zapisywane do pliku JSON.

Cele projektu

Celem programu jest:

prezentacja działania algorytmu ewolucyjnego,

wizualizacja rozkładu rozwiązań na przestrzeni iteracji,

pokazanie znajomości:

struktur danych w Pythonie,

operacji wejścia/wyjścia,

programowania strukturalnego i obiektowego,

obsługi plików JSON,

wykorzystania wyrażeń regularnych.

Wymagania systemowe

Python 3.9+

biblioteki:

pip install numpy matplotlib

 Uruchomienie programu
Uruchomienie domyślne (ZDT1)
python main.py

Wybór problemu
python main.py --problem ZDT3


Dostępne problemy: ZDT1, ZDT2, ZDT3, ZDT4, ZDT6.

Zapis wyników do JSON
python main.py --problem ZDT2 --save


Wyniki zostaną zapisane w pliku:

ZDT2_D_results.json

 Wczytanie zapisanych wyników
python main.py --problem ZDT2 --load ZDT2_D_results.json


Program wczyta dane z pliku i wygeneruje wykresy ponownie bez uruchamiania algorytmu.

Wyniki i wizualizacja

Dla każdej kombinacji problemu ZDT i wymiaru (10, 30, 50) program generuje wykresy frontu Pareto:

ZDT1_D10_pareto.png
ZDT1_D30_pareto.png
ZDT1_D50_pareto.png


Każdy wykres przedstawia kolejne fronty Pareto dla zapisanych iteracji (np. 20, 50, 100, 500).

 Struktura projektu
NSGA/
├── main.py # główny kod programu (implementacja NSGA-II)
├── requirements.txt # wymagane biblioteki (numpy, matplotlib)
├── README.md # opis projektu i instrukcja uruchomienia
├── .gitignore # wykluczenia z repozytorium
└── results/ # przykładowe wyniki działania programu
    ├── ZDT1_D10_pareto.png
    ├── ZDT1_D30_pareto.png
    ├── ZDT1_D50_pareto.png
    └── ZDT1_D_results.json

Struktura kodu

Klasa Individual – reprezentuje pojedynczego osobnika z populacji (chromosom + wartości funkcji celu).

Funkcje zdtX_f1, zdtX_f2 – implementacje funkcji testowych ZDT1–ZDT6.

Funkcje pomocnicze:

initialize_population() – losowa inicjalizacja populacji,

evaluate_population() – obliczanie wartości funkcji celu,

non_dominated_sorting() – sortowanie względem dominacji Pareto,

calculate_crowding_distance() – obliczanie odległości zatłoczenia,

crossover(), mutate() – operatory genetyczne,

tournament_selection() – selekcja turniejowa,

save_results_to_json() / load_results_from_json() – operacje I/O z plikami JSON,

plot_pareto() – wizualizacja wyników w postaci wykresu.

Spełnienie wymagań przedmiotu
Wymaganie	Spełnienie w projekcie
Znajomość typów i struktur danych	użyto: list, dict, numpy.ndarray
Operacje wejścia/wyjścia (I/O)	zapis/odczyt JSON, zapis PNG, CLI (argparse)
Dekompzycja problemu na części składowe	podział kodu na funkcje i logiczne sekcje
Programowanie strukturalne (funkcje)	liczne funkcje modularne (np. evaluate_population, mutate, plot_pareto)
Programowanie obiektowe (klasy, obiekty)	klasa Individual z metodą to_dict()
Obsługa formatu JSON	save_results_to_json() i load_results_from_json()
Wyrażenia regularne (regex)	extract_problem_number() do walidacji nazw problemów
Przykład działania (skrót)

Dla problemu ZDT3, wymiaru 30 i 500 generacji:

program generuje kolejne fronty Pareto,

zapisuje wyniki do ZDT3_D_results.json,

tworzy pliki graficzne ZDT3_D10_pareto.png, ZDT3_D30_pareto.png, ZDT3_D50_pareto.png.

Autor

Zuzanna Kulpa
Projekt wykonany w ramach zajęć „Podstawy programowania w języku Python”.
Rok akademicki 2025/2026

Informacje o pochodzeniu projektu

Pierwotna wersja programu została opracowana w ramach zajęć „Algorytmy Genetyczne”, jako implementacja algorytmu NSGA-II służącego do rozwiązywania problemów optymalizacji wielokryterialnej.

Na potrzeby obecnych zajęć z „Programowania w Pythonie” projekt został zmodyfikowany i rozszerzony, tak aby spełniał wszystkie wymagania kursu, w tym:

zastosowanie programowania obiektowego (klasa Individual),

dodanie operacji wejścia/wyjścia (CLI, wczytywanie i zapis plików JSON, generowanie wykresów PNG),

wykorzystanie wyrażeń regularnych do walidacji nazw problemów,

rozbudowaną strukturę funkcji i modułów zgodną z zasadami dekompozycji problemu.

W efekcie powstała wersja projektu, która łączy wcześniejsze rozwiązania z nowymi elementami programistycznymi, stanowiąc kompletny przykład praktycznego zastosowania Pythona do algorytmów ewolucyjnych.