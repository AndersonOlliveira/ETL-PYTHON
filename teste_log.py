import logging
import sys
import os

# 1. Definir um formatador comum para os logs
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# 2. Obter os dois loggers nomeados
logger_proscore = logging.getLogger('progestor_proscore')
logger_finalizar = logging.getLogger('progestor_proscore_finalizar')
logger_finalizar_erro = logging.getLogger('progestor_proscore_finalizar_erro')

# 3. Definir o nível mínimo de log para cada um
logger_proscore.setLevel(logging.INFO)
logger_finalizar.setLevel(logging.INFO)
logger_finalizar_erro.setLevel(logging.INFO)

# =======================================================
# Configuração do Logger 'progestor_proscore'
# =======================================================

# Handler de arquivo para o primeiro logger
file_handler_proscore = logging.FileHandler('progestor_proscore.log')
file_handler_proscore.setFormatter(formatter)
logger_proscore.addHandler(file_handler_proscore)

# Handler de console para o primeiro logger
stream_handler_proscore = logging.StreamHandler(sys.stdout)
stream_handler_proscore.setFormatter(formatter)
logger_proscore.addHandler(stream_handler_proscore)


# =======================================================
# Configuração do Logger 'progestor_proscore_finalizar'
# =======================================================

# Handler de arquivo para o segundo logger (NOVO ARQUIVO!)
file_handler_finalizar = logging.FileHandler('progestor_proscore_finalizar.log')
file_handler_finalizar.setFormatter(formatter)
logger_finalizar.addHandler(file_handler_finalizar)

# Handler de console para o segundo logger
stream_handler_finalizar = logging.StreamHandler(sys.stdout)
stream_handler_finalizar.setFormatter(formatter)
logger_finalizar.addHandler(stream_handler_finalizar)

# ==========================================================
# Configuração do Logger 'progestor_proscore_finalizar_erro'
# ==========================================================

# Handler de arquivo para o segundo logger (NOVO ARQUIVO!)
file_handler_finalizar_erro = logging.FileHandler('arquivos_/progestor_proscore_finalizar_erro.log')
file_handler_finalizar_erro.setFormatter(formatter)
logger_finalizar_erro.addHandler(file_handler_finalizar_erro)

# Handler de console para o segundo logger
stream_handler_erro = logging.StreamHandler(sys.stdout)
stream_handler_erro.setFormatter(formatter)
logger_finalizar_erro.addHandler(stream_handler_erro)
