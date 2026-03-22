import pandas as pd

URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-07-27/olympics.csv"
USECOLS = ["id", "noc", "year", "season", "sport", "event", "medal"]

olympics = pd.read_csv(URL, usecols=USECOLS)
olympics = olympics[
    (olympics["season"] == "Summer") & olympics["year"].between(2000, 2016)
].copy()

medal_rows = olympics[olympics["medal"].notna() & olympics["medal"].ne("NA")].copy()
medal_events = medal_rows[
    ["year", "season", "sport", "event", "medal", "noc"]
].drop_duplicates()

athletes_sport = (
    olympics.groupby(["year", "season", "noc", "sport"], as_index=False)["id"]
    .nunique()
    .rename(columns={"id": "athletes_sport"})
)

medals_event_sport = (
    medal_events.groupby(["year", "season", "noc", "sport"], as_index=False)
    .size()
    .rename(columns={"size": "medals_event_sport"})
)

sport_results = athletes_sport.merge(
    medals_event_sport,
    on=["year", "season", "noc", "sport"],
    how="left",
    validate="one_to_one",
)
sport_results["medals_event_sport"] = (
    sport_results["medals_event_sport"].fillna(0).astype(int)
)

rate_sport = (
    sport_results.groupby(["year", "season", "sport"], as_index=False)
    .agg(
        total_athletes_sport=("athletes_sport", "sum"),
        total_medals_event_sport=("medals_event_sport", "sum"),
    )
    .assign(
        rate_sport=lambda x: x["total_medals_event_sport"]
        / x["total_athletes_sport"]
    )
)

sport_results = sport_results.merge(
    rate_sport[["year", "season", "sport", "rate_sport"]],
    on=["year", "season", "sport"],
    how="left",
    validate="many_to_one",
)
sport_results["expected_component"] = (
    sport_results["rate_sport"] * sport_results["athletes_sport"]
)

athletes = (
    olympics.groupby(["year", "season", "noc"], as_index=False)["id"]
    .nunique()
    .rename(columns={"id": "athletes"})
)

medals_event = (
    medal_events.groupby(["year", "season", "noc"], as_index=False)
    .size()
    .rename(columns={"size": "medals_event"})
)

expected_medals = (
    sport_results.groupby(["year", "season", "noc"], as_index=False)
    .agg(expected_medals=("expected_component", "sum"))
)

result = (
    athletes.merge(medals_event, on=["year", "season", "noc"], how="left")
    .merge(expected_medals, on=["year", "season", "noc"], how="left")
    .fillna({"medals_event": 0})
)
result["medals_event"] = result["medals_event"].astype(int)
result["ratio"] = (
    result["medals_event"] / result["expected_medals"]
).where(result["expected_medals"] > 0)
result["residual"] = result["medals_event"] - result["expected_medals"]

filtered = result[
    (result["athletes"] >= 50)
    & (result["expected_medals"] >= 1)
    & result["ratio"].notna()
].copy()

print("Top 5 krajów wg ratio dla każdej edycji:")
for (year, season), group in filtered.groupby(["year", "season"], sort=True):
    top5 = group.nlargest(
        5, "ratio"
    )[
        [
            "year",
            "season",
            "noc",
            "athletes",
            "medals_event",
            "expected_medals",
            "ratio",
            "residual",
        ]
    ]
    print(f"\n== {year} {season} ==")
    print(
        top5.to_string(
            index=False,
            formatters={
                "expected_medals": lambda x: f"{x:.2f}",
                "ratio": lambda x: f"{x:.2f}",
                "residual": lambda x: f"{x:.2f}",
            },
        )
    )

consistent = (
    filtered.groupby("noc", as_index=False)
    .agg(editions=("year", "nunique"), median_ratio=("ratio", "median"))
)
top10_consistent = consistent[consistent["editions"] == 5].nlargest(10, "median_ratio")

print("\nTop 10 najbardziej konsekwentnych liderów ratio:")
print(
    top10_consistent.to_string(
        index=False,
        formatters={"median_ratio": lambda x: f"{x:.2f}"},
    )
)

top_nocs = top10_consistent["noc"]

dominant_sport = (
    sport_results[sport_results["noc"].isin(top_nocs)]
    .groupby(["noc", "sport"], as_index=False)
    .agg(medals_event_sport=("medals_event_sport", "sum"))
)

dominant_sport = dominant_sport.merge(
    dominant_sport.groupby("noc", as_index=False).agg(
        medals_event=("medals_event_sport", "sum")
    ),
    on="noc",
    how="left",
    validate="many_to_one",
)

dominant_sport = (
    dominant_sport.sort_values(["noc", "medals_event_sport"], ascending=[True, False])
    .groupby("noc", as_index=False)
    .head(1)
)
dominant_sport["top_sport_share"] = (
    dominant_sport["medals_event_sport"] / dominant_sport["medals_event"]
)

dominant_sport = top10_consistent.merge(
    dominant_sport[["noc", "sport", "medals_event_sport", "medals_event", "top_sport_share"]],
    on="noc",
    how="left",
    validate="one_to_one",
)

print("\nDominująca dyscyplina dla 10 najbardziej konsekwentnych liderów ratio:")
print(
    dominant_sport.to_string(
        index=False,
        formatters={
            "median_ratio": lambda x: f"{x:.2f}",
            "top_sport_share": lambda x: f"{x:.2f}",
        },
    )
)
