from src.gui_inicio import MenuPrincipal
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipal(root)

    def on_closing():
        from src.conexion_mysql import vaciar_puntajes
        vaciar_puntajes()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()