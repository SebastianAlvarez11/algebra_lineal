from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
import pandas as pd


Builder.load_file('src/view/kv/interfaz.kv')

class MyApp(App):
    def build(self):
        df = self.cargar_datos_desde_excel("C:/Users/alvar/Desktop/SebasU/PLANTILLA INVENTARIO.xlsx")
        tabla = self.generar_matriz(df)
        
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        title = Label(text="INVENTARIO", font_size=24, size_hint=(1, 0.1), bold=True)
        layout.add_widget(title)

        if tabla is not None:
            scroll = ScrollView(size_hint=(1, 0.7)) 
            grid = GridLayout(cols=2, size_hint_y=None, height=40*len(tabla)) 
            grid.bind(minimum_height=grid.setter('height'))

            grid.add_widget(Label(text="Producto", bold=True))
            grid.add_widget(Label(text="Cantidad", bold=True))

            for producto, cantidad in tabla.items():
                grid.add_widget(Label(text=str(producto) if producto is not None else "Producto Desconocido"))
                grid.add_widget(Label(text=str(cantidad) if cantidad is not None else "0"))

            scroll.add_widget(grid)
            layout.add_widget(scroll)

        boton_cerrar = Button(text="Cerrar", size_hint=(1, 0.1), on_press=self.stop)
        layout.add_widget(boton_cerrar)

        return layout

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