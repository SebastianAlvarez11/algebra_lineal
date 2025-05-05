import numpy as np
import pandas as pd
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.label import Label
import matplotlib.pyplot as plt
import os

Builder.load_file('src/view/kv/mostrar_comparacion_minimos_cuadrados_screen.kv')

class MostrarComparacionMinimosCuadradosScreen(Screen):
    def on_enter(self):
        self.mostrar_comparacion()

    def mostrar_comparacion(self):
        layout = self.ids.layout_root_mc
        layout.clear_widgets()

        df = self.cargar_datos("C:/Users/alvar/Desktop/SebasU/PLANTILLA INVENTARIO.xlsx", "COMPARACION")
        if df is None:
            self.ids.resultado_label_mc.text = "No se pudo cargar el archivo."
            return

        self.mostrar_tabla(layout, df)
        self.resolver_minimos_cuadrados(df)

    def cargar_datos(self, path, hoja):
        try:
            df = pd.read_excel(path, sheet_name=hoja)
            df.columns = df.columns.str.strip().str.upper()
            return df
        except:
            return None


    def mostrar_tabla(self, layout, df):
        layout.clear_widgets()

        for encabezado in ["PRODUCTO", "VENTAS TOTALES", "VENTAS WHATSAPP", "VENTAS FERIA"]:
            layout.add_widget(self.crear_label(encabezado))

        for i, producto in enumerate(df["PRODUCTO"]):
            layout.add_widget(self.crear_label(producto))
            layout.add_widget(self.crear_label(df.loc[i, "VENTAS TOTALES"]))
            layout.add_widget(self.crear_label(df.loc[i, "VENTAS WHATSAPP"]))
            layout.add_widget(self.crear_label(df.loc[i, "VENTAS FERIA"]))

    def crear_label(self, texto):
        return Label(
            text=str(texto),
            font_size=16,
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=40,
            text_size=(None, None),
        )

    def resolver_minimos_cuadrados(self, df):
        sistema = []
        nombres_productos = []

        for i in range(len(df)):
            x = df.loc[i, "VENTAS WHATSAPP"]
            y = df.loc[i, "VENTAS FERIA"]
            total = df.loc[i, "VENTAS TOTALES"]
            producto = df.loc[i, "PRODUCTO"]
            if pd.notna(x) and pd.notna(y) and pd.notna(total):
                sistema.append([x, y, total])
                nombres_productos.append(producto)

        A = np.array([f[:2] for f in sistema])
        b = np.array([f[2] for f in sistema])

        try:
            coef, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
            estimado = A @ coef

            resultado = f"[b]Resultado:[/b]\nWhatsApp = {coef[0]:.2f}\nFeria = {coef[1]:.2f}"
            procedimiento = f"[b]Procedimiento:[/b]\nA = {A.tolist()}\nb = {b.tolist()}"
            self.ids.resultado_label_mc.text = resultado + "\n\n" + procedimiento

            # --- GRAFICAR ---
            plt.figure(figsize=(10, 5))
            plt.plot(nombres_productos, b, marker='o', color='orange', label='Ventas Reales')
            plt.plot(nombres_productos, estimado, linestyle='--', marker='x', color='orangered', label='Ventas Estimadas')
            plt.title("Comparación de Ventas Reales vs Estimadas por Producto")
            plt.xlabel("Producto")
            plt.ylabel("Ventas Totales")
            plt.legend()
            plt.tight_layout()

            # Ruta donde guardar la imagen (asegúrate de tener esta carpeta creada)
            ruta_imagen = "src/view/graficas/comparacion_mc.png"
            os.makedirs(os.path.dirname(ruta_imagen), exist_ok=True)
            plt.savefig(ruta_imagen)
            plt.close()

            # Mostrar imagen en la interfaz
            self.ids.imagen_comparacion_mc.source = ruta_imagen
            self.ids.imagen_comparacion_mc.reload()

        except Exception as e:
            self.ids.resultado_label_mc.text = f"Error: {e}"


    def volver_al_menu(self):
        self.manager.current = "MainScreen"