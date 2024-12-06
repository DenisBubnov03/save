import logging

# Настройка логирования
logging.basicConfig(
    filename="bot_logs.log",  # Имя файла для логирования
    level=logging.INFO,       # Уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат логов
)

logger = logging.getLogger(__name__)
