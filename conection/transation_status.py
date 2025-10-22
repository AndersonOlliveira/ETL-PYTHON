from conection.conexao import conexao
from tabulate import tabulate
import time
import json
from typing import Dict, List, Optional, Tuple
import threading
import classLogger
from conection import ConectionClass
from psycopg2.extras import RealDictCursor


def insert_transation(row):
     context_conection = conexao()
     if context_conection is None:
          return
     cursor = context_conection.cursor()

     print('sai no insert')
     # print(row)
     
     for registros in row:
          
      print(registros['processo_id'])
   
      cmd_insert = "INSERT INTO progestor.log_transacao (id_processo,campo_aquisicao,status) VALUES (%s,%s,%s);"
      values = registros['processo_id'],registros['campo_aquisicao'],1
      cursor.execute(cmd_insert,values)
      context_conection.commit()
      print(f"Dados Inseridos no Log transação")
     # da para recuperar o id e atribir a linha elaborar, 
     # elaborar algo para salvar estes logs de forma melhorada para náo ocupar espacos, 
     # pode se pensar em salvar no campo resposta_json o uma chave e acessar ela pra gerar os dados no caso os arquivos

     return True

def insertNewStatus(row):
     context_conection = conexao()
     if context_conection is None:
          return
     cursor = context_conection.cursor()
     
     # print(row['campo_aquisicao'])

   
     for registros in row:
           cmd_insert = "INSERT INTO progestor.log_transacao (id_processo,campo_aquisicao,status, sucesso,resposta_json) VALUES (%s,%s,%s,%s,%s);"
           values = registros['processo_id'],registros['campo_aquisicao'],registros['status'],registros['sucesso'],registros['resposta_json']
           cursor.execute(cmd_insert,values)
           context_conection.commit()
           print(f"Dados Inseridos Novos Dados log  transação")

     return True

def up_process(registros):
     print(registros)
     
     context_conection = conexao()
     if context_conection is None:
          return
     cursor = context_conection.cursor()
   
     for new_registro in registros:
      print(new_registro['processo_id'])
     
      cmd_update = """UPDATE progestor.processo SET finalizado = %s, data_finalizacao =%s WHERE processo_id = %s;"""
      values = (new_registro['new_status'],new_registro['data_finalizacao'],new_registro['processo_id'])
      cursor.execute(cmd_update,values)
      context_conection.commit()
      print(f"Processo tabela Progestror finalizado com sucesso!")

     return True


def push_status():
      context_conection = conexao()
      if context_conection is None:
          return
      cursor = context_conection.cursor()

      dados = ("""select DISTINCT ON( t.transacao_id) t.transacao_id as id_transacao, lt.log_id, 
               lt.id_processo from progestor.log_transacao as lt 
               LEFT JOIN progestor.transacao as t on (t.status = lt.status and t.status = 5 and t.id_processo = lt.id_processo) where t.id_processo = 322 and  t.data_cadastro < now() - interval '30 minutes' LIMIT 4;""")
      cursor.execute(dados)
      result_dados = cursor.fetchall()
      if not result_dados:
           return None
      colunas = [desc[0] for desc in cursor.description]
    
    #   linha = result_dados[0]
      registro = [dict(zip(colunas, linha)) for linha in  result_dados]
    
      return registro
 
 
def push_status_zero():
      context_conection = conexao()
      if context_conection is None:
          return
      cursor = context_conection.cursor()

      dados = ("""select DISTINCT ON( t.transacao_id) t.transacao_id as id_transacao, lt.log_id, 
               lt.id_processo from progestor.log_transacao as lt 
               LEFT JOIN progestor.transacao as t on (t.status = lt.status and t.status = 1 and t.id_processo = lt.id_processo) where  t.data_cadastro < now() - interval '30 minutes' limit 10;""")
      cursor.execute(dados)
      result_dados = cursor.fetchall()
      if not result_dados:
           return None
      colunas = [desc[0] for desc in cursor.description]
    
    #   linha = result_dados[0]
      registro = [dict(zip(colunas, linha)) for linha in  result_dados]
    
      return registro
 
 
 
def up_status_transaction(rows):
      context_conection = conexao()
      if context_conection is None:
          return
      cursor = context_conection.cursor()
      
      print('estou na transation')
      print(rows)
      for new in rows:
          print(new['id_processo'])
          print(new['log_id'])
          print(new['id_transacao'])
          cmd_update = """UPDATE progestor.transacao SET status = %s , sucesso = %s WHERE id_processo = %s and transacao_id = %s;"""
          values = (new['status'],new['sucesso'],new['id_processo'],new['id_transacao'])
          cursor.execute(cmd_update,values)
          time.sleep(10)
        
      context_conection.commit()
      print(f"Atualizado o Status da tabela transaco para {new['status']} Alterador com sucesso!")


      return True
       

def atualiza_status_processando(self,registro: Dict, cursor, connection):

    classLogger.logger.warn('estou aquiiiiiiii')
    classLogger.logger.warn(f"estou aquiiiiiiii {self.batch_counter_status1}")
    classLogger.logger.warn(f"estou aquiiiiiiii {connection}")
    classLogger.logger.warn(f"estou aquiiiiiiii {registro}")
    # classLogger.logger.warn(f"estou aquiiiiiiii {connection}")
  

    query = """
           INSERT INTO progestor.log_transacao 
               (id_processo, campo_aquisicao, status,resposta_json,sucesso)
           VALUES 
               (%s, %s, %s,%s,%s)
       """
    try:
        cursor.execute(query, (
            registro['processo_id'],
            registro['campo_aquisicao'],
            registro['new_status'],
            registro['resposta_json'],
            registro['sucesso']
        ))
     
        classLogger.logger.info('Tentando adquirir o lock...') # Adicione este log
        with self.lock:
            classLogger.logger.info('tenho algo aqui depios do lock')
            self.batch_counter_status1 += 1
            classLogger.logger.info('Contador depois do incremento: %s', self.batch_counter_status1)
            if self.batch_counter_status1 >= 1:
               connection.commit()
               self.batch_counter_status1 = 0

               classLogger.logger.info(f"Status atualizado para 1 - Transação {registro.get('transacao_id')}")

    except Exception as e:
     classLogger.logger.error(f"Erro ao atualizar status para 1: {str(e)}")



def process_status_five(self):
      
     classLogger.logger.warn('tenho dados')
     

     query_status = ("""SELECT DISTINCT (t.transacao_id) as id_transacao, lt.log_id, 
               lt.id_processo from progestor.log_transacao as lt 
               LEFT JOIN progestor.transacao as t on 
               (t.status = lt.status and t.status = 5 and t.id_processo = lt.id_processo) 
               where t.data_cadastro < now() - interval '30 minutes'    """)
    
     params = []

     if self.idProcesso is not None:
       query_status += ' AND t.id_processo = %s '
       params.append(self.idProcesso)
                              
     query_status += " ORDER BY lt.id_processo LIMIT %s;";
     params.append(self.batch_size)

            
     classLogger.logger.info(query_status)
     classLogger.logger.warn(f"[DEBUG SQL] Query gerada:\n{query_status}")
     classLogger.logger.warn(f"[DEBUG SQL] Parâmetros: {params}")
     
     with ConectionClass.DbConnect(self.config) as conn:
             with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query_status, tuple(params))
                registros = cursor.fetchall()
                classLogger.logger.info(f" Dados Capturados Status 5 {len(registros)} registros para processamento.")
                return [dict(registro) for registro in registros]
     
     
def set_campos_valores_aquisicao_status(self,status_registros):
    
          classLogger.logger.info(f" MEU DADOS PARA SE ATUALIZADO    {status_registros}")
          classLogger.logger.info(f" MEU DADOS PARA SE ATUALIZADO  MEU SELF  {self}")
    
          cmd_update = """UPDATE progestor.transacao SET status = %s , sucesso = %s WHERE id_processo = %s and transacao_id = %s;"""
          values = (status_registros['new_status'],status_registros['sucesso'],status_registros['id_processo'],status_registros['id_transacao'])
          with ConectionClass.DbConnect(self.config) as conn:
             with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                  cursor.execute(cmd_update,values)
                  conn.commit()
          time.sleep(10)

          return True          