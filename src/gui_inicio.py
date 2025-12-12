import tkinter as tk
from .gui_tragamonedas import TragaperrasGUI
from .conexion_mysql import obtener_top_puntajes, vaciar_puntajes


class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("NOMBRE DEL JUEGO")

        # Obtener dimensiones de la pantalla
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Ventana sin bordes y tamaño completo
        self.root.overrideredirect(True)
        self.root.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
        self.root.configure(bg="black")

        # Título del juego
        textmenu = tk.Label(
            self.root,
            text="TRAGAPERRAS",
            bg="black",
            fg="white",
            font=("Arial", 60),
            width=20,
            height=2
        )
        textmenu.place(x=300, y=100)

        # Botones
        iniciar = tk.Button(
            self.root,
            text="Iniciar partida",
            bg="black",
            fg="white",
            font=("Arial", 20),
            command=self.runjuego,
            width=20,
            height=2
        )
        iniciar.place(x=600, y=350)

        puntajes_btn = tk.Button(
            self.root,
            text="Puntajes",
            bg="black",
            fg="white",
            font=("Arial", 20),
            width=20,
            height=2,
            command=self.runpuntajes
        )
        puntajes_btn.place(x=600, y=470)

        salir = tk.Button(
            self.root,
            text="Salir",
            bg="black",
            fg="white",
            font=("Arial", 20),
            command=self.salir_programa,  # ← Cambiado
            width=20,
            height=2
        )
        salir.place(x=600, y=590)

    def salir_programa(self):
        vaciar_puntajes()  # ← Borra los puntajes antes de salir
        self.root.destroy()

    def runjuego(self):
        # Crear una ventana para ingresar el nombre
        entrada = tk.Toplevel(self.root)
        entrada.title("Iniciar Sesión")
        entrada.geometry("400x200")
        entrada.resizable(False, False)
        entrada.transient(self.root)  # Mantiene encima del menú
        entrada.grab_set()  # Bloquea interacción con el fondo

        tk.Label(entrada, text="Ingresa tu nombre:", font=("Arial", 16)).pack(pady=20)
        nombre_entry = tk.Entry(entrada, font=("Arial", 14), justify="center")
        nombre_entry.pack(pady=10)
        nombre_entry.focus()

        def iniciar_juego():
            nombre = nombre_entry.get().strip()
            if nombre:
                entrada.destroy()
                self.root.withdraw()  # ← Oculta el menú (no lo destruye)

                # Abrir nueva ventana para el juego
                juego_ventana = tk.Tk()
                app = TragaperrasGUI(juego_ventana, nombre, self)  # ← Pasamos self
                juego_ventana.mainloop()
                # Nota: el menú se restaurará desde el botón "Menú" en TragaperrasGUI

        tk.Button(
            entrada,
            text="Iniciar",
            font=("Arial", 14),
            bg="#722F37",
            fg="white",
            command=iniciar_juego,
            width=10
        ).pack(pady=10)

        nombre_entry.bind("<Return>", lambda event: iniciar_juego())

    def runpuntajes(self):
        puntos = tk.Toplevel(self.root)
        puntos.title("Puntos")
        puntos.geometry("550x650")  # ← Aumentado
        puntos.resizable(False, False)
        puntos.transient(self.root)
        puntos.grab_set()

        tk.Label(puntos, text="Puntajes Altos", font=("Arial", 24)).pack(pady=20)

        # Obtener y mostrar los puntajes desde MySQL
        puntajes = obtener_puntajes()
        if puntajes:
            for i, (nombre, pts, fecha) in enumerate(puntajes, start=1):
                tk.Label(puntos, text=f"{i}. {nombre}: {pts} pts ({fecha})", font=("Arial", 16)).pack(pady=8)
        else:
            tk.Label(puntos, text="No hay puntajes aún.", font=("Arial", 16)).pack(pady=50)

        tk.Button(puntos, text="Cerrar", command=puntos.destroy, font=("Arial", 14)).pack(pady=20)