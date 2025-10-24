from teste_log import logger_finalizar_erro
import os


def main():
    pasta = 'arquivos_'
    if not os.path.exists(pasta):
        os.mkdir(pasta)
    else:

        logger_finalizar_erro.info('pasta exite')


if __name__ == '__main__':
    main()


