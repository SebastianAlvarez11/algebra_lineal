from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import pandas as pd

Builder.load_file('src/view/kv/mostrar_ventas_screen.kv')

class MostrarVentasScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.df = None

    def on_enter(self):
        self.mostrar_ventas()

    def mostrar_ventas(self):
        layout = self.ids.layout_root
        layout.clear_widgets()

        title = Label(text="VENTAS MENSUALES", font_size=24, size_hint=(1, 0.1), bold=True)
        layout.add_widget(title)

        df = self.cargar_datos_desde_excel("C:/Users/alvar/Desktop/SebasU/PLANTILLA INVENTARIO.xlsx", hoja='VENTAS')

        if df is not None:
            try:
                # Verificar si las columnas necesarias están presentes
                if not set(['COLLARES', 'ARETES', 'TOBILLERAS', 'PULSERAS', 'ANILLOS', 'PRECIO']).issubset(df.columns):
                    layout.add_widget(Label(text="Error: Algunas columnas no están presentes en el archivo."))
                    return

                # Extraer matriz A (COLLARES a ANILLOS)
                A = df[['COLLARES', 'ARETES', 'TOBILLERAS', 'PULSERAS', 'ANILLOS']].to_numpy()

                # Verificar que la columna de precios tenga el número correcto de elementos
                precios = df['PRECIO'].dropna().to_numpy()
                if len(precios) != 5:
                    layout.add_widget(Label(text="Error: El número de precios no coincide con los productos."))
                    return

                # Reshape el vector de precios a una columna de 5x1
                precios = precios.reshape(-1, 1)

                # Calcular totales: t = A @ p
                totales = A @ precios

                # Agregar columna 'TOTAL' al DataFrame
                df['TOTAL'] = totales

                # Crear scroll con tabla
                scroll = ScrollView(size_hint=(1, 0.8))
                grid = GridLayout(cols=2, size_hint_y=None, height=40 * (len(df) + 1))  # Ajustar altura para la fila extra
                grid.bind(minimum_height=grid.setter('height'))

                grid.add_widget(Label(text="Cliente", bold=True))
                grid.add_widget(Label(text="Total", bold=True))

                # Formatear los totales en la columna
                for index, row in df.iterrows():
                    grid.add_widget(Label(text=str(row['CLIENTE'])))  # Cliente
                    total_formateado = f"${row['TOTAL']:,.2f}"  # Formato monetario
                    grid.add_widget(Label(text=total_formateado))  # Total

                # Calcular la suma total de la columna 'TOTAL'
                suma_total = df['TOTAL'].sum()
                suma_total_formateado = f"${suma_total:,.2f}"

                # Agregar la suma total en una nueva fila
                grid.add_widget(Label(text="Suma Total", bold=True))
                grid.add_widget(Label(text=suma_total_formateado, bold=True))

                scroll.add_widget(grid)
                layout.add_widget(scroll)

            except Exception as e:
                layout.add_widget(Label(text=f"Error al calcular: {e}"))

        boton_volver = Button(text="Volver", size_hint=(1, 0.1), 
                              background_normal='',
                              background_down='',
                              background_color=(1, 0.44, 0.26, 1),  # Naranja
                              color=(1, 1, 1, 1),  # Texto blanco
                              font_size=18)
        boton_volver.bind(on_press=self.volver_al_menu)
        layout.add_widget(boton_volver)

    def cargar_datos_desde_excel(self, path, hoja):
        try:
            xls = pd.ExcelFile(path)
            df = pd.read_excel(path, sheet_name=hoja)

            # Normalizar nombres de columnas
            df.columns = df.columns.str.strip().str.upper()
            return df
        except FileNotFoundError:
            print(f"Error: No se encuentra el archivo {path}")
            return None
        except ValueError:
            print(f"Error: La hoja '{hoja}' no existe en el archivo.")
            return None

    def generar_matriz(self, df):
        if df is not None:
            clientes = df['CLIENTE'].values
            productos = df['PRODUCTO'].values
            cantidades = df['CANTIDAD VENDIDA'].values
            return zip(clientes, productos, cantidades)
        else:
            return None
    
    def volver_al_menu(self, *args):
        self.manager.current = "MainScreen"


    

