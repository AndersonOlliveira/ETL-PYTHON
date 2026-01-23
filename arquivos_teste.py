import os
import threading
import glob


from delete_logs.limpar_logs import limpar_pasta_logs

def remove_lines_from_log(log_file, lines_to_exclude, max_linhas=1000):
   
    try: 

            with open(log_file, 'r' , encoding='utf-8', errors="ignore") as f:
                
                lines = f.readlines()
                print(f"Total de Lines antes da Limpeza : {len(lines)}")

            # 2. Filter out the lines you want to exclude
            filtered_lines = [line for line in lines if not any(exclude_str in line for exclude_str in lines_to_exclude)]
            print(f"Total de Lines filtradas para Limpeza : {len(filtered_lines)}")


            if len(filtered_lines) > max_linhas:
                filtered_lines = filtered_lines[-max_linhas:]

            print(f"Total final mantido no log: {len(filtered_lines)}")

            
            with open(log_file, 'w') as f:
                f.writelines(filtered_lines)

    except FileNotFoundError:
        print("UTF-8 decoding failed. Trying Latin-1...")
    try:
        with open(log_file, 'r', encoding='latin-1') as f:
            content = f.read()
    except Exception as e:
        print(f"Latin-1 decoding also failed: {e}")
     
        print(f"\nArquivo não encontrado em: {log_file}")

# def limpar_pasta_logs(pasta_logs, lines_to_exclude, max_linhas=1000):
def limpar_pasta_logs(lines_to_exclude, max_linhas=1000): 
    
     #aqui vou deletar de outra pasta
    arquivos_para_limpeza = set()
    caminho_base = "/home/proscore/mvc/"
    padrao = os.path.join(caminho_base, "**", "*.log")
    arquivos_encontrados = glob.glob(padrao, recursive=True)

    print(f"Arquivos .log encontrados: {arquivos_encontrados}")
    for arquivos in arquivos_encontrados:
         if arquivos.endswith('.log'):
            print(f"meu arquivo de log para limpeza da pagina mvc: {arquivos}")
            caminhos = os.path.join(caminho_base, arquivos)
            remove_lines_from_log(caminhos, lines_to_exclude, max_linhas)

   
    pasta_logs = os.getcwd()
    for arquivo in os.listdir(pasta_logs):
        if arquivo.endswith('.log'):
            print(f"meu arquivo de log para limpeza: {arquivo}")
            caminho = os.path.join(pasta_logs, arquivo)
            remove_lines_from_log(caminho, lines_to_exclude, max_linhas)

if __name__ == "__main__":

      thread_limpeza = threading.Thread(
                target=limpar_pasta_logs,
                kwargs={
                #   "pasta_logs": "logs",
                "lines_to_exclude": ["DEBUG", "INFO", "secret","WARNING"],
                "max_linhas": 10
                },
                daemon=True
                )
      thread_limpeza.start()
      thread_limpeza.join()