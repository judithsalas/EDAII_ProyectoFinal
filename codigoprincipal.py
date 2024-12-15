import csv
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import requests

# Leer datos de la base de datos CSV
def leer_base_datos(nombre_archivo):
    try:
        productos = []
        with open(nombre_archivo, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                fila["precio"] = float(fila["precio"].replace("€", "").strip())  # Convertir precio a float
                fila["puntuacion"] = float(fila["puntuacion"])  # Convertir puntuación a float
                productos.append(fila)
        return productos
    except FileNotFoundError:
        messagebox.showerror("Error", f"El archivo '{nombre_archivo}' no se encontró.")
        return []
    except Exception as e:
        messagebox.showerror("Error", f"Error al leer el archivo: {e}")
        return []

# Programación Dinámica para seleccionar productos según presupuesto
def mochila(productos, presupuesto):
    """
    Resuelve el problema de la mochila para maximizar la puntuación total dentro del presupuesto.
    """
    n = len(productos)
    presupuesto_entero = int(presupuesto)  # Asegurarse de trabajar con valores enteros para la matriz
    dp = [[0] * (presupuesto_entero + 1) for _ in range(n + 1)]

    # Rellenar la tabla DP
    for i in range(1, n + 1):
        for w in range(presupuesto_entero + 1):
            if productos[i - 1]["precio"] <= w:
                dp[i][w] = max(dp[i - 1][w], 
                               dp[i - 1][w - int(productos[i - 1]["precio"])] + productos[i - 1]["puntuacion"])
            else:
                dp[i][w] = dp[i - 1][w]

    # Reconstruir la combinación óptima
    w = presupuesto_entero
    combinacion_optima = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            combinacion_optima.append(productos[i - 1])
            w -= int(productos[i - 1]["precio"])

    return combinacion_optima, dp[n][presupuesto_entero]

# Mostrar el grafo organizado con imágenes y etiquetas
def mostrar_grafo_con_datos(G, nodo_central):
    fig, ax = plt.subplots(figsize=(14, 14))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=False, node_size=0, edge_color='gray', width=2.0, ax=ax)

    def dividir_nombre(nombre, max_caracteres=25):
        """Divide el nombre largo en varias líneas."""
        return "\n".join([nombre[i:i + max_caracteres] for i in range(0, len(nombre), max_caracteres)])

    def on_click(event):
        """Abre la URL al hacer clic en una imagen."""
        x, y = event.xdata, event.ydata
        if x is None or y is None:
            return
        for nodo, (xn, yn) in pos.items():
            if abs(x - xn) < 0.05 and abs(y - yn) < 0.05:
                url = G.nodes[nodo].get("pagina")
                if url:
                    webbrowser.open(url)
                break

    fig.canvas.mpl_connect("button_press_event", on_click)

    for nodo, (x, y) in pos.items():
        node_data = G.nodes[nodo]
        if nodo == nodo_central:
            ax.text(x, y, nodo_central, color="white", fontsize=12, fontweight='bold', ha='center', va='center',
                    bbox=dict(facecolor='#4CAF50', edgecolor='black', boxstyle='circle'))
        else:
            try:
                response = requests.get(node_data['imagen'])
                img = Image.open(BytesIO(response.content)).resize((80, 80))
            except:
                img = Image.new("RGB", (80, 80), color="lightgray")

            imagebox = OffsetImage(img, zoom=0.5)
            ab = AnnotationBbox(imagebox, (x, y), frameon=False)
            ax.add_artist(ab)

            nombre_dividido = dividir_nombre(nodo)
            label = f"{nombre_dividido}\n{node_data['precio']} € | {node_data['puntuacion']} *"
            ax.text(x, y - 0.1, label, fontsize=8, ha='center', va='top', color='#333333')

    plt.axis("off")
    plt.tight_layout()
    plt.show()

# Ventana principal
def abrir_ventana_principal(tipo_piel=None):
    productos = leer_base_datos("productos_skincare.csv")
    ventana = tk.Tk()
    ventana.title("Selecciona tus preferencias")
    ventana.geometry("600x800")

    tipo_piel_var = tk.StringVar(value=tipo_piel)  # Variable para tipo de piel seleccionada
    rutina_var = tk.StringVar(value="Simple")
    categoria_var = tk.StringVar()
    alergenos_var = tk.StringVar()

    # Obtener todas las categorías y alérgenos únicos
    categorias = sorted(set(p["tipo"] for p in productos))
    alergenos = sorted(set(ingrediente.strip() for p in productos for ingrediente in p["ingredientes"].split(",")))
    tipos_piel = ["Grasa", "Seca", "Mixta", "Sensible", "Normal"]

    # Desplegable para seleccionar tipo de piel
    ttk.Label(ventana, text="Selecciona tu tipo de piel:").pack(pady=5)
    ttk.Combobox(ventana, textvariable=tipo_piel_var, values=tipos_piel).pack(pady=5)

    ttk.Label(ventana, text="Selecciona el tipo de rutina:").pack(pady=5)
    ttk.Combobox(ventana, textvariable=rutina_var, 
                 values=["Simple", "Completa", "Categorías específicas"]).pack(pady=5)

    ttk.Label(ventana, text="Selecciona una categoría específica:").pack(pady=5)
    ttk.Combobox(ventana, textvariable=categoria_var, values=categorias).pack(pady=5)

    ttk.Label(ventana, text="Selecciona ingredientes/alérgenos (opcional):").pack(pady=5)
    ttk.Combobox(ventana, textvariable=alergenos_var, values=alergenos, state="readonly").pack(pady=5)

    puntuacion_min_var = tk.StringVar(value="")
    precio_min_var = tk.StringVar(value="")
    precio_max_var = tk.StringVar(value="")

    ttk.Label(ventana, text="Puntuación mínima (opcional):").pack(pady=5)
    ttk.Entry(ventana, textvariable=puntuacion_min_var).pack(pady=5)

    ttk.Label(ventana, text="Precio mínimo (opcional):").pack(pady=5)
    ttk.Entry(ventana, textvariable=precio_min_var).pack(pady=5)

    ttk.Label(ventana, text="Precio máximo (opcional):").pack(pady=5)
    ttk.Entry(ventana, textvariable=precio_max_var).pack(pady=5)

    def generar():
        rutina = rutina_var.get()
        categoria = categoria_var.get()
        alergeno = alergenos_var.get()
        tipo_piel_seleccionado = tipo_piel_var.get().lower()
        puntuacion_min = float(puntuacion_min_var.get()) if puntuacion_min_var.get() else 0
        precio_min = float(precio_min_var.get()) if precio_min_var.get() else 0
        precio_max = float(precio_max_var.get()) if precio_max_var.get() else float('inf')

        # Filtrar productos según tipo de piel y alergeno
        productos_filtrados = [
            p for p in productos 
            if p["tipo_piel"].lower() == tipo_piel_seleccionado and 
               (not alergeno or alergeno not in p["ingredientes"]) and
               p["puntuacion"] >= puntuacion_min and
               p["precio"] >= precio_min
        ]

        if rutina == "Simple":
            categorias_simple = ["limpiador facial", "crema hidratante", "protector solar"]
            productos_filtrados = [p for p in productos_filtrados if p["tipo"] in categorias_simple]
        elif rutina == "Categorías específicas" and categoria:
            productos_filtrados = [p for p in productos_filtrados if p["tipo"] == categoria]

        if not productos_filtrados:
            messagebox.showinfo("Sin resultados", "No se encontraron productos con los filtros seleccionados.")
            return

        # Aplicar el algoritmo de la mochila para seleccionar los mejores productos
        combinacion_optima, puntuacion_total = mochila(productos_filtrados, precio_max)

        if not combinacion_optima:
            messagebox.showinfo("Sin resultados", "No se encontraron combinaciones válidas dentro del presupuesto.")
            return

        # Mostrar los productos seleccionados en el grafo
        G = nx.Graph()
        G.add_node(f"Piel {tipo_piel_seleccionado.capitalize()}")

        for producto in combinacion_optima:
            G.add_node(producto["nombre"], imagen=producto["imagen"], pagina=producto["pagina"],
                       precio=producto["precio"], puntuacion=producto["puntuacion"])
            G.add_edge(f"Piel {tipo_piel_seleccionado.capitalize()}", producto["nombre"])

        ventana.destroy()
        mostrar_grafo_con_datos(G, f"Piel {tipo_piel_seleccionado.capitalize()}")

    ttk.Button(ventana, text="Generar productos", command=generar).pack(pady=20)
    ventana.mainloop()

def test_tipo_piel(callback):
    ventana_test = tk.Toplevel()
    ventana_test.title("Test para determinar tu tipo de piel")
    ventana_test.geometry("500x400")

    respuestas = {"grasa": 0, "seca": 0, "mixta": 0, "sensible": 0, "normal": 0}
    preguntas = [
        ("¿Tu piel se ve brillante al final del día?", "grasa"),
        ("¿Sientes tu piel tirante después de lavarla?", "seca"),
        ("¿Tienes áreas grasas y áreas secas al mismo tiempo?", "mixta"),
        ("¿Tu piel reacciona fácilmente a productos o al clima?", "sensible"),
        ("¿Tu piel no presenta problemas significativos?", "normal")
    ]

    def siguiente_pregunta(indice=0):
        for widget in ventana_test.winfo_children():
            widget.destroy()
        if indice < len(preguntas):
            pregunta, tipo = preguntas[indice]
            tk.Label(ventana_test, text=pregunta, font=('Arial', 12), wraplength=400).pack(pady=20)
            tk.Button(ventana_test, text="Sí", command=lambda: [respuestas.__setitem__(tipo, respuestas[tipo] + 1), siguiente_pregunta(indice + 1)]).pack(pady=5)
            tk.Button(ventana_test, text="No", command=lambda: siguiente_pregunta(indice + 1)).pack(pady=5)
        else:
            tipo_piel = max(respuestas, key=respuestas.get)
            messagebox.showinfo("Resultado", f"Tu tipo de piel es: {tipo_piel.capitalize()}")
            ventana_test.destroy()
            callback(tipo_piel)

    siguiente_pregunta()

# Inicio
def main():
    ventana_inicio = tk.Tk()
    ventana_inicio.title("Bienvenido")
    ventana_inicio.geometry("400x200")
    tk.Label(ventana_inicio, text="¿Sabes qué tipo de piel tienes?", font=('Arial', 14)).pack(pady=20)
    ttk.Button(ventana_inicio, text="Sí", command=lambda: [ventana_inicio.destroy(), abrir_ventana_principal()]).pack(pady=5)
    ttk.Button(ventana_inicio, text="No", command=lambda: [ventana_inicio.destroy(), test_tipo_piel(abrir_ventana_principal)]).pack(pady=5)
    ventana_inicio.mainloop()

if __name__ == "__main__":
    main()
