import pandas as pd
import folium

df = pd.read_csv("./data/starbucks_dataset.csv")

df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
df_geo = df.dropna(subset=['Latitude', 'Longitude'])

m = folium.Map(location=[39.82, -98.57], zoom_start=4)

title_html = '''
             <h3 align="center" style="font-size:20px"><b>Starbucks Point Map</b></h3>
             '''
m.get_root().html.add_child(folium.Element(title_html))


css_fix = """
<style>
html, body {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
}
.folium-map {
    width: 100%;
    height: 95%;
}
</style>
"""
m.get_root().header.add_child(folium.Element(css_fix))


for lat, lon in zip(df_geo['Latitude'], df_geo['Longitude']):
    folium.CircleMarker(
        location=[lat, lon],
        radius=2,   
        color='green',
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

m.save("starbucks_point_map.html")
print("Point map saved!")
