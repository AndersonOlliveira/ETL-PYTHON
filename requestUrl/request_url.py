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

        rede = str(registro['rede'])
        loja = str(registro['loja'])
        contrato = str(registro['contrato'])
        codigo_cns = str(registro['codcns'])
        processo_id = str(registro['processo_id'])
        parametros = registro.get('parametros', '')

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

        if not resposta or resposta.strip() == "" or len(resposta) == 2:
            resposta = "RESPOSTA NAO OBTIDA"
            erro = True

        registro['url'] = url
        registro['resposta_json'] = resposta
        registro['erro'] = erro

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

            #//* step 5 e 6 ou 7
            if registro['erro']:
                #//* step 7
                registro['resposta_json'] = 'ERRO NO PROCESSAMENTO'
                registro['new_status'] = 7
                registro['sucesso'] = False

                new_array['id_processo'] = registro['processo_id']
                new_array['resposta_json'] = 'ERRO NO PROCESSAMENTO'
                new_array['new_status'] = 7
                new_array['sucesso' ] = False
                new_array['time'] =  time.strftime('t%Y-%m-%d %H:%M:%S') 
        
                
                atualiza_status_processando(self,registro, cursor4, conn_status4)
                colletion_repository = Coletion(collection.name,db,collection_json.name)
               
                get_id = colletion_repository.insert_document(new_array)
            else:
                #//* step 5 e 6
                registro , testeS = limpa_resposta_premium(self,registro)
                
                
                atualiza_status_processando(self,registro, cursor2, conn_status2)
               
                colletion_repository = Coletion(collection.name,db,collection_json.name)
                classLogger.logger.warning(f"*-*" * 5);
                
                get_id = colletion_repository.insert_document(testeS)
               

                
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