# SIMULADOR DE BALANZA COMERCIAL

## Descripción General

Aquí se guarda todo el código fuente de la práctica 3.1: **Simulador Interactivo de Balanza Comercial: Plataforma para el Análisis de Flujos Comerciales**, una aplicación de escritorio capaz de simular el comercio entre múltiples países, el cual incorpora las siguientes funcionalidades clave:
- Permitir al usuario seleccionar países y productos específicos para la simulación.
- Determinación de costos asociados a la importación y exportación (aranceles, fletes, etc.)
- Análisis del impacto del tipo de cambio sobre los precios de los productos.
- Cálculo y presentación de la balanza comercial resultante.
- Mostrar gráficos interactivos (barras, timelines, etc.) que representen claramente los flujos comerciales y sus resultados.
- La posibilidad para el usuario de modificar variables (tipo de cambio, aranceles) y observar el impacto en los resultados comerciales.

## Módulos

La aplicación posee una arquitectura modular, destacando por cada módulo un aspecto primordial del programa. Estos son los módulos que integra el programa:

### 1. Base de dastos
Por medio de la librería `sqlite3`, se cargan y descargan datos necesarios para el cálculo de la balanza comercial, pudiendo generar DataFrames directamente para poder pasarlos al tercer módulo y graficarlos. Además, brinda la posibilidad al usuario de modificar ciertas variables para simular distintos escenarios de balanza comercial.

### 2. Lógica de Intercambio
Aquí se procesan los datos puros extraídos desde la base de datos para calcular los costos finales de importación/exportación y la balanza comercial entre países; Todo esto encapsulado en una clase “TradeSimulator” la cual incluye un único método que calcula el costo final de los productos y la balanza comercial mediante operaciones que combinan querys de SQL y funciones de Pandas y Matplotlib

### 3. Gráficos
Aquí se concentran todos los procesos encargados de renderizar los gráficos para mostrar la balanza comercial y el impacto del costo total por IPP (Importaciones por País)

### 4. Interfaz
Aquí se construye toda la interfaz gráfica principal, usando la librería `tkinter`, conectando porfín los controles (modificar aranceles y tipo de cambio) con la base de datos y la actualización de los gráficos que vimos anteriormente. La clase `TradeApp` es la encargada de crear todos los assets de la GUI, cargar nombres de países y de rutas de intercambio y actualizar el tipo de cambio y los aranceles dependiendo de las interacciones del usuario.

### 5. Main
Este es el módulo final o "módulo de ejecución", simplemente se inicializa la base de datos y la ventana para la interfaz y se corre el programa.

## Dependencias

Este es un proyecto que se llevó a cabo 100% en Python, usando las siguientes librerías:
~~~
tkinter
matplotlib
pandas
sqlite3
typing (para tipado, no tiene úsos primordiales)
~~~
