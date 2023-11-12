# Importa a biblioteca 'json'.
import json

# Importa a biblioteca 'sqlite3' para trabalhar com SQLite.
import sqlite3


def read_all_items(database):  # Função que retorna e lista todos os 'items'.

    # Conecta ao banco de dados.
    conn = sqlite3.connect(database)

    # Define a fábrica de linhas como dicionário.
    conn.row_factory = sqlite3.Row

    # Cria um cursor de dados.
    cursor = conn.cursor()

    # Consultar dados
    cursor.execute("SELECT * FROM item WHERE item_status = 'on' ORDER BY item_date DESC")
    dados = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    conn.close()

    # Criar uma lista para armazenar os registros.
    registros = []

    # Converter cada objeto Row em um dicionário e adicionar à lista 'registros'.
    for registro in dados:
        registros.append(dict(registro))

    # Verificar se há registros antes de retornar.
    if registros:
        # Se houver registros, serializar os dados em formato JSON e retornar.
        return json.dumps(registros, indent=2)
    else:
        # Se não houver registros, retornar um JSON indicando a ausência de registros.
        return json.dumps({"message": "Nenhum registro encontrado"}, indent=2)

# Exemplo de uso para obter todos os 'itens' da tabela 'item'.
# print(get_all_items())


def read_one_item(database, item_id):  # Função que retorna um 'item' identificado pelo 'ID'.

    # Conecta ao banco de dados, define a saída como um dicionário e cria um cursor.
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Consulta um registro específico pelo ID.
    cursor.execute("SELECT * FROM item WHERE item_id = ? AND item_status = 'on'", (item_id,))
    dado = cursor.fetchone()

    # Fechar a conexão com o banco de dados.
    conn.close()

    # Se o registro com o ID existir, converte para um dicionário e retorna como JSON.
    if dado:
        return json.dumps(dict(dado), indent=2)
    else:
        # Se não encontrar o registro, retorna uma mensagem indicando que o ID não foi encontrado.
        return json.dumps({"error": "ID não encontrado"}, indent=2)


# Exemplo de uso para obter um registro pelo ID.
# item_id = 1  # Substitua pelo ID desejado.
# print(get_one_item(item_id))

def create_item(database, item_json):
    try:
        # Converte o JSON para um dicionário.
        new_item = json.loads(item_json)

        # Conecta ao banco de dados e cria um cursor.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Insere um novo registro na tabela 'item'.
        sql = "INSERT INTO item (item_name, item_description, item_location, item_owner) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, (new_item['name'], new_item['description'], new_item['location'], new_item['owner']))

        # Commit para salvar as alterações.
        conn.commit()

        # Fechar a conexão com o banco de dados.
        conn.close()

        return json.dumps({"message": "Registro criado com sucesso"}, indent=2)
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Erro ao decodificar JSON: {str(e)}"}, indent=2)
    except sqlite3.Error as e:
        return json.dumps({"error": f"Erro ao inserir registro no banco de dados: {str(e)}"}, indent=2)


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

        return json.dumps({"message": "Registro apagado com sucesso"}, indent=2)
    except sqlite3.Error as e:
        return json.dumps({"error": f"Erro ao apagar registro: {str(e)}"}, indent=2)

# Exemplo de uso para deletar um registro pelo ID.
# item_id_to_delete = 1  # Substitua pelo ID desejado.
# print(delete_item(item_id_to_delete))


def update_item(database, item_id, item_json):
    try:
        # Converte o JSON para um dicionário.
        updated_item = json.loads(item_json)

        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Loop para atualizar os campos específicos do registro na tabela 'item'.
        # Observe que o prefixo 'item_' é adicionado ao(s) nome(s) do(s) campo(s).
        set_clause = ', '.join([f"item_{key} = ?" for key in updated_item.keys()])

        # Monta SQL com base nos campos a serem atualizados.
        sql = f"UPDATE item SET {set_clause} WHERE item_id = ? AND item_status = 'on'"
        cursor.execute(sql, (*updated_item.values(), item_id))

        # Commit para salvar as alterações.
        conn.commit()

        # Fechar a conexão com o banco de dados.
        conn.close()

        return json.dumps({"message": "Registro atualizado com sucesso"}, indent=2)
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Erro ao decodificar JSON: {str(e)}"}, indent=2)
    except sqlite3.Error as e:
        return json.dumps({"error": f"Erro ao atualizar registro no banco de dados: {str(e)}"}, indent=2)

# Exemplo de uso para atualizar um registro pelo ID com dados de um JSON.
# item_id_to_update = 1  # Substitua pelo ID desejado.
# updated_item_json = '{"name": "Novo Nome", "description": "Nova Descrição"}'
# print(update_item(item_id_to_update, updated_item_json))
