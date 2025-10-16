import requests

def request_all(rows):
    
    print(rows)
    resultados = []

#     print('Estou no request')
#     print(f"Quantidade de registros recebidos: {len(rows)}")

    for registros in rows:
        rede = str(registros.get('rede', ''))
        loja = str(registros.get('loja', ''))
        contrato = str(registros.get('contrato', ''))
        codigo_cns = str(registros.get('codcns', ''))
        processo_id = registros.get('processo_id')
        parametros = registros.get('parametros', '')  # corrigido: era "paramentros"
        servidor = 'proscore.com.br'

        # Monta URL
        url = (
            f"https://{servidor}/cns/json.chp?"
            f"progestor_prc={processo_id}&rde={rede}&rdelja={loja}"
            f"&ctr={contrato}&srvcns=1&tcnscod={codigo_cns}{parametros}"
        )

     
        erro = False
        resposta = ""

        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            resposta = r.text.strip()

            if not resposta:
                resposta = "RESPOSTA NAO OBTIDA"
                erro = True

        except Exception as e:
            resposta = f"Erro na requisição: {e}"
            erro = True

        # Monta saída
        row_up = registros.copy()
        row_up.update({
            "url": url,
            "resposta_json": resposta,
            "erro": erro
        })

     
        resultados.append(row_up)

    return resultados
