import pandas as pd
from sources.ventas_csv import cargar_desde_csv


df = cargar_desde_csv()


df = df.drop_duplicates()
df = df.dropna()


df["Fecha_Pedido"] = pd.to_datetime(df["Fecha_Pedido"])


df["Anio"] = df["Fecha_Pedido"].dt.year
df["Mes"] = df["Fecha_Pedido"].dt.month
df["Anio_Mes"] = df["Fecha_Pedido"].dt.to_period("M").astype(str)
df["Margen_Pct"] = (df["Ganancia"] / df["Ventas"] * 100).round(2)


def ventas_por_mes():
    return df.groupby("Anio_Mes", as_index=False)["Ventas"].sum()

def ganancia_por_categoria():
    return df[["Categoria", "Ganancia"]]

def ventas_por_region(anio=None):
    data = df
    if anio is not None:
        data = data[data["Anio"] == anio]
    return data.groupby("Region", as_index=False)["Ventas"].sum()


if __name__ == "__main__":
    print(df.head())
    print(f"\nFilas: {len(df)}")
    print(f"Columnas nuevas: Anio, Mes, Anio_Mes, Margen_Pct")