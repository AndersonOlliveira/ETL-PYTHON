import logging
from logging.handlers import RotatingFileHandler
#//*====================================================
#//*Config do log
#//*====================================================
class log:
# classLogger.py
 logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('progestor_proscore.log'),
        logging.StreamHandler()
    ]
)
 
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('arquivos_/progestor_proscore_finalizar_erro.log'),
#         logging.StreamHandler()
#     ]
# )

logger = logging.getLogger('progestor_proscore')
logger_finalizar = logging.getLogger('progestor_proscore_finalizar')