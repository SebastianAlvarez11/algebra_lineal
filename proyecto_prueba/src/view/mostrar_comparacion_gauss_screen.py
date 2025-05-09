import numpy as np
import pandas as pd
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty

Builder.load_file('src/view/kv/mostrar_comparacion_gauss_screen.kv')

class MostrarComparacionGaussJordanScreen(Screen):
    resultado_text = StringProperty("")
    procedimiento_text = StringProperty("")
    
    def on_enter(self):
        Clock.schedule_once(lambda dt: self.mostrar_comparacion(), 0)

    def mostrar_comparacion(self):
        self.ids.tabla_gj.clear_widgets()
        self.resultado_text = ""
        self.procedimiento_text = ""

        df = self.cargar_datos("C:/Users/alvar/Desktop/SebasU/PLANTILLA INVENTARIO.xlsx", "GAUSS")
        if df is None:
            self.resultado_text = "Error al cargar los datos"
            return

        self.mostrar_tabla(df)
        self.resolver_gauss_jordan(df)

    def cargar_datos(self, path, hoja):
        try:
            df = pd.read_excel(path, sheet_name=hoja)
            df.columns = df.columns.str.strip().str.upper()
            return df
        except Exception as e:
            self.resultado_text = f"Error al cargar los datos: {e}"
            return None

    def mostrar_tabla(self, df):
        tabla = self.ids.tabla_gj
        tabla.clear_widgets()
        encabezados = df.columns
        
        grid = GridLayout(cols=len(encabezados), size_hint_y=None, spacing=dp(5), 
                         padding=dp(10), row_default_height=dp(30))
        grid.bind(minimum_height=grid.setter('height'))

        for encabezado in encabezados:
            grid.add_widget(Label(
                text=encabezado, 
                bold=True, 
                font_size=dp(16),
                color=(0.9, 0.9, 0.9, 1),
                size_hint_y=None, 
                height=dp(30)
            ))

        for i in range(len(df)):
            for col in encabezados:
                grid.add_widget(Label(
                    text=str(df.loc[i, col]), 
                    font_size=dp(14),
                    color=(0.8, 0.8, 0.8, 1),
                    size_hint_y=None, 
                    height=dp(30)
                ))

        tabla.add_widget(grid)

    def resolver_gauss_jordan(self, df):
        columnas = ["VENTAS EMPRESARIALES", "VENTAS PERSONA NATURAL", "VENTAS TOTALES"]
        if not all(col in df.columns for col in columnas):
            self.resultado_text = "Columnas incorrectas o faltantes"
            return

        sistema = []
        for i in range(len(df)):
            x = df.loc[i, "VENTAS EMPRESARIALES"]
            y = df.loc[i, "VENTAS PERSONA NATURAL"]
            total = df.loc[i, "VENTAS TOTALES"]
            if pd.notna(x) and pd.notna(y) and pd.notna(total):
                sistema.append([x, y, total])

        A = np.array([fila[:2] for fila in sistema], dtype=float)
        b = np.array([fila[2] for fila in sistema], dtype=float)

        # Inicializamos el texto del procedimiento
        proc_text = "[b]PROCEDIMIENTO GAUSS-JORDAN[/b]\n\n"
        proc_text += f"Matriz A:\n{A}\n\nVector b:\n{b}\n\n"
        proc_text += f"Matriz Aumentada (antes de Gauss-Jordan):\n{np.hstack((A, b.reshape(-1, 1)))}\n\n"

        try:
            aug = np.hstack((A, b.reshape(-1, 1)))
            n = len(b)
            
            for i in range(n):
                pivote = aug[i][i]
                
                proc_text += f"\n[b]Paso {i+1}:[/b] Normalización de la fila {i} (pivote = {pivote:.4f})\n"
                aug[i] = aug[i] / pivote
                proc_text += f"{aug}\n\n"
                
                proc_text += f"Eliminación en otras filas:\n"
                for j in range(n):
                    if i != j:
                        factor = aug[j][i]
                        aug[j] -= factor * aug[i]
                        proc_text += f"Fila {j} -= {factor:.4f} * Fila {i}\n"
                proc_text += f"Resultado:\n{aug}\n\n"

            soluciones = aug[:, -1]
            a, b = soluciones

            # Resultados finales
            self.resultado_text = f"[b]Modelo estimado por Gauss-Jordan:[/b]\n"
            self.resultado_text += f"ventas_totales = [color=00FF00]{a:.4f}[/color] * empresariales + [color=00FF00]{b:.4f}[/color] * naturales\n\n"
            
            self.resultado_text += "[b]Cálculo por vendedor:[/b]\n"
            for i in range(len(df)):
                nombre = df.loc[i, "VENDEDORES"]
                emp = df.loc[i, "VENTAS EMPRESARIALES"]
                nat = df.loc[i, "VENTAS PERSONA NATURAL"]
                total = a * emp + b * nat
                self.resultado_text += f"  {nombre}: {a:.4f} * {emp} + {b:.4f} * {nat} = [color=FFFF00]{total:.2f}[/color]\n"

            # Asignamos el procedimiento completo
            self.procedimiento_text = proc_text

        except Exception as e:
            self.resultado_text = f"[color=FF0000]Error al resolver con Gauss-Jordan: {e}[/color]"

    def volver_al_menu(self):
        self.manager.current = "MainScreen"











