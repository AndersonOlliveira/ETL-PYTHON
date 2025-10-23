from classsProcessor_teste import Processor
import time
from threading import Timer

if __name__ == "__main__":
    time_execute = 60
    instance = Processor(max_workers=10, batch_size=5, idProcesso=338)
    # instance = Processor(max_workers=10, batch_size=2)
    instance.executar()
    # time.sleep(1000)
    tempo_finalizar = Timer(time_execute,instance.executar_finalizar)
    tempo_finalizar.start()
    pass
    
    tempo_zero = Timer(time_execute,instance.executar_zero)
    tempo_zero.start()
    pass
    # aqui finalizo os processo tem o mesma quantidade de registro e processos
    tempo_finish = Timer(time_execute,instance.executar_finalizar_process)
    tempo_finish.start()
