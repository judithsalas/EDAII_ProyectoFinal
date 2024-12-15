import requests
import csv
import random

# Configuración de la API
API_KEY = #te la adjunto en otro documento si es necesaria
SEARCH_ENGINE_ID = "f4438e74b14cb45d4"

# Lista de ingredientes según el tipo de producto
INGREDIENTES = {
    "limpiador facial": ["Agua micelar", "Ácido salicílico", "Glicerina", "Niacinamida", "Extracto de té verde"],
    "crema hidratante": ["Ácido hialurónico", "Ceramidas", "Aloe vera", "Manteca de karité", "Escualano"],
    "mascarilla facial": ["Arcilla blanca", "Carbón activado", "Ácido láctico", "Pepino", "Vitamina C"],
    "serum": ["Retinol", "Vitamina C", "Niacinamida", "Ácido ferúlico", "Ácido glicólico"],
    "protector solar": ["Óxido de zinc", "Dióxido de titanio", "Ácido hialurónico", "Vitamina E", "Alantoína"],
    "exfoliante": ["Ácido salicílico", "Ácido glicólico", "Bambú micronizado", "Jojoba", "AHA/BHA"],
    "tónico facial": ["Hamamelis", "Ácido láctico", "Pepino", "Niacinamida", "Glicerina"],
    "aceite facial": ["Aceite de jojoba", "Aceite de argán", "Aceite de rosa mosqueta", "Vitamina E", "Escualano"]
}

# Función para buscar productos en Google Custom Search
def buscar_productos(consulta, num_resultados=10):
    """
    Realiza una búsqueda en la API de Google Custom Search y devuelve los resultados.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": consulta,
        "searchType": "image",  # Buscar imágenes relacionadas con productos
        "num": num_resultados
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        resultados = response.json().get("items", [])
        productos = []
        for item in resultados:
            productos.append({
                "nombre": item.get("title"),
                "imagen": item.get("link"),
                "descripcion": item.get("snippet", "Sin descripción"),
                "pagina": item.get("image", {}).get("contextLink", "Sin URL exacta"),  # URL específica
                "precio": f"{round(random.uniform(3, 150), 2)} €",  # Precio aleatorio entre 3 y 150
                "ingredientes": "No especificado",  # Se rellenará más adelante
                "beneficios": "No especificado",
                "puntuacion": round(random.uniform(3.0, 5.0), 1)  # Puntuación entre 3.0 y 5.0
            })
        return productos
    else:
        print(f"Error al consultar la API: {response.status_code}")
        return []

# Función para asignar ingredientes aleatorios
def asignar_ingredientes(tipo_producto):
    """
    Devuelve una lista de ingredientes aleatorios según el tipo de producto.
    """
    lista = INGREDIENTES.get(tipo_producto, ["Ingrediente genérico"])
    num_ingredientes = random.randint(2, 4)  # Selecciona entre 2 y 4 ingredientes
    return ", ".join(random.sample(lista, num_ingredientes))

# Función para guardar los productos en un archivo CSV
def guardar_en_csv(productos, nombre_archivo):
    """
    Guarda una lista de productos en un archivo CSV.
    """
    fieldnames = [
        "nombre",
        "imagen",
        "descripcion",
        "pagina",
        "tipo_piel",
        "tipo",
        "precio",
        "ingredientes",
        "beneficios",
        "puntuacion"
    ]
    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=fieldnames)
        escritor.writeheader()
        escritor.writerows(productos)
    print(f"Productos guardados en {nombre_archivo}")

# Categorías de productos y consultas por tipo de piel
categorias = {
    "limpiador facial": "limpiador facial",
    "crema hidratante": "crema hidratante facial",
    "mascarilla facial": "mascarilla facial",
    "serum": "serum facial",
    "protector solar": "protector solar facial",
    "exfoliante": "exfoliante facial",
    "tónico facial": "tónico facial",
    "aceite facial": "aceite facial"
}

tipos_piel = ["Grasa", "Seca", "Mixta", "Sensible", "Normal"]

# Obtener y guardar productos para cada tipo de piel y categoría
todos_los_productos = []
for tipo_piel in tipos_piel:
    for categoria, consulta_base in categorias.items():
        consulta = f"{consulta_base} piel {tipo_piel.lower()}"
        print(f"Buscando productos para {categoria} (Piel {tipo_piel})...")
        productos = buscar_productos(consulta, num_resultados=5)
        for producto in productos:
            producto["tipo_piel"] = tipo_piel
            producto["tipo"] = categoria
            producto["ingredientes"] = asignar_ingredientes(categoria)
            producto["beneficios"] = f"Ideal para piel {tipo_piel.lower()} en cuidado {categoria}"
        todos_los_productos.extend(productos)

# Guardar los resultados en un archivo CSV
guardar_en_csv(todos_los_productos, "productos_skincare.csv")
