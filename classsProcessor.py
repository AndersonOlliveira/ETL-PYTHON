import time
import threading
from conection import ConectionClass
 


class Processor:
    def __init__(self, max_workers: int = 10, batch_size: int = 1000):
        
        self.config = ConectionClass.DbConfig()
        self.max_workers = max_workers #//?número de threads paralelas para REQUEST
        self.batch_size = batch_size #//?Número máximo de registros a processar por execução
        self.servidor = 'proscore.com.br'
        self.batch_counter_status1 = 0
        self.batch_counter_status2 = 0
        self.batch_counter_status4 = 0
        self.lock = threading.Lock()

        