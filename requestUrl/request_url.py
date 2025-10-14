import requests


def request_all(row):

 print(row)
 rede = str(row.get('rede', ''))
 loja= str(row.get('loja',''))
 contrato = str(row.get('contrato', ''))
 codigo_cns = str(row.get('codcns', ''))
 processo_id = row.get('processo_id')
 parametros = row.get('paramentros', '')

 servidor = 'proscore.com.br'
 url = (
  f"https://{servidor}/cns/json.chp?"
  f"progestor_prc={processo_id}&rde={rede}&rdelja={loja}"
  f"&ctr={contrato}&srvcns=1&tcnscod=281998{parametros}"
 )
 print(f"URL:", url)
 
 erro = False
 resposta = ""
 try:
        r = requests.get(url, timeout=300)  # timeout em segundos
        r.raise_for_status()  # levanta erro se status != 200
        resposta = r.text
        #erro = True
        print("Resposta:", resposta)
        if not None:
              erro = True
       
        else:
         erro = False

 except Exception as e:
        resposta = str(e)
        erro = True

 if not resposta.strip():
        resposta = "RESPOSTA NAO OBTIDA"
        erro = True

    # --- Montando linha de saída ---
 output = {
        "url": url,
        "resposta_json": resposta,
        "erro": erro
    }
 
 row.update(output)
 
  
 return row

 #print(f"RESULTADO DA SOLICITACAO:", output)