from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from src.view.mostrar_inventario_screen import MostrarInventarioScreen
from src.view.main_screen import MainScreen
from src.view.mostrar_ventas_screen import MostrarVentasScreen
from src.view.mostrar_comparacion_gauss_screen import MostrarComparacionGaussJordanScreen
from src.view.mostrar_comparacion_minimos_cuadrados_screen import MostrarComparacionMinimosCuadradosScreen


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(MainScreen(name="MainScreen"))
        screen_manager.add_widget(MostrarInventarioScreen(name="MostrarInventarioScreen"))
        screen_manager.add_widget(MostrarVentasScreen(name="MostrarVentasScreen"))
        screen_manager.add_widget(MostrarComparacionGaussJordanScreen(name="MostrarComparacionGuassJordanScreen"))
        screen_manager.add_widget(MostrarComparacionMinimosCuadradosScreen(name="MostrarComparacionMinimosCuadradosScreen"))

        return screen_manager



