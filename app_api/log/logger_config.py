from loguru import logger
import sys
import os

# 📁 Directorio donde se guardarán los logs
LOG_DIR = "logs"

# 📌 Asegurar que el directorio de logs exista
os.makedirs(LOG_DIR, exist_ok=True)

# 🛑 Eliminar configuraciones previas de Loguru
logger.remove()

# 🎨 Formato de logs con detalles de tiempo, nivel, módulo, función y línea
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {module}:{function}:{line} - {message}"

# 📌 Configuración de logs en consola con colores
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    colorize=True
)

# 📁 Log general (todos los niveles INFO en adelante)
# This code snippet is configuring a log handler using Loguru in Python. Let's break down
# the `logger.add` function call:
logger.add(
    os.path.join(LOG_DIR, "app_api.log"),
    format=LOG_FORMAT,
    rotation="10 MB",
    retention="7 days",
    level="INFO"
)

# 🛠 Log de depuración (solo DEBUG)
logger.add(
    os.path.join(LOG_DIR, "debug_api.log"),
    format=LOG_FORMAT,
    rotation="10 MB",
    retention="7 days",
    level="DEBUG"
)

# ❌ Log de errores (solo ERROR y CRITICAL)
logger.add(
    os.path.join(LOG_DIR, "error_api.log"),
    format=LOG_FORMAT,
    rotation="10 MB",
    retention="7 days",
    level="ERROR"
)
