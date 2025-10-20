import threading
from datetime import datetime
import classLogger
from process_lote import processar_lote
from conection import ConectionClass


class Processor:
    def __init__(self, max_workers: int = 10, batch_size: int = 1000):
        self.config = ConectionClass.DbConfig()
        self.max_workers = max_workers
        self.batch_size = batch_size
        self.servidor = 'proscore.com.br'
        self.batch_counter_status1 = 0
        self.batch_counter_status2 = 0
        self.batch_counter_status4 = 0
        self.lock = threading.Lock()

    def executar(self):
        inicio = datetime.now()
        classLogger.logger.info("=" * 80)
        classLogger.logger.info(f"Iniciando Progestor - Consulta Proscore - {inicio}")
        classLogger.logger.info("=" * 80)

        try:
            total_processados = processar_lote(self)
          
            fim = datetime.now()
            duracao = (fim - inicio).total_seconds()

            classLogger.logger.info("---" * 80)
            classLogger.logger.info(f"Processamento concluído em {duracao:.2f} segundos")
            classLogger.logger.info(f"Total de registros processados: {total_processados}")

        except Exception as e:
            classLogger.logger.error(f"Erro fatal na execução: {str(e)}", exc_info=True)
