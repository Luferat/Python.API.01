# -*- coding: utf-8 -*-

# Importa a biblioteca 'json'.
import json

# Importa a biblioteca 'sqlite3' para trabalhar com SQLite.
import sqlite3


def prefix_remove(prefix, data):  # Função que remove os prefixos dos nomes dos campos.
    new_data = {}
    for key, value in data.items():
        if key.startswith(prefix):
            new_key = key[len(prefix):]
            new_data[new_key] = value
        else:
            new_data[key] = value
    return new_data


def read_all_items(database):  # Função que retorna e lista todos os 'items'.

    try:

        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)

        # Formata os dados retornados na factory como SQLite.Row.
        conn.row_factory = sqlite3.Row

        # Cria um cursor de dados.
        cursor = conn.cursor()

        # Executa o SQL.
        cursor.execute("SELECT * FROM item WHERE item_status = 'on' ORDER BY item_date DESC")

        # Retorna todos os resultados da consulta para 'items_rows'.
        items_rows = cursor.fetchall()

        # Fecha a conexão com o banco de dados
        conn.close()

        # Cria uma lista para armazenar os registros.
        items = []

        # Converte cada SQLite.Row em um dicionário e adiciona à lista 'registros'.
        for item in items_rows:
            items.append(dict(item))

        # Verifica se há registros antes de retornar.
        if items:

            # Remove prefixos dos campos.
            new_items = [prefix_remove('item_', item) for item in items]

            # Se houver registros, retorna tudo.
            return new_items
        else:
            # Se não houver registros, retorna erro.
            return {"error": "Nenhum item encontrado"}

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}

# Exemplo de uso para obter todos os 'itens' da tabela 'item'.
# database = "./dbitem.db"
# print(read_all_items(database))


def read_one_item(database, item_id):  # Função que retorna um 'item' identificado pelo 'ID'.

    try:
        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Executa o SQL.
        cursor.execute("SELECT * FROM item WHERE item_id = ? AND item_status = 'on'", (item_id,))

        # Retorna o resultado da consulta para 'item_row'.
        item_row = cursor.fetchone()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Se o registro existe...
        if item_row:

            # Converte SQLite.Row para dicionário e armazena em 'item'.
            item = dict(item_row)

            # Remove prefixos dos campos.
            new_item = prefix_remove('item_', item)

            # Retorna item.
            return new_item
        else:
            # Se não encontrar o registro, retorna erro.
            return {"error": "Item não encontrado"}

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}


# Exemplo de uso para obter um registro pelo ID.
# item_id = 1  # Substitua pelo ID desejado.
# print(read_one_item(item_id))

def create_item(database, item_json):

    try:
        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Query que insere um novo registro na tabela 'item'.
        sql = "INSERT INTO item (item_name, item_description, item_location, item_owner) VALUES (?, ?, ?, ?)"

        # Executa a query, fazendo as devidas substituições.
        cursor.execute(sql, (item_json['name'], item_json['description'], item_json['location'], item_json['owner']))

        # Salvar as alterações no banco de dados.
        conn.commit()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Retorna com sucesso.
        return {"success": "Registro criado com sucesso"}

    except json.JSONDecodeError as e:  # Erro ao obter dados do JSON.
        return {"error": f"Erro ao decodificar JSON: {str(e)}"}

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}


# Exemplo de uso para criar um novo item a partir de um JSON.
# new_item_json = '''{
#     "name": "Turiparalho",
#     "description": "Usado na fabricação de coisas",
#     "location": "Nun pote cheio",
#     "owner": "1"
# }'''
# print(create_item(new_item_json))


def delete_item(database, item_id):

    try:
        # Conecta ao banco de dados e cria um cursor.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Atualiza o campo 'item_status' para 'off' para o registro específicado pelo ID.
        cursor.execute("UPDATE item SET item_status = 'off' WHERE item_id = ?", (item_id,))

        # Commit para salvar as alterações.
        conn.commit()

        # Fechar a conexão com o banco de dados.
        conn.close()

        return {"success": "Registro apagado com sucesso"}

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}


# Exemplo de uso para deletar um registro pelo ID.
# item_id_to_delete = 1  # Substitua pelo ID desejado.
# print(delete_item(item_id_to_delete))


def update_item(database, item_id, item_json):

    try:
        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Loop para atualizar os campos específicos do registro na tabela 'item'.
        # Observe que o prefixo 'item_' é adicionado ao(s) nome(s) do(s) campo(s).
        set_clause = ', '.join([f"item_{key} = ?" for key in item_json.keys()])

        # Monta SQL com base nos campos a serem atualizados.
        sql = f"UPDATE item SET {set_clause} WHERE item_id = ? AND item_status = 'on'"
        cursor.execute(sql, (*item_json.values(), item_id))

        # Commit para salvar as alterações.
        conn.commit()

        # Fechar a conexão com o banco de dados.
        conn.close()

        return {"success": "Registro atualizado com sucesso"}

    except json.JSONDecodeError as e:
        return {"error": f"Erro ao decodificar JSON: {str(e)}"}

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}


# Exemplo de uso para atualizar um registro pelo ID com dados de um JSON.
# item_id_to_update = 1  # Substitua pelo ID desejado.
# updated_item_json = '{"name": "Novo Nome", "description": "Nova Descrição"}'
# print(update_item(item_id_to_update, updated_item_json))
