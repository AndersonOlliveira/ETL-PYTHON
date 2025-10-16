from conection.busca_dados import selecionar
from tratamento.incia_process import prepara_campos
from tratamento.resposta import respost_transfor
from conection.transation_status import insert_transation
from conection.transation_status import insertNewStatus
from requestUrl.request_url import request_all
# from FinalProces.verifiy_process import up_process
from tabulate import tabulate
import json

def main():
       
        dados = selecionar()
        if dados is None:
          print('Sem dados localizado para o id informado')
          # se e none vou realizar o up na minha tabela para processar
          return
      #   print("dados selecionados")
      #   print(dados)
      #   print(dados["processo_id"])
      #   print(dados["contrato"])
      #   print(dados["campo_aquisicao"])
        
        
      #   traformado em lista agora percorrer os dados
      #   para percorrer
      #   for retorno_dados in dados:
         #  print("dados selecionados")
         #  print(retorno_dados)
         #  print(retorno_dados["processo_id"])
         #  print(retorno_dados["contrato"])
         #  print(retorno_dados["campo_aquisicao"])
        
         
        
        result_campos =  prepara_campos(dados)
        
      #   print('meus campos')
      #   print(result_campos)
        
		#insert base log_trasancao 
        info_transation = insert_transation(result_campos)
      #   print(f"o que tenho de resultado {info_transation}")
        if(info_transation):
               #aqui vou fazer a solicitacao do request
               reult_request = request_all(result_campos)
            #    print('já estou pegando o retorno')
               #print(reult_request)
               tratemento_reposta = respost_transfor(reult_request)
            #    print('meu retorno do tramento da resposta')
            #    print(tratemento_reposta)
             
               new =[]
               for t in tratemento_reposta:
                     t['status'] = 2
                     t['sucesso'] = True
                     
                     new.append(t.copy())
                 
               # print(new)  
               insertNewStatus(new)
               
               
               
               
               
               
               
              





if __name__ == "__main__":
     main()