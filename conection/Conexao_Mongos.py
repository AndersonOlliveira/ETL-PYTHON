from conection.Conection_Mongo import DBMongoManager
    #iniciando a conexao
 
def mongoConect():

   db_handle = DBMongoManager()

   if db_handle.connect_to_db():
        try:
            db = db_handle.get_db_connection()
            # print(f" Banco acessecivel : {db}")
            return db_handle
        except Exception as e:
            print(f" Erro ao accessar o banco de dados apósc conexão:  {e}")

        finally:
           
           client = db_handle.get_db_client()
        # if client:
        #    client.close()
        #    print('Conexão Fechada')

   else:
    print('FINALIZANDO, FALHA NA CONEXÃO')


# conn = db_handle.get_db_connection()

# db_handle.connect_to_db()
# conn1 = db_handle.get_db_connection()

# print(f"minha colecction {conn1}")


# print("---" *20)

# collection = conn1.get_collection(db_handle.get_db_colletion())

# print(f"meu nome da colletion {collection}")

# collection.insert_one({
#     'estou aqui': 'inserindo',
#     'Numero': [123,31231,5454,545,'121']
# })


