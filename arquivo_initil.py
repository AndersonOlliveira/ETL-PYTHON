from classsProcessor import Processor
from delete_logs.limpar_logs import limpar_pasta_logs
import time
from threading import Timer
import classLogger
import threading

if __name__ == "__main__":
    # instance = Processor(max_workers=10, batch_size=1, idProcesso=133)
    instance = Processor(max_workers=10, batch_size=10)
    tempo_espera_ciclo = 60  # Tempo de espera (em segundos) entre um ciclo e outro
    
    classLogger.logger.info(f"[{time.strftime('%H:%M:%S')}] Iniciando loop contínuo...")

    # Loop Infinito
    while True:
        try:
           
            instance.executar_ciclo()

            thread_limpeza = threading.Thread(
              target=limpar_pasta_logs,
              kwargs={
            #   "pasta_logs": "logs",
              "lines_to_exclude": ["DEBUG", "INFO", "secret","WARNING"],
              "max_linhas": 1000
              },
              daemon=True
              )
            thread_limpeza.start()
            
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