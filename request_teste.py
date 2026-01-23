
def request(self, registro: Dict) -> Dict:
        
        dados_plugin = False

        rede = str(registro['rede'])
        loja = str(registro['lj'])
        contrato = str(registro['contrato'])
        codigo_cns = str(registro['codcns'])
        processo_id = str(registro['processo_id'])
        parametros = registro.get('parametros', '')


        classLogger.logger.info(f"minha rede de loja {loja}")

        url = (
            f"{self.servidor}/cns/json.chp?"
            f"progestor_prc={processo_id}&"
            f"rde={rede}&"
            f"rdelja={loja}&"
            f"ctr={contrato}&"
            f"srvcns=1&"
            f"tcnscod={codigo_cns}"
            f"{parametros}"
        )
        
        classLogger.logger.info(f"Requisição: {url}")

        erro = registro.get('erro', False)
        resposta = ""

        if not erro:
            try:
                response = requests.get(url, timeout=(300, 300))
                response.raise_for_status()
                resposta = response.text

                classLogger.logger.info(f"Resposta: {resposta[:100]}...")
                erro = False
            except requests.exceptions.Timeout:
                resposta = "TIMEOUT: Requisição excedeu 5 minutos"
                erro = True
                classLogger.logger.error(f"Timeout na requisição: {url}")

            except requests.exceptions.RequestException as e:
                resposta = f"ERRO: {str(e)}"
                erro = True
                classLogger.logger.error(f"Erro na requisição: {str(e)}")
                # ajuste neste local

        classLogger.logger.error(f"MINHA RESPOSTA TEM O QUE? {resposta}")
        # if not resposta or resposta.strip() == "" or len(resposta) == 2:
        if resposta.strip() == "":
        # if  resposta.strip() == "" or len(resposta) == 2:
            resposta = "RESPOSTA NâO OBTIDA"
            erro = True 
        

        else:
          
          erro = False
          if not len(resposta) == 2:
         
            try:
                dados = json.loads(resposta)

                print(f"MEU JSON DENTRO DE DADOS {len(resposta)}")
            
                # if dados:
                print(f"MEU JSON DENTRO DE DADOS {dados}")
                lista_registros = dados.get("registro", [])

                contador_total = len(lista_registros)
                contador_plugin_9 = sum(
                        1 for item in lista_registros
                        if item.get("numero_plugin") == "9")
                        #    for item in lista_registros:
                        #         print(f"Plugin: {item.get('numero_plugin')}")
                        #         print(f"Código: {item.get('codigo_da_mensagem')}")
                        #         print(f"Descrição: {item.get('descricao_da_mensagem')}")
                        #         print("----")

                        #    print(f"Total de retornos: {contador_total}")
                        #    print(f"Total plugin 9: {contador_plugin_9}")
                
                if contador_total > 0 and contador_plugin_9 == contador_total:
                    erro = True
                    dados_plugin = True
            except json.JSONDecodeError:
                resposta = "RESPOSTA INVALIDA — NÃO É UM JSON"
                erro = True

        print(f"MEUS DADOS DE RESPOSTA {resposta}")
        
        registro["url"] = url
        registro["resposta_json"] = resposta
        registro["erro"] = erro
        registro["puglin"] = dados_plugin

        print(f"meu registro final: {registro}")

        return registro


if __name__ . main():