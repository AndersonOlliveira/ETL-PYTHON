import psycopg2 as pg
from psycopg2 import Error
from dotenv import load_dotenv
import os

load_dotenv()
pwd = os.getenv("DB_PASSWORD")

def conexao():
    try:
      
        conn = pg.connect(
            database="AuCom.Com",
            user="sysdba",
            password=pwd,
            host="10.115.10.5",
            port="5493"
        )
        print("Conexão estabelecida com sucesso!")
        return conn

    except Error as e:
        print(f"Erro ao conectar: {e}")
