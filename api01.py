# Importa a biblioteca 'json'.
import json

items = [
    {
        "id": 1,
        "name": "Bagulho",
        "description": "Apenas um bagulho",
        "location": "Em uma caixa"
    }, {
        "id": 2,
        "name": "Tranqueira",
        "description": "Apenas uma tranqueira qualquer",
        "location": "Em um gaveteiro"
    }, {
        "id": 3,
        "name": "Bagulete",
        "description": "Um bagulete qualquer",
        "location": "Na esquina"
    }
]

def get_all():
    # Converte o dicionario 'items' para json e armazena em 'var_json'
    var_json = json.dumps(items, indent=2)
    
    # Imprime o json.
    print(var_json)

def get_one(id):
    var_json = json.dumps(items[id], indent=2)
    print(var_json)
    
# get_all()

get_one(1)