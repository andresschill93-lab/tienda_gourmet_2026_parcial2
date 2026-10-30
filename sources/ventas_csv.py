import pandas as pd

def cargar_desde_csv():
    df = pd.read_csv("data/ventas_gourmet.csv")
    return df


if __name__ == "__main__":
    df = cargar_desde_csv()
    print(df.head())
    print(f"\nFilas: {len(df)}")
    print(f"Columnas: {list(df.columns)}")