import matplotlib.pyplot as plt
import seaborn as sns
from data_processing import ganancia_por_categoria

def grafico_ganancia_categoria():
    # 1. Traemos los datos desagregados de las categorías
    data = ganancia_por_categoria()
    
    # 2. Configuramos el estilo visual blanco con cuadrícula de Seaborn
    sns.set_theme(style="whitegrid")
    
    # 3. Creamos el lienzo
    plt.figure(figsize=(10, 5))
    
    # 4. Dibujamos el gráfico de barras (barplot)
    # Usamos la paleta "copper" (tonos marrón/tierra) para mantener la estética Gourmet
    sns.barplot(
        x="Categoria", 
        y="Ganancia", 
        data=data, 
        estimator=sum,      # Le ordenamos a Seaborn que sume las ganancias
        errorbar=None,      # Quitamos las barras de error para que quede limpio
        palette="copper"
    )
    
    # 5. Títulos y etiquetas estéticas
    plt.title("Ganancia Total por Categoría de Producto - Tienda Gourmet", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Categoría", fontsize=12)
    plt.ylabel("Ganancia Total ($)", fontsize=12)
    plt.xticks(rotation=15)
    plt.tight_layout()
    
    # 6. Guardamos la foto en view para el PDF del parcial y lo mostramos
    plt.savefig("view/ganancia_por_categoria.png")
    plt.show()

if __name__ == "__main__":
    grafico_ganancia_categoria()