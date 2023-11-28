# -*- coding: utf-8 -*-

# Importa bibliotecas.
from flask import Flask, request, json, render_template
import sqlite3

# Cria aplicativo Flask.
app = Flask(__name__)

# Configura o character set das transações HTTP para UTF-8.
json.provider.DefaultJSONProvider.ensure_ascii = False

# Especifica a base de dados SQLite3.
database = "./db/temp_db.db"


def prefix_remove(prefix, data):

    # Função que remove os prefixos dos nomes dos campos de um 'dict'.
    # Por exemplo, prefix_remove('item_', { 'item_id': 2, 'item_name': 'Coisa', 'item_status': 'on' })
    # retorna { 'id': 2, 'name': 'Coisa', 'status': 'on' }
    # Créditos: Comunidade StackOverflow.

    new_data = {}
    for key, value in data.items():
        if key.startswith(prefix):
            new_key = key[len(prefix):]
            new_data[new_key] = value
        else:
            new_data[key] = value
    return new_data


@app.route('/')
def home():
    return render_template('index.html')


# ########################### #
# Rotas para consumir 'item'. #
# ########################### #


@app.route("/items", methods=["GET"])
def item_get_all():

    # Obtém todos os registros válidos de 'item'.
    # Request method → GET
    # Request endpoint → /items
    # Response → JSON

    try:

        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)

        # Formata os dados retornados na factory como SQLite.Row.
        conn.row_factory = sqlite3.Row

        # Cria um cursor de dados.
        cursor = conn.cursor()

        # Executa o SQL.
        cursor.execute(
            "SELECT * FROM item WHERE item_status != 'off' ORDER BY item_date DESC")

        # Retorna todos os resultados da consulta para 'items_rows'.
        items_rows = cursor.fetchall()

        # Fecha a conexão com o banco de dados
        conn.close()

        # Cria uma lista para armazenar os registros.
        items = []

        # Converte cada SQLite.Row em um dicionário e adiciona à lista 'registros'.
        for item in items_rows:
            items.append(dict(item))

        # Verifica se há registros antes de retornar...
        if items:

            # Remove prefixos dos campos.
            new_items = [prefix_remove('item_', item) for item in items]

            # Se houver registros, retorna tudo.
            return new_items, 200
        else:
            # Se não houver registros, retorna erro.
            return {"error": "Nenhum item encontrado"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route("/items/<int:id>", methods=["GET"])
def item_get_one(id):

    # Obtém um registro único de 'item', identificado pelo 'id'.
    # Request method → GET
    # Request endpoint → /items/<id>
    # Response → JSON

    try:
        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Executa o SQL.
        cursor.execute(
            "SELECT * FROM item WHERE item_id = ? AND item_status != 'off'", (id,))

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
            return new_item, 200
        else:
            # Se não encontrar o registro, retorna erro.
            return {"error": "Item não encontrado"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route('/items', methods=["POST"])
def item_create():

    # Cadastra um novo registro em 'item'.
    # Request method → POST
    # Request endpoint → /items
    # Request body → JSON (raw) → { String:name, String:description, String:location, int:owner }
    # Response → JSON → { "success": "Registro criado com sucesso", "id": id do novo registro }

    try:
        # Recebe dados do body da requisição na forma de 'dict'.
        new_item = request.get_json()

        # Conecta ao banco de dados.
        # Observe que 'row_factory' é desnecessário porque não receberemos dados do banco de dados.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Query que insere um novo registro na tabela 'item'.
        sql = "INSERT INTO item (item_name, item_description, item_location, item_owner) VALUES (?, ?, ?, ?)"

        # Dados a serem inseridos, obtidos do request.
        sql_data = (
            new_item['name'],
            new_item['description'],
            new_item['location'],
            new_item['owner']
        )

        # Executa a query, fazendo as devidas substituições dos curingas (?) pelos dados (sql_data).
        cursor.execute(sql, sql_data)

        # Obter o ID da última inserção
        inserted_id = int(cursor.lastrowid)

        # Salvar as alterações no banco de dados.
        conn.commit()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Retorna com mensagem de sucesso e status HTTP "201 Created".
        return {"success": "Registro criado com sucesso", "id": inserted_id}, 201

    except json.JSONDecodeError as e:  # Erro ao obter dados do JSON.
        return {"error": f"Erro ao decodificar JSON: {str(e)}"}, 500

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route("/items/<int:id>", methods=["DELETE"])
def item_delete(id):

    # Marca, como apagado, um registro único de 'item', identificado pelo 'id'.
    # Request method → DELETE
    # Request endpoint → /items/<id>
    # Response → JSON → { "success": "Registro apagado com sucesso", "id": id do registro }

    try:

        # Conecta ao banco de dados.
        # Observe que 'row_factory' é desnecessário porque não receberemos dados do banco de dados.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Query que pesquisa a existência do registro.
        sql = "SELECT item_id FROM item WHERE item_id = ? AND item_status != 'off'"

        # Executa a query.
        cursor.execute(sql, (id,))

        # Retorna o resultado da consulta para 'item_row'.
        item_row = cursor.fetchone()

        # Se o registro exite e está ativo...
        if item_row:

            # Query para atualizar o item no banco de dados.
            sql = "UPDATE item SET item_status = 'off' WHERE item_id = ?"

            # Executa a query.
            cursor.execute(sql, (id,))

            # Salvar no banco de dados.
            conn.commit()

            # Fecha o banco de dados.
            conn.close()

            # Retorna com mensagem de sucesso e status HTTP "200 Ok".
            return {"success": "Registro apagado com sucesso", "id": id}, 200

        # Se o registro não existe, não pode ser apagado.
        else:

            # Fecha o banco de dados.
            conn.close()

            # Retorna mensagem de erro 404.
            return {"error": "Item não existe"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route("/items/<int:id>", methods=["PUT", "PATCH"])
def item_edit(id):

    # Edita um registro em 'item', identificado pelo 'id'.
    # Request method → PUT ou PATCH
    # Request endpoint → /items/<id>
    # Request body → JSON (raw) → { String:name, String:description, String:location, int:owner }
    #       OBS: usando "PATCH", não é necessário enviar todos os campos, apenas os que serão alterados.
    # Response → JSON → { "success": "Registro atualizado com sucesso", "id": id do registro }

    try:

        # Recebe os dados do corpo da requisição.
        item_json = request.get_json()

        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Loop para atualizar os campos específicos do registro na tabela 'item'.
        # Observe que o prefixo 'item_' é adicionado ao(s) nome(s) do(s) campo(s).
        set_clause = ', '.join([f"item_{key} = ?" for key in item_json.keys()])

        # Monta SQL com base nos campos a serem atualizados.
        sql = f"UPDATE item SET {set_clause} WHERE item_id = ? AND item_status != 'off'"
        cursor.execute(sql, (*item_json.values(), id))

        # Commit para salvar as alterações.
        conn.commit()

        # Fechar a conexão com o banco de dados.
        conn.close()

        # Confirma a atualização.
        return {"success": "Registro atualizado com sucesso", "id": id}, 201

    # except json.JSONDecodeError as e:  # Erro ao obter dados do JSON.
    #    return {"error": f"Erro ao decodificar JSON: {str(e)}"}, 500

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route("/items/search/<string:query>")
def item_search(query):

    # Pesquisa todos os registros válidos de 'item' que conténha 'query' nos campos
    # 'item_name', 'item_description' ou 'item_location'.
    # Request method → GET
    # Request endpoint → /items/search/<string:query>
    # Response → JSON

    try:
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sql = """
            SELECT * FROM item
            WHERE item_status != 'off' AND (
                item_name LIKE '%' || ? || '%' OR
                item_description LIKE '%' || ? || '%' OR
                item_location LIKE '%' || ? || '%'
            );        
        """
        cursor.execute(sql, (query, query, query))
        items_rows = cursor.fetchall()
        conn.close()

        items = []
        for item in items_rows:
            items.append(dict(item))

        if items:
            new_items = [prefix_remove('item_', item) for item in items]
            return new_items, 200
        else:
            return {"error": "Nenhum item encontrado"}, 404

    except sqlite3.Error as e:
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}, 500


# ############################ #
# Rotas para consumir 'owner'. #
# ############################ #


@app.route("/owners", methods=["GET"])
def owner_get_all():

    # Obtém todos os registros válidos de 'owner'.
    # Request method → GET
    # Request endpoint → /owners
    # Response → JSON

    try:
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sql = "SELECT * FROM owner WHERE owner_status != 'off' ORDER BY owner_name"
        cursor.execute(sql)
        items_rows = cursor.fetchall()
        conn.close()

        items = []
        for item in items_rows:
            items.append(dict(item))

        if items:
            new_items = [prefix_remove('owner_', item) for item in items]
            return new_items, 200
        else:
            return {"error": "Nenhum item encontrado"}, 404

    except sqlite3.Error as e:
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500
    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route("/owners/<int:id>", methods=["GET"])
def owner_get_one(id):

    # Obtém um registro único de 'owner', identificado pelo 'id'.
    # Request method → GET
    # Request endpoint → /owners/<id>
    # Response → JSON

    try:
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sql = "SELECT * FROM owner WHERE owner_id = ? AND owner_status != 'off'"
        cursor.execute(sql, (id,))
        item_row = cursor.fetchone()
        conn.close()

        if item_row:
            item = dict(item_row)
            new_item = prefix_remove('owner_', item)
            return new_item, 200
        else:
            return {"error": "Item não encontrado"}, 404

    except sqlite3.Error as e:
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500
    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route('/owners', methods=["POST"])
def owner_create():

    # Cadastra um novo registro em 'owner'.
    # Request method → POST
    # Request endpoint → /owners
    # Request body → JSON (raw) → { String: name, String:email, string:password, string:birth }
    # Response → JSON → { "success": "Registro criado com sucesso", "id": id do novo registro }

    try:
        new_item = request.get_json()
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        sql = "INSERT INTO owner (owner_name, owner_email, owner_password, owner_birth) VALUES (?, ?, ?, ?)"
        sql_data = (
            new_item['name'],
            new_item['email'],
            new_item['password'],
            new_item['birth']
        )
        cursor.execute(sql, sql_data)
        inserted_id = int(cursor.lastrowid)
        conn.commit()
        conn.close()

        if inserted_id > 0:
            return {"success": "Registro criado com sucesso", "id": inserted_id}, 201

    except json.JSONDecodeError as e:
        return {"error": f"Erro ao decodificar JSON: {str(e)}"}, 500
    except sqlite3.Error as e:
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500
    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route("/owners/<int:id>", methods=["PATCH"])
def owner_edit(id):

    # Edita um registro em 'owner', identificado pelo 'id'.
    # Request method → PATCH
    # Request endpoint → /owners/<id>
    # Request body → JSON (raw) → { String: name, String:email, string:password, string:birth }
    #       OBS: usando "PATCH", não é necessário enviar todos os campos, apenas os que serão alterados.
    # Response → JSON → { "success": "Registro atualizado com sucesso", "id": id do registro }

    try:
        item_json = request.get_json()
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Loop para atualizar os campos específicos do registro na tabela 'item'.
        # Observe que o prefixo 'item_' é adicionado ao(s) nome(s) do(s) campo(s).
        set_clause = ', '.join(
            [f"owner_{key} = ?" for key in item_json.keys()])

        # Monta SQL com base nos campos a serem atualizados.
        sql = f"UPDATE owner SET {set_clause} WHERE owner_id = ? AND owner_status != 'off'"
        cursor.execute(sql, (*item_json.values(), id))

        # Envia dados e fecha a conexão com o banco de dados.
        conn.commit()
        conn.close()

        return {"success": "Registro atualizado com sucesso", "id": id}, 201

    except sqlite3.Error as e:
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500
    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route("/owners/<int:id>", methods=["DELETE"])
def owner_delete(id):

    # Marca, como apagado, um registro único de 'owner', identificado pelo 'id'.
    # Request method → DELETE
    # Request endpoint → /owners/<id>
    # Response → JSON → { "success": "Registro apagado com sucesso", "id": id do registro }

    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        sql = "SELECT owner_id FROM owner WHERE owner_id = ? AND owner_status != 'off'"
        cursor.execute(sql, (id,))
        item_row = cursor.fetchone()

        if item_row:
            sql = "UPDATE owner SET owner_status = 'off' WHERE owner_id = ?"
            cursor.execute(sql, (id,))
            conn.commit()
            conn.close()
            return {"success": "Registro apagado com sucesso", "id": id}, 200
        else:
            conn.close()
            return {"error": "Item não existe"}, 404

    except sqlite3.Error as e:
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500
    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route("/owners/items/<int:id>", methods=["GET"])
def owner_item_get_all(id):

    # Obtém todos os registros válidos de 'item' para um 'owner' específico,
    # identificado pelo 'id'.
    # Request method → GET
    # Request endpoint → /owners/items/<id>
    # Response → JSON

    try:
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        sql = """
            SELECT * FROM item
            WHERE item_status != 'off'
                AND item_owner = ? 
            ORDER BY item_date DESC
            """
        cursor.execute(sql, (id,))
        items_rows = cursor.fetchall()
        conn.close()

        items = []
        for item in items_rows:
            items.append(dict(item))

        if items:
            new_items = [prefix_remove('item_', item) for item in items]
            return new_items, 200
        else:
            return {"error": "Nenhum item encontrado"}, 404

    except sqlite3.Error as e:
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route("/items/all/<int:id>", methods=["GET"])
def item_all_get_all(id):

    # Obtém todos os campos válidos de 'item' identificado pelo 'id',
    # juntamente com os dados de 'owner' correspondente.
    # Request method → GET
    # Request endpoint → /items/all/<id>
    # Response → JSON

    try:
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        sql = """
            SELECT * FROM item 
                INNER JOIN owner ON item_owner = owner_id
            WHERE item_status != 'off'
                AND item_id = ?
            ORDER BY item_date DESC
        """
        cursor.execute(sql, (id,))
        items_rows = cursor.fetchall()
        conn.close()

        items = []
        for item in items_rows:
            items.append(dict(item))

        if items:
            # Só removemos o prefixo de 'item' para não gerar dados homônimos.
            new_items = [prefix_remove('item_', item) for item in items]
            return new_items, 200
        else:
            return {"error": "Nenhum item encontrado"}, 404

    except sqlite3.Error as e:
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}, 500


# ############################## #
# Rotas para consumir 'contact'. #
# ############################## #


@app.route("/contacts", methods=["POST"])
def contacts():

    # Cadastra um novo contato em 'contact'.
    # Request method → POST
    # Request endpoint → /contacts
    # Request body → JSON (raw) → { string:name, string:email, string:subject, string:message }
    # Response → JSON → { "success": "Registro criado com sucesso", "id": id do novo registro }

    try:
        new_item = request.get_json()
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        sql = "INSERT INTO contact (name, email, subject, message) VALUES (?, ?, ?, ?)"
        sql_data = (
            new_item['name'],
            new_item['email'],
            new_item['subject'],
            new_item['message']
        )
        cursor.execute(sql, sql_data)
        inserted_id = int(cursor.lastrowid)
        conn.commit()
        conn.close()

        if inserted_id > 0:
            return {"success": "Contato enviado com sucesso", "id": inserted_id, "name": new_item['name']}, 201

    except json.JSONDecodeError as e:
        return {"error": f"Erro ao decodificar JSON: {str(e)}"}, 500
    except sqlite3.Error as e:
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500
    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}, 500


# Roda aplicativo Flask.
if __name__ == "__main__":
    app.run(debug=True)
