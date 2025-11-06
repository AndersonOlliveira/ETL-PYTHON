import json
import re
import classLogger
from typing import Dict, List, Optional, Tuple, Any
import time

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





def limpa_resposta_premium(self, registro: dict) -> tuple[dict, dict]:
            # dicionário de teste que será retornado/gravado
            teste: dict = {}

            resposta_premium = registro.get('resposta_json', '') or ''

            resposta_premium = re.sub(r'\\n', '', resposta_premium)

            registro['resposta_json'] = resposta_premium
            registro['new_status'] = 2
            registro['sucesso'] = True

            # preferir usar get para suportar ambos os nomes de campo
            teste['id_processo'] = registro.get('id_processo') or registro.get('processo_id')
            teste['transacao_id'] = registro.get('transacao_id') or registro.get('transacao_id')
            teste['resposta_json'] = resposta_premium
            teste['new_status'] = 2
            teste['sucesso'] = True
            teste['campo_aquisicao'] = registro.get('campo_aquisicao')
            teste['time'] =  time.strftime('t%Y-%m-%d %H:%M:%S') 

            classLogger.logger.error(f"Resposta premium limpa: {resposta_premium[:100]}...")
            classLogger.logger.error(f"Resposta do teste: {teste}...")

    
            return registro, teste
    