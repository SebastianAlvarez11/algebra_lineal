import pandas as pd

# Ruta del archivo
archivo = "C:/Users/alvar/Desktop/SebasU/PLANTILLA INVENTARIO.xlsx"

# Leer todo el archivo sin asumir encabezados
df_bruto = pd.read_excel(archivo, header=None)

# Buscar la primera fila que tenga la palabra "VENTAS" para usarla como encabezado
fila_encabezado = df_bruto[df_bruto.apply(lambda row: row.astype(str).str.contains("VENTAS", case=False).any(), axis=1)].index[0] - 1

# Volver a leer el archivo, esta vez usando esa fila como encabezado
df = pd.read_excel(archivo, header=fila_encabezado)

# Mostrar las primeras filas
print(df.head())

class Proyecto:
    pass


