import tkinter as tk
import time
import random
from .logica_tragamonedas import generar_tablero, validar_premios, SIMBOLOS, actualizar_multiplicador
from .conexion_mysql import guardar_puntaje


class TragaperrasGUI:
    def __init__(self, root, nombre_usuario, menu_principal=None):
        self.nombre_usuario = nombre_usuario
        self.root = root
        self.menu_principal = menu_principal
        self.root.title("Tragaperras Avanzado 3x5")
        
        # Créditos iniciales y costo por giro
        self.creditos = 50
        self.costo_giro_base = 10
        self.costo_giro = self.costo_giro_base
        self.contador_giros = 0  # Contador para aumentar el costo cada 5 giros

        # Multiplicadores comprados (inicialmente vacío)
        self.multiplicadores_comprados = {"🍋": 2, "🍒": 2, "🍇": 5, "🔔": 5, "⭐": 20, "💎": 20, "💰": 50}

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

        self.creditos_lbl = tk.Label(
            frame_superior,
            text=f"Créditos: {self.creditos}",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#111111"
        )
        self.creditos_lbl.pack(side="left", padx=20, pady=10)

        # Etiqueta para mostrar el costo actual del giro
        self.costo_lbl = tk.Label(
            frame_superior,
            text=f"Costo por giro: {self.costo_giro}",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#111111"
        )
        self.costo_lbl.pack(side="left", padx=20, pady=10)

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

        # === Botón de Tienda ===
        self.boton_tienda = tk.Button(
            self.root,
            text="Tienda",
            font=("Arial", 16, "bold"),
            bg="#06355B",  # Azul brillante
            fg="white",
            activebackground="#042037",  # Azul más oscuro al hacer clic
            activeforeground="white",
            command=self.abrir_tienda,
            width=10,
            height=2,
            relief="raised",
            bd=2
        )
        self.boton_tienda.place(x=20, y=alto_pantalla - 80)  # Ajustado para mayor altura

    def abrir_tienda(self):
        # Ventana emergente de la tienda
        tienda = tk.Toplevel(self.root)
        tienda.title("Tienda")
        tienda.geometry("500x450")
        tienda.configure(bg="#111111")

        tk.Label(
            tienda,
            text="Tienda",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#111111"
        ).pack(pady=10)

        # Lista de símbolos del juego
        simbolos = ["🍋", "🍒", "🍇", "🔔", "⭐", "💎", "💰"]

        for simbolo in simbolos:
            frame_simbolo = tk.Frame(tienda, bg="#111111")
            frame_simbolo.pack(fill="x", padx=20, pady=5)

            tk.Label(
                frame_simbolo,
                text="Multiplicar",
                font=("Arial", 14),
                fg="white",
                bg="#111111"
            ).pack(side="left", padx=(0, 5))

            tk.Label(
                frame_simbolo,
                text=simbolo,
                font=("Arial", 14),
                fg="white",
                bg="#111111"
            ).pack(side="left", padx=(0, 5))

            # Botón de compra
            boton_comprar = tk.Button(
                frame_simbolo,
                text="+",
                font=("Arial", 10),
                bg="#FFD700",
                fg="black",
                width=2,
                height=1
            )
            boton_comprar.pack(side="left", padx=(5, 5))

            # Etiqueta de precio
            precio_lbl = tk.Label(
                frame_simbolo,
                text="Precio: 70",
                font=("Arial", 12),
                fg="white",
                bg="#111111"
            )
            precio_lbl.pack(side="left")

            # Variables para controlar el precio de cada símbolo
            contador = [0]  # Usamos una lista para que sea mutable en el closure

            def comprar(simb=simbolo, cont=contador, lbl=precio_lbl, btn=boton_comprar):
                precio_actual = 70 * (cont[0] + 1)
                if self.creditos < precio_actual:
                    lbl.config(text="❌", fg="red")
                    tienda.after(1000, lambda: lbl.config(text=f"Precio: {70 * (cont[0] + 1)}", fg="white"))
                    return

                self.creditos -= precio_actual
                self.creditos_lbl.config(text=f"Créditos: {self.creditos}")
                cont[0] += 1
                lbl.config(text=f"Precio: {70 * (cont[0] + 1)}", fg="white")
                
                # Duplicar el multiplicador del símbolo
                self.multiplicadores_comprados[simb] *= 2
                actualizar_multiplicador(simb, self.multiplicadores_comprados[simb])

            boton_comprar.config(command=comprar)

    def actualizar_costo_giro(self):
        # Calcular cuántos aumentos de 20% se deben aplicar
        aumentos = self.contador_giros // 5
        self.costo_giro = int(self.costo_giro_base * (1.2 ** aumentos))
        self.costo_lbl.config(text=f"Costo por giro: {self.costo_giro}")

    def volver_menu(self):
        # Guardar puntaje antes de volver al menú
        guardar_puntaje(self.nombre_usuario, self.creditos)
        self.root.destroy()
        if self.menu_principal:
            self.menu_principal.root.deiconify()

    def guardar_y_salir(self):
        # Esta función se llama al intentar cerrar la ventana
        guardar_puntaje(self.nombre_usuario, self.creditos)
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
        # ✅ Actualizar el costo por giro si corresponde
        self.actualizar_costo_giro()

        # ✅ Verificar si hay suficientes créditos
        if self.creditos < self.costo_giro:
            self.mensaje_lbl.config(text="❌ No tienes suficientes créditos para girar.", fg="red")
            return

        # ✅ Descontar el costo del giro
        self.creditos -= self.costo_giro
        self.creditos_lbl.config(text=f"Créditos: {self.creditos}")

        # ✅ Incrementar contador de giros
        self.contador_giros += 1

        # ✅ Deshabilitar el botón para evitar múltiples giros
        self.boton.config(state="disabled", text="Girando...", bg="#3a0a0a")
        self.root.update()  # Asegurar que el cambio se muestre

        try:
            self.animacion()
            self.matriz = generar_tablero()
            for i in range(3):
                for j in range(5):
                    simbolo = self.matriz[i][j]
                    self.canvas.itemconfig(self.textos[i][j], text=simbolo)

            premios = validar_premios(self.matriz)
            puntaje_ronda = sum(p["pago_base"] for p in premios)

            # ✅ Sumar premio a créditos si hay premios
            if premios:
                self.creditos += puntaje_ronda
                self.creditos_lbl.config(text=f"Créditos: {self.creditos}")

            # Actualizar interfaz
            self.puntaje_lbl.config(text=f"Este giro: {puntaje_ronda}")

            if premios:
                self.resaltar_celdas_ganadoras(premios)
                
                lineas_premios = []
                for p in premios:
                    simb = p["simbolo"]
                    cnt = p["conteo"]
                    pago = p["pago_base"]
                    lineas_premios.append(f"{cnt} {simb} → +{pago}")
                
                grupos = []
                for i in range(0, len(lineas_premios), 4):
                    grupos.append(lineas_premios[i:i+4])
                
                lineas_formateadas = ["    ".join(grupo) for grupo in grupos]
                mensaje = "🎉 ¡Premios!\n" + "\n".join(lineas_formateadas)
                
                self.mensaje_lbl.config(text=mensaje, fg="#FFD700")
            else:
                # Restaurar bordes si no hay premios
                for i in range(3):
                    for j in range(5):
                        self.canvas.itemconfig(self.rectangulos[i][j], outline="black", width=2)
                self.mensaje_lbl.config(text="🚫 No hubo premios esta vez.", fg="red")

        finally:
            # ✅ Siempre reactivar el botón al final
            self.boton.config(state="normal", text="Girar", bg="#570C0C")