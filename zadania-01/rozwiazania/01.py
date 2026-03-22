import pandas as pd

URL = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"
USECOLS = ["code", "country", "date", "new_cases", "population"]

df = pd.read_csv(
    URL,
    usecols=USECOLS,
    parse_dates=["date"],
)
df = df.rename(columns={"code": "iso_code", "country": "location"})

df = df[df["iso_code"].str.len().eq(3)].copy()
df = df[df["date"].between("2021-01-01", "2021-12-31")].copy()

df = df[df["population"] > 1_000_000]

df = (
    df.groupby(["iso_code", "date"], as_index=False)
    .agg(
        location=("location", "first"),
        new_cases=("new_cases", "sum"),
        population=("population", "first"),
    )
    .sort_values(["iso_code", "date"])
    .reset_index(drop=True)
)

df["ma7_new_cases"] = (
    df.groupby("iso_code", sort=False)["new_cases"]
    .rolling(window=7, min_periods=7)
    .mean()
    .reset_index(level=0, drop=True)
)

df["incidence_7d_1M"] = df["ma7_new_cases"] / df["population"] * 1_000_000.0

peak_idx = (
    df.dropna(subset=["incidence_7d_1M"])
    .groupby("iso_code", sort=False)["incidence_7d_1M"]
    .idxmax()
)

peak_rows = (
    df.loc[peak_idx, ["iso_code", "location", "population", "date", "incidence_7d_1M"]]
    .copy()
    .rename(
        columns={
            "iso_code": "country_code",
            "location": "country_name",
            "population": "population_2021",
            "date": "peak_date",
            "incidence_7d_1M": "peak_incidence_7d_1M",
        }
    )
    .set_index("country_code")
)

median_inc = (
    df.groupby("iso_code", sort=False)["incidence_7d_1M"]
    .median(skipna=True)
    .rename("median_incidence_7d_1M")
)

result = peak_rows.join(median_inc, how="left")
result["sharpness"] = (
    result["peak_incidence_7d_1M"] / result["median_incidence_7d_1M"]
).where(result["median_incidence_7d_1M"] > 0)

result = result.reset_index()

top15_peak = result.sort_values("peak_incidence_7d_1M", ascending=False).head(15)
top10_sharp = (
    result[result["sharpness"].notna()]
    .sort_values("sharpness", ascending=False)
    .head(10)
)

formatters = {
    "population_2021": lambda x: str(int(x)),
    "peak_incidence_7d_1M": lambda x: f"{x:.2f}",
    "median_incidence_7d_1M": lambda x: f"{x:.2f}",
    "sharpness": lambda x: f"{x:.2f}",
}

print("Top 15 7-dniowej zapadalności / 1M:")
print(top15_peak.to_string(index=False, formatters=formatters))

print("\nTop 10 wg ostrości fali:")
print(top10_sharp.to_string(index=False, formatters=formatters))
