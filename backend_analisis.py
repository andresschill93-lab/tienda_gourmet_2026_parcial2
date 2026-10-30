import json
import os

import numpy as np
import plotly.graph_objects as go
from scipy import stats
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error

from data_processing import df

HORIZONTE = 6  # meses a pronosticar
RUTA_METRICAS_DL = "analisis_backend.json"  # generado por examen_parcial2_analisis.ipynb


def resumen_estadistico():
    """Estadística descriptiva de ventas y márgenes, y ANOVA entre categorías."""
    ventas = df["Ventas"]
    ic_bajo, ic_alto = stats.t.interval(
        0.95, len(ventas) - 1, loc=ventas.mean(), scale=stats.sem(ventas)
    )
    grupos = [g["Margen_Pct"].values for _, g in df.groupby("Categoria")]
    f_stat, p_valor = stats.f_oneway(*grupos)
    r, p_r = stats.pearsonr(df["Descuento"], df["Margen_Pct"])
    return {
        "venta_promedio": float(ventas.mean()),
        "ic95": [float(ic_bajo), float(ic_alto)],
        "asimetria": float(stats.skew(ventas)),
        "anova_f": float(f_stat),
        "anova_p": float(p_valor),
        "corr_descuento_margen": float(r),
        "corr_p": float(p_r),
    }


def pronostico_holt_winters():
    """Ajusta Holt-Winters sobre ventas mensuales y devuelve pronóstico y error de prueba."""
    serie = df.groupby(df["Fecha_Pedido"].dt.to_period("M").dt.to_timestamp())["Ventas"].sum().asfreq("MS")
    train, test = serie[:-HORIZONTE], serie[-HORIZONTE:]

    modelo_eval = ExponentialSmoothing(
        train, trend="add", seasonal="add", seasonal_periods=12
    ).fit()
    pred_test = modelo_eval.forecast(HORIZONTE)
    mae = mean_absolute_error(test, pred_test)
    rmse = float(np.sqrt(mean_squared_error(test, pred_test)))

    modelo_final = ExponentialSmoothing(
        serie, trend="add", seasonal="add", seasonal_periods=12
    ).fit()
    pronostico = modelo_final.forecast(HORIZONTE)
    return serie, pronostico, {"mae": float(mae), "rmse": rmse}


def metricas_lstm():
    """Lee el MAE de la LSTM del notebook, si el archivo existe."""
    if not os.path.exists(RUTA_METRICAS_DL):
        return None
    with open(RUTA_METRICAS_DL, encoding="utf-8") as archivo:
        return json.load(archivo)["metricas_modelos"]


def figura_pronostico(serie, pronostico):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=serie.index, y=serie.values, mode="lines+markers",
                             name="Histórico", line=dict(color="#6b4226")))
    fig.add_trace(go.Scatter(x=pronostico.index, y=pronostico.values, mode="lines+markers",
                             name="Pronóstico (Holt-Winters)", line=dict(color="#d4a373", dash="dash")))
    fig.update_layout(
        title="Ventas mensuales y pronóstico a 6 meses",
        title_x=0.5, template="plotly_white", title_font_size=18,
        yaxis_title="Ventas ($)", xaxis_title="Mes",
    )
    return fig


estadistica = resumen_estadistico()
serie_mensual, pronostico_ventas, metricas_hw = pronostico_holt_winters()
metricas_dl = metricas_lstm()
fig_pronostico = figura_pronostico(serie_mensual, pronostico_ventas)
