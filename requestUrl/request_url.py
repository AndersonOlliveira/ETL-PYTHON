import requests
from typing import Dict, List, Optional, Tuple
import classLogger
from conection.transation_status import atualiza_status_processando
from tratamento.resposta import limpa_resposta_premium
from conection.Conexao_Mongos import mongoConect
from models.colletion_repository import Coletion
import json
import time
conn = mongoConect()



if conn:
    db = conn.get_db_connection()
    collection = db.get_collection(conn.get_db_colletion())
    collection_json = db.get_collection(conn.get_db_colletion_json())
    connection = db
    print(f" Minha Collection: {collection_json.name}")
    print(f"--"*20)
    print(f"Conexao: {db}")
    


def request(self, registro: Dict) -> Dict:
        
        print(f"MEUS REGISTROS: {registro}")
        dados_plugin = False

        rede = str(registro['rede'])
        loja = str(registro['lj'])
        contrato = str(registro['contrato'])
        codigo_cns = str(registro['codcns'])
        processo_id = str(registro['processo_id'])
        parametros = registro.get('parametros', '')

        classLogger.logger.info(f"minha rede de loja {loja}")

        url = (
            f"https://{self.servidor}/cns/json.chp?"
            f"progestor_prc={processo_id}&"
            f"rde={rede}&"
            f"rdelja={loja}&"
            f"ctr={contrato}&"
            f"srvcns=1&"
            f"tcnscod={codigo_cns}"
            f"{parametros}"
        )
        
        classLogger.logger.info(f"Requisição: {url}")

        erro = registro.get('erro', False)
        resposta = ""

        if not erro:
            try:
                response = requests.get(url, timeout=(300, 300))
                response.raise_for_status()
                resposta = response.text

                classLogger.logger.info(f"Resposta: {resposta[:100]}...")
                erro = False
            except requests.exceptions.Timeout:
                resposta = "TIMEOUT: Requisição excedeu 5 minutos"
                erro = True
                classLogger.logger.error(f"Timeout na requisição: {url}")

            except requests.exceptions.RequestException as e:
                resposta = f"ERRO: {str(e)}"
                erro = True
                classLogger.logger.error(f"Erro na requisição: {str(e)}")
                # ajuste neste local

        classLogger.logger.error(f"MINHA RESPOSTA TEM O QUE? {resposta}")
        # if not resposta or resposta.strip() == "" or len(resposta) == 2:
        if  resposta.strip() == "" or len(resposta) == 2:
            resposta = "RESPOSTA NAO OBTIDA"
            erro = True
        else:
        
          try:
               dados = json.loads(resposta)
               lista_registros = dados.get("registro", [])

               contador_total = len(lista_registros)
               contador_plugin_9 = sum(
               1 for item in lista_registros
               if item.get("numero_plugin") == "9")
               for item in lista_registros:
                    print(f"Plugin: {item.get('numero_plugin')}")
                    print(f"Código: {item.get('codigo_da_mensagem')}")
                    print(f"Descrição: {item.get('descricao_da_mensagem')}")
                    print("----")

               print(f"Total de retornos: {contador_total}")
               print(f"Total plugin 9: {contador_plugin_9}")

       
               if contador_total > 0 and contador_plugin_9 == contador_total:
                   erro = True
                   dados_plugin = True
          except json.JSONDecodeError:
               resposta = "RESPOSTA INVALIDA — NÃO É UM JSON"
               erro = True
        
        registro["url"] = url
        registro["resposta_json"] = resposta
        registro["erro"] = erro
        registro["puglin"] = dados_plugin

        print(f"meu registro final: {registro}")

        return registro

def request_all(rows):
    
    print(rows)
    resultados = []

#     print('Estou no request')
#     print(f"Quantidade de registros recebidos: {len(rows)}")

    for registros in rows:
        rede = str(registros.get('rede', ''))
        loja = str(registros.get('loja', ''))
        contrato = str(registros.get('contrato', ''))
        codigo_cns = str(registros.get('codcns', ''))
        processo_id = registros.get('processo_id')
        parametros = registros.get('parametros', '')  
        servidor = 'proscore.com.br'


        url = (
            f"https://{servidor}/cns/json.chp?"
            f"progestor_prc={processo_id}&rde={rede}&rdelja={loja}"
            f"&ctr={contrato}&srvcns=1&tcnscod={codigo_cns}{parametros}"
        )
     
        erro = False
        resposta = ""

        try:
            r = requests.get(url, timeout=100)
            r.raise_for_status()
            resposta = r.text.strip()
         
          
            if not resposta or len(resposta) == 2:
                resposta = "RESPOSTA NAO OBTIDA"
                erro = True

        except Exception as e:
            resposta = f"Erro na requisição: {e}"
            erro = True

       
        row_up = registros.copy()
        row_up.update({
            "url": url,
            "resposta_json": resposta,
            "erro": erro
        })

     
        resultados.append(row_up)

    return resultados



def processar_request(self, registro: Dict, conn_status2, conn_status4) -> None:
      
        new_array = {} 

        classLogger.logger.info('INICIO DO PROCESSAR REQUEST')
      
        try:
            cursor2 = conn_status2.cursor()
            cursor4 = conn_status4.cursor()
            
            #//* step 4 - REQUEST
            registro = request(self,registro)

            classLogger.logger.warn(registro)

            if registro["erro"] and registro["puglin"]:
                # ERRO DO PLUGIN 9
                status = 7
                resposta_json = registro["resposta_json"]
                sucesso = False

            elif registro["erro"]:
               
                status = 4
                resposta_json = "RESPOSTA NÃO OBTIDA"
                sucesso = False

            else:
                # SUCESSO
                registro, testeS = limpa_resposta_premium(self, registro)
                status = registro.get("new_status", 2)
                resposta_json = registro["resposta_json"]
                sucesso = True


            # Mapeia dados para salvar
            new_array["id_processo"] = registro["processo_id"]
            new_array["resposta_json"] = resposta_json
            new_array["new_status"] = status
            new_array["sucesso"] = sucesso
            new_array["time"] = time.strftime("t%Y-%m-%d %H:%M:%S")

            # Atualiza status
            if sucesso:
                atualiza_status_processando(self, registro, cursor2, conn_status2)
            else:
                atualiza_status_processando(self, registro, cursor4, conn_status4)

            # Salva no MongoDB
            colletion_repository = Coletion(collection.name, db, collection_json.name)

            if sucesso:
                get_id = colletion_repository.insert_document(testeS)
            else:
                get_id = colletion_repository.insert_document(new_array)

            cursor2.close()
            cursor4.close()
                            
        except Exception as e:
            teste = Dict[List] = {}
            classLogger.logger.error(f"Erro inesperado ao processar registro {registro.get('transacao_id')}: {str(e)}")
            registro['erro'] = True
            registro['resposta_json'] = f"ERRO INESPERADO: {str(e)}"

            teste['id_processo'] = registro['processo_id'],
            teste['resposta_json'] = f"ERRO INESPERADO: {str(e)}",
            teste['new_status'] =  7,
            teste['erro' ] = True
            teste['time'] =  time.strftime('t%Y-%m-%d %H:%M:%S') 
        

            cursor4 = conn_status4.cursor()
            atualiza_status_processando(self,registro, cursor4, conn_status4)
            colletion_repository = Coletion(collection.name,db,collection_json.name)
            get_id = colletion_repository.insert_document(teste)
            cursor4.close()