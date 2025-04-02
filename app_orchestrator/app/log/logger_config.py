from loguru import logger
import sys
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger.remove()  # Eliminar configuraciones previas

LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {module}:{function}:{line} - {message}"

# Log en consola con colores
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    colorize=True
)

# Log de depuración (DEBUG incluye INFO y superiores)
logger.add(
    os.path.join(LOG_DIR, "debug_OR.log"),
    format=LOG_FORMAT,
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
    compression="zip"
)

# Log de errores críticos (ERROR y CRITICAL únicamente)
logger.add(
    os.path.join(LOG_DIR, "error_OR.log"),
    format=LOG_FORMAT,
    rotation="10 MB",
    retention="7 days",
    level="ERROR",
    compression="zip"
)
