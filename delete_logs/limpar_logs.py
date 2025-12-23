import os 


def remove_lines_from_log(log_file, lines_to_exclude, max_linhas=1000):
    # 1. Read all lines from the file
    with open(log_file, 'r') as f:
        
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

# def limpar_pasta_logs(pasta_logs, lines_to_exclude, max_linhas=1000):
def limpar_pasta_logs(lines_to_exclude, max_linhas=1000):
    pasta_logs = os.getcwd()

    # print(f"iniciando e listando a pasta  de logs: {pasta_logs}")


    for arquivo in os.listdir(pasta_logs):
        if arquivo.endswith('.log'):
            # print(f"meu arquivo de log para limpeza: {arquivo}")
            caminho = os.path.join(pasta_logs, arquivo)
            remove_lines_from_log(caminho, lines_to_exclude, max_linhas)