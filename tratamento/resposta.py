import json
import re

def respost_transfor(dados):
    print(dados)
    print('éstou recebendo os dados')
    new =[]
    for registro in dados:
    
        resposta = registro.get('resposta_json', '')
    
    
        resposta_limpa = re.sub(r"[\n\r\t]+", "" ,resposta).strip()
    
        registro['resposta_json'] = resposta_limpa
        new.append(registro.copy())
    
    return new
    
    
    