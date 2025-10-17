from conection.push_process import process
from conection.transation_status import up_process
from tabulate import tabulate
from datetime import datetime


def new_main():
    
   
   new =[]
   dados,colunas = process()
   print(dados)

   for result in dados: 
       
    #    print(result['iniciado_a_mais_de_tres_dias'])
      inicio = result['iniciado_a_mais_de_tres_dias']
      rTotal = result['qt_registros_total']
      rFinalizado = result['qt_registros_finalizados']
       
      if rFinalizado == rTotal and rTotal > 0:
        # print(result['processo_id'])
        result['data_finalizacao'] = datetime.now()
        result.update(result.copy())
        row_out = result.copy()
        row_out.update({
         "new_status": True,
        })
        

        new.append(row_out)
        
        
         #realizo o up dentro da tabela 
        
            
 
 
   if new is not None:
      result = up_process(new)   
    # print('saiu aqui o meu resultado')
      print(result)
          
           
         
    
#    print(tabulate(dados, headers=colunas, tablefmf="grid"))







if __name__ == "__main__":
     new_main()