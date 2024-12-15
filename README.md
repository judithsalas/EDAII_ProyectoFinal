# **README: Proyecto de Selección Óptima de Productos de Skincare**

## **Descripción del Proyecto**

Este proyecto tiene como objetivo ofrecer una herramienta interactiva para ayudar a los usuarios a seleccionar los mejores productos de skincare según sus necesidades específicas.

La aplicación se basa en un enfoque personalizado que combina:
- **Un test para identificar el tipo de piel** del usuario si este no lo sabe.
- **Filtros avanzados** que permiten especificar presupuesto, ingredientes a evitar y preferencias.
- **Algoritmos eficientes**, como la **Programación Dinámica** (Problema de la Mochila), para garantizar que el usuario reciba la mejor combinación de productos dentro de su presupuesto.

**Nota:** Las puntuaciones y los precios de los productos se generan de forma aleatoria debido a que la API utilizada no proporciona acceso directo a estos datos. Sin embargo, al hacer clic en la imagen de un producto en la visualización interactiva, se accede al enlace del producto real. Esta funcionalidad sirve como una demostración de cómo sería el sistema si se integraran datos reales.

---

## **Estructura del Proyecto**

### **1. Código para Generar la Base de Datos**

El primer componente del proyecto se encarga de generar una base de datos con información sobre productos de skincare.

- **Fuente de Datos:**
  - Los datos se obtienen mediante consultas a la API de Google Custom Search para buscar productos de skincare con atributos como:
    - Nombre del producto.
    - Imagen del producto.
    - Descripción.
    - Precio (simulado dentro de un rango).
    - Puntuación (generada aleatoriamente dentro de un rango específico).
    - Tipo de piel para el que está destinado.

- **Salidas:**
  - Un archivo CSV (`productos_skincare.csv`) que contiene toda la información de los productos.

### **2. Código Principal**

Este componente es la interfaz principal con la que interactúa el usuario. Ofrece varias funcionalidades clave:

#### **a. Test para Determinar el Tipo de Piel**

- **¿Qué hace?**
  - Si el usuario no sabe cuál es su tipo de piel, la aplicación ofrece un test interactivo.
  - El test se basa en preguntas sencillas y prácticas, como:
    - ¿Tu piel se ve brillante al final del día?
    - ¿Tu piel se siente tirante después de lavarla?

- **¿Qué resultados genera?**
  - El test clasifica al usuario en uno de los siguientes tipos de piel:
    - Grasa.
    - Seca.
    - Mixta.
    - Sensible.
    - Normal.

#### **b. Selección de Productos con Filtros Personalizados**

- **Parámetros que el usuario puede configurar:**
  - Tipo de piel (puede ser ingresado directamente o determinado por el test).
  - Presupuesto máximo.
  - Puntuación mínima de los productos.
  - Ingredientes a evitar (para alérgenos o preferencias específicas).
  - Tipo de rutina (simple, completa o personalizada por categorías).

#### **c. Algoritmo de la Mochila**

- **¿Qué hace?**
  - Resuelve el problema de optimizar la selección de productos para maximizar la puntuación total sin exceder el presupuesto.

- **¿Cómo funciona?**
  - Utiliza un enfoque de **Programación Dinámica**:
    - Evalúa todas las combinaciones posibles de productos.
    - Determina la combinación que maximiza la puntuación total dentro del presupuesto especificado.

#### **d. Visualización Interactiva**

- **¿Qué hace?**
  - Muestra los productos seleccionados en un grafo interactivo.
  - Los nodos del grafo incluyen:
    - La imagen del producto.
    - Su precio.
    - Su puntuación.
    - Un enlace a su página (si está disponible).

---

## **Requisitos del Sistema**

### **Dependencias**

- **Bibliotecas de Python:**
  - `csv`: Para manejar la base de datos.
  - `networkx`: Para crear grafos interactivos.
  - `matplotlib`: Para la visualización gráfica.
  - `tkinter`: Para la interfaz gráfica de usuario.
  - `requests`: Para realizar consultas a la API.
  - `Pillow`: Para manejar imágenes de los productos.

- **API de Google Custom Search:**
  - Es necesario configurar una clave de API y un ID de motor de búsqueda para generar la base de datos de productos.

### **Archivos Generados**

1. `productos_skincare.csv`: Archivo CSV que contiene los datos de los productos generados.
2. Archivos Python:
   - `generar_base_datos.py`: Código para generar la base de datos.
   - `main_skincare.py`: Código principal de la aplicación.

---

## **Cómo Ejecutar el Proyecto**

### **1. Generar la Base de Datos**

1. Configura tu clave de API y tu ID de motor de búsqueda en el archivo `generar_base_datos.py`.
2. Ejecuta el script:
   ```bash
   python generar_base_datos.py
   ```
3. Este script generará un archivo llamado `productos_skincare.csv`.

### **2. Ejecutar la Aplicación Principal**

1. Asegúrate de que el archivo `productos_skincare.csv` esté en el mismo directorio que `main_skincare.py`.
2. Ejecuta el script principal:
   ```bash
   python main_skincare.py
   ```

### **3. Uso de la Aplicación**

1. Si no conoces tu tipo de piel, realiza el test interactivo.
2. Configura los filtros según tus preferencias.
3. Observa los resultados óptimos y explora los productos seleccionados en el grafo interactivo.

---

## **Análisis de los Algoritmos**

### **Test para Tipo de Piel**
- Basado en preguntas simples y respuestas binarias (sí/no).
- Clasifica de manera eficiente al usuario según sus respuestas acumuladas.

### **Algoritmo de la Mochila (Programación Dinámica)**
- Resuelve el problema de maximizar la puntuación total de los productos seleccionados dentro del presupuesto.
- Garantiza la solución óptima utilizando una matriz de programación dinámica para almacenar subproblemas.
- Complejidad:
  - Temporal: \( O(n \cdot W) \), donde \( n \) es el número de productos y \( W \) es el presupuesto máximo.
  - Espacial: \( O(n \cdot W) \) (se puede optimizar a \( O(W) \) usando una matriz unidimensional).

---

## **Contribuciones y Extensiones Futuras**

1. **Mejorar la Base de Datos:**
   - Ampliar la cantidad de productos disponibles mediante integraciones con otras APIs.

2. **Optimización del Algoritmo:**
   - Implementar una versión más eficiente del algoritmo de la mochila para grandes bases de datos.

3. **Mejoras en la Interfaz:**
   - Agregar más opciones de personalización, como rutinas nocturnas o específicas para estaciones del año.

4. **Análisis de Resultados:**
   - Incorporar gráficos adicionales que muestren el uso del presupuesto y el impacto de las preferencias del usuario.

---

¡Gracias por utilizar esta herramienta! Si tienes alguna pregunta o sugerencia, no dudes en contactar al desarrollador.
