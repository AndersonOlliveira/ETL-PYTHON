from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_USER = os.getenv('BD_MONGO_USER')
MONGO_PASS = os.getenv('BD_MONGO_PASS')
MONGO_HOST = os.getenv('BD_MONGO_HOST') 
MONGO_PORT = os.getenv('BD_MONGO_PORT')   
MONGO_DB_NAME = os.getenv('BD_MONGO_BD_NAME')   
MONGO_DB_COLLE = os.getenv('BD_MONGO_BD_COLLETION')   
MONGO_DB_COLLE_JSON = os.getenv('BD_MONGO_BD_COLLETION_JSON')   

MONGO_URI_AUTH = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"

# print(f"minha conexao::{MONGO_URI_AUTH}")


# try:
#       Client = MongoClient(MONGO_URI_AUTH)
#       Client.admin.command('ping')
#       print(f"minha conexao, foi realizada com sucesso de forma local")
#       bd = Client.get_database('progesto_Colletion')
#       # MongoManager(self,bd)

# except Exception as e:
#       print("\n[ERRO] Falha na Conexão ou Autenticação.")
#       print(f"Detalhes: {e}")


class DBMongoManager:
      def __init__(self) -> None:
          self.__connection_string = MONGO_URI_AUTH
          self.__database_name = MONGO_DB_NAME
          self.__client = None
          self.__db_connection_name = None
          self.__db_name_colletion = MONGO_DB_COLLE
          self.__db_name_colletion_json = MONGO_DB_COLLE_JSON

          

      def connect_to_db(self):
            try:

                  self.__client = MongoClient(self.__connection_string,serverSelectionTimeoutMS=5000)
                  self.__db_connection_name = self.__client[self.__database_name]

                  self.__client.admin.command('ping')
                  print(f"Conexao Realizada com sucesso")
                  return True
            except Exception as e:
                   print("\n[ERRO] Falha na Conexão ou Autenticação.")
                   print(f"Detalhes: {e}")

      def get_db_connection(self):
            return self.__db_connection_name
     
      def get_db_client(self):
            return self.__client
      def get_db_colletion(self):
            return self.__db_name_colletion 
      def get_db_colletion_json(self):
            return self.__db_name_colletion_json
        

# Client = MongoClient(f"mongodb+srv://{os.getenv("BD_MONGO_USER")}:{os.getenv("BD_MONGO_PASS")}@cluster0.pdkxk52.mongodb.net/")
# db_con = Client['progesto_Colletion']

# bd = Client.get_database('progesto_Colletion')
# print(f"meu data base{bd}")
# colecao = bd.get_collection('progestor_transaction')


# dado = {
#     "nome": "anderson Oliveira araujo",
#     "telefone":"19971101711"
# }

# colecao.insert_one(dado)

