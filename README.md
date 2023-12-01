# Python.API.01

Minha primeira API REST em Python.

## Requisitos

- Python 3.12.0^
- Flask 3.0.0^
- Flask-Cors 4.0.0^

## Opcionais

- [DB Browser (SQLite)](https://sqlitebrowser.org/) para gerenciar o banco de dados local.

## Rotas e Endpoints

Obtém todos os registros válidos de 'item'.

- Request method → `GET`
- Request endpoint → `/items`
- Response → JSON[]

Obtém um registro único de 'item', identificado pelo 'id'.

- Request method → `GET`
- Request endpoint → `/items/<id>`
- Response → JSON{}

Cadastra um novo registro em 'item'.

- Request method → `POST`
- Request endpoint → `/items`
- Request body → JSON (raw) → `{ string:name, string:description, string:location, int:owner }`
- Response → JSON → `{ "success": "Registro criado com sucesso", "id": id do novo registro }`

Marca, como apagado, um registro único de 'item', identificado pelo 'id'.

- Request method → `DELETE`
- Request endpoint → `/items/<id>`
- Response → JSON → `{ "success": "Registro apagado com sucesso", "id": id do registro }`

Edita um registro em 'item', identificado pelo 'id'.

- Request method → `PUT` ou `PATCH`
- Request endpoint → `/items/<id>`
- Request body → JSON (raw) → `{ string:name, string:description, string:location, int:owner }`
    - *OBS: usando `PATCH`, não é necessário enviar todos os campos, apenas os que serão alterados.*
- Response → JSON → `{ "success": "Registro atualizado com sucesso", "id": id do registro }`

Pesquisa todos os registros válidos de 'item' que contenha 'query' nos campos `item_name`, `item_description` ou `item_location`.

- Request method → `GET`
- Request endpoint → `/items/search/<string:query>`
- Response → JSON[]

Obtém todos os registros válidos de 'owner'.

- Request method → `GET`
- Request endpoint → `/owners`
- Response → JSON[]

Obtém um registro único de 'owner', identificado pelo 'id'.

- Request method → `GET`
- Request endpoint → `/owners/<id>`
- Response → JSON{}

Cadastra um novo registro em 'owner'.

- Request method → `POST`
- Request endpoint → `/owners`
- Request body → JSON (raw) → `{ string: name, string:email, string:password, string:birth }`
- Response → JSON → `{ "success": "Registro criado com sucesso", "id": id do novo registro }`

Edita um registro em 'owner', identificado pelo 'id'.

- Request method → `PATCH`
- Request endpoint → `/owners/<id>`
- Request body → JSON (raw) → `{ string: name, string:email, string:password, string:birth }`
    - *OBS: usando "PATCH", não é necessário enviar todos os campos, apenas os que serão alterados.*
- Response → JSON → `{ "success": "Registro atualizado com sucesso", "id": id do registro }`

Marca, como apagado, um registro único de 'owner', identificado pelo 'id'.

- Request method → `DELETE`
- Request endpoint → `/owners/<id>`
- Response → JSON → `{ "success": "Registro apagado com sucesso", "id": id do registro }`

Obtém todos os registros válidos de 'item' para um 'owner' específico, identificado pelo 'id'.

- Request method → `GET`
- Request endpoint → `/owners/items/<id>`
- Response → JSON[]

Obtém todos os campos válidos de 'item' identificado pelo 'id', juntamente com os dados de 'owner' correspondente.

- Request method → `GET`
- Request endpoint → `/items/all/<id>`
- Response → JSON{}

Cadastra um novo contato em 'contact'.

- Request method → `POST`
- Request endpoint → `/contacts`
- Request body → JSON (raw) → `{ string:name, string:email, string:subject, string:message }`
- Response → JSON → `{ "success": "Registro criado com sucesso", "id": id do novo registro }`

----
