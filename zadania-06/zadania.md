## Zadanie 1

Dla zbioru danych
[`Digits`](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html)
dostępnego w `sklearn.datasets.load_digits` wykonaj PCA, korzystając z
rozkładu SVD.

Wykonaj następujące kroki:
   - wczytaj dane i oddziel macierz cech `X` od etykiet `y`,
   - wycentruj dane, odejmując od każdej cechy jej średnią,
   - wykonaj rozkład SVD wycentrowanej macierzy danych: $X = U S V^T$,
   - oblicz składowe główne na podstawie macierzy $V^T$,
   - oblicz współrzędne próbek w przestrzeni PCA,
   - oblicz wariancję wyjaśnianą przez kolejne składowe:
     ```text
     explained_variance_i = S_i^2 / (n - 1)
     ```
   - oblicz procent wyjaśnianej wariancji dla każdej składowej,
   - narysuj wykres skumulowanej wyjaśnionej wariancji,
   - wyznacz najmniejszą liczbę składowych potrzebną do wyjaśnienia co
     najmniej 80%, 90% i 95% wariancji,
   - narysuj wykres punktowy pierwszych dwóch składowych głównych
     (`PC1`, `PC2`), kolorując punkty według cyfry.

Czy dwie pierwsze składowe pozwalają dobrze rozdzielić cyfry oraz
które cyfry najłatwiej lub najtrudniej odróżnić na wykresie.

## Zadanie 2

Rozwiąż zadanie 1 ponownie, tym razem korzystając z klasy
`PCA` z pakietu `sklearn.decomposition`.

Wykonaj następujące kroki:
   - uruchom `PCA` dla wszystkich 64 cech,
   - porównaj wartości `explained_variance_`,
     `explained_variance_ratio_` oraz `components_` z wynikami
     otrzymanymi samodzielnie przez SVD,
   - sprawdź, czy współrzędne próbek w pierwszych dwóch składowych są
     takie same jak w zadaniu 1,
   - narysuj obok siebie dwa wykresy `PC1`--`PC2`: jeden z własnej
     implementacji SVD i jeden z `sklearn.PCA`,
   - policz maksymalną różnicę bezwzględną między skumulowaną wariancją
     wyjaśnioną przez własne PCA i przez `sklearn.PCA`.

## Zadanie 3

Wykorzystaj PCA do kompresji i rekonstrukcji obrazów cyfr ze zbioru
`Digits`.

Wykonaj następujące kroki:
   - dla kilku wartości liczby składowych, np. `2`, `5`, `10`, `20`,
     `30` i `40`, wykonaj:
       - rzutowanie danych na wybraną liczbę składowych,
       - rekonstrukcję danych z tych składowych,
       - obliczenie średniego błędu rekonstrukcji, np. MSE,
   - przygotuj tabelę pokazującą liczbę składowych, procent zachowanej
     wariancji i błąd rekonstrukcji,
   - wybierz kilka przykładowych cyfr i narysuj ich rekonstrukcje dla
     różnej liczby składowych,
   - porównaj, przy ilu składowych cyfry zaczynają być rozpoznawalne
     wizualnie,
   - opcjonalnie dodaj do danych losowy szum i sprawdź, czy rekonstrukcja
     z ograniczonej liczby składowych częściowo usuwa ten szum.
