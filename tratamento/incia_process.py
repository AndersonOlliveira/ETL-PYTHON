import re
def prepara_campos(row):

     print(f"meus dados vindo para a tela de row")
    #  print(row)

     #procuro o campo 
     linha = row.get("campo_aquisicao") or ""
     campos_aquisicao = row.get("campos_aquisicao") or "tcpfcnpj"
     print(linha)
     print(f"que campo recebi aqui")
     print(campos_aquisicao)

     campos = campos_aquisicao.split(",")
     valores  = linha.split(';')

     erro = False
     paramentos = ""

     for i in range(min(len(campos), len(valores))):
          cAquisicao = campos[i].strip()
          valor = valores[i].strip()
          try:
               paramentos +=f"&{cAquisicao}={valor}"
          except Exception as e:
           erro =True
           print(f"Erro ao gerar Parametros da consulta: {e}")

     campo_aquisicao_limpo = re.sub("r\|", " ", linha)
      
     row_out = row.copy()
     row_out.update({
        "paramentros": paramentos,
        "campo_aquisicao": campo_aquisicao_limpo,
        "erro": erro,
        "status": 0
     })
    #  print(row_out)
     return row_out


