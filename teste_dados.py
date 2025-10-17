from conection.transation_status import (
    push_status,
    up_status_transaction,
    push_status_zero,
)
import time
new = []

def teste():
    dados = push_status()
    print("tenho dados aqui de retorno")
    print(dados)
    if dados is None:
        print("Nada localicalizado com o status 5")
        # se e none vou realizar o up na minha tabela para processar
        return  # realizo o update quando ele esta no status 5 pois já tem dados processado
    
    
    for tdados in dados:

        row_out = tdados.copy()
        row_out.update(
            {
                "status": 3,
                "sucesso": True,
            }
        )

        new.append(row_out)
        
        print('novos dados populados')
        print(new)

    up_status_transaction(new)





def verificar_dados():

    dados_paradoos = push_status_zero()
    print(dados_paradoos)
    if dados_paradoos is None:
        print("Nada localizado com o status 1")
        # se é None vou realizar o up na minha tabela para processar
        return

    print(len(dados_paradoos))
    for tdados in dados_paradoos:

        row_out = tdados.copy()
        row_out.update(
            {
                "status": 0,
                "sucesso": False,
            }
        )

        new.append(row_out)

    print("meu novos dados")
    print(new)
    up_status_transaction(new)


def main():
    print("=== Inciando processo")
    teste()
#     while True:
#          time.sleep(60)
#          verificar_dados()
#          print("=== final processo")


if __name__ == "__main__":
    main()
