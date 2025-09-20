import pandas as pd
import folium

df = pd.read_csv("./data/starbucks_dataset.csv")

df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
df_geo = df.dropna(subset=['Latitude', 'Longitude'])

grouped = (
    df_geo
    .groupby('State/Province')
    .agg({
        'Latitude': 'mean',   
        'Longitude': 'mean',
        'Store Number': 'count' 
    })
    .reset_index()
    .rename(columns={'Store Number': 'Count'})
)
m = folium.Map(location=[39.82, -98.57], zoom_start=4)

title_html = '''
             <h3 align="center" style="font-size:20px"><b>Starbucks Proportional Symbol Map by State</b></h3>
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

for _, row in grouped.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=max(3, row['Count']**0.5),
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        popup=f"{row['State/Province']}: {row['Count']} stores"
    ).add_to(m)

m.save("starbucks_proportional_map_state.html")
print("Proportional symbol map by state saved!")
