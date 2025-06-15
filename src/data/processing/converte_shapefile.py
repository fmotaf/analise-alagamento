import geopandas as gpd

# --- Ler um Shapefile ---
caminho_shapefile = "BA_bairros_CD2022.shp"  # Substitua

try:
    gdf = gpd.read_file(caminho_shapefile)

    # 'gdf' é um GeoDataFrame, similar a um DataFrame do pandas, mas com uma coluna de geometria
    print("Informações do GeoDataFrame lido do Shapefile:")
    print(gdf.info())
    print("\nPrimeiras linhas do GeoDataFrame:")
    print(gdf.head())
    print(f"\nSistema de Coordenadas de Referência (CRS): {gdf.crs}")

    # --- Converter e salvar como GeoJSON ---
    caminho_saida_geojson = "feira_de_santana_convertido.geojson"
    gdf.to_file(caminho_saida_geojson, driver="GeoJSON")
    print(f"\nShapefile convertido e salvo como GeoJSON em: '{caminho_saida_geojson}'")

    # --- Se você já tem um GeoJSON e quer lê-lo com geopandas ---
    # caminho_geojson_existente = 'feira_de_santana_urbano.geojson'
    # gdf_from_geojson = gpd.read_file(caminho_geojson_existente)
    # print("\nGeoDataFrame lido de um arquivo GeoJSON existente:")
    # print(gdf_from_geojson.head())

    # --- Operações comuns com GeoDataFrame ---
    # Exemplo: Acessar a coluna de geometria
    # print("\nGeometrias:")
    # print(gdf['geometry'].head())

    # Exemplo: Acessar propriedades (colunas do Shapefile/GeoJSON)
    # if 'NOME_BAIRRO' in gdf.columns: # Supondo que exista uma coluna com nome do bairro
    #     print("\nNomes dos Bairros (exemplo):")
    #     print(gdf['NOME_BAIRRO'].head())

except FileNotFoundError:
    print(f"Erro: Arquivo Shapefile não encontrado em '{caminho_shapefile}'")
except Exception as e:
    print(f"Ocorreu um erro com o geopandas: {e}")
