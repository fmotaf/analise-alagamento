# Análise de Alagamento

## Objetivo

Este projeto tem como objetivo analisar, prever e visualizar riscos de alagamento em uma região específica utilizando dados meteorológicos, geoespaciais e modelos de machine learning. O sistema coleta, processa, valida dados, treina modelos de previsão e disponibiliza uma API e frontend para consulta de risco de alagamento.

## Abordagem Conceitual: Random Forest

O algoritmo **Random Forest** é um método de aprendizado de máquina do tipo ensemble, baseado em árvores de decisão. Ele constrói diversas árvores de decisão independentes durante o treinamento e, para cada previsão, retorna a classe mais votada (classificação) ou a média das saídas (regressão). Suas principais vantagens são:
- Redução do risco de overfitting em relação a uma única árvore.
- Robustez a ruídos e outliers.
- Capacidade de lidar com dados de alta dimensionalidade e variáveis correlacionadas.
No contexto deste projeto, o Random Forest é utilizado para prever a ocorrência de alagamentos a partir de variáveis climáticas e ambientais.

## Como rodar o projeto

1. **Clone o repositório:**
   ```sh
   git clone https://github.com/fmotaf/analise-alagamento.git
   cd analise-alagamento
   ```

2. **Crie e ative um ambiente virtual:**
   ```sh
   python -m venv .venv
   .venv\\Scripts\\activate  # Windows
   source .venv/bin/activate # Linux/Mac
   ```

3. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Execute os notebooks ou scripts para gerar as features e treinar o modelo:**
   - Notebooks em `src/notebooks/`
   - Scripts em `src/data/collection/` e `src/models/training/`

5. **Inicie a API:**
   ```sh
   uvicorn src.api.main:app --reload
   ```

6. **Acesse o frontend:**
   - Abra o arquivo `src/frontend/index.html` no navegador.

## Principais arquivos

- `src/data/collection/test_power_region_api.py`: Coleta dados meteorológicos da NASA POWER API.
- `src/notebooks/train_model_save_and_predict.ipynb`: Treinamento e avaliação do modelo de previsão de alagamento.
- `src/api/main.py`: API FastAPI para consulta de risco de alagamento.
- `src/frontend/script.js`: Script JS do frontend para consulta e visualização.
- `flood_features_3.csv`: Base de dados de features para o modelo.
- `flood_model.pkl`: Modelo treinado.

## Estrutura dos diretórios

```
.
|   README.md
|   requirements.txt
|   pyproject.toml
|
+---src
|   +---api
|   |       main.py
|   +---data
|   |   +---collection
|   |   +---processing
|   |   +---validation
|   +---models
|   |   +---training
|   |   +---prediction
|   +---notebooks
|   +---visualization
|   |   +---charts
|   |   +---maps
|   +---utils
|       +---geo
|       +---weather
|       +---satellite
|       +---data
+---logs
+---reports
+---static
```

> **Obs:** Para mais detalhes, consulte os notebooks e scripts em cada pasta.
