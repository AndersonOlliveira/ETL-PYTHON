from classsProcessor import Processor
import time
from threading import Timer
import classLogger

# from conection.Conexao_Mongos import mongoConect
# from models.colletion_repository import Coletion
# # from request.r import request_all
# import pandas as pd
   

# conn = mongoConect()
# print(f" minha conexao {conn}")



# if conn:
#     db = conn.get_db_connection()
#     collection = db.get_collection(conn.get_db_colletion())
#     collection_json = db.get_collection(conn.get_db_colletion_json())
#     connection = db
#     print(f" Minha Collection: {collection_json.name}")
#     print(f"--"*20)
#     print(f"Conexao: {db}")

if __name__ == "__main__":
    instance = Processor(max_workers=10, batch_size=10, idProcesso=353)
    # instance = Processor(max_workers=10, batch_size=3)
    tempo_espera_ciclo = 60  # Tempo de espera (em segundos) entre um ciclo e outro
    
    classLogger.logger.info(f"[{time.strftime('%H:%M:%S')}] Iniciando loop contínuo...")

    # Loop Infinito
    while True:
        try:
           
            instance.executar_ciclo()
            
            # Pausa antes de recomeçar
            classLogger.logger.info(f"[{time.strftime('%H:%M:%S')}] Aguardando {tempo_espera_ciclo} segundos para o próximo ciclo...")
            time.sleep(tempo_espera_ciclo)

        except KeyboardInterrupt:
            # Permite parar o script com Ctrl+C no terminal
            classLogger.logger.info("\nEncerrando loop por comando do usuário (Ctrl+C).")
            break
        except Exception as e:
            # Lida com erros inesperados e continua o loop
            classLogger.logger.info(f"[{time.strftime('%H:%M:%S')}] Erro inesperado: {e}. Continuará em 30 segundos.")
            time.sleep(tempo_espera_ciclo)