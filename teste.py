import datetime
import requests
import pandas as pd
import time
import json

# Caminho do arquivo com os CPFs (sem cabeçalho)
arquivo_entrada = 'arquivos/new_lista_crm.csv'
arquivo_saida = 'saida.csv'

# Lê o CSV sem cabeçalho
dados_ = pd.read_csv(arquivo_entrada, sep=';', header=None)


def request_all(dados_):
    resultados = []

    for index, row in dados_.iterrows():
        cpf = str(row[0]).strip()
        print(f" Consultando CPF {index+1}/{len(dados_)}: {cpf}")

        # Monta o dicionário base
        registro = {
            'processo_id': 309,
            'contrato': 417039,
            'rede': 2620,
            'codcns': 262936, #360 E CLONE
            # 'codcns': 270309,
            'nome_arquivo': arquivo_entrada,
            'aceite_execucao': True,
            'mensagem_alerta': None,
            'data_cadastro': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'configuracao_json': '[{"plugin":111,"separar":true,"ocorrencias":10,"campos":[1,2,3,4,5,6]},{"plugin":311,"separar":false,"ocorrencias":1,"campos":[1,2]}]',
            'campos_aquisicao': 'tlidersinistrocrmmed',
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
            'parametros': f'&tlidersinistrocrmmed={cpf}',
            'erro': False
        }

        dados_plugin = False
        resposta_nobitida = False
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
        erro = registro.get('erro', False)
        resposta = ""

        if not erro:   erro = registro.get('erro', False)
        resposta = ""

        if not erro:

            try:
                print(f"ESTOU SAINDO AQUI {url}")
                response = requests.get(url, timeout=(300, 300))
                response.raise_for_status()
                resposta = response.text
                print(f"Resposta: {resposta[:100]}...")
                erro = False
            except requests.exceptions.Timeout:
                resposta = "TIMEOUT: Requisição excedeu 5 minutos"
                erro = True
                print(f"Timeout na requisição: {url}")

            except requests.exceptions.RequestException as e:
                resposta = f"ERRO: {str(e)}"
                erro = True
                print(f"Erro na requisição: {str(e)}")
                # ajuste neste local

            print(f"MINHA RESPOSTA TEM O QUE? {resposta}")
        # if not resposta or resposta.strip() == "" or len(resposta) == 2:
        if resposta.strip() == "":
        # if  resposta.strip() == "" or len(resposta) == 2:
            resposta = "RESPOSTA NâO OBTIDAS"
            erro = True
            resposta_nobitida = True 
        

        else:
          
          erro = False
          if not len(resposta) == 2:
          
         
            try:
                dados = json.loads(resposta)

                print(f"MEU JSON DENTRO DE DADOS {len(resposta)}")
            
                # if dados:
                print(f"MEU JSON DENTRO DE DADOS {dados}")
                lista_registros = dados.get("registro", [])

                contador_total = len(lista_registros)
                contador_plugin_9 = sum(
                        1 for item in lista_registros
                        if item.get("numero_plugin") == "9")
                        #    for item in lista_registros:
                        #         print(f"Plugin: {item.get('numero_plugin')}")
                        #         print(f"Código: {item.get('codigo_da_mensagem')}")
                        #         print(f"Descrição: {item.get('descricao_da_mensagem')}")
                        #         print("----")

                        #    print(f"Total de retornos: {contador_total}")
                        #    print(f"Total plugin 9: {contador_plugin_9}")
                
                if contador_total > 0 and contador_plugin_9 == contador_total:
                    erro = True
                    dados_plugin = True
            except json.JSONDecodeError:
                resposta = "RESPOSTA INVALIDA — NÃO É UM JSON"
                erro = True
          else:
            print(f"VOU SAIR AQUI?  {len(resposta)}")
            resposta = "RESPOSTA NâO OBTIDA"
            erro = True
            resposta_nobitida = True 

        print(f"MEUS DADOS DE RESPOSTA {resposta}")
        
        registro["url"] = url
        registro["resposta_json"] = resposta
        registro["erro"] = erro
        registro["puglin"] = dados_plugin
        registro["resposta_nObitida"] = resposta_nobitida

        print(f"meu registro final: {registro}")

        time.sleep(0.3)
    resultados.append(registro)
    # Salva o resultado em CSV
    df_saida = pd.DataFrame(resultados)
    df_saida.to_csv(arquivo_saida, index=False, sep=';', encoding='utf-8-sig')

    print(f"\n Arquivo '{arquivo_saida}' salvo com {len(df_saida)} registros!")
    return resultados


if __name__ == "__main__":
    request_all(dados_)
