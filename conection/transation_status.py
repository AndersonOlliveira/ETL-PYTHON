from conection.conexao import conexao
from tabulate import tabulate
import json



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
      print(f"Dados Inseridos")
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
           print(f"Dados Inseridos")

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
      print(f"Processo finalizado com sucesso!")

     return True
