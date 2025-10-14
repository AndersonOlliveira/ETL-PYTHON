from conection.conexao import conexao
from tabulate import tabulate
import json

def selecionar():
      context_conection = conexao()
      if context_conection is None:
          return

      cursor = context_conection.cursor()

      dados = ("""SELECT p.processo_id,
                    p.contrato,p.rede,p.codcns,p.nome_arquivo,p.aceite_execucao,	
                    p.mensagem_alerta,p.data_cadastro,p.configuracao_json,
                    p.campos_aquisicao,p.loja,p.finalizado,p.data_finalizacao,p.pause,
                    t.transacao_id,t.id_processo,t.campo_aquisicao,t.status,t.sucesso,
	                t.data_cadastro as data_cadastro_transacao,t.resposta,t.resposta_json 
                    FROM progestor.transacao t INNER JOIN progestor.processo p ON p.processo_id = t.id_processo 
                    WHERE t.status in (0,4) AND (p.finalizado = false OR p.finalizado is null) AND 
                    p.pause = false AND p.error = false AND p.processo_id = 303
            
               ORDER BY random() limit 1;""")
      cursor.execute(dados)
      result_dados = cursor.fetchall()
      colunas = [desc[0] for desc in cursor.description]
      if not result_dados:
           return None
      linha = result_dados[0]
      registro = dict(zip(colunas, linha))
    
      return registro
#  where p.processo_id =  and t.transacao_id in (2995922,2995923,2995924,2995925,2995926,2995927,2995928,2995929)

    #    print(tabulate(result_dados,headers=colunas,tablefmt="grid"))
    #   print("\n linha ind")
    #   for linha in result_dados:
    #           print(linha)
    #        # transforma em lista de dicionários
        #    registros = [dict(zip(colunas, linha)) for linha in result_dados]
        #    print(json.dumps(registros, indent=4, ensure_ascii=False))
        #    return registros
