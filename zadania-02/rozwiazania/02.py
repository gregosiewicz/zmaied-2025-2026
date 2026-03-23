import re
import geopandas as gpd
import pandas as pd


PLIK_5G = "../dane/5g.xlsx"
PLIK_WOJEWODZTWA = "../dane/NUTS_RG_10M_2024_4326_LEVL_2.geojson"


def dms_na_stopnie(wartosc):
    stopnie, kierunek, minuty, sekundy = re.match(
        r"(\d+)([NSEW])(\d+)'(\d+)\"", str(wartosc)
    ).groups()
    wynik = int(stopnie) + int(minuty) / 60 + int(sekundy) / 3600
    if kierunek in ("N", "E"):
        return wynik
    return (-1) * wynik


def przygotuj_wojewodztwa():
    wojewodztwa = gpd.read_file(PLIK_WOJEWODZTWA)
    wojewodztwa = wojewodztwa[wojewodztwa["CNTR_CODE"] == "PL"][
        ["NUTS_ID", "NUTS_NAME", "geometry"]
    ].copy()
    wojewodztwa = wojewodztwa.rename(columns={"NUTS_ID": "id", "NUTS_NAME": "nazwa"})
    return wojewodztwa.to_crs(2180)


def przygotuj_nadajniki():
    dane = pd.read_excel(PLIK_5G)
    dane = dane.rename(
        columns={
            "Nazwa Operatora": "operator",
            "Dł geogr stacji": "dlugosc",
            "Szer geogr stacji": "szerokosc",
            "Miejscowość": "miejscowosc",
            "Lokalizacja": "lokalizacja",
            "IdStacji": "id_stacji",
        }
    )
    dane["lon"] = dane["dlugosc"].map(dms_na_stopnie)
    dane["lat"] = dane["szerokosc"].map(dms_na_stopnie)

    nadajniki = gpd.GeoDataFrame(
        dane[["id_stacji", "operator", "miejscowosc", "lokalizacja"]],
        geometry=gpd.points_from_xy(dane["lon"], dane["lat"]),
        crs="EPSG:4326",
    )
    return nadajniki.to_crs(2180)


def policz_pokrycie_wojewodztw(wojewodztwa, bufory):
    zasieg = bufory.geometry.union_all()
    wynik = wojewodztwa[["nazwa", "geometry"]].copy()
    wynik["powierzchnia_km2"] = wynik.area / 1_000_000
    wynik["pokrycie_km2"] = wynik.geometry.intersection(zasieg).area / 1_000_000
    wynik["pokrycie_proc"] = wynik["pokrycie_km2"] / wynik["powierzchnia_km2"] * 100
    return (
        wynik[["nazwa", "pokrycie_km2", "pokrycie_proc"]]
        .round({"pokrycie_km2": 2, "pokrycie_proc": 2})
        .sort_values("pokrycie_proc", ascending=False)
    )


def policz_ranking_operatorow(wojewodztwa, bufory):
    wyniki = []

    for operator, grupa in bufory.groupby("operator"):
        zasieg = grupa.geometry.union_all()
        ranking = wojewodztwa[["nazwa", "geometry"]].copy()
        ranking["operator"] = operator
        ranking["pokrycie_km2"] = ranking.geometry.intersection(zasieg).area / 1_000_000
        wyniki.append(ranking[["nazwa", "operator", "pokrycie_km2"]])

    ranking_operatorow = pd.concat(wyniki, ignore_index=True)
    ranking_operatorow["pokrycie_km2"] = ranking_operatorow["pokrycie_km2"].round(2)
    ranking_operatorow["miejsce"] = (
        ranking_operatorow.groupby("nazwa")["pokrycie_km2"]
        .rank(method="dense", ascending=False)
        .astype(int)
    )
    return ranking_operatorow.sort_values(["nazwa", "miejsce", "operator"])


def pokaz_tytul(tekst):
    print()
    print(tekst)
    print("=" * len(tekst))


def main():
    wojewodztwa = przygotuj_wojewodztwa()
    nadajniki = przygotuj_nadajniki()
    bufory = nadajniki.copy()
    bufory["geometry"] = bufory.buffer(1000)

    pokrycie_wojewodztw = policz_pokrycie_wojewodztw(wojewodztwa, bufory)
    ranking_operatorow = policz_ranking_operatorow(wojewodztwa, bufory)

    pokaz_tytul("Pokrycie 5G w województwach")
    print(pokrycie_wojewodztw.to_string(index=False))

    pokaz_tytul("Ranking operatorów w województwach")
    print(ranking_operatorow.to_string(index=False))


if __name__ == "__main__":
    main()
