import numpy as np
import pandas as pd
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

Builder.load_file('src/view/kv/mostrar_comparacion_gauss_screen.kv')

class MostrarComparacionGaussJordanScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(lambda dt: self.mostrar_comparacion(), 0)

    def mostrar_comparacion(self):
        self.ids.tabla_gj.clear_widgets()
        self.ids.resultado_label.text = ""

        df = self.cargar_datos("C:/Users/alvar/Desktop/SebasU/PLANTILLA INVENTARIO.xlsx", "GAUSS")
        if df is None:
            self.ids.resultado_label.text = "Error al cargar los datos"
            return

        self.mostrar_tabla(df)
        self.resolver_gauss_jordan(df)

    def cargar_datos(self, path, hoja):
        try:
            df = pd.read_excel(path, sheet_name=hoja)
            df.columns = df.columns.str.strip().str.upper()
            return df
        except:
            return None

    def mostrar_tabla(self, df):
        tabla = self.ids.tabla_gj

        encabezados = df.columns
        grid = GridLayout(cols=len(encabezados), size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        for encabezado in encabezados:
            grid.add_widget(Label(text=encabezado, bold=True, size_hint_y=None, height=30, font_size=18))

        for i in range(len(df)):
            for col in encabezados:
                grid.add_widget(Label(text=str(df.loc[i, col]), size_hint_y=None, height=30, font_size=18))

        tabla.add_widget(grid)

    def resolver_gauss_jordan(self, df):
        sistema = []
        columnas_validas = ["VENTAS EMPRESARIALES", "VENTAS PERSONA NATURAL", "VENTAS TOTALES"]

        if not all(col in df.columns for col in columnas_validas):
            self.ids.resultado_label.text = "Columnas incorrectas o faltantes"
            return

        for i in range(len(df)):
            x = df.loc[i, "VENTAS EMPRESARIALES"]
            y = df.loc[i, "VENTAS PERSONA NATURAL"]
            total = df.loc[i, "VENTAS TOTALES"]
            if pd.notna(x) and pd.notna(y) and pd.notna(total):
                sistema.append([x, y, total])

        A = np.array([f[:2] for f in sistema])
        b = np.array([f[2] for f in sistema])

        if A.shape[0] != A.shape[1]:
            min_dim = min(A.shape[0], A.shape[1])
            A = A[:min_dim, :]
            b = b[:min_dim]
            aviso = f"El sistema no era cuadrado. Se usaron las primeras {min_dim} filas.\n"
        else:
            aviso = ""

        try:
            aug = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])
            n = len(b)
            for i in range(n):
                if aug[i][i] == 0:
                    raise ValueError("Pivote cero, no se puede resolver con Gauss-Jordan.")
                aug[i] = aug[i] / aug[i][i]
                for j in range(n):
                    if i != j:
                        aug[j] -= aug[j][i] * aug[i]
            soluciones = aug[:, -1]

            # Mostrar el modelo estimado y el cálculo
            ecuacion = (
                aviso +
                f"Modelo estimado:\n  ventas_totales = {soluciones[0]:.4f} * empresariales + {soluciones[1]:.4f} * naturales\n\n"
            )

            # Cálculo para cada vendedor
            detalles_estimaciones = "Cálculo de ventas estimadas por vendedor:\n"
            for i in range(len(df)):
                nombre = df.loc[i, "VENDEDORES"]
                emp = df.loc[i, "VENTAS EMPRESARIALES"]
                nat = df.loc[i, "VENTAS PERSONA NATURAL"]
                estimada = soluciones[0] * emp + soluciones[1] * nat
                detalles_estimaciones += f"  {nombre}: {soluciones[0]:.4f}*{emp} + {soluciones[1]:.4f}*{nat} = {estimada:.2f}\n"

            # Asegurarse de que el texto es visible, y ajustar el tamaño
            self.ids.resultado_label.font_size = 20  # Aumentar el tamaño de la fuente
            self.ids.resultado_label.text = (
                ecuacion + detalles_estimaciones
            )
            self.ids.resultado_label.height = self.ids.resultado_label.texture_size[1] + 20

        except Exception as e:
            self.ids.resultado_label.text = f"Error al resolver: {e}"

    def volver_al_menu(self):
        self.manager.current = "MainScreen"





