## Zadanie 1

Zaimplementuj analizę dyskryminacyjną Fishera dla dwóch klas. Nie
korzystaj z gotowych implementacji LDA, w szczególności z
`sklearn.discriminant_analysis.LinearDiscriminantAnalysis`.

Wygeneruj sztuczny zbiór danych składający się z dwóch klas punktów w
przestrzeni dwuwymiarowej:

```python
import numpy as np

rng = np.random.default_rng(20260525)

mean0 = np.array([0.0, 0.0])
mean1 = np.array([2.0, 2.0])

cov = np.array([
    [1.0, 0.7],
    [0.7, 1.0],
])

X0 = rng.multivariate_normal(mean0, cov, size=100)
X1 = rng.multivariate_normal(mean1, cov, size=100)

X = np.vstack([X0, X1])
y = np.array([0] * len(X0) + [1] * len(X1))
```

Wykonaj następujące kroki:
   - podziel dane losowo na zbiór treningowy i testowy, np. w proporcji
     70%--30%,
   - oblicz wektory średnich obu klas na zbiorze treningowym,
   - oblicz macierz rozrzutu wewnątrzklasowego
     $S_W = S_0 + S_1$, gdzie
     ```text
     S_k = sum_{x w klasie k} (x - m_k)(x - m_k)^T,
     ```
   - wyznacz kierunek dyskryminacyjny Fishera
     ```text
     w = S_W^{-1}(m_1 - m_0),
     ```
   - zrzutuj punkty treningowe i testowe na kierunek `w`,
   - wyznacz próg klasyfikacji jako średnią z rzutów średnich obu klas,
   - przypisz etykiety klas na podstawie położenia rzutu punktu względem
     progu,
   - policz dokładność klasyfikacji na zbiorze treningowym i testowym.

Przygotuj wykresy:
   - wykres punktowy danych w przestrzeni oryginalnej, z kolorami
     odpowiadającymi klasom,
   - ten sam wykres z zaznaczonym kierunkiem Fishera,
   - histogram rzutów punktów na kierunek Fishera dla obu klas, z
     zaznaczonym progiem klasyfikacji.

Rozwiązanie powinno zawierać klasę lub zestaw funkcji umożliwiających
ponowne użycie implementacji, np.:

```python
class FisherLDA:
    def fit(self, X, y):
        ...

    def project(self, X):
        ...

    def predict(self, X):
        ...
```

## Zadanie 2

Zbadaj, jak położenie i rozrzut klas wpływają na skuteczność analizy
dyskryminacyjnej Fishera.

Wykorzystując implementację z zadania 1, wygeneruj kilka zbiorów danych,
zmieniając:
   - odległość między średnimi klas,
   - wariancję punktów w obu klasach,
   - korelację między współrzędnymi punktów,
   - liczność klas, w tym przypadek klas niezbalansowanych.

Dla każdego zbioru:
   - narysuj dane w przestrzeni oryginalnej,
   - narysuj histogram rzutów na kierunek Fishera,
   - policz dokładność klasyfikacji na zbiorze testowym,
   - krótko skomentuj, w których przypadkach klasy są dobrze rozdzielone,
     a w których metoda popełnia więcej błędów.

## Zadanie 3

Dla zbioru danych [`Breast Cancer
Wisconsin`](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html)
dostępnego w `sklearn.datasets.load_breast_cancer` zastosuj własną
implementację analizy dyskryminacyjnej Fishera z zadania 1.

Zbiór zawiera pomiary cech komórek nowotworowych oraz etykietę klasy
opisującą, czy przypadek jest złośliwy czy łagodny. W tym zadaniu
traktujemy go jako problem klasyfikacji binarnej.

Wykonaj następujące kroki:
   - wczytaj dane:
     ```python
     from sklearn.datasets import load_breast_cancer

     data = load_breast_cancer()
     X = data.data
     y = data.target
     ```
   - podziel dane losowo na zbiór treningowy i testowy, np. w proporcji
     70%--30%,
   - wystandaryzuj cechy, obliczając średnie i odchylenia standardowe
     wyłącznie na zbiorze treningowym, a następnie stosując tę samą
     transformację do zbioru treningowego i testowego,
   - dopasuj własny model Fishera na zbiorze treningowym,
   - oblicz dokładność klasyfikacji na zbiorze treningowym i testowym,
   - narysuj histogram rzutów obserwacji testowych na kierunek Fishera
     dla obu klas, z zaznaczonym progiem klasyfikacji,
   - przygotuj macierz pomyłek dla zbioru testowego,
   - wskaż pięć cech o największych wartościach bezwzględnych
     współczynników wektora `w` i sprawdź ich nazwy w `data.feature_names`.

Nie korzystaj z `sklearn.discriminant_analysis.LinearDiscriminantAnalysis`
ani z innych gotowych klasyfikatorów. Pakiet `sklearn` może być użyty do
wczytania zbioru danych.
