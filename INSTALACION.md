# Guía de Instalación - PYControlAsistencia

## 📋 Prerrequisitos

### Software Requerido

#### 1. Python 3.8 o Superior
- **Descarga**: [python.org](https://www.python.org/downloads/)
- **Verificación**: `python --version`
- **Recomendado**: Python 3.11 o 3.12

#### 2. SQL Server 2019 o Superior
- **Descarga**: [Microsoft SQL Server](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)
- **Edición**: Express (gratuita) o Developer
- **Configuración**: Autenticación mixta (Windows + SQL Server)

#### 3. ODBC Driver 17 for SQL Server
- **Descarga**: [Microsoft ODBC Driver](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
- **Versión**: 17.x o superior
- **Arquitectura**: x64 (recomendado)

### Herramientas Opcionales
- **SQL Server Management Studio (SSMS)**: Para administrar la BD
- **Visual Studio Code**: Editor de código recomendado
- **Git**: Control de versiones

## 🚀 Instalación Paso a Paso

### Paso 1: Clonar el Repositorio

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd PYControlAsistencia

# O descargar como ZIP y extraer
```

### Paso 2: Crear Entorno Virtual (Recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
# Instalar dependencias desde requirements.txt
pip install -r requirements.txt

# O instalar manualmente:
pip install ttkbootstrap>=1.10.0
pip install pyodbc>=4.0.35
pip install opencv-python>=4.8.0
pip install numpy>=1.24.0
pip install Pillow>=10.0.0
pip install face-recognition>=1.3.0
```

### Paso 4: Configurar Base de Datos

#### 4.1 Instalar SQL Server
1. Ejecutar el instalador de SQL Server
2. Seleccionar "Nueva instalación independiente"
3. Elegir "Desarrollo" o "Express"
4. Configurar autenticación mixta
5. Establecer contraseña para usuario 'sa'

#### 4.2 Crear Base de Datos
```sql
-- Ejecutar en SQL Server Management Studio o sqlcmd
CREATE DATABASE BDControlAsistencia;
GO
```

#### 4.3 Ejecutar Scripts de Base de Datos
```bash
# Opción 1: Desde SSMS
# Abrir database_scripts.sql y ejecutar

# Opción 2: Desde línea de comandos
sqlcmd -S localhost -U sa -P tu_password -i database_scripts.sql
```

#### 4.4 Verificar Conexión
```python
# Crear archivo test_connection.py
import pyodbc

try:
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=BDControlAsistencia;'
        'UID=sa;'
        'PWD=tu_password'
    )
    print("✅ Conexión exitosa a la base de datos")
    conn.close()
except Exception as e:
    print(f"❌ Error de conexión: {e}")
```

### Paso 5: Configurar Credenciales

#### 5.1 Editar config.py
```python
DATABASE_CONFIG = {
    'driver': 'ODBC Driver 17 for SQL Server',
    'server': 'localhost',  # o IP del servidor
    'database': 'BDControlAsistencia',
    'username': 'sa',
    'password': 'tu_password_aqui',  # Cambiar por tu contraseña
    'trusted_connection': False
}
```

#### 5.2 Editar Repository/ClDataBase.py
```python
def __SetupConnection() -> str:
    OdbcDriver = 'ODBC Driver 17 for SQL Server'
    Servidor = 'localhost'  # Cambiar si es necesario
    BaseDatos = 'BDControlAsistencia'
    Usuario = 'sa'
    Password = 'tu_password_aqui'  # Cambiar por tu contraseña
    return f'DRIVER={{{OdbcDriver}}};SERVER={Servidor};DATABASE={BaseDatos};UID={Usuario};PWD={Password}'
```

### Paso 6: Verificar Instalación

#### 6.1 Probar Conexión
```bash
python -c "
import sys
sys.path.append('Repository')
from ClDataBase import ClDataBase
try:
    cursor = ClDataBase.OpenConnection()
    print('✅ Conexión exitosa')
    ClDataBase.CloseConnection(cursor)
except Exception as e:
    print(f'❌ Error: {e}')
"
```

#### 6.2 Probar Interfaz
```bash
# Ejecutar la aplicación
python UserInterface/FrMain.py
```

## 🔧 Configuración Avanzada

### Configuración de Red
Si SQL Server está en otra máquina:

```python
# En config.py
DATABASE_CONFIG = {
    'server': '192.168.1.100',  # IP del servidor
    'port': '1433',  # Puerto SQL Server
    # ... resto de configuración
}
```

### Configuración de Seguridad
```python
# Usar autenticación de Windows
DATABASE_CONFIG = {
    'trusted_connection': True,
    # No incluir username/password
}
```

### Configuración de Pool de Conexiones
```python
# Para mejor rendimiento
import pyodbc
from pyodbc import pooling

# Habilitar pooling
pyodbc.pooling = True
```

## 🐛 Solución de Problemas

### Error: "ODBC Driver 17 for SQL Server not found"
```bash
# Solución 1: Instalar driver
# Descargar desde Microsoft y reinstalar

# Solución 2: Usar driver alternativo
# Cambiar en ClDataBase.py:
OdbcDriver = 'SQL Server'  # En lugar de 'ODBC Driver 17 for SQL Server'
```

### Error: "Login failed for user 'sa'"
```sql
-- En SQL Server Management Studio:
-- 1. Habilitar autenticación mixta
-- 2. Cambiar contraseña de sa
ALTER LOGIN sa WITH PASSWORD = 'nueva_contraseña';
ALTER LOGIN sa ENABLE;
```

### Error: "Database 'BDControlAsistencia' does not exist"
```sql
-- Crear la base de datos
CREATE DATABASE BDControlAsistencia;
GO
USE BDControlAsistencia;
GO
-- Ejecutar scripts de database_scripts.sql
```

### Error: "ModuleNotFoundError: No module named 'ttkbootstrap'"
```bash
# Reinstalar dependencias
pip uninstall ttkbootstrap
pip install ttkbootstrap

# O verificar entorno virtual
pip list | grep ttkbootstrap
```

### Error: "Access denied" en Windows
```bash
# Ejecutar como administrador
# O configurar permisos de firewall para SQL Server
```

## 📊 Verificación de Instalación

### Checklist de Verificación
- [ ] Python 3.8+ instalado
- [ ] SQL Server funcionando
- [ ] ODBC Driver instalado
- [ ] Base de datos creada
- [ ] Tablas creadas
- [ ] Dependencias instaladas
- [ ] Credenciales configuradas
- [ ] Conexión exitosa
- [ ] Aplicación ejecutándose

### Comandos de Verificación
```bash
# Verificar Python
python --version

# Verificar pip
pip --version

# Verificar dependencias
pip list

# Verificar SQL Server
sqlcmd -S localhost -U sa -P tu_password -Q "SELECT @@VERSION"

# Verificar aplicación
python UserInterface/FrMain.py
```

## 🔄 Actualización

### Actualizar Código
```bash
# Si usas Git
git pull origin main

# Si descargaste ZIP
# Descargar nueva versión y reemplazar archivos
```

### Actualizar Dependencias
```bash
pip install --upgrade -r requirements.txt
```

### Actualizar Base de Datos
```sql
-- Ejecutar scripts de migración si existen
-- O restaurar desde backup
```

## 📞 Soporte

### Información de Contacto
- **Email**: soporte@unal.edu.co
- **Documentación**: [Enlace a documentación]
- **Issues**: [Enlace al repositorio]

### Información del Sistema
```bash
# Generar reporte de sistema
python -c "
import sys
import platform
print(f'Python: {sys.version}')
print(f'OS: {platform.system()} {platform.release()}')
print(f'Architecture: {platform.architecture()}')
"
```

---

**Última actualización**: 2024
**Versión de la guía**: 1.0.0 