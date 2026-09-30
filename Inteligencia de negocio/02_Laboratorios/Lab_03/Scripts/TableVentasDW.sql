USE VentasDW;

GO 

CREATE TABLE Dim_Producto(
	ProductoSK INT IDENTITY(1,1) PRIMARY KEY,
    ProductID_OLTP INT NOT NULL,               -- ID original del producto en el OLTP
    Codigo VARCHAR(20) NOT NULL,               
    Nombre_Producto VARCHAR(100) NOT NULL,
    Nombre_SubCategoria VARCHAR(50) NOT NULL,  
    Nombre_Categoria VARCHAR(50) NOT NULL,    
    PrecioBase DECIMAL(10,2) NOT NULL,
    Descripcion VARCHAR(200) NULL,
    Activo BIT NOT NULL DEFAULT 1
);

CREATE TABLE Dim_Vendedor(
	VendedorSK INT IDENTITY(1,1) PRIMARY KEY,
	VendedorID_OLTP INT NOT NULL,
    Nombre VARCHAR(100) NOT NULL,
    Sucursal VARCHAR(50) NOT NULL
);

CREATE TABLE Dim_Cliente(
	ClienteSK INT IDENTITY(1,1) PRIMARY KEY,
	ClienteID_OLTP INT NOT NULL,
    Documento VARCHAR(20) NOT NULL,
    Nombre VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NULL,
    FechaAlta DATE NOT NULL,
	Nombre_Ciudad VARCHAR(50) NOT NULL,
    Pais VARCHAR(50) NOT NULL,
    Region VARCHAR(50) NOT NULL
);

CREATE TABLE Dim_Tiempo(
	TiempoSK INT PRIMARY KEY,              
    Fecha DATE NOT NULL UNIQUE,           
    Anio INT NOT NULL,                     
    Trimestre INT NOT NULL,               
    NombreTrimestre VARCHAR(20) NOT NULL,  
    Mes INT NOT NULL,                      
    NombreMes VARCHAR(20) NOT NULL,       
    Dia INT NOT NULL,                   
    DiaSemana INT NOT NULL,               
    NombreDia VARCHAR(20) NOT NULL,      
    EsFinDeSemana BIT NOT NULL
);

CREATE TABLE Fact_Ventas(
	VentaID INT IDENTITY(1,1) PRIMARY KEY,
	NumeroFactura VARCHAR(20) NOT NULL UNIQUE,
	Cantidad INT NOT NULL,
	PrecioUnit DECIMAL(10,2) NOT NULL,
	Descuento DECIMAL(5,2) NOT NULL DEFAULT 0,
	-- Claves Foráneas (Conexión con las Dimensiones)
	ProductoSK INT NOT NULL FOREIGN KEY REFERENCES Dim_Producto(ProductoSK),
	VendedorSK INT NOT NULL FOREIGN KEY REFERENCES Dim_Vendedor(VendedorSK),
	ClienteSK INT NOT NULL FOREIGN KEY REFERENCES Dim_Cliente(ClienteSK),
	TiempoSK INT NOT NULL FOREIGN KEY REFERENCES Dim_Tiempo(TiempoSK),

	-- Métricas Calculadas (Acelera las consultas analíticas en Power BI / SQL)

	MontoBruto AS (Cantidad * PrecioUnit) PERSISTED,
    MontoDescuento AS (Cantidad * PrecioUnit * (Descuento / 100.0)) PERSISTED,
    MontoNeto AS ((Cantidad * PrecioUnit) - (Cantidad * PrecioUnit * (Descuento / 100.0))) PERSISTED
);