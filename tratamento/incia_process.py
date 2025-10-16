import re

def prepara_campos(rows):
    resultados = []

    for retorno_dados in rows:
     
     #    print(retorno_dados)
        # Captura valores
        linha = retorno_dados.get("campo_aquisicao") or ""
        campos_aquisicao = retorno_dados.get("campos_aquisicao") or "tcpfcnpj"

        # Debug opcional
     #    print(f"\nRecebido campo_aquisicao: {linha}")
     #    print(f"Campos de aquisição: {campos_aquisicao}")

        # Divide campos e valores
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

        # Limpa possíveis caracteres estranhos (ex: r|)
        campo_aquisicao_limpo = re.sub(r"r\|", " ", linha)

        # Atualiza o dicionário com os novos campos
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
