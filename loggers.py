import logging
import sys

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)

# Определяем первый вид форматирования
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Инициализируем хэндлер, который будет перенаправлять логи в stderr
stderr_handler = logging.StreamHandler()
# Инициализируем хэндлер, который будет перенаправлять логи в stdout
stdout_handler = logging.StreamHandler(sys.stdout)

# Устанавливаем форматтеры для хэндлеров
stderr_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)

# Добавляем хэндлеры логгеру
logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)

