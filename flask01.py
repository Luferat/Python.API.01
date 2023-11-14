# -*- coding: utf-8 -*-

# Importa bibliotecas.
from flask import Flask, jsonify, request, abort, make_response, json, Response

# Importa as funções para detectar a criar o database.
from createdb import check_db

# Importa funções CRUD para item.
from items_crud import read_all_items, read_one_item, create_item, delete_item, update_item

# Cria aplicativo Flask.
app = Flask(__name__)

# Configura o character set das transações HTTP para UTF-8.
json.provider.DefaultJSONProvider.ensure_ascii = False

# Especifica a base de dados SQLite3.
database = "./dbitem.db"

@app.route("/install", methods=["GET"])
def install(database):
    return check_db(database)

# Obtém todos os registros válidos de 'item'.
# Request method → GET
# Request endpoint → /items
# Response → JSON
@app.route("/items", methods=["GET"])
def get_all():
    return jsonify(read_all_items(database))

# Obtém um registro único de 'item' pelo ID.
# Request method → GET
# Request endpoint → /items/<id>
# Response → JSON
@app.route("/items/<int:id>", methods=["GET"])
def get_one(id):
    return jsonify(read_one_item(database, id))

# Cadastra novo registro em 'item'.
# Request method → POST
# Request endpoint → /items
# Request body → JSON
# Response → JSON
@app.route("/items", methods=["POST"])
def new():
    new_item = request.get_json()
    print(new_item)
    return jsonify(create_item(database, new_item))

# Atualiza um registro único de 'item' pelo ID.
# Request method → PUT ou PATCH
# Request endpoint → /items/<id>
# Request body → JSON
# Response → JSON
# Observação: PUT atualiza todos os campos e PATCH somente os campos informados.
#             Prefira PATCH
@app.route("/items/<int:id>", methods=["PUT", "PATCH"])
def edit(id):
    edited_item = request.get_json()
    return jsonify(update_item(database, id, edited_item))

# Marca, como apagado, um registro único de 'item' pelo ID.
# Request method → DELETE
# Request endpoint → /items/<id>
# Response → JSON
@app.route("/items/<int:id>", methods=["DELETE"])
def delete(id):
    return jsonify(delete_item(database, id))


# Roda aplicativo Flask.
if __name__ == "__main__":
    app.run(debug=True)
