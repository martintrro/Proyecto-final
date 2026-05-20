import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import database  # Conecta con tu backend limpio

class EconoscanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Econoscan v1.0 - Monitoreo de Precios e Inflación")
        self.root.geometry("700x550")
        
        # Inicializar la base de datos al arrancar
        database.inicializar_sistema_economico()
        
        # Estilos visuales
        style = ttk.Style()
        style.theme_use('clam')
        
        # Pestañas del programa
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tab_registrar = ttk.Frame(self.notebook)
        self.tab_visualizar = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_registrar, text="Registrar Precios")
        self.notebook.add(self.tab_visualizar, text="Historial de Datos")
        
        self.crear_pestana_registro()
        self.crear_pestana_visualizacion()

    def conectar_db(self):
        return sqlite3.connect('economia_analytics.db')

    def obtener_lista_productos(self):
        conn = self.conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT ProductoID, NombreProducto FROM Dim_Productos")
        productos = cursor.fetchall()
        conn.close()
        return productos

    def obtener_lista_regiones(self):
        conn = self.conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT RegionID, NombreRegion FROM Dim_Regiones")
        regiones = cursor.fetchall()
        conn.close()
        return regiones

    def crear_pestana_registro(self):
        frame = ttk.LabelFrame(self.tab_registrar, text=" Nuevo Registro de Precio (Canasta Básica) ", padding=20)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="Producto:").grid(row=0, column=0, sticky='w', pady=10)
        self.combo_producto = ttk.Combobox(frame, width=40, state="readonly")
        self.combo_producto.grid(row=0, column=1, pady=10)
        
        ttk.Label(frame, text="Región / Ciudad:").grid(row=1, column=0, sticky='w', pady=10)
        self.combo_region = ttk.Combobox(frame, width=40, state="readonly")
        self.combo_region.grid(row=1, column=1, pady=10)
        
        ttk.Label(frame, text="Precio Unitario ($):").grid(row=2, column=0, sticky='w', pady=10)
        self.entry_precio = ttk.Entry(frame, width=43)
        self.entry_precio.grid(row=2, column=1, pady=10)
        
        ttk.Label(frame, text="Índice de Inflación (Ej: 0.06 para 6%):").grid(row=3, column=0, sticky='w', pady=10)
        self.entry_inflacion = ttk.Entry(frame, width=43)
        self.entry_inflacion.grid(row=3, column=1, pady=10)
        
        self.cargar_selectores()
        
        btn_guardar = ttk.Button(frame, text="Guardar Registro Económico", command=self.guardar_registro)
        btn_guardar.grid(row=4, column=0, columnspan=2, pady=30, ipadx=20, ipady=5)

    def cargar_selectores(self):
        self.productos_data = self.obtener_lista_productos()
        self.regiones_data = self.obtener_lista_regiones()
        
        self.combo_producto['values'] = [p[1] for p in self.productos_data]
        self.combo_region['values'] = [r[1] for r in self.regiones_data]

    def guardar_registro(self):
        idx_prod = self.combo_producto.current()
        idx_reg = self.combo_region.current()
        precio = self.entry_precio.get()
        inflacion = self.entry_inflacion.get()
        
        if idx_prod == -1 or idx_reg == -1 or not precio or not inflacion:
            messagebox.showwarning("Campos Incompletos", "Por favor, llena todos los campos.")
            return
            
        try:
            prod_id = self.productos_data[idx_prod][0]
            reg_id = self.regiones_data[idx_reg][0]
            precio_flt = float(precio)
            inflacion_flt = float(inflacion)
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")
            
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Fact_Precios (ProductoID, RegionID, FechaRegistro, PrecioUnitario, IndiceInflacion)
                VALUES (?, ?, ?, ?, ?)
            ''', (prod_id, reg_id, fecha_hoy, precio_flt, inflacion_flt))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Éxito", "¡Registro económico guardado!")
            
            self.entry_precio.delete(0, tk.END)
            self.entry_inflacion.delete(0, tk.END)
            self.actualizar_tabla_historial()
            
        except ValueError:
            messagebox.showerror("Error", "Precio e Inflación deben ser números (usa punto para decimales).")

    def crear_pestana_visualizacion(self):
        frame = ttk.Frame(self.tab_visualizar, padding=10)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Historial de Precios Registrados (Fact_Precios)", font=('Helvetica', 11, 'bold')).pack(pady=5)
        
        columnas = ('ID', 'Producto', 'Región', 'Fecha', 'Precio', 'Inflación')
        self.tabla = ttk.Treeview(frame, columns=columnas, show='headings')
        
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100, anchor='center')
            
        self.tabla.pack(fill='both', expand=True, pady=10)
        self.actualizar_tabla_historial()

    def actualizar_tabla_historial(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
            
        conn = self.conectar_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT f.RegistroID, p.NombreProducto, r.NombreRegion, f.FechaRegistro, f.PrecioUnitario, f.IndiceInflacion
            FROM Fact_Precios f
            INNER JOIN Dim_Productos p ON f.ProductoID = p.ProductoID
            INNER JOIN Dim_Regiones r ON f.RegionID = r.RegionID
            ORDER BY f.RegistroID DESC
        ''')
        
        for fila in cursor.fetchall():
            precio_fmt = f"${fila[4]:,.0f}"
            inflacion_fmt = f"{fila[5]*100:.1f}%"
            self.tabla.insert('', tk.END, values=(fila[0], fila[1], fila[2], fila[3], precio_fmt, inflacion_fmt))
            
        conn.close()

if __name__ == '__main__':
    root = tk.Tk()
    app = EconoscanApp(root)
    root.mainloop()