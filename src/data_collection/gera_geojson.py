# import osmnx as ox
# import geopandas as gpd
#
# # Define a cidade
# cidade = "Feira de Santana, Bahia, Brazil"
#
# # Busca bairros urbanos classificados como 'neighbourhood' ou 'suburb'
# bairros = ox.features_from_place(
#     cidade,
#     tags={"place": ["neighbourhood", "suburb"]}
# )
#
# # Mantém apenas geometrias do tipo polígono
# bairros = bairros[bairros.geometry.type.isin(["Polygon", "MultiPolygon"])]
#
#
# print(bairros)
# # Salva para GeoJSON
# bairros.to_file("teste.geojson", driver="GeoJSON")


import matplotlib.pyplot as plt
import osmnx as ox

# Step 1: Get the boundary of Feira de Santana
city = "Feira de Santana, Bahia, Brazil"
feira_boundary = ox.geocode_to_gdf(city)

# Step 2: Download administrative boundaries inside the city
neighborhoods = ox.features_from_place(
    city, tags={"boundary": "administrative", "admin_level": "10"}  # level 10 is usually neighborhood
)

# Alternative tag: smaller districts or places
# neighborhoods = ox.geometries_from_place(
#     city,
#     tags={"place": ["neighbourhood", "suburb"]}
# )

# Step 3: Keep only polygons (some might be points/lines)
neighborhoods = neighborhoods[neighborhoods.geometry.type == "Polygon"]


# Step 4: Plot to check
fig, ax = plt.subplots(figsize=(10, 8))
feira_boundary.boundary.plot(ax=ax, color="black", linewidth=1)
neighborhoods.boundary.plot(ax=ax, color="blue", linewidth=0.5)
plt.title("Neighborhood Boundaries - Feira de Santana")
plt.axis("off")
plt.show()

# Step 5: Save for later use
neighborhoods.to_file("teste2.geojson", driver="GeoJSON")
