import matplotlib.pyplot as plt
from data_processing import ventas_por_mes

def grafico_ventas_mensuales():
    data = ventas_por_mes()

    plt.figure(figsize=(10, 5))
    plt.plot(data["Anio_Mes"], data["Ventas"], marker="o", color="#6b4226")

    plt.title("Evolución de Ventas Mensuales - Tienda Gourmet")
    plt.xlabel("Mes")
    plt.ylabel("Ventas ($)")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    plt.savefig("view/ventas_mensuales.png")
    plt.show()

if __name__ == "__main__":
    grafico_ventas_mensuales()