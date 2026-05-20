# Econoscan v1.0 - Sistema de Monitoreo de Precios e Inflación

Este proyecto corresponde al entregable final del Corte 3. Consiste en un ecosistema de Inteligencia de Negocios diseñado para monitorear y analizar el comportamiento de los precios de la canasta básica y la inflación en diferentes regiones de Colombia.

## 👥 Integrantes
* Daniel Camilo López Piraquive
* Juan José Caballero Mantilla
* Martín Trujillo Rodríguez

## 🛠️ Arquitectura del Sistema
El proyecto está estructurado bajo un enfoque limpio y eficiente:
* **Backend (`database.py`):** Inicializa la base de datos SQLite y define un Modelo Estrella (Tablas de Dimensión para Productos y Regiones, y una Tabla de Hechos para el Historial de Precios).
* **Frontend (`app.py`):** Interfaz gráfica desarrollada en Python (Tkinter) que permite la gestión y el ingreso de nuevos registros económicos en tiempo real.
* **Data Analytics (`.pbix`):** Dashboard en Power BI conectado a la base de datos, que implementa medidas avanzadas en DAX y visualizaciones orientadas a resolver preguntas críticas de negocio.