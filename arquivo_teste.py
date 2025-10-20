from classsProcessor_teste import Processor

if __name__ == "__main__":
    instance = Processor(max_workers=10, batch_size=1)
    instance.executar()
