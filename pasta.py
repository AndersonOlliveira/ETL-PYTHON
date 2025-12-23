import os
import json

path = "/nfs/progestor/infoJson"

print("É diretório?", os.path.isdir(path))
print("Arquivos:", os.listdir(path))

for arquivo in os.listdir(path):
    if arquivo.endswith(".json"):
        with open(os.path.join(path, arquivo), "r", encoding="utf-8") as f:
            dados = json.load(f)
            print(dados)
