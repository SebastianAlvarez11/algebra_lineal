from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
import pandas as pd


Builder.load_file('src/view/kv/mostrar_inventario_screen.kv')

class MostrarInventarioScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.df = None

    def on_enter(self):
        self.mostrar_inventario()

    def mostrar_inventario(self):
        layout = self.ids.layout_root
        layout.clear_widgets()

        title = Label(text="INVENTARIO", font_size=24, size_hint=(1, 0.1), bold=True)
        layout.add_widget(title)

        df = self.cargar_datos_desde_excel("C:/Users/alvar/Desktop/SebasU/PLANTILLA INVENTARIO.xlsx")
        tabla = self.generar_matriz(df)

        if tabla is not None:
            # Crear la vista de scroll y grid
            scroll = ScrollView(size_hint=(1, 0.8))
            grid = GridLayout(cols=2, size_hint_y=None, height=40 * (len(tabla) + 1))  # Añadimos una fila más para el total
            grid.bind(minimum_height=grid.setter('height'))

            # Agregar encabezados de la tabla
            grid.add_widget(Label(text="Producto", bold=True, font_size=24))
            grid.add_widget(Label(text="Cantidad", bold=True, font_size=24))

            # Agregar los productos y cantidades a la tabla
            for producto, cantidad in tabla.items():
                grid.add_widget(Label(text=str(producto)))
                grid.add_widget(Label(text=str(cantidad)))

            # Convertir las cantidades a un pandas.Series y manejar NaN
            cantidades_series = pd.Series(tabla.values())
            cantidades_series = pd.to_numeric(cantidades_series, errors='coerce').fillna(0)
            
            # Calcular la suma de las cantidades
            suma_cantidades = cantidades_series.sum()

            # Agregar la fila con el total de la suma de cantidades
            grid.add_widget(Label(text="Total", bold=True, font_size=24))  # A la izquierda "Total"
            grid.add_widget(Label(text=str(suma_cantidades)))  # A la derecha la suma de cantidades

            scroll.add_widget(grid)
            layout.add_widget(scroll)

        # Botón de volver al menú
        boton_volver = Button(text="Volver", size_hint=(1, 0.1), background_normal='',
                              background_down='',
                              background_color=(1, 0.44, 0.26, 1),  # Naranja
                              color=(1, 1, 1, 1),  # Texto blanco
                              font_size=18)
        boton_volver.bind(on_press=self.volver_al_menu)
        layout.add_widget(boton_volver)



    def cargar_datos_desde_excel(self, path):
        try:
            df = pd.read_excel(path, header=9)
            print(df.head())  
            return df
        except FileNotFoundError:
            print(f"Error: No se encuentra el archivo {path}")
            return None

    def generar_matriz(self, df):
        if df is not None:
            productos = df['DETALLE PRODUCTO'].values
            cantidades = df['CANTIDAD'].values
            return dict(zip(productos, cantidades))
        else:
            return None
    
    def volver_al_menu(self, *args):
        self.manager.current = "MainScreen"