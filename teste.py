import datetime
import requests
import pandas as pd
import time

# Caminho do arquivo com os CPFs (sem cabeçalho)
arquivo_entrada = 'poucas_linhas.csv'
arquivo_saida = 'saida.csv'

# Lê o CSV sem cabeçalho
dados_ = pd.read_csv(arquivo_entrada, sep=';', header=None)


def request_all(dados_):
    resultados = []

    for index, row in dados_.iterrows():
        cpf = str(row[0]).strip()
        print(f"➡️ Consultando CPF {index+1}/{len(dados_)}: {cpf}")

        # Monta o dicionário base
        registro = {
            'processo_id': 309,
            'contrato': 417039,
            'rede': 2620,
            'codcns': 270309,
            'nome_arquivo': arquivo_entrada,
            'aceite_execucao': True,
            'mensagem_alerta': None,
            'data_cadastro': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'configuracao_json': '[{"plugin":111,"separar":true,"ocorrencias":10,"campos":[1,2,3,4,5,6]},{"plugin":311,"separar":false,"ocorrencias":1,"campos":[1,2]}]',
            'campos_aquisicao': 'tcpfcnpj',
            'loja': 134387,
            'finalizado': False,
            'data_finalizacao': None,
            'pause': False,
            'transacao_id': 2997520,
            'id_processo': 309,
            'campo_aquisicao': cpf,
            'status': 0,
            'sucesso': False,
            'data_cadastro_transacao': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'parametros': f'&tcpfcnpj={cpf}',
            'erro': False
        }

        # Monta a URL da requisição
        servidor = "proscore.com.br" # link para do servidor
        url = (
            f"https://{servidor}/cns/json.chp?"
            f"progestor_prc={registro['processo_id']}"
            f"&rde={registro['rede']}"
            f"&rdelja={registro['loja']}"
            f"&ctr={registro['contrato']}"
            f"&srvcns=1"
            f"&tcnscod={registro['codcns']}{registro['parametros']}"
        )

        registro["url"] = url

      
        try:
            r = requests.get(url, timeout=300000)
            r.raise_for_status()
            resposta_texto = r.text.strip()

            if not resposta_texto:
                resposta_texto = "RESPOSTA NÃO OBITIDA"
                registro["erro"] = True
            else:
                registro["sucesso"] = True

        except Exception as e:
            resposta_texto = f"Erro: {e}"
            registro["erro"] = True

        # Guarda o resultado
        registro["resposta_json"] = resposta_texto
        resultados.append(registro)

        # Pequena pausa para evitar bloqueio (opcional)
        time.sleep(0.3)

    # Salva o resultado em CSV
    df_saida = pd.DataFrame(resultados)
    df_saida.to_csv(arquivo_saida, index=False, sep=';', encoding='utf-8-sig')

    print(f"\n Arquivo '{arquivo_saida}' salvo com {len(df_saida)} registros!")
    return resultados


if __name__ == "__main__":
    request_all(dados_)
