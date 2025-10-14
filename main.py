from conection.busca_dados import selecionar
from tratamento.incia_process import prepara_campos
from tratamento.resposta import respost_transfor
from conection.transation_status import insert_transation
from conection.transation_status import insertNewStatus
from requestUrl.request_url import request_all
from tabulate import tabulate
import json

def main():

        dados = selecionar()
        print("dados selecionados")
        # print(dados)
        print(dados["processo_id"])
        print(dados["contrato"])
        print(dados["campo_aquisicao"])
        
	
        result_campos =  prepara_campos(dados)
        
		#insert base log_trasancao 
        info_transation = insert_transation(result_campos)
        print(f"o que tenho de resultado {info_transation}")
        if(info_transation):
               #aqui vou fazer a solicitacao do request
               reult_request = request_all(result_campos)
            #    print('já estou pegando o retorno')
               #print(reult_request)
               tratemento_reposta = respost_transfor(reult_request)
            #    print('meu retorno do tramento da resposta')
            #    print(tratemento_reposta)
               
               new_status =  tratemento_reposta.get('status','')
               new_sucesso =  tratemento_reposta.get('status','')
               new_status = 2
               new_sucesso = True
               tratemento_reposta['status'] = new_status
               tratemento_reposta['sucesso'] = new_sucesso
               insertNewStatus(tratemento_reposta)
               
               
               
               
               
               
               
              





if __name__ == "__main__":
     main()