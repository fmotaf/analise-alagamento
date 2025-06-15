

## Source Code Organization

- src/
  - data/ - Data handling
    - collection/ - Data collection
    - processing/ - Data processing
    - alidation/ - Data validation
  - models/ - Model code
    - 	raining/ - Model training
    - prediction/ - Model prediction
  - isualization/ - Visualization code
    - maps/ - Map visualization
    - charts/ - Statistical charts
  - utils/ - Utility functions
    - geo/ - Geospatial utilities
    - weather/ - Weather utilities
    - satellite/ - Satellite data utilities
    - data/ - General data utilities

## Code Organization

### Data Collection
- src/data/collection/
  - gera_geojson.py - Create GeoJSON files
  - identifica_bairro.py - Neighborhood identification

### Data Processing
- src/data/processing/
  - hands_por_bairros.py - HAND data by neighborhoods
  - merge_hand_with_climate.py - Merge HAND with climate data
  - converte_shapefile.py - Shapefile conversion
  - merge_fsa_rasters.py - Raster merging

### Data Validation
- src/data/validation/
  - Data quality checks
  - Data cleaning

### Model Training
- src/models/training/
  - 	rain_flood_model.py - Main training script
  - Feature engineering
  - Model selection

### Model Prediction
- src/models/prediction/
  - predict_future_floods.py - Flood prediction
  - Climate forecasting

### Visualization
- src/visualization/charts/
  - Statistical visualizations
  - Data distributions
- src/visualization/maps/
  - Geospatial visualizations
  - Flood region maps

### Utilities
- src/utils/geo/
  - Geospatial operations
  - Neighborhood analysis
- src/utils/weather/
  - Weather data handling
  - Climate data processing
- src/utils/satellite/
  - Satellite data processing
  - Raster operations
- src/utils/data/
  - General data utilities
  - Data scraping
  - News analysis
