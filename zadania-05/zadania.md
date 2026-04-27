## Zadanie 1

Zaimplementuj następujące miary oceny jakości klasteryzacji:
   - [indeks
     Calińskiego--Harabasza](https://en.wikipedia.org/wiki/Calinski%E2%80%93Harabasz_index),
   - [indeks
     sylwetki](https://en.wikipedia.org/wiki/Silhouette_(clustering)),
   - [indeks
     Daviesa--Bouldina](https://en.wikipedia.org/wiki/Davies%E2%80%93Bouldin_index),
   - [indeks Dunna](https://en.wikipedia.org/wiki/Dunn_index),
   - [indeks Randa](https://en.wikipedia.org/wiki/Rand_index).

## Zadanie 2

Dla zbioru danych
[`Wine`](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_wine.html)
dostępnego w `sklearn.datasets.load_wine` przeprowadź porównanie algorytmów
klasteryzacji. Zbiór zawiera 178 próbek win opisanych 13 cechami chemicznymi
oraz etykietę odmiany winogron. Etykietę odmiany wykorzystaj wyłącznie do
obliczenia indeksu Randa, a nie jako cechę wejściową algorytmów.

Wykonaj następujące kroki:
   - wczytaj dane, oddziel macierz cech od etykiet klas i wystandaryzuj cechy,
     np. za pomocą `StandardScaler`,
   - uruchom kilka algorytmów klasteryzacji z pakietu `scikit-learn`, w tym
     co najmniej:
       - `KMeans` z losową inicjalizacją centroidów,
       - `KMeans` z inicjalizacją `k-means++`,
       - `DBSCAN`,
       - jeden inny algorytm, np. `AgglomerativeClustering`,
         `GaussianMixture` albo `SpectralClustering`,
   - dla algorytmów wymagających podania liczby klastrów sprawdź kilka wartości
     tego parametru, np. od 2 do 8,
   - dla algorytmu `DBSCAN` sprawdź kilka par parametrów `eps` i `min_samples`,
   - dla każdego uruchomienia policz indeksy zaimplementowane w zadaniu 1:
     indeks Calińskiego--Harabasza, indeks sylwetki, indeks
     Daviesa--Bouldina, indeks Dunna oraz indeks Randa,
   - przygotuj tabelę z wynikami i wskaż, które algorytmy oraz parametry zostały
     najlepiej ocenione przez poszczególne indeksy.
