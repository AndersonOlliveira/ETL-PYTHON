import re
import classLogger
from typing import Dict, List, Optional, Tuple

def prepara_campos(rows):
    resultados = []

    for retorno_dados in rows:
     
     #    print(retorno_dados)
        # Captura valores
        linha = retorno_dados.get("campo_aquisicao") or ""
        campos_aquisicao = retorno_dados.get("campos_aquisicao") or "tcpfcnpj"

    
     #    print(f"\nRecebido campo_aquisicao: {linha}")
     #    print(f"Campos de aquisição: {campos_aquisicao}")

    
        campos = campos_aquisicao.split(",")
        valores = linha.split(";")

        erro = False
        parametros = ""

        # Gera parâmetros da query
        for i in range(min(len(campos), len(valores))):
            cAquisicao = campos[i].strip()
            valor = valores[i].strip()
            try:
                parametros += f"&{cAquisicao}={valor}"
            except Exception as e:
                erro = True
                print(f"Erro ao gerar parâmetros: {e}")

        # Limpa caracteres estranhos (ex: r|)
        campo_aquisicao_limpo = re.sub(r"r\|", " ", linha)

        # Atualiza  novos campos
        row_out = retorno_dados.copy()
        row_out.update({
            "parametros": parametros,
            "campo_aquisicao": campo_aquisicao_limpo,
            "erro": erro,
            "status": 0
        })

        resultados.append(row_out)
        
     #    print(resultados)

    return resultados




def set_campos_valores_aquisicao(registro: Dict) -> Tuple[Dict, bool]:

    linha = registro.get('campo_aquisicao', '') or ''  
    linhas = '10676485774;10676485775;10676485776'

    campos_aquisicao = registro.get('campos_aquisicao', '') or 'tcpfcnpj'

    classLogger.logger.warning(f"Campos aquisição: {campos_aquisicao}")

    campos = [c.strip() for c in campos_aquisicao.split(',')]
    valores = [v.strip() for v in linha.split(';')]
    valoress = [v.strip() for v in linhas.split(';')]

    classLogger.logger.warning(f"Quantidade de valores: {len(valores)}")
    classLogger.logger.warning(f"Quantidade de valores: {valores}")
    classLogger.logger.warning(f"meus campos depois do split: {campos}")

    erro = False
    parametros = ""

    try:
        for i, (campo) in enumerate(campos):
            if i < len(valoress):
                
                valor = valoress[i]
        
            # valor = valor[i] if i < len(valor) else ""
            classLogger.logger.info(f" meu enumerate :: {(valor)}")
            classLogger.logger.info(f" meu campo {(campo)}")
                    
            if 'tcpfcnpj' in campo and len(valor) in [11,14]:
                    parametros += f"&{'tcpfcnpj'}={valor}"
                    classLogger.logger.info(f"CPF/CNPJ atribuído a {campo}: {valor}")
                        
            else:
                    parametros += f"&{campo}={''}"

                    classLogger.logger.info(f"Parâmetros finais: {parametros}")
                    classLogger.logger.warning(f"Valor faltando para campo {campo} no registro {registro.get('transacao_id')}")

        campo_aquisicao_limpo = re.sub(r'\|', ' ', linha)

        registro['parametros'] = parametros
        registro['campo_aquisicao'] = campo_aquisicao_limpo
        registro['erro'] = erro
        registro['status'] = 0

        classLogger.logger.debug(f"Parâmetros gerados: {parametros}")

    except Exception as e:
        classLogger.logger.error(f"Erro ao gerar parâmetros: {str(e)}")
        erro = True
        registro['erro'] = erro

        
        classLogger.logger.warn(f"meus parametros {registro}")

    return registro, erro