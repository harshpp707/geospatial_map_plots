import json
import pandas as pd
import folium
from folium.plugins import MarkerCluster

with open("airline_routes.json", "r", encoding="utf-8") as f:
    data = json.load(f)

airport_coords = {
    iata: (
        float(info["latitude"]),
        float(info["longitude"]),
        info.get("display_name", iata)
    )
    for iata, info in data.items()
    if info.get("latitude") and info.get("longitude")
}

routes_list = [
    {
        "source_iata": src_iata,
        "dest_iata": dst["iata"],
        "source_lat": src_lat,
        "source_lon": src_lon,
        "dest_lat": airport_coords[dst["iata"]][0],
        "dest_lon": airport_coords[dst["iata"]][1],
        "carriers": (
            ", ".join(c["iata"] for c in dst.get("carriers", []))
            if dst.get("carriers")
            else "Unknown"
        ),
        "distance_km": dst.get("km"),
        "duration_min": dst.get("min"),
    }
    for src_iata, (src_lat, src_lon, _) in airport_coords.items()
    for dst in data[src_iata].get("routes", [])
    if dst["iata"] in airport_coords
]

df_routes = pd.DataFrame(routes_list)

m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")


routes_layer = folium.FeatureGroup(name="Flight Routes", show=True).add_to(m)
airports_layer = folium.FeatureGroup(name="Airports", show=True).add_to(m)

for row in df_routes.itertuples(index=False):
    tooltip = (
        f"✈ {row.source_iata} → {row.dest_iata}<br>"
        f"Carriers: {row.carriers}<br>"
        f"Distance: {row.distance_km or 'N/A'} km<br>"
        f"Duration: {row.duration_min or 'N/A'} min"
    )
    folium.PolyLine(
        locations=[[row.source_lat, row.source_lon], [row.dest_lat, row.dest_lon]],
        color="blue",
        weight=1.2,
        opacity=0.4,
        tooltip=tooltip,
        highlight=True
    ).add_to(routes_layer)

marker_cluster = MarkerCluster(name="Airports Cluster", disableClusteringAtZoom=5)
for iata, (lat, lon, name) in airport_coords.items():
    folium.CircleMarker(
        location=[lat, lon],
        radius=3,
        color="red",
        fill=True,
        fill_opacity=0.8,
        tooltip=f"{name} ({iata})",
    ).add_to(marker_cluster)

marker_cluster.add_to(airports_layer)

folium.LayerControl().add_to(m)

m.save("json_flight_routes_map.html")
print("Map saved as json_flight_routes_map.html")
