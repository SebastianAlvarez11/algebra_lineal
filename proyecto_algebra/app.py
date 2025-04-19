from src.view.interfaz import MiInterfaz

class App(App):
    def build(self):
        return MiInterfaz()

if __name__ == '__main__':
    App().run()