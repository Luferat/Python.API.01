# Importa a biblioteca 'json'.
import json

# Importar a biblioteca sqlite3 para trabalhar com SQLite
import sqlite3

# Especifica a base de dados SQLite3.
database = "./dbitems.db"


def get_all():  # Função que lê e lista todos os itens da coleção.

    # Conectar ao banco de dados
    conn = sqlite3.connect(database)

    # Definir a fábrica de linhas como dicionário
    conn.row_factory = sqlite3.Row

    # Criar um cursor
    cursor = conn.cursor()

    # Consultar dados
    cursor.execute(
        "SELECT * FROM item WHERE item_status = 'on' ORDER BY item_date DESC")
    dados = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    conn.close()

    # Criar uma lista para armazenar os registros
    registros = []

    # Converter cada objeto Row em um dicionário e adicionar à lista
    for registro in dados:
        registros.append(dict(registro))

    # Serializar os dados em formato JSON como uma string e retornar.
    return json.dumps(registros, indent=2)


# Chama a função get_all().
print(get_all())
