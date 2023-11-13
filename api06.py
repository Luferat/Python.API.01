# Importa as funções para detectar a criar o database.
from createdb import check_db

# Importa funções CRUD para item.
from items_crud import read_all_items, read_one_item, create_item, delete_item, update_item

# Importa a biblioteca 'os' para acessar o sistema operacional.
import os

# Especifica a base de dados SQLite3.
database = "./dbitems.db"

# Exemplo de uso para obter todos os 'itens' da tabela 'item'.
check_db(database)
os.system('cls')
print(read_all_items(database))

# Exemplo de uso para obter um item pelo ID.
# item_id = 1  # Substitua pelo ID desejado.
# print(get_one_item(item_id))

# Exemplo de uso para criar um novo item a partir de um JSON.
# new_item_json = '''{
#     "name": "Turiparalho",
#     "description": "Usado na fabricação de coisas",
#     "location": "Nun pote cheio",
#     "owner": "1"
# }'''
# os.system('cls')
# print(create_item(database, new_item_json))


# Exemplo de uso para deletar um registro pelo ID.
# item_id_to_delete = 2  # Substitua pelo ID desejado.
# os.system('cls')
# print(delete_item(database, item_id_to_delete))


# Exemplo de uso para atualizar um registro pelo ID com dados de um JSON.
# item_id_to_update = 1  # Substitua pelo ID desejado.
# updated_item_json = '''{
#     "name": "Coisica",
#     "description": "Apenas uma coisica de nada"
# }'''
# os.system('cls')
# print(update_item(database, item_id_to_update, updated_item_json))
