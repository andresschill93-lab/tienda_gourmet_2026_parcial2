# Dashboard Interactivo - Tienda Gourmet

Sistema de control comercial que procesa datos históricos de ventas para apoyar
la toma de decisiones. Incluye gráficos estáticos e interactivos integrados en
un dashboard web, con una paleta de colores personalizada (tonos café y cobre).

Trabajo de la materia Programación Orientada al Análisis de Datos (2do 4, Instituto Superior Manuel Belgrano, Godoy Cruz, 2026).
Alumnos: Victoria Di Natale, Andrés Schilliagi.

## Funcionalidades

- **Pandas:** limpieza de datos y cálculo de márgenes de ganancia
- **Matplotlib:** evolución mensual de ventas (gráfico de líneas)
- **Seaborn:** rentabilidad por categoría (gráfico de barras)
- **Plotly:** distribución de ganancias (gráfico de torta interactivo)
- **Dash:** panel de control unificado en servidor web local
- **Backend de análisis (parcial 2):** estadística descriptiva (IC 95%, ANOVA, correlación), pronóstico Holt-Winters a 6 meses y una red LSTM con Keras, comparada contra Holt-Winters

## Estructura

```
tienda_gourmet_2026/
├── data/                          → datos (ventas_gourmet.csv) y ETL generado
├── sources/                       → carga de datos
├── view/                          → gráficos (matplotlib, seaborn, plotly)
├── data_processing.py             → ETL y lógica de negocio (pandas)
├── backend_analisis.py            → estadística, pronóstico y métricas del backend
├── main.py                        → punto de entrada del dashboard
├── examen_parcial2_analisis.ipynb → notebook con el análisis completo y la LSTM
├── analisis_backend.json          → KPI, pronóstico y métricas (generado por el notebook)
└── documentacion_parcial2.pdf     → documentación del proyecto
```

## Instalación

```bash
pip install pandas matplotlib seaborn plotly dash openpyxl scipy statsmodels scikit-learn tensorflow
```

## Ejecución del dashboard

```bash
python main.py
```

Abrí el navegador en: http://127.0.0.1:8050

El panel muestra los gráficos del parcial 1 y, debajo, la sección de análisis y pronóstico del backend. La tarjeta de la LSTM muestra "Sin datos" si falta `analisis_backend.json`; para generarlo, ejecutá el notebook.

## Ejecución del análisis (notebook)

Abrí `examen_parcial2_analisis.ipynb` en VS Code o Google Colab y ejecutá todas las celdas en orden. Genera `analisis_backend.json` y `data/ventas_limpias.csv`.
