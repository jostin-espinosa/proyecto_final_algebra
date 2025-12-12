import tkinter as tk
import time
import random
from .logica_tragamonedas import generar_tablero, validar_premios, SIMBOLOS
from .conexion_mysql import guardar_puntaje


class TragaperrasGUI:
    def __init__(self, root, nombre_usuario, menu_principal=None):
        self.nombre_usuario = nombre_usuario
        self.root = root
        self.menu_principal = menu_principal
        self.root.title("Tragaperras Avanzado 3x5")

        # Pantalla completa sin bordes
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        self.root.overrideredirect(True)
        self.root.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
        self.root.configure(bg="black")

        # Asociar evento de cierre para guardar puntaje
        self.root.protocol("WM_DELETE_WINDOW", self.guardar_y_salir)

        # === Barra superior ===
        frame_superior = tk.Frame(self.root, bg="#111111", height=60)
        frame_superior.pack(fill="x")
        frame_superior.pack_propagate(False)

        tk.Label(
            frame_superior,
            text=f"Usuario: {self.nombre_usuario}",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#111111"
        ).pack(side="left", padx=20, pady=10)

        self.puntos_acumulados = 0
        self.puntos_lbl = tk.Label(
            frame_superior,
            text=f"Puntos acumulados: {self.puntos_acumulados}",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#111111"
        )
        self.puntos_lbl.pack(side="left", padx=20, pady=10)

        tk.Button(
            frame_superior,
            text="← Menú",
            font=("Arial", 14),
            bg="#570C0C",
            fg="white",
            command=self.volver_menu,
            relief="flat",
            padx=10
        ).pack(side="right", padx=20, pady=10)

        # === Área del juego ===
        frame_principal = tk.Frame(self.root, bg="black")
        frame_principal.place(relx=0.5, rely=0.5, anchor="center")

        frame_central = tk.Frame(frame_principal, bg="black")
        frame_central.pack()

        self.canvas = tk.Canvas(frame_central, bg="black", width=700, height=400, highlightthickness=0)
        self.canvas.pack(pady=10)

        self.celda_ancho = 120
        self.celda_alto = 120
        self.margen = 10

        # Dibujar celdas y guardar referencias
        self.rectangulos = []
        self.posiciones = []
        self.textos = []

        for i in range(3):
            fila_rects = []
            fila_pos = []
            fila_textos = []
            for j in range(5):
                x = j * (self.celda_ancho + self.margen) + self.margen
                y = i * (self.celda_alto + self.margen) + self.margen

                rect_id = self.canvas.create_rectangle(
                    x, y,
                    x + self.celda_ancho, y + self.celda_alto,
                    fill="white",
                    outline="black",
                    width=2
                )
                texto_id = self.canvas.create_text(
                    x + self.celda_ancho // 2,
                    y + self.celda_alto // 2,
                    text="?",
                    font=("Arial", 36, "bold"),
                    fill="black"
                )

                fila_rects.append(rect_id)
                fila_pos.append((x, y))
                fila_textos.append(texto_id)

            self.rectangulos.append(fila_rects)
            self.posiciones.append(fila_pos)
            self.textos.append(fila_textos)

        # === Controles inferiores ===
        frame_controles = tk.Frame(frame_central, bg="black")
        frame_controles.pack(pady=10)

        self.boton = tk.Button(
            frame_controles,
            text="Girar",
            font=("Arial", 20, "bold"),
            bg="#570C0C",
            fg="white",
            activebackground="#722F37",
            activeforeground="white",
            command=self.girar,
            width=8,
            height=1,
            relief="raised",
            bd=2
        )
        self.boton.pack(pady=5)

        self.puntaje_lbl = tk.Label(
            frame_controles,
            text="Este giro: 0",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="black"
        )
        self.puntaje_lbl.pack(pady=5)

        self.mensaje_lbl = tk.Label(
            frame_controles,
            text="",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="black",
            wraplength=650,
            justify="center"
        )
        self.mensaje_lbl.pack(pady=5)

    def volver_menu(self):
        # Guardar puntaje antes de volver al menú
        guardar_puntaje(self.nombre_usuario, self.puntos_acumulados)
        self.root.destroy()
        if self.menu_principal:
            self.menu_principal.root.deiconify()

    def guardar_y_salir(self):
        # Esta función se llama al intentar cerrar la ventana
        guardar_puntaje(self.nombre_usuario, self.puntos_acumulados)
        self.root.destroy()
        if self.menu_principal:
            self.menu_principal.root.deiconify()

    def resaltar_celdas_ganadoras(self, lista_premios):
        # Restaurar bordes a negro
        for i in range(3):
            for j in range(5):
                self.canvas.itemconfig(self.rectangulos[i][j], outline="black", width=2)

        # Resaltar celdas ganadoras con dorado
        celdas_ganadoras = set()
        for premio in lista_premios:
            for (fila, col) in premio.get("coordenadas", []):
                if 0 <= fila < 3 and 0 <= col < 5:
                    celdas_ganadoras.add((fila, col))

        for (fila, col) in celdas_ganadoras:
            self.canvas.itemconfig(
                self.rectangulos[fila][col],
                outline="#FFD700",  # Dorado brillante
                width=4
            )

    def animacion(self):
        for _ in range(10):
            for i in range(3):
                for j in range(5):
                    simbolo = random.choice(SIMBOLOS)
                    self.canvas.itemconfig(self.textos[i][j], text=simbolo)
            self.root.update()
            time.sleep(0.1)

    def girar(self):
        self.animacion()
        self.matriz = generar_tablero()
        for i in range(3):
            for j in range(5):
                simbolo = self.matriz[i][j]
                self.canvas.itemconfig(self.textos[i][j], text=simbolo)

        premios = validar_premios(self.matriz)
        puntaje_ronda = sum(p["pago_base"] for p in premios)
        self.puntos_acumulados += puntaje_ronda

        # Actualizar interfaz
        self.puntos_lbl.config(text=f"Puntos acumulados: {self.puntos_acumulados}")
        self.puntaje_lbl.config(text=f"Este giro: {puntaje_ronda}")

        if premios:
            self.resaltar_celdas_ganadoras(premios)

            # Crear lista de premios como texto
            lineas_premios = []
            for p in premios:
                simb = p["simbolo"]
                cnt = p["conteo"]
                pago = p["pago_base"]
                lineas_premios.append(f"{cnt} {simb} → +{pago}")

            # Dividir en grupos de 4 para columnas
            grupos = []
            for i in range(0, len(lineas_premios), 4):
                grupos.append(lineas_premios[i:i+4])

            # Unir cada grupo con espacios amplios
            lineas_formateadas = ["    ".join(grupo) for grupo in grupos]
            mensaje = "🎉 ¡Premios!\n" + "\n".join(lineas_formateadas)

            self.mensaje_lbl.config(text=mensaje, fg="#FFD700")
        else:
            # Restaurar bordes si no hay premios
            for i in range(3):
                for j in range(5):
                    self.canvas.itemconfig(self.rectangulos[i][j], outline="black", width=2)
            self.mensaje_lbl.config(text="🚫 No hubo premios esta vez.", fg="red")