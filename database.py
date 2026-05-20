import sqlite3

def inicializar_sistema_economico():
    # Conexión limpia a la nueva base de datos
    conexion = sqlite3.connect('economia_analytics.db')
    cursor = conexion.cursor()
    
    # 1. Dimensión: Productos de la Canasta Familiar
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Dim_Productos (
            ProductoID INTEGER PRIMARY KEY AUTOINCREMENT,
            NombreProducto TEXT NOT NULL,
            Categoria TEXT NOT NULL
        )
    ''')
    
    # 2. Dimensión: Regiones o Sectores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Dim_Regiones (
            RegionID INTEGER PRIMARY KEY AUTOINCREMENT,
            NombreRegion TEXT NOT NULL,
            EstratoPredominante INTEGER
        )
    ''')
    
    # 3. Tabla de Hechos: Registro de Precios (La que analiza Power BI)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Fact_Precios (
            RegistroID INTEGER PRIMARY KEY AUTOINCREMENT,
            ProductoID INTEGER,
            RegionID INTEGER,
            FechaRegistro TEXT,
            PrecioUnitario REAL,
            IndiceInflacion REAL,
            FOREIGN KEY (ProductoID) REFERENCES Dim_Productos (ProductoID),
            FOREIGN KEY (RegionID) REFERENCES Dim_Regiones (RegionID)
        )
    ''')
    
    # Insertar datos base si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM Dim_Productos")
    if cursor.fetchone()[0] == 0:
        productos = [
            ('Arroz 1kg', 'Alimentos'),
            ('Leche 1L', 'Alimentos'),
            ('Gasolina Galón', 'Transporte'),
            ('Arriendo Promedio', 'Vivienda'),
            ('Energía Eléctrica KW', 'Servicios Públicos')
        ]
        cursor.executemany("INSERT INTO Dim_Productos (NombreProducto, Categoria) VALUES (?, ?)", productos)
        
    cursor.execute("SELECT COUNT(*) FROM Dim_Regiones")
    if cursor.fetchone()[0] == 0:
        regiones = [
            ('Bogotá D.C.', 3),
            ('Medellín', 3),
            ('Cali', 3),
            ('Barranquilla', 2)
        ]
        cursor.executemany("INSERT INTO Dim_Regiones (NombreRegion, EstratoPredominante) VALUES (?, ?)", regiones)

    # Insertar datos de hechos simulados para que Power BI tenga vida
    cursor.execute("SELECT COUNT(*) FROM Fact_Precios")
    if cursor.fetchone()[0] == 0:
        datos_precios = [
            # Enero 2026
            (1, 1, '2026-01-15', 4200, 0.05),
            (2, 1, '2026-01-15', 3800, 0.04),
            (3, 1, '2026-01-15', 15000, 0.08),
            # Febrero 2026
            (1, 1, '2026-02-15', 4350, 0.06),
            (2, 1, '2026-02-15', 3900, 0.05),
            (3, 2, '2026-02-15', 15500, 0.09),
            # Marzo 2026
            (1, 1, '2026-03-15', 4400, 0.05),
            (4, 1, '2026-03-15', 850000, 0.12),
            # Abril 2026
            (1, 3, '2026-04-15', 16200, 0.10),
            (5, 1, '2026-04-15', 650, 0.07),
            # Mayo 2026
            (1, 1, '2026-05-10', 4600, 0.08)
        ]
        cursor.executemany("INSERT INTO Fact_Precios (ProductoID, RegionID, FechaRegistro, PrecioUnitario, IndiceInflacion) VALUES (?, ?, ?, ?, ?)", datos_precios)
        
    conexion.commit()
    conexion.close()
    print("¡Base de datos 'economia_analytics.db' inicializada con éxito y con estructura de Modelo Estrella!")

if __name__ == '__main__':
    inicializar_sistema_economico()