import numpy as np
from vega_datasets import data

EARTH_RADIUS_KM = 6371.0


def haversine_km(lat1, lon1, lat2, lon2):
    lat1 = np.deg2rad(lat1)
    lon1 = np.deg2rad(lon1)
    lat2 = np.deg2rad(lat2)
    lon2 = np.deg2rad(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    )
    return 2 * EARTH_RADIUS_KM * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


airports = data.airports().copy()
routes = data.flights_airport().copy()

origin_airports = airports.rename(
    columns={
        "iata": "origin",
        "name": "origin_name",
        "city": "origin_city",
        "latitude": "origin_lat",
        "longitude": "origin_lon",
    }
)[["origin", "origin_name", "origin_city", "origin_lat", "origin_lon"]]

destination_airports = airports.rename(
    columns={
        "iata": "destination",
        "name": "destination_name",
        "city": "destination_city",
        "latitude": "destination_lat",
        "longitude": "destination_lon",
    }
)[
    [
        "destination",
        "destination_name",
        "destination_city",
        "destination_lat",
        "destination_lon",
    ]
]

routes_full = (
    routes.merge(origin_airports, on="origin", how="left", validate="many_to_one")
    .merge(destination_airports, on="destination", how="left", validate="many_to_one")
)

routes_full["distance_km"] = haversine_km(
    routes_full["origin_lat"],
    routes_full["origin_lon"],
    routes_full["destination_lat"],
    routes_full["destination_lon"],
)
routes_full["total_km"] = routes_full["count"] * routes_full["distance_km"]

routes_full = routes_full[
    [
        "origin",
        "origin_name",
        "origin_city",
        "origin_lat",
        "origin_lon",
        "destination",
        "destination_name",
        "destination_city",
        "destination_lat",
        "destination_lon",
        "count",
        "distance_km",
        "total_km",
    ]
]

total_count = routes_full.groupby("origin")["count"].sum()
airports["total_count"] = airports["iata"].map(total_count).fillna(0).astype(int)

top10_airports = (
    airports.sort_values("total_count", ascending=False)
    .head(10)[["iata", "name", "city", "total_count"]]
)

top10_routes = (
    routes_full.sort_values("total_km", ascending=False)
    .head(10)[
        [
            "origin",
            "origin_city",
            "destination",
            "destination_city",
            "count",
            "distance_km",
            "total_km",
        ]
    ]
)

hub_stats = (
    routes_full.assign(short_count=routes_full["count"].where(routes_full["distance_km"] <= 500, 0))
    .groupby("origin", as_index=False)
    .agg(total_count=("count", "sum"), short_count=("short_count", "sum"))
)
hub_stats["short_share"] = hub_stats["short_count"] / hub_stats["total_count"]

threshold = hub_stats["total_count"].quantile(0.8)

top10_short_share = (
    hub_stats[hub_stats["total_count"] > threshold]
    .merge(
        origin_airports[["origin", "origin_name", "origin_city"]],
        on="origin",
        how="left",
        validate="one_to_one",
    )
    .sort_values("short_share", ascending=False)
    .head(10)[
        [
            "origin",
            "origin_name",
            "origin_city",
            "total_count",
            "short_count",
            "short_share",
        ]
    ]
)

print("Top 10 lotnisk wg total_count:")
print(top10_airports.to_string(index=False))

print("\nTop 10 połączeń wg total_km:")
print(
    top10_routes.to_string(
        index=False,
        formatters={
            "distance_km": lambda x: f"{x:.2f}",
            "total_km": lambda x: f"{x:.2f}",
        },
    )
)

print("\nTop 10 lotnisk z największym udziałem lotów krótkodystansowych:")
print(
    top10_short_share.to_string(
        index=False,
        formatters={"short_share": lambda x: f"{x:.4f}"},
    )
)
