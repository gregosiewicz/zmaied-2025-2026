## Zadanie 1

Wygeneruj losowy zbiór punktów na płaszczyźnie i dopasuj do niego model
regresji liniowej jednej zmiennej. Nie korzystaj z gotowych
implementacji regresji liniowej, w szczególności z
`sklearn.linear_model.LinearRegression`.

Generowanie danych:

```python
import numpy as np

rng = np.random.default_rng(20260601)

n = 100
X = rng.uniform(-4, 4, size=(n, 1))
noise = rng.normal(0, 2, size=n)

y = 3.0 * X[:, 0] - 2.0 + noise
```

Wykonaj następujące kroki:
   - podziel dane losowo na zbiór treningowy i testowy,
   - dopasuj model regresji liniowej na zbiorze treningowym, korzystając
     z jawnego wzoru:
     ```text
     beta = (X^T X)^(-1) X^T y
     ```
   - oblicz predykcje dla zbioru treningowego i testowego,
   - policz błąd MSE, RMSE, MAE dla zbioru treningowego i testowego,
   - narysuj wykres punktowy danych treningowych i testowych oraz prostą
     regresji,
   - na tym samym wykresie zaznacz prostą bez szumu, która została użyta
     do wygenerowania danych,
   - narysuj wykres reszt, czyli wartości
     ```text
     residual = y_true - y_pred
     ```
     w zależności od wartości przewidywanej przez model.

Następnie powtórz eksperyment dla kilku poziomów szumu, np. dla odchyleń
standardowych `0.5`, `2.0` i `5.0`. Przygotuj tabelę porównującą
otrzymane współczynniki modelu oraz wartości metryk na zbiorze testowym.

## Zadanie 2

Dla zbioru danych
[`Diabetes`](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_diabetes.html)
dostępnego w `sklearn.datasets.load_diabetes` zbuduj wielowymiarowy
model regresji liniowej. Zbiór zawiera 442 obserwacje opisane 10 cechami
liczbowymi, a zmienna docelowa opisuje ilościowy pomiar postępu choroby
rok po wykonaniu pomiarów wejściowych.

Nie korzystaj z gotowych implementacji regresji liniowej, w
szczególności z `sklearn.linear_model.LinearRegression`. Współczynniki
modelu wyznacz samodzielnie z równań normalnych.

Wykonaj następujące kroki:
   - wczytaj dane:
     ```python
     from sklearn.datasets import load_diabetes

     data = load_diabetes()
     X = data.data
     y = data.target
     ```
   - podziel dane losowo na zbiór treningowy i testowy,
   - wystandaryzuj cechy, obliczając średnie i odchylenia standardowe
     wyłącznie na zbiorze treningowym, a następnie stosując tę samą
     transformację do zbioru treningowego i testowego,
   - dopasuj model regresji liniowej na zbiorze treningowym, korzystając
     z jawnego wzoru:
     ```text
     beta = (X^T X)^(-1) X^T y
     ```
   - oblicz predykcje dla zbioru treningowego i testowego,
   - policz MSE, RMSE, MAE dla zbioru treningowego i testowego,
   - porównaj wynik modelu z prostym modelem bazowym, który dla każdej
     obserwacji przewiduje średnią wartość `y` ze zbioru treningowego,
   - przygotuj tabelę współczynników regresji z nazwami cech,
     posortowaną malejąco według wartości bezwzględnej współczynnika;
   - wskaż trzy cechy o największym wpływie na predykcję według
     dopasowanego modelu,
   - narysuj wykres punktowy wartości prawdziwych względem wartości
     przewidywanych na zbiorze testowym,
   - narysuj histogram reszt na zbiorze testowym.

## Zadanie 3

Wykorzystaj zbiór `Diabetes` z zadania 2 do zbudowania modelu regresji
logistycznej. Tym razem potraktuj problem jako klasyfikację binarną:
przewiduj, czy wartość zmiennej docelowej jest wysoka.

Użyj tego samego podziału na zbiór treningowy i testowy co w zadaniu 2.
Próg wysokiej wartości zmiennej docelowej wyznacz jako medianę `y` na
zbiorze treningowym:

```python
threshold = np.median(y_train)
y_train_class = (y_train >= threshold).astype(int)
y_test_class = (y_test >= threshold).astype(int)
```

Wykonaj następujące kroki:
   - wystandaryzuj cechy tak samo jak w zadaniu 2, używając parametrów
     obliczonych wyłącznie na zbiorze treningowym,
   - dopasuj model `LogisticRegression` ze `sklearn.linear_model` na
     zbiorze treningowym,
   - oblicz przewidywane klasy oraz prawdopodobieństwa klasy `1` dla
     zbioru treningowego i testowego,
   - policz accuracy, precision, recall, F1-score dla zbioru
     treningowego i testowego,
   - narysuj wykres punktowy prawdziwych wartości `y_test` względem
     prawdopodobieństwa przewidywanego przez model dla klasy `1`,
   - przygotuj tabelę współczynników regresji logistycznej z nazwami
     cech, posortowaną malejąco według wartości bezwzględnej
     współczynnika,
   - porównaj trzy najważniejsze cechy według regresji logistycznej z
     trzema najważniejszymi cechami według regresji liniowej z zadania 2.

Sprawdź także, jak zmieniają się precision i recall na zbiorze testowym
dla kilku progów decyzyjnych, np. `0.3`, `0.5` i `0.7`. Krótko
skomentuj, czy próg `0.5` jest najlepszym wyborem w tym zadaniu oraz jak
zmiana progu wpływa na liczbę fałszywie dodatnich i fałszywie ujemnych
klasyfikacji.
