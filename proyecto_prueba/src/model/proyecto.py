import pandas as pd

class Proyecto:
    @staticmethod
    def cargar_datos_desde_excel(path):
        df_bruto = pd.read_excel(path, header=None)

        fila_encabezado = df_bruto[df_bruto.apply(
            lambda row: row.astype(str).str.contains("DETALLE PRODUCTO", case=False).any(),
            axis=1
        )].index[0]

        df = pd.read_excel(path, header=fila_encabezado)
        return df

    @staticmethod
    def generar_matriz(df):
        if "DETALLE PRODUCTO" not in df.columns or "CANTIDAD" not in df.columns:
            return None

        tabla = df.groupby("DETALLE PRODUCTO")["CANTIDAD"].sum()
        return tabla
