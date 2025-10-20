import logging
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

logger = logging.getLogger('progestor_proscore')