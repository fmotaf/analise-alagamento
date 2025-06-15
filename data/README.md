# Data Organization

## Raw Data
### Geospatial Data (aw/geospatial/)
- BA_bairros_CD2022.* - Neighborhood boundaries
- feira_de_santana_convertido.geojson - Feira de Santana shapefile

### Weather Data (aw/weather/)
- flood_previsao_2024_2025.csv - Historical weather data

### Satellite Data (aw/satellite/)
- Copernicus DSM TIF files - Digital Surface Model data
- HAND_merged_fsa.tif - Merged HAND data

## Processed Data
### Features (processed/features/)
- flood_features.csv - Processed flood features
- flood_dataset_full.csv - Main flood dataset
- flood_dataset_full_with_flood_occurrence.csv - Dataset with flood occurrence

### Models (processed/models/)
- modelo_flood_rf_mais_novo_e_melhor.pkl - Random Forest model for flood prediction

## Data Flow
1. Raw data is processed and cleaned
2. Features are extracted and combined
3. Models are trained and saved
4. Predictions are generated from the models
