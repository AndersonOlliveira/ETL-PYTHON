from conection.Conection_Mongo import DBMongoManager
from typing import Dict,List
import classLogger
import time
    #iniciando a conexao

class Coletion:
    
    def __init__(self,db_colletion,db_connection,db_colletion_json) -> None:
        self.__name_colletion = db_colletion
        self.__name_colletion_json = db_colletion_json
        self.__db_connection = db_connection

   
    # def insert_document(self,document: list[Dict]) -> list[Dict]:
    def insert_document(self,document: Dict) -> Dict:
        classLogger.logger.error(f"MEU DADOS VINDO DO {document}")
        collection = self.__db_connection.get_collection(self.__name_colletion_json)
        result = collection.insert_one(document)
        document['_id'] = result.inserted_id
        classLogger.logger.error(f"[{time.strftime('%H:%M:%S')}] FOI INSERIDO O ID :: {document}")
          
        return document 
    
    def insert_document_may(self,document_list: List[Dict]) -> List[Dict]:
        collection = self.__db_connection.get_collection(self.__name_colletion)
        result = collection.insert_many(document_list)
        # document_list['_id'] = result.inserted_id
        return result

