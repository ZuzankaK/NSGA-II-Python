# Algorytm genetyczny NSGA-II (Python)

## Opis projektu

Program implementuje algorytm genetyczny **NSGA-II (Non-dominated Sorting Genetic Algorithm II)**,  
który służy do rozwiązywania problemów **optymalizacji wielokryterialnej**.  

Zaimplementowano pięć klasycznych funkcji testowych z rodziny **ZDT1–ZDT6**,  
służących do oceny jakości algorytmu.  
Wyniki są prezentowane w formie wykresów frontu Pareto oraz zapisywane do pliku **JSON**.

---

## Cele projektu

Celem programu jest:

- prezentacja działania algorytmu ewolucyjnego,  
- wizualizacja rozkładu rozwiązań na przestrzeni iteracji,  
- pokazanie znajomości:
  - struktur danych w Pythonie,  
  - operacji wejścia/wyjścia,  
  - programowania strukturalnego i obiektowego,  
  - obsługi plików JSON,  
  - wyrażeń regularnych (regex).

---

## Wymagania systemowe

- **Python 3.9+**
- **Biblioteki:**

```bash
pip install numpy matplotlib
```

---

## Uruchomienie programu

### Uruchomienie domyślne (ZDT1)

```bash
python main.py
```

### Wybór problemu

```bash
python main.py --problem ZDT3
```

Dostępne problemy: `ZDT1`, `ZDT2`, `ZDT3`, `ZDT4`, `ZDT6`.

### Zapis wyników do JSON

```bash
python main.py --problem ZDT2 --save
```

Wyniki zostaną zapisane w pliku:

```
results/ZDT2_D_results.json
```

### Wczytanie zapisanych wyników

```bash
python main.py --problem ZDT2 --load results/ZDT2_D_results.json
```

---

## Wyniki i wizualizacja

Dla każdej kombinacji problemu ZDT i wymiaru (10, 30, 50) program generuje wykresy frontu Pareto:

```
results/ZDT1_D10_pareto.png
results/ZDT1_D30_pareto.png
results/ZDT1_D50_pareto.png
```

Każdy wykres przedstawia kolejne fronty Pareto dla zapisanych iteracji (np. 20, 50, 100, 500).

---

## Struktura projektu

```plaintext
├── main.py                 # główny kod programu
├── results/                # folder z przykładowymi wynikami
│   ├── ZDT1_D10_pareto.png
│   ├── ZDT1_D30_pareto.png
│   └── ZDT1_D50_pareto.png
├── README.md               # opis projektu
├── requirements.txt        # biblioteki
└── .gitignore              # ignorowane pliki
```

---

## Struktura kodu

- **Klasa `Individual`** – reprezentuje osobnika populacji (chromosom + wartości funkcji celu).
- **Funkcje `zdtX_f1`, `zdtX_f2`** – implementacje funkcji testowych ZDT1–ZDT6.
- **Funkcje pomocnicze:**
  - `initialize_population()` – inicjalizacja populacji,
  - `evaluate_population()` – obliczanie wartości funkcji celu,
  - `non_dominated_sorting()` – sortowanie względem dominacji Pareto,
  - `calculate_crowding_distance()` – obliczanie odległości zatłoczenia,
  - `crossover()`, `mutate()` – operatory genetyczne,
  - `tournament_selection()` – selekcja turniejowa,
  - `save_results_to_json()` / `load_results_from_json()` – zapis i odczyt danych,
  - `plot_pareto()` – wizualizacja wyników.

---

## Spełnienie wymagań przedmiotu

| Wymaganie | Spełnienie |
|------------|------------|
| Znajomość typów i struktur danych | list, dict, numpy.ndarray |
| Operacje wejścia/wyjścia (I/O) | zapis/odczyt JSON, zapis PNG, CLI (argparse) |
| Dekompzycja problemu | podział kodu na funkcje i sekcje logiczne |
| Programowanie strukturalne | modularne funkcje (`evaluate_population`, `mutate`, `plot_pareto`) |
| Programowanie obiektowe | klasa `Individual` z metodą `to_dict()` |
| Obsługa formatu JSON | `save_results_to_json()` i `load_results_from_json()` |
| Wyrażenia regularne | `extract_problem_number()` do walidacji nazw problemów |

---

## Informacje o pochodzeniu projektu

Projekt pierwotnie powstał w ramach zajęć **„Algorytmy Genetyczne”**,  
a następnie został zmodyfikowany i rozszerzony na potrzeby przedmiotu  
**„Podstawy programowania w języku Python”**, aby spełnić wszystkie wymagania kursu.

---

## Autor

**Zuzanna Kulpa**  
Rok akademicki 2025/2026
