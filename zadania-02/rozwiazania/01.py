import geopandas as gpd
import pandas as pd

PLIK_WOJEWODZTWA = "../dane/NUTS_RG_10M_2024_4326_LEVL_2.geojson"
PLIK_MIASTA = "../dane/miasta.geojson"


def wczytaj_wojewodztwa():
    wojewodztwa = gpd.read_file(PLIK_WOJEWODZTWA)
    wojewodztwa = wojewodztwa[wojewodztwa["CNTR_CODE"] == "PL"][
        ["NUTS_ID", "NUTS_NAME", "geometry"]
    ].copy()
    wojewodztwa = wojewodztwa.rename(
        columns={"NUTS_ID": "id", "NUTS_NAME": "nazwa"}
    ).rename_geometry("geometria")
    wojewodztwa.to_file("wojewodztwa.geojson", driver="GeoJSON")
    return wojewodztwa


def wczytaj_miasta():
    miasta = gpd.read_file(PLIK_MIASTA)[["@id", "name", "population", "geometry"]].copy()
    miasta = miasta.rename(
        columns={"@id": "id", "name": "nazwa", "population": "ludnosc"}
    ).rename_geometry("geometria")
    miasta["ludnosc"] = pd.to_numeric(miasta["ludnosc"], errors="coerce").fillna(0).astype(int)
    return miasta


def policz_statystyki(miasta_w_wojewodztwach, wojewodztwa):
    statystyki = (
        miasta_w_wojewodztwach.groupby("wojewodztwo")
        .agg(
            liczba_miast=("id", "size"),
            ludnosc_miast=("ludnosc", "sum"),
        )
        .reset_index()
        .rename(columns={"wojewodztwo": "nazwa"})
    )
    statystyki = wojewodztwa[["nazwa"]].merge(statystyki, on="nazwa", how="left")
    statystyki = statystyki.fillna({"liczba_miast": 0, "ludnosc_miast": 0})
    statystyki["liczba_miast"] = statystyki["liczba_miast"].astype(int)
    statystyki["ludnosc_miast"] = statystyki["ludnosc_miast"].astype(int)
    return statystyki


def drukuj_naglowek(tekst):
    print()
    print(tekst)
    print("=" * len(tekst))


def main():
    wojewodztwa = wczytaj_wojewodztwa()
    miasta = wczytaj_miasta()

    miasta_w_wojewodztwach = gpd.sjoin(
        miasta,
        wojewodztwa[["nazwa", "geometria"]].rename(columns={"nazwa": "wojewodztwo"}),
        how="left",
        predicate="within",
    )
    statystyki = policz_statystyki(miasta_w_wojewodztwach, wojewodztwa)

    drukuj_naglowek("Liczba miast w województwach")
    print(statystyki[["nazwa", "liczba_miast"]].to_string(index=False))

    drukuj_naglowek("Województwa posortowane według liczby miast")
    print(
        statystyki[["nazwa", "liczba_miast"]]
        .sort_values("liczba_miast", ascending=False)
        .to_string(index=False)
    )

    drukuj_naglowek("Liczba mieszkańców miast w województwach")
    print(statystyki[["nazwa", "ludnosc_miast"]].to_string(index=False))

    wojewodztwa_2180 = wojewodztwa.to_crs(2180)
    miasta_2180 = miasta.to_crs(2180)

    gestosc = wojewodztwa_2180.merge(
        statystyki[["nazwa", "ludnosc_miast"]], on="nazwa", how="left"
    )
    gestosc["powierzchnia_km2"] = gestosc.area / 1_000_000
    gestosc["gestosc_zaludnienia"] = (
        gestosc["ludnosc_miast"] / gestosc["powierzchnia_km2"]
    )

    drukuj_naglowek("Województwa posortowane według gęstości zaludnienia")
    print(
        gestosc.assign(
            gestosc_zaludnienia=gestosc["gestosc_zaludnienia"].round(2)
        )[["nazwa", "gestosc_zaludnienia"]]
        .sort_values("gestosc_zaludnienia", ascending=False)
        .to_string(index=False)
    )

    warszawa = miasta_2180.loc[miasta_2180["nazwa"] == "Warszawa", "geometria"].iloc[0]
    liczba_miast_do_50_km = (
        (miasta_2180["nazwa"] != "Warszawa")
        & (miasta_2180.distance(warszawa) <= 50_000)
    ).sum()

    drukuj_naglowek("Liczba miast oddalonych od Warszawy o co najwyżej 50 km")
    print(liczba_miast_do_50_km)

    suma_odleglosci = miasta_2180["geometria"].apply(
        lambda geometria: miasta_2180.distance(geometria).sum()
    )
    centralne_miasto = miasta_2180.loc[suma_odleglosci.idxmin(), "nazwa"]

    drukuj_naglowek("Miasto o najmniejszej sumie odległości do pozostałych miast")
    print(centralne_miasto)


if __name__ == "__main__":
    main()
