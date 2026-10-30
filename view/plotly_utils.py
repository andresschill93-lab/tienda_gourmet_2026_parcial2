import plotly.express as px
from data_processing import ganancia_por_categoria

def grafico_interactivo_ganancia():
    print("¡Procesando datos y generando gráfico interactivo en Plotly...!")
    
    # 1. Traemos los datos de las categorías
    data = ganancia_por_categoria()
    
    # 2. Creamos el gráfico de torta interactivo (Pie Chart)
    # Usamos la paleta 'copper' para mantener la misma identidad visual gourmet
   # Cambiamos Copper por copper (en minúscula)
    colores_gourmet = ["#4a2c11", "#6b4226", "#8c5a3c", "#b07d62", "#d4a373"]
    fig = px.pie(
        data, 
        values="Ganancia", 
        names="Categoria", 
        title="Distribución Porcentual de Ganancias por Categoría",
        color_discrete_sequence=colores_gourmet
    )
    
    
    # 3. Mejoramos el diseño (diseño limpio y centrado)
    fig.update_layout(
        title_font_size=18,
        title_x=0.5 # Centra el título en la pantalla
    )
    
    # 4. Guardamos el resultado como un archivo HTML adentro de view
    fig.write_html("view/ganancia_interactiva.html")
    print("¡Archivo HTML guardado con éxito en la carpeta view!")
    
    # 5. Abrimos el gráfico automáticamente en tu navegador web
    fig.show()

if __name__ == "__main__":
    grafico_interactivo_ganancia()