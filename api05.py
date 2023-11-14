# Importa bilbioteca de manipulação de JSON.
import json

# Importa bilbioteca de gestão do SQLite3.
import sqlite3

# Importa biblioteca de acesso ao sistema operacional.
import os

# Define o banco de dados.
database = './temp_db.db'


# Função que obtém e retorna (JSON) todos os 'item' do banco de dados.
def get_all_items():

    # Faz a conexão com o banco de dados.
    conn = sqlite3.connect(database)

    # Abre toda a base de dados na RAM do computador na forma de 'list'.
    # Isso permite acessar as colunas tanto por índice quanto por nome.
    conn.row_factory = sqlite3.Row

    # Cria um objeto de cursor, utilizado para percorrer os resultados de consultas SQL.
    # Ele permite que você execute comandos SQL, recupere dados do banco de dados e iteraja sobre os resultados.
    # Mantém um 'ponteiro' que indica onde você está nos resultados da consulta, permitindo que você itere sobre eles ou recupere dados específicos.
    cursor = conn.cursor()

    # Comando SQL a ser executado no SQLite, seguindo o padrão desta plataforma.
    # O Python só executa um comando SQL de cada vez, não suportando lotes.
    sql = 'SELECT * FROM item'

    # Executa o comando SQL no SQLite.
    # O cursor recebe os resultados da consulta e armazena na RAM.
    cursor.execute(sql)

    # Obtém os dados da 'row_factory' na forma de 'list' e armazena em uma variável (data).
    # Cada item de 'data' é uma representação binária (object) de cada linha (Row) retornada do banco de dados.
    data = cursor.fetchall()

    # Fecha a conexçao com o banco de dados, pois não precisamos mais dele.
    # Evita desperdíssio de recursos, a corrupção dos dados e libera a conexão para outros usos.
    conn.close()

    # Apenas um 'list' para armazenar todos os itens.
    all_items = []

    # Loop que itera 'data', armazenando cada linha (row) na variável 'item'.
    for item in data:

        # Adiciona cada item, na forma de 'dict' no final de 'all_items' (list).
        all_items.append(dict(item))

    # Retorna todos os 'item' na forma de JSON.
    return json.dumps(all_items, indent=2)

# Exemplo de uso de 'get_all_items()'.
# Dica: melhore o 'sql' da função para obter resultados mais específicos.


# Limpa e view do console.
os.system('cls')

# Executa a função e exibe os resultados.
print(get_all_items())
