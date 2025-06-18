-- Scripts SQL para PYControlAsistencia
-- Base de datos: BDControlAsistencia

-- Crear base de datos
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'BDControlAsistencia')
BEGIN
    CREATE DATABASE BDControlAsistencia;
END
GO

USE BDControlAsistencia;
GO

-- Tabla de Administradores
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[MdAdministrador]') AND type in (N'U'))
BEGIN
    CREATE TABLE MdAdministrador (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        TipoDocumento INT NOT NULL,
        Documento VARCHAR(20) NOT NULL UNIQUE,
        PrimerNombre VARCHAR(50) NOT NULL,
        SegundoNombre VARCHAR(50) NULL,
        PrimerApellido VARCHAR(50) NOT NULL,
        SegundoApellido VARCHAR(50) NULL,
        Email VARCHAR(100) NOT NULL UNIQUE,
        Password VARCHAR(255) NOT NULL,
        Activo BIT DEFAULT 1,
        FechaCreacion DATETIME DEFAULT GETDATE(),
        FechaModificacion DATETIME DEFAULT GETDATE()
    );
END
GO

-- Tabla de Docentes
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[MdDocente]') AND type in (N'U'))
BEGIN
    CREATE TABLE MdDocente (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        TipoDocumento INT NOT NULL,
        Documento VARCHAR(20) NOT NULL UNIQUE,
        PrimerNombre VARCHAR(50) NOT NULL,
        SegundoNombre VARCHAR(50) NULL,
        PrimerApellido VARCHAR(50) NOT NULL,
        SegundoApellido VARCHAR(50) NULL,
        Email VARCHAR(100) NOT NULL UNIQUE,
        Password VARCHAR(255) NOT NULL,
        TarjetaProfesional VARCHAR(50) NOT NULL UNIQUE,
        Activo BIT DEFAULT 1,
        FechaCreacion DATETIME DEFAULT GETDATE(),
        FechaModificacion DATETIME DEFAULT GETDATE()
    );
END
GO

-- Tabla de Estudiantes
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[MdEstudiante]') AND type in (N'U'))
BEGIN
    CREATE TABLE MdEstudiante (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        TipoDocumento INT NOT NULL,
        Documento VARCHAR(20) NOT NULL UNIQUE,
        PrimerNombre VARCHAR(50) NOT NULL,
        SegundoNombre VARCHAR(50) NULL,
        PrimerApellido VARCHAR(50) NOT NULL,
        SegundoApellido VARCHAR(50) NULL,
        Email VARCHAR(100) NOT NULL UNIQUE,
        Password VARCHAR(255) NOT NULL,
        NumeroCarne VARCHAR(20) NOT NULL UNIQUE,
        Foto VARBINARY(MAX) NULL,
        Vector VARBINARY(MAX) NULL,
        Activo BIT DEFAULT 1,
        FechaCreacion DATETIME DEFAULT GETDATE(),
        FechaModificacion DATETIME DEFAULT GETDATE()
    );
END
GO

-- Tabla de Asignaturas
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[MdAsignatura]') AND type in (N'U'))
BEGIN
    CREATE TABLE MdAsignatura (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Nombre VARCHAR(100) NOT NULL,
        Codigo VARCHAR(20) NOT NULL UNIQUE,
        Creditos INT NOT NULL,
        Activo BIT DEFAULT 1,
        FechaCreacion DATETIME DEFAULT GETDATE(),
        FechaModificacion DATETIME DEFAULT GETDATE()
    );
END
GO

-- Tabla de Clases
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[MdClase]') AND type in (N'U'))
BEGIN
    CREATE TABLE MdClase (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        IdAsignatura INT NOT NULL,
        IdDocente INT NOT NULL,
        FechaInicio DATETIME NOT NULL,
        FechaFin DATETIME NOT NULL,
        Estado VARCHAR(20) DEFAULT 'Programada', -- Programada, EnCurso, Finalizada, Cancelada
        Activo BIT DEFAULT 1,
        FechaCreacion DATETIME DEFAULT GETDATE(),
        FechaModificacion DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (IdAsignatura) REFERENCES MdAsignatura(Id),
        FOREIGN KEY (IdDocente) REFERENCES MdDocente(Id)
    );
END
GO

-- Tabla de Asistencia
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[MdAsistencia]') AND type in (N'U'))
BEGIN
    CREATE TABLE MdAsistencia (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        IdClase INT NOT NULL,
        IdEstudiante INT NOT NULL,
        FechaHora DATETIME DEFAULT GETDATE(),
        TipoAsistencia VARCHAR(20) DEFAULT 'Presente', -- Presente, Ausente, Tardanza
        MetodoRegistro VARCHAR(20) DEFAULT 'Manual', -- Manual, Facial, QR
        Activo BIT DEFAULT 1,
        FechaCreacion DATETIME DEFAULT GETDATE(),
        FechaModificacion DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (IdClase) REFERENCES MdClase(Id),
        FOREIGN KEY (IdEstudiante) REFERENCES MdEstudiante(Id)
    );
END
GO

-- Insertar datos de prueba

-- Administrador por defecto
IF NOT EXISTS (SELECT * FROM MdAdministrador WHERE Documento = 'admin')
BEGIN
    INSERT INTO MdAdministrador (TipoDocumento, Documento, PrimerNombre, PrimerApellido, Email, Password)
    VALUES (1, 'admin', 'Administrador', 'Sistema', 'admin@unal.edu.co', '123');
END
GO

-- Docente de prueba
IF NOT EXISTS (SELECT * FROM MdDocente WHERE Documento = '12345678')
BEGIN
    INSERT INTO MdDocente (TipoDocumento, Documento, PrimerNombre, PrimerApellido, Email, TarjetaProfesional, Password)
    VALUES (1, '12345678', 'Juan', 'Pérez', 'juan.perez@unal.edu.co', 'TP001', '123');
END
GO

-- Estudiante de prueba
IF NOT EXISTS (SELECT * FROM MdEstudiante WHERE Documento = '87654321')
BEGIN
    INSERT INTO MdEstudiante (TipoDocumento, Documento, PrimerNombre, PrimerApellido, Email, NumeroCarne, Password)
    VALUES (1, '87654321', 'María', 'García', 'maria.garcia@unal.edu.co', '2023001', '123');
END
GO

-- Asignatura de prueba
IF NOT EXISTS (SELECT * FROM MdAsignatura WHERE Codigo = 'MAT001')
BEGIN
    INSERT INTO MdAsignatura (Nombre, Codigo, Creditos)
    VALUES ('Matemáticas Básicas', 'MAT001', 3);
END
GO

PRINT 'Scripts de base de datos ejecutados correctamente.'; 