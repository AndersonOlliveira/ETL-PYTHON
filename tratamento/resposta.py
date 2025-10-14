import json
import re

def respost_transfor(dados):
    print(dados)
    print('éstou recebendo os dados')
    resposta = dados.get('resposta_json', '')
    
    
    resposta_limpa = re.sub(r"[\n\r\t]+", "" ,resposta).strip()
    
    dados['resposta_json'] = resposta_limpa
    
    
    return dados
    
    
    