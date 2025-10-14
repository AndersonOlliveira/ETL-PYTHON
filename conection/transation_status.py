from conection.conexao import conexao
from tabulate import tabulate
import json



def insert_transation(row):
     context_conection = conexao()
     if context_conection is None:
          return
     cursor = context_conection.cursor()

   
     cmd_insert = "INSERT INTO progestor.log_transacao (id_processo,campo_aquisicao,status) VALUES (%s,%s,%s);"
     values = row['processo_id'],row['campo_aquisicao'],1
     cursor.execute(cmd_insert,values)
     context_conection.commit()
     print(f"Dados Inseridos")
     #da para recuperar o id e atribir a linha elaborar, 
     # elaborar algo para salvar estes logs de forma melhorada para náo ocupar espacos, 
     #pode se pensar em salvar no campo resposta_json o uma chave e acessar ela pra gerar os dados no caso os arquivos

     return True

def insertNewStatus(row):
     context_conection = conexao()
     if context_conection is None:
          return
     cursor = context_conection.cursor()
     
     print(row['campo_aquisicao'])

     
     cmd_insert = "INSERT INTO progestor.log_transacao (id_processo,campo_aquisicao,status, sucesso,resposta_json) VALUES (%s,%s,%s,%s,%s);"
     values = row['processo_id'],row['campo_aquisicao'],row['status'],row['sucesso'],row['resposta_json']
     cursor.execute(cmd_insert,values)
     context_conection.commit()
     print(f"Dados Inseridos")

     return True
