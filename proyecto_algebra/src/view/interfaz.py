from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargamos la interfaz desde el archivo .kv
Builder.load_file("src/view/kv/interfaz.kv")

class MiInterfaz(BoxLayout):
    def cargar_datos(self):
        try:
            df = pd.read_csv("src/ventas.csv")
            matriz = df.drop("Cliente", axis=1).values
            productos = df.columns[1:]
            totales = np.sum(matriz, axis=0)

            # Graficar productos más vendidos
            plt.bar(productos, totales)
            plt.title("Productos más vendidos")
            plt.xlabel("Producto")
            plt.ylabel("Cantidad")
            plt.show()

        except Exception as e:
            print(f"Error al cargar datos: {e}")