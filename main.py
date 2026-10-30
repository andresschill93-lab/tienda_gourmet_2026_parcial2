import dash
from dash import dcc, html
import plotly.express as px
from data_processing import ganancia_por_categoria
from backend_analisis import estadistica, fig_pronostico, metricas_hw, metricas_dl

# Importamos las funciones para asegurarnos de que generen las imágenes al arrancar
from view.matplotlib_utils import grafico_ventas_mensuales
from view.seaborn_utils import grafico_ganancia_categoria

import base64

# Función auxiliar para que Dash pueda leer imágenes locales .png
def codificar_imagen(ruta_imagen):
    try:
        with open(ruta_imagen, "rb") as image_file:
            return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"
    except:
        return ""

# 1. Forzamos a que se generen y actualicen las imágenes en la carpeta view
grafico_ventas_mensuales()
grafico_ganancia_categoria()

# 2. Inicializamos la aplicación de Dash
app = dash.Dash(__name__)
app.title = "Dashboard Tienda Gourmet"

# Codificamos las imágenes estáticas para la web
img_matplotlib = codificar_imagen("view/ventas_mensuales.png")
img_seaborn = codificar_imagen("view/ganancia_por_categoria.png")

# Gráfico interactivo de Plotly
df_categorias = ganancia_por_categoria()
colores_gourmet = ["#4a2c11", "#6b4226", "#8c5a3c", "#b07d62", "#d4a373"]
fig_plotly = px.pie(
    df_categorias, 
    values="Ganancia", 
    names="Categoria", 
    title="Rentabilidad y Ganancia por Rubro de Producto (Interactivo)",
    color_discrete_sequence=colores_gourmet
)
fig_plotly.update_layout(title_x=0.5, template="plotly_white", title_font_size=18)

# 3. Diseño de la Interfaz Web Completa
app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#f8f9fa", "padding": "20px"},
    children=[
        
        # Encabezado Principal
        html.Div(
            style={"textAlign": "center", "backgroundColor": "#4a2c11", "padding": "25px", "borderRadius": "8px", "color": "white", "marginBottom": "25px"},
            children=[
                html.H1("Panel de Control - Tienda Gourmet", style={"margin": "0"}),
                html.P("Sistema Integral para la Toma de Decisiones Estratégicas", style={"margin": "10px 0 0 0", "opacity": "0.8"})
            ]
        ),
        
        # CONTENEDOR DE GRÁFICOS ESTÁTICOS (Matplotlib y Seaborn uno al lado del otro)
        html.Div(
            style={"display": "flex", "justifyContent": "space-between", "marginBottom": "25px"},
            children=[
                # Tarjeta Matplotlib
                html.Div(
                    style={"backgroundColor": "white", "padding": "15px", "borderRadius": "8px", "boxShadow": "0px 2px 4px rgba(0,0,0,0.05)", "width": "48%"},
                    children=[
                        html.H4("Tendencia Temporal (Matplotlib)", style={"color": "#6b4226", "marginTop": "0"}),
                        html.Img(src=img_matplotlib, style={"width": "100%", "borderRadius": "4px"})
                    ]
                ),
                # Tarjeta Seaborn
                html.Div(
                    style={"backgroundColor": "white", "padding": "15px", "borderRadius": "8px", "boxShadow": "0px 2px 4px rgba(0,0,0,0.05)", "width": "48%"},
                    children=[
                        html.H4("Análisis de Rendimiento (Seaborn)", style={"color": "#6b4226", "marginTop": "0"}),
                        html.Img(src=img_seaborn, style={"width": "100%", "borderRadius": "4px"})
                    ]
                ),
            ]
        ),
        
        # CONTENEDOR DEL GRÁFICO INTERACTIVO (Plotly abajo ocupando el ancho completo)
        html.Div(
            style={"backgroundColor": "white", "padding": "20px", "borderRadius": "8px", "boxShadow": "0px 2px 4px rgba(0,0,0,0.05)", "marginBottom": "25px"},
            children=[
                dcc.Graph(id="grafico-torta-gourmet", figure=fig_plotly)
            ]
        ),

        # ANÁLISIS (backend): estadística y pronóstico
        html.H2("Análisis y pronóstico (backend)", style={"color": "#4a2c11"}),

        html.Div(
            style={"display": "flex", "gap": "15px", "marginBottom": "25px", "flexWrap": "wrap"},
            children=[
                html.Div(
                    style={"backgroundColor": "white", "padding": "15px", "borderRadius": "8px", "flex": "1", "minWidth": "180px"},
                    children=[
                        html.P("Venta promedio por pedido", style={"margin": "0", "color": "#6b4226"}),
                        html.H3(f"$ {estadistica['venta_promedio']:,.0f}", style={"margin": "5px 0 0 0", "color": "#4a2c11"}),
                    ]
                ),
                html.Div(
                    style={"backgroundColor": "white", "padding": "15px", "borderRadius": "8px", "flex": "1", "minWidth": "180px"},
                    children=[
                        html.P("IC 95% de la venta promedio", style={"margin": "0", "color": "#6b4226"}),
                        html.H3(f"$ {estadistica['ic95'][0]:,.0f} - $ {estadistica['ic95'][1]:,.0f}",
                                style={"margin": "5px 0 0 0", "color": "#4a2c11", "fontSize": "18px"}),
                    ]
                ),
                html.Div(
                    style={"backgroundColor": "white", "padding": "15px", "borderRadius": "8px", "flex": "1", "minWidth": "180px"},
                    children=[
                        html.P("Error del pronóstico (MAE Holt-Winters)", style={"margin": "0", "color": "#6b4226"}),
                        html.H3(f"$ {metricas_hw['mae']:,.0f}", style={"margin": "5px 0 0 0", "color": "#4a2c11"}),
                    ]
                ),
                html.Div(
                    style={"backgroundColor": "white", "padding": "15px", "borderRadius": "8px", "flex": "1", "minWidth": "180px"},
                    children=[
                        html.P("Error del modelo LSTM (MAE)", style={"margin": "0", "color": "#6b4226"}),
                        html.H3(
                            f"$ {metricas_dl['mae_lstm']:,.0f}" if metricas_dl else "Sin datos",
                            style={"margin": "5px 0 0 0", "color": "#4a2c11"},
                        ),
                    ]
                ),
            ]
        ),

        html.Div(
            style={"backgroundColor": "white", "padding": "20px", "borderRadius": "8px", "boxShadow": "0px 2px 4px rgba(0,0,0,0.05)", "marginBottom": "25px"},
            children=[
                html.P(
                    f"Asimetría de las ventas: {estadistica['asimetria']:.2f}. "
                    f"ANOVA del margen entre categorías: p = {estadistica['anova_p']:.4f}. "
                    f"Correlación descuento vs. margen: r = {estadistica['corr_descuento_margen']:.3f}.",
                    style={"color": "#4a2c11"},
                ),
                dcc.Graph(id="grafico-pronostico-gourmet", figure=fig_pronostico),
            ]
        ),
    ]
)

def main():
    print("=== SERVIDOR DASH COMPLETO ENCENDIDO ===")
    print("Entrá a: http://127.0.0.1:8050/")
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    main()