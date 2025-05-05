from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file("src/view/kv/main_screen.kv")

class MainScreen(Screen):  
    def __init__(self, **kw):
        super().__init__(**kw)

    def abrir_pantalla_mostrar_ventas(self):
        self.manager.current = "MostrarVentasScreen"

    def abrir_pantalla_mostrar_inventario(self):
        self.manager.current = "MostrarInventarioScreen"

    def abrir_pantalla_mostrar_comparacion_gauss(self):
        self.manager.current = "MostrarComparacionGuassJordanScreen"

    def abrir_pantalla_mostrar_comparacion_minimos_cuadrados(self):
        self.manager.current = "MostrarComparacionMinimosCuadradosScreen"

    def salir(self):
        exit()