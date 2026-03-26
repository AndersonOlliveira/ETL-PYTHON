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
      print(f"processo_id {new_registro['processo_id']}")
     
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



    query = """
           INSERT INTO progestor.log_transacao 
               (id_processo, campo_aquisicao, status,sucesso)
           VALUES 
               (%s, %s, %s,%s)  """

    
    try:
        cursor.execute(query, (
            registro['processo_id'],
            registro['campo_aquisicao'],
            registro['new_status'],
          #   registro['resposta_json'],
            registro['sucesso']
        ))
     
      
        with self.lock:
          
            self.batch_counter_status1 += 1
           
            if self.batch_counter_status1 >= 1:
               connection.commit()
               self.batch_counter_status1 = 0

               classLogger.logger.info(f"Status atualizado para :: {registro.get('new_status')} - Transação {registro.get('transacao_id')}")

    except Exception as e:
     classLogger.logger.error(f"Erro ao atualizar status para :: {registro.get('new_status')} - {str(e)}")


# grava no banco a resposta com o erro do puglin
def atualiza_status_processando_seven(self,registro: Dict, cursor, connection):
    
          print(f"QUE DADOS VEM AQUI")
          print(f"QUE DADOS VEM AQUI{registro}")
          print(f"QUAL E O MEU ID DO REGISTRO::{registro['transacao_id']}")
          
          tentativas = process_status_for(self, registro['transacao_id'])
          
          print(f"MINHA QUANTIDADE DE TENTATIVAS  {tentativas['total']}")
          
          MAX_TENTATIVAS = 4
          bloquear = False

          if(tentativas['total'] >= MAX_TENTATIVAS and tentativas['info_eleven'] == 0):
               registro['new_status'] = 10
               mensagens_concat = (
               f"Transação bloqueada após {tentativas['total']} tentativas "
               f"sem resposta da API") 
               bloquear = True
          elif tentativas['info_eleven'] > 0:
               registro['new_status'] = 3
               registro['sucesso'] = True
               mensagens_concat = (
               f"Transação com retorno invalido depois de x {tentativas['total']} tentativas "
               f"sem resposta da API") 
               bloquear = True
               registro['resposta_json'] = 'error'
          else:   

            # segue fluxo normal
              mensagens_concat = ""
         
          if not bloquear:
               json_resposta = registro['resposta_json']
               try:
                    dados = json.loads(json_resposta)
                    lista_registros = dados.get("registro", [])
                    if lista_registros:
                         mensagens_concat = "; ".join(f"[{item.get('codigo_da_mensagem')}] {item.get('descricao_da_mensagem')}"
                                        for item in lista_registros)
                    else:
                         mensagens_concat = registro['resposta_json']

               except Exception as e:
                    print("Erro ao abrir JSON:", e)
                    mensagens_concat = json_resposta
              
          
         
         
          print(f"Mensagens concatenadas:")
          # print(f"Mensagens concatenadas: {registro['resposta_json']}")
          print(mensagens_concat)

          print(f"""Meu status atualizado:: {registro['new_status']} - Transação {registro['transacao_id']}""")

               
          colunas = [
          "id_processo",
          "campo_aquisicao",
          "status",
          "sucesso",
          "resposta"
          ]

          valores = [
          registro['processo_id'],
          registro['campo_aquisicao'],
          registro['new_status'],
          registro['sucesso'],
          mensagens_concat
          ]

          placeholders = ["%s", "%s", "%s", "%s","%s"]

          # Só adiciona resposta_json quando new_status == 4
          if registro['new_status'] == 4:
               colunas.append("resposta_json")
               valores.append(registro['transacao_id'])
               placeholders.append("%s")
          
          if registro['new_status'] == 3:
               colunas.append("resposta_json")
               valores.append(registro['resposta_json'])
               placeholders.append("%s")

          query = f"""
          INSERT INTO progestor.log_transacao
          ({", ".join(colunas)})
          VALUES
          ({", ".join(placeholders)})
          """

          print(f"Meus SQL{query}")
          try:
               cursor.execute(query,valores)
               # registro['processo_id'],
               # registro['campo_aquisicao'],
               # registro['new_status'],
               # registro['sucesso'],
               # mensagens_concat
          #   ))
          
          
               with self.lock:
                    
                    self.batch_counter_status1 += 1
                    
                    if self.batch_counter_status1 >= 1:
                         connection.commit()
                         self.batch_counter_status1 = 0

                         classLogger.logger.info(f"Status atualizado para :: {registro.get('new_status')} - Transação {registro.get('transacao_id')}")

          except Exception as e:
           classLogger.logger.error(f"NOVO ERRO PARA SALVAR :: {registro.get('new_status')} - {str(e)}")



def process_status_five(self):
      
     # classLogger.logger.warn('tenho dados')
     

     query_status = ("""SELECT  (t.transacao_id) as id_transacao,t.id_processo
                      FROM progestor.transacao as t 
                      where t.status = 5  and t.data_cadastro < now() - interval '30 minutes'    """)
    
     params = []

     if self.idProcesso is not None:
       query_status += ' AND t.id_processo = %s '
       params.append(self.idProcesso)
                              
     query_status += " ORDER BY random()  LIMIT %s;";
     params.append(self.batch_size)

          
     with ConectionClass.DbConnect(self.config) as conn:
             with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query_status, tuple(params))
                registros = cursor.fetchall()
                classLogger.logger.info(f" Dados Capturados Status 5 {len(registros)} registros para processamento.")
                return [dict(registro) for registro in registros]
     
     

def process_status_zero(self):
      

     

     query_status = ("""SELECT  (t.transacao_id) as id_transacao,t.id_processo
                      FROM progestor.transacao as t 
                      where t.status in (1) and t.data_cadastro < now() - interval '30 minutes'    """)
    
     params = []

     if self.idProcesso is not None:
       query_status += ' AND t.id_processo = %s '
       params.append(self.idProcesso)
                              
     query_status += " ORDER BY RANDOM() LIMIT %s;";
     params.append(self.batch_size)

            
     # classLogger.logger.info(query_status)
     # classLogger.logger.warn(f"[DEBUG SQL] Query gerada:\n{query_status}")
     # classLogger.logger.warn(f"[DEBUG SQL] Parâmetros: {params}")
     
     with ConectionClass.DbConnect(self.config) as conn:
             with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query_status, tuple(params))
                registros = cursor.fetchall()
                classLogger.logger.info(f" Dados Capturados Status 1 {len(registros)} registros para processamento.")
                return [dict(registro) for registro in registros]
        

def process_status_for(self,trasancao):
      
     print(f"ESTOU CHAMANDO O PROCESS FOR ")
     
     query = """
        SELECT COUNT(*) AS total,
         (select count(t.status) as info_eleven FROM progestor.log_transacao as t 
          where t.status = 11 and t.resposta_json::text = '%s' limit 1)
          FROM progestor.log_transacao AS t
          WHERE t.status IN (4,7)
          AND t.resposta_json::text = '%s' and t.resposta_json is not null
    """
     try:
          with ConectionClass.DbConnect(self.config) as conn:
           with conn.cursor() as cursor:
               cursor.execute(query, (trasancao,trasancao,))
               print(f"meu resultado{cursor}")
               resultado = cursor.fetchone()  # <-- UMA LINHA

               if resultado:
                    total, info_eleven = resultado
                    return {
                        "total": total,
                        "info_eleven": info_eleven
                    }
     except Exception as e:
       classLogger.logger.error(f"FALHA EM PEGAR DADOS  {str(e)}")



def process_status_eleven(self,trasancao):
      
     print(f"ESTOU CHAMANDO O PROCESS FOR ")
     
     query = """
        SELECT COUNT(*) AS total
        FROM progestor.log_transacao AS t
        WHERE t.status IN (11)
        AND t.campo_aquisicao is not null and t.resposta_json is not null and t.id_processo = %s 
    """
     try:
          with ConectionClass.DbConnect(self.config) as conn:
           with conn.cursor() as cursor:
               cursor.execute(query, (trasancao,))
               total = cursor.fetchone()[0]
               return total
     except Exception as e:
       classLogger.logger.error(f"FALHA EM PEGAR DADOS  {str(e)}")
     

def up_status(self,status_registros:Dict, cursor,connection):
    
    
     cmd_update = """UPDATE progestor.transacao SET 
                  status = %s , sucesso = %s WHERE id_processo = %s and transacao_id = %s;"""
         
     try:
          cursor.execute(cmd_update,(
               status_registros['new_status'],
               status_registros['sucesso'],
               status_registros['id_processo'],
               status_registros['id_transacao']
          ))
         
          with self.lock:
          #   classLogger.logger.info('Lock do up status')
            self.batch_counter_status1 += 1
          #   classLogger.logger.info('Contador depois do incremento do status: %s', self.batch_counter_status1)
            if self.batch_counter_status1 >= 1:
               connection.commit()
               self.batch_counter_status1 = 0

               classLogger.logger.info(f"Status atualizado para {status_registros.get('new_status')} - Transação {status_registros.get('id_transacao')}")

     except Exception as e:
      classLogger.logger.error(f"Erro ao atualizar status para 1: {str(e)}")
        

def process_finish_all(self):
          
     query = ("""SELECT p.processo_id,p.data_cadastro,p.data_finalizacao,
               p.finalizado, 
          p.data_cadastro + interval '3 days' < now() as iniciado_a_mais_de_tres_dias,
               p.error,
          
               COALESCE(SUM(CASE WHEN t.status != 6 THEN 1 ELSE 0 END), 0) AS qt_registros_total,
               COALESCE(SUM(CASE WHEN t.status = 3 THEN 1 ELSE 0 END), 0) AS qt_registros_finalizados,
	          COALESCE(SUM(CASE WHEN t.status = 7 THEN 1 ELSE 0 END), 0) AS qt_registros_erros ,
	          COALESCE(SUM(CASE WHEN t.status = 8 THEN 1 ELSE 0 END), 0) AS qt_registros_erros_resposta,
               COALESCE(SUM(CASE WHEN t.status = 10 THEN 1 ELSE 0 END), 0) AS qt_registros_erros_tentativas
              FROM 
               progestor.processo as p
          INNER JOIN progestor.transacao as t on (t.id_processo = p.processo_id)
          WHERE 
               (p.finalizado = false or p.finalizado is null) and
               p.pause = false 
                AND p.error = false AND p.processo_id = 170
          GROUP BY p.processo_id,p.data_cadastro,p.data_finalizacao, p.finalizado,p.error
          HAVING COUNT(t.transacao_id) > 0  
          ORDER BY p.processo_id desc;""")
               
               
     with ConectionClass.DbConnect(self.config) as conn:
             with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query,)
                registros = cursor.fetchall()
                classLogger.logger.info(f" Dados Capturados do que esta em andamento {len(registros)} registros para processamento.")
                return [dict(registro) for registro in registros]






def up_finish_process(self, status_registros:Dict, cursor,connection):

      
     cmd_update = """UPDATE progestor.processo
                     SET finalizado = %s, data_finalizacao = %s 
                     WHERE processo_id = %s;"""
                     
     try:
         cursor.execute(cmd_update,(
              status_registros['new_status'],
              status_registros['data_finalizacao'],
              status_registros['processo_id'],
         ))
                     
     
             
         with self.lock:
             self.batch_counter_status1 += 1
             
         return status_registros 
         
     except Exception as e:
         classLogger.logger.error(f"Erro ao gerar parâmetros: {str(e)}")
         raise 


def up_status_process_seven(self, status_registros:Dict, cursor,connection):

     classLogger.logger.info(f" MEU DADOS PARA SE ATUALIZADO STATUS 7 ou 8   {status_registros}")

      
     cmd_update = """UPDATE progestor.processo
                     SET  data_finalizacao = %s, error = %s
                     WHERE processo_id = %s;"""
                     
     try:
         cursor.execute(cmd_update,(
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
              True,
              status_registros,
         ))
                     
     
             
         with self.lock:
             self.batch_counter_status1 += 1
             
         return status_registros 
         
     except Exception as e:
         classLogger.logger.error(f"Erro ao gerar parâmetros: {str(e)}")
         raise 



def up_status_process(self,registros:Dict, cursor,connection):
     # REALIZO O UP SE TIVER MAIS DE 3 DIAS NO STATUS 7

     classLogger.logger.info(f"ids para atualizar: {registros}")    
    
     cmd_update = """UPDATE progestor.transacao SET 
                  status = %s , sucesso = %s WHERE id_processo = %s and status = %s;"""
         
     try:
          cursor.execute(cmd_update,(
               3,
               True,
               registros,
               7
          ))
         
          with self.lock:
          
            self.batch_counter_status1 += 1
            if self.batch_counter_status1 >= 1:
               connection.commit()
               self.batch_counter_status1 = 0

               classLogger.logger.info(f"Status atualizado para o Status - Para todos que tem o id {registros}")

     except Exception as e:
      classLogger.logger.error(f"Erro ao atualizar status para 3: {str(e)}")
        

def up_status_processs(self,registros:Dict, cursor,connection):
     # REALIZO O UP SE TIVER MAIS DE 3 DIAS NO STATUS 10

     classLogger.logger.info(f"ids para atualizar: {registros}")    
    
     cmd_update = """UPDATE progestor.transacao SET 
                  status = %s , sucesso = %s WHERE id_processo = %s and status = %s;"""
         
     try:
          cursor.execute(cmd_update,(
               3,
               True,
               registros,
               10
          ))
         
          with self.lock:
          
            self.batch_counter_status1 += 1
            if self.batch_counter_status1 >= 1:
               connection.commit()
               self.batch_counter_status1 = 0

               classLogger.logger.info(f"Status atualizado para o Status - Para todos que tem o id {registros}")

     except Exception as e:
      classLogger.logger.error(f"Erro ao atualizar status para 3: {str(e)}")
        
