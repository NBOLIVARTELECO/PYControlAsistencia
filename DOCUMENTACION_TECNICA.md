# Documentación Técnica - PYControlAsistencia

## 📋 Índice

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Modelos de Datos](#modelos-de-datos)
3. [Capa de Acceso a Datos](#capa-de-acceso-a-datos)
4. [Interfaz de Usuario](#interfaz-de-usuario)
5. [Flujo de Autenticación](#flujo-de-autenticación)
6. [Patrones de Diseño](#patrones-de-diseño)
7. [Configuración](#configuración)
8. [Manejo de Errores](#manejo-de-errores)
9. [Seguridad](#seguridad)
10. [Pruebas](#pruebas)

## 🏗️ Arquitectura del Sistema

### Patrón Arquitectónico
El sistema sigue una arquitectura en **3 capas**:

```
┌─────────────────────────────────────┐
│           PRESENTACIÓN              │
│        (UserInterface/)             │
├─────────────────────────────────────┤
│           LÓGICA DE NEGOCIO         │
│           (Models/)                 │
├─────────────────────────────────────┤
│         ACCESO A DATOS              │
│        (Repository/)                │
└─────────────────────────────────────┘
```

### Responsabilidades por Capa

#### Capa de Presentación (UserInterface/)
- **Responsabilidad**: Interfaz gráfica y interacción con el usuario
- **Componentes**: Formularios, ventanas, controles
- **Tecnología**: ttkbootstrap (Tkinter moderno)

#### Capa de Lógica de Negocio (Models/)
- **Responsabilidad**: Reglas de negocio y validaciones
- **Componentes**: Modelos de dominio, enums, validaciones
- **Patrón**: Active Record (modelos con métodos de persistencia)

#### Capa de Acceso a Datos (Repository/)
- **Responsabilidad**: Persistencia y recuperación de datos
- **Componentes**: Clase de conexión, queries SQL
- **Tecnología**: pyodbc + SQL Server

## 📊 Modelos de Datos

### Jerarquía de Clases

```
MdBase (Clase Base)
├── MdUsuario (Usuario Genérico)
│   ├── MdAdministrador
│   ├── MdDocente
│   └── MdEstudiante
└── MdAsignatura
```

### MdBase
```python
class MdBase():
    Id: int
    
    def EstablecerId(self, id) -> None:
        self.Id = id
```

### MdUsuario
```python
class MdUsuario(MdBase):
    TipoDocumento: EnTipoDocumento
    Documento: str
    PrimerNombre: str
    SegundoNombre: str
    PrimerApellido: str
    SegundoApellido: str
    Email: str
    Password: str
    Activo: bool
```

### Enums

#### EnTipoUsuario
```python
class EnTipoUsuario(Enum):
    Administrador = 0
    Docente = 1
    Estudiante = 2
```

#### EnTipoDocumento
```python
class EnTipoDocumento(Enum):
    NA = 0  # No Aplica
    CC = 1  # Cédula de Ciudadanía
    CE = 2  # Cédula de Extranjería
    TI = 3  # Tarjeta de Identidad
    PT = 4  # Pasaporte
```

## 🗄️ Capa de Acceso a Datos

### ClDataBase
Clase singleton para manejo de conexiones a SQL Server.

```python
class ClDataBase():
    @staticmethod
    def __SetupConnection() -> str:
        # Configuración de conexión
        
    @staticmethod
    def OpenConnection() -> pyodbc.Cursor:
        # Abre conexión y retorna cursor
        
    @staticmethod
    def CloseConnection(cursor: pyodbc.Cursor) -> None:
        # Cierra conexión
```

### Patrón de Uso
```python
# Abrir conexión
cursor = ClDataBase.OpenConnection()

# Ejecutar query
cursor.execute("SELECT * FROM Tabla")

# Procesar resultados
resultados = cursor.fetchall()

# Cerrar conexión
ClDataBase.CloseConnection(cursor)
```

## 🖥️ Interfaz de Usuario

### Framework: ttkbootstrap
- **Ventaja**: Tema moderno tipo Bootstrap
- **Tema**: Flatly (verde como color principal)
- **Responsive**: Adaptable a diferentes tamaños

### Estructura de Ventanas

#### FrLogin (Ventana de Login)
```python
def FrLogin(root: ttk.Window, onCallBack) -> ttk.Toplevel:
    # Ventana modal de autenticación
    # Parámetros:
    # - root: Ventana padre
    # - onCallBack: Función callback al autenticarse
```

#### FrMain (Ventana Principal)
```python
# Ventana principal con menús dinámicos según tipo de usuario
# Configuración de menús por rol:
# - Administrador: Gestión de usuarios y asignaturas
# - Docente: Control de clases y asistencia
# - Estudiante: Consulta de asistencia
```

### Componentes UI Utilizados
- **ttk.Label**: Etiquetas de texto
- **ttk.Entry**: Campos de entrada
- **ttk.Button**: Botones de acción
- **ttk.Combobox**: Listas desplegables
- **ttk.Frame**: Contenedores de layout

## 🔐 Flujo de Autenticación

### Secuencia de Autenticación

1. **Usuario ingresa credenciales** en FrLogin
2. **Se crea objeto MdInicioSesion** con datos del formulario
3. **Se valida tipo de usuario** (Administrador/Docente/Estudiante)
4. **Se llama método ValidarUsuario** del modelo correspondiente
5. **Se ejecuta query SQL** para verificar credenciales
6. **Si válido**: Se cierra login y se abre ventana principal
7. **Si inválido**: Se muestra mensaje de error

### Código de Validación
```python
def ValidarUsuario(mdInicioSesion: MdInicioSesion) -> bool:
    cursor = ClDataBase.OpenConnection()
    strSearch = f"SELECT Id FROM Tabla WHERE Documento='{usuario}' AND Password='{password}' AND Activo=1"
    cursor.execute(strSearch)
    objValor = cursor.fetchval()
    return objValor != None
```

## 🎨 Patrones de Diseño

### 1. Active Record
Los modelos contienen métodos de persistencia:
```python
class MdDocente(MdUsuario):
    def InsertarRegistro(self) -> None:
        # Lógica de inserción
        
    def ActualizarRegistro(self) -> None:
        # Lógica de actualización
        
    def EliminarRegistro(self) -> None:
        # Lógica de eliminación
```

### 2. Factory Method
Para crear objetos según tipo de usuario:
```python
def ValidarUsuario(inicioSesion: MdInicioSesion) -> bool:
    if inicioSesion.TipoUsuario == EnTipoUsuario.Docente:
        return MdDocente.ValidarUsuario(inicioSesion)
    elif inicioSesion.TipoUsuario == EnTipoUsuario.Estudiante:
        return MdEstudiante.ValidarUsuario(inicioSesion)
    # ...
```

### 3. Callback Pattern
Para comunicación entre ventanas:
```python
def FrLogin(root: ttk.Window, onCallBack):
    # onCallBack se ejecuta cuando el login es exitoso
    onCallBack(mdInicioSesion)
```

## ⚙️ Configuración

### Archivo config.py
Configuración centralizada en diccionarios:

```python
DATABASE_CONFIG = {
    'driver': 'ODBC Driver 17 for SQL Server',
    'server': '(Local)',
    'database': 'BDControlAsistencia',
    'username': 'sa',
    'password': 'CC80737015'
}

APP_CONFIG = {
    'title': 'UNAL - Control de Asistencia',
    'theme': 'flatly',
    'version': '1.0.0'
}
```

### Variables de Entorno (Recomendado)
```bash
# .env
DB_SERVER=localhost
DB_NAME=BDControlAsistencia
DB_USER=sa
DB_PASSWORD=CC80737015
```

## 🚨 Manejo de Errores

### Errores Comunes

1. **Error de Conexión a BD**
   ```python
   try:
       cursor = ClDataBase.OpenConnection()
   except pyodbc.Error as e:
       Messagebox.show_error(f"Error de conexión: {e}")
   ```

2. **Error de Autenticación**
   ```python
   if not MdUsuario.ValidarUsuario(mdInicioSesion):
       Messagebox.show_warning('Usuario o Contraseña inválida!!')
   ```

3. **Error de Validación**
   ```python
   if not documento or not password:
       Messagebox.show_warning('Todos los campos son obligatorios')
   ```

### Logging (Pendiente)
```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

## 🔒 Seguridad

### Medidas Implementadas
- ✅ Validación de tipos de usuario
- ✅ Verificación de credenciales en BD
- ✅ Control de acceso por roles
- ✅ Campos Activo para soft delete

### Medidas Pendientes
- ❌ Encriptación de contraseñas (hash)
- ❌ Validación de entrada (SQL Injection)
- ❌ Timeout de sesión
- ❌ Logs de auditoría
- ❌ Rate limiting

### Recomendaciones de Seguridad

1. **Encriptar Contraseñas**
   ```python
   import hashlib
   
   def hash_password(password: str) -> str:
       return hashlib.sha256(password.encode()).hexdigest()
   ```

2. **Prevenir SQL Injection**
   ```python
   # Usar parámetros en lugar de concatenación
   cursor.execute("SELECT * FROM Usuario WHERE Documento = ? AND Password = ?", 
                 (usuario, password))
   ```

3. **Validar Entrada**
   ```python
   import re
   
   def validar_email(email: str) -> bool:
       pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
       return re.match(pattern, email) is not None
   ```

## 🧪 Pruebas

### Pruebas Unitarias (Pendiente)
```python
import unittest

class TestMdUsuario(unittest.TestCase):
    def test_validar_usuario_exitoso(self):
        # Arrange
        inicio_sesion = MdInicioSesion()
        inicio_sesion.Usuario = "admin"
        inicio_sesion.Password = "123"
        inicio_sesion.TipoUsuario = EnTipoUsuario.Administrador
        
        # Act
        resultado = MdUsuario.ValidarUsuario(inicio_sesion)
        
        # Assert
        self.assertTrue(resultado)
```

### Pruebas de Integración
```python
class TestConexionBD(unittest.TestCase):
    def test_conexion_exitosa(self):
        cursor = ClDataBase.OpenConnection()
        self.assertIsNotNone(cursor)
        ClDataBase.CloseConnection(cursor)
```

### Datos de Prueba
```sql
-- Usuarios de prueba
INSERT INTO MdAdministrador VALUES (1, 'admin', 'Admin', 'Sistema', 'admin@unal.edu.co', '123', 1);
INSERT INTO MdDocente VALUES (1, '12345678', 'Juan', 'Pérez', 'juan@unal.edu.co', 'TP001', '123', 1);
INSERT INTO MdEstudiante VALUES (1, '87654321', 'María', 'García', 'maria@unal.edu.co', '2023001', '123', 1);
```

## 📈 Métricas y Monitoreo

### Métricas Sugeridas
- Tiempo de respuesta de autenticación
- Número de intentos fallidos de login
- Uso de memoria y CPU
- Errores de conexión a BD

### Logs de Auditoría
```python
def log_auditoria(usuario: str, accion: str, resultado: bool):
    logging.info(f"Usuario: {usuario}, Acción: {accion}, Resultado: {'Exitoso' if resultado else 'Fallido'}")
```

## 🔄 Mantenimiento

### Tareas de Mantenimiento
1. **Backup de Base de Datos** (diario)
2. **Limpieza de Logs** (semanal)
3. **Actualización de Dependencias** (mensual)
4. **Revisión de Seguridad** (trimestral)

### Scripts de Mantenimiento
```sql
-- Backup automático
BACKUP DATABASE BDControlAsistencia 
TO DISK = 'C:\Backups\BDControlAsistencia_' + CONVERT(VARCHAR(8), GETDATE(), 112) + '.bak'
```

---

**Documentación actualizada**: 2024
**Versión**: 1.0.0
**Autor**: Universidad Nacional de Colombia 