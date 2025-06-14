# api/utils/logger.py
import logging
import os

LOG_FILE = os.getenv("SECURITY_LOG_FILE", "security.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),     # 파일로 기록
        logging.StreamHandler()            # 콘솔 출력도 동시에
    ]
)

logger = logging.getLogger("security_logger")