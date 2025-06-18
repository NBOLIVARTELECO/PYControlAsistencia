"""
Archivo de configuración centralizada para PYControlAsistencia
"""

# Configuración de Base de Datos
DATABASE_CONFIG = {
    'driver': 'ODBC Driver 17 for SQL Server',
    'server': '(Local)',
    'database': 'BDControlAsistencia',
    'username': 'sa',
    'password': 'CC80737015',
    'trusted_connection': False
}

# Configuración de la Aplicación
APP_CONFIG = {
    'title': 'UNAL - Control de Asistencia',
    'theme': 'flatly',
    'version': '1.0.0',
    'author': 'Universidad Nacional de Colombia'
}

# Configuración de Reconocimiento Facial
FACE_RECOGNITION_CONFIG = {
    'tolerance': 0.6,
    'model': 'hog',  # 'hog' o 'cnn'
    'upsample_times': 1
}

# Configuración de Seguridad
SECURITY_CONFIG = {
    'password_min_length': 8,
    'session_timeout': 3600,  # segundos
    'max_login_attempts': 3
} 