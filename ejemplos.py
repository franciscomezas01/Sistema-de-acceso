import tkinter as tk
from tkinter import ttk

class MiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Usuario")

        self.frame_usuario = tk.Frame(self.root, bg='#FFA07A')
        self.frame_usuario.pack(padx=10, pady=10)

        self.boton_registrar = ttk.Button(self.frame_usuario, text="Registrar", command=self.mostrar_formulario, style='TButton')
        self.boton_registrar.grid(row=0, column=0, pady=10)

    def mostrar_formulario(self):
        # Ocultar el marco de usuario
        self.frame_usuario.pack_forget()

        # Mostrar el formulario
        self.frame_formulario = tk.Frame(self.root, bg='#FFA07A')
        self.frame_formulario.pack(padx=10, pady=10)

        tk.Label(self.frame_formulario, text="Nombre: ", font=('Helvetica', 12), bg='#FFA07A').grid(row=0, column=0)
        ttk.Button(self.frame_formulario, text="Guardar usuario", command=self.limpiar_interfaz, style='TButton').grid(row=1, columnspan=2, sticky=tk.W + tk.E)

    def limpiar_interfaz(self):
        # Limpiar el formulario
        self.frame_formulario.pack_forget()

        # Volver a mostrar el marco de usuario
        self.frame_usuario.pack(padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MiApp(root)
    root.mainloop()
