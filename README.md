# PYControlAsistencia

Sistema de Control de Asistencia para la Universidad Nacional de Colombia (UNAL) desarrollado en Python con interfaz gráfica moderna.

## 📋 Descripción

PYControlAsistencia es una aplicación de escritorio diseñada para gestionar la asistencia de estudiantes en la Universidad Nacional de Colombia. El sistema permite diferentes tipos de usuarios (Administrador, Docente, Estudiante) con funcionalidades específicas para cada rol.

## 🏗️ Arquitectura del Proyecto

El proyecto sigue una arquitectura en capas con separación clara de responsabilidades:

```
PYControlAsistencia/
├── Models/              # Capa de modelos de datos
├── Repository/          # Capa de acceso a datos
├── UserInterface/       # Capa de presentación
├── FaceRecognition/     # Módulo de reconocimiento facial
└── README.md
```

## 🎯 Funcionalidades

### 👨‍💼 Administrador
- Gestión de docentes
- Gestión de estudiantes  
- Gestión de asignaturas
- Administración general del sistema

### 👨‍🏫 Docente
- Iniciar clases
- Añadir estudiantes a clases
- Control de asistencia en tiempo real

### 👨‍🎓 Estudiante
- Consultar historial de asistencia
- Verificar estado de asistencia

## 🛠️ Tecnologías Utilizadas

- **Python 3.x** - Lenguaje principal
- **ttkbootstrap** - Framework de interfaz gráfica moderna
- **pyodbc** - Conexión a base de datos SQL Server
- **SQL Server** - Base de datos relacional
- **OpenCV** (planificado) - Reconocimiento facial

## 📦 Requisitos del Sistema

### Software Requerido
- Python 3.8 o superior
- SQL Server 2019 o superior
- ODBC Driver 17 for SQL Server

### Dependencias Python
```
ttkbootstrap>=1.10.0
pyodbc>=4.0.35
opencv-python>=4.8.0
numpy>=1.24.0
```

## 🚀 Instalación

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd PYControlAsistencia
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar Base de Datos
1. Instalar SQL Server
2. Crear la base de datos `BDControlAsistencia`
3. Ejecutar los scripts SQL para crear las tablas
4. Configurar las credenciales en `Repository/ClDataBase.py`

### 4. Ejecutar la Aplicación
```bash
python UserInterface/FrMain.py
```

## 🗄️ Estructura de la Base de Datos

### Tablas Principales
- **MdAdministrador** - Información de administradores
- **MdDocente** - Información de docentes
- **MdEstudiante** - Información de estudiantes
- **MdAsignatura** - Información de asignaturas

### Campos Comunes
- Id (Primary Key)
- TipoDocumento (CC, CE, TI, PT)
- Documento
- PrimerNombre, SegundoNombre
- PrimerApellido, SegundoApellido
- Email
- Password
- Activo

## 👥 Tipos de Usuario

### EnTipoUsuario (Enum)
- **0** - Administrador
- **1** - Docente  
- **2** - Estudiante

### EnTipoDocumento (Enum)
- **0** - NA (No Aplica)
- **1** - CC (Cédula de Ciudadanía)
- **2** - CE (Cédula de Extranjería)
- **3** - TI (Tarjeta de Identidad)
- **4** - PT (Pasaporte)

## 🔧 Configuración

### Configuración de Base de Datos
Editar `Repository/ClDataBase.py`:
```python
OdbcDriver = 'ODBC Driver 17 for SQL Server'
Servidor = '(Local)'  # o IP del servidor
BaseDatos = 'BDControlAsistencia'
Usuario = 'sa'
Password = 'tu_password'
```

## 🎨 Interfaz de Usuario

La aplicación utiliza **ttkbootstrap** para una interfaz moderna y responsiva:

- **Tema**: Flatly (bootstrap theme)
- **Colores**: Verde (success) como color principal
- **Ventanas**: Modales para login, formularios responsivos
- **Componentes**: Botones, comboboxes, entradas de texto estilizadas

## 🔐 Seguridad

- Autenticación por usuario y contraseña
- Validación de tipos de usuario
- Contraseñas encriptadas (pendiente de implementar)
- Control de acceso por roles

## 🚧 Estado del Proyecto

### ✅ Completado
- [x] Estructura base del proyecto
- [x] Sistema de autenticación
- [x] Modelos de datos
- [x] Conexión a base de datos
- [x] Interfaz de login
- [x] Interfaz principal con menús por rol

### 🔄 En Desarrollo
- [ ] Formularios de gestión (CRUD)
- [ ] Sistema de reconocimiento facial
- [ ] Control de asistencia en tiempo real
- [ ] Reportes de asistencia

### 📋 Pendiente
- [ ] Encriptación de contraseñas
- [ ] Validaciones de entrada
- [ ] Manejo de errores
- [ ] Logs del sistema
- [ ] Backup automático
- [ ] Documentación técnica detallada

## 🐛 Problemas Conocidos

1. **Error en MdAdministrador.py**: Línea 58 tiene una comilla extra en el UPDATE
2. **Error en MdEstudiante.py**: Línea 48 usa `self.id` en lugar de `self.Id`
3. **Inconsistencia en métodos**: `AbrirConexion()` vs `OpenConnection()`
4. **Falta herencia**: MdAdministrador no hereda de MdUsuario

## 👨‍💻 Desarrollo

### Estructura de Archivos
- **Models/**: Clases de dominio y lógica de negocio
- **Repository/**: Acceso a datos y conexión a BD
- **UserInterface/**: Formularios y ventanas
- **FaceRecognition/**: Módulo de reconocimiento facial

### Convenciones de Código
- Nombres de clases: PascalCase (ej: `MdUsuario`)
- Nombres de métodos: PascalCase (ej: `ValidarUsuario`)
- Variables: camelCase (ej: `tipoDocumento`)
- Enums: Prefijo `En` (ej: `EnTipoUsuario`)

## 📞 Soporte

Para reportar bugs o solicitar nuevas funcionalidades, crear un issue en el repositorio del proyecto.

## 📄 Licencia

Este proyecto es desarrollado para la Universidad Nacional de Colombia.

---

**Desarrollado con ❤️ para la UNAL**
