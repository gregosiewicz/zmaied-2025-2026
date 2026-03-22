## Zadanie 1

Wykorzystując dane [Our World in Data
(OWID)](https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv),
przeprowadź analizę zachorowań na COVID-19.

Wczytaj z pliku dane dotyczące roku 2021 dla krajów, których populacja
jest większa niż 1 mln. Wykorzystaj kolumny `code`, `country`, `date`,
`new_cases`, `population` (odpowiednio kod i nazwa kraju). Przygotuj
DataFrame z następującymi kolumnami dotyczącymi każdego kraju osobno:
- `peak_incidence_7d_1M` -- Maksymalna wartość (pik) średniej ruchomej
  liczby nowych przypadków (`new_cases`) z 7 dni na 1 milion
  mieszkańców (`population`). Jeżeli w oknie 7 dni występuje chociaż
  jeden brak danych, to przyjmujemy, że średnia ma wartość `NaN`.
- `peak_date` -- Data wystąpienia piku (jeśli pik występuje w wielu
  dniach, wybierz najwcześniejszy).
- `median_incidence_7d_1M` -- Mediana 7-dniowej zachorowalności
  (ignorujemy braki).
- `sharpness` -- Ostrość fali zachorowań, to znaczy
  `peak_incidence_7d_1M` / `median_incidence_7d_1M`.

Następnie wypisz:
- top 15 krajów z największym `peak_incidence_7d_1M` posortowanych
  malejąco,
- top 10 krajów z największym `sharpness` posortowanych malejąco.

## Zadanie 2

Wykorzystując dane z biblioteki `vega_datasets`, przeprowadź analizę
ruchu lotniczego w USA.

Wczytaj dane dotyczące lotnisk i tras:
```python
from vega_datasets import data

airports = data.airports().copy()
routes = data.flights_airport().copy()
```
Utwórz DataFrame będący połączeniem `routes` i `airports` z kolumnami:
- `origin` -- identyfikator lotniska początkowego,
- `origin_name` -- nazwa lotniska początkowego,
- `origin_city` -- miasto lotniska początkowego,
- `origin_lat` -- szerokość geograficzna lotniska początkowego,
- `origin_lon` -- długość geograficzna lotniska początkowego,
- `destination` -- j.w. dla lotniska docelowego,
- `destination_name`,
- `destination_city`,
- `destination_lat`,
- `destination_lon`,
- `count` -- liczba lotów na danej trasie,
- `distance_km` -- długość trasy (wykorzystaj wzór na [odległość po
  powierzchni kuli](https://en.wikipedia.org/wiki/Haversine_formula)),
- `total_km` -- łączna liczba kilometrów pokonanych przez samoloty na
  tej trasie.

Następnie:
- do ramki `airports` dodaj kolumnę `total_count` będącą łączną liczbą
  lotów wychodzących dla poszczególnych lotnisk,
- wypisz top 10 lotnisk względem `total_count` posortowaną malejąco,
- wypisz top 10 połączeń z największym `total_km` posortowaną malejąco,
- wypisz top 10 lotnisk startowych (`origin`) o największym udziale
  lotów krótkodystansowych (co najwyżej 500 km) w całym ruchu
  wychodzącym, rozpatrując tylko lotniska, dla których `total_count`
  jest większy od 80 percentyla rozkładu `total_count` dla wszystkich
  lotnisk startowych.

## Zadanie 3

Wykorzystując
[dane](https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-07-27/olympics.csv)
o igrzyskach olimpijskich, znajdź kraje zdobywające więcej medali niż
wynikałoby to z liczby reprezentantów.

Ogranicz dane do igrzysk letnich w latach 2000--2016. Wykorzystaj
kolumny `id`, `noc`, `year`, `season`, `sport`, `event`, `medal`.

Dla każdej edycji igrzysk i sportu policz globalną ,,stopę medalową'':
- `rate_sport`, równą `total_medals_event_sport /
  total_athletes_sport`, gdzie `total_*` to odpowiednio suma medali i
  liczba wszystkich sportowców w danej edycji i sporcie.

Dla każdego kraju w danej edycji policz:
- `athletes` -- liczba unikalnych zawodników,
- `athletes_sport` -- liczba unikalnych zawodników w danym sporcie,
- `medals_event` -- liczba medali, tj. liczba unikalnych krotek
  (`year`, `season`, `medal`, `noc`),
- `medals_event_sport` -- liczba medali w danym sporcie,
- `expected_medals` -- oczekiwana liczba medali po uwzględnieniu stopy
  medalowe, tj. `sum_sport(rate_sport * athletes_sport)`
- `ratio` -- stosunek liczby zdobytych medali do oczekiwanej liczby
  medali (jeśli `expected_medals <= 0`, to przypisz `NaN`),
- `residual` -- różnica między zdobytymi a oczekiwanymi medalami.

Wynikiem ma być DataFrame z kolumnami: `year`, `season`, `noc`,
`athletes`, `medals_event`, `expected_medals`, `ratio`, `residual`.

Wypisz:
- dla każdej edycji igrzysk: top 5 krajów wg `ratio` (malejąco),
  rozpatrując tylko kraje z `athletes >= 50` oraz `expected_medals >=
  1`,
- top 10 najbardziej konsekwentnych liderów `ratio`: dla każdego `noc`
  policz medianę `ratio` po edycjach (wymagaj udziału we wszystkich 5
  edycjach),
- dla 10 najbardziej konsekwentnych liderów `ratio` ich dominującą
  dyscyplinę: udział medali z jednego najbardziej medalowego sportu,
  czyli stosunek liczby wszystkich medali w sporcie o największej
  liczbie medali do liczby wszystkich medali (medale liczymy po
  wszystkich rozważanych edycjach).
