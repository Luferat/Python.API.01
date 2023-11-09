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

# Função que lê e lista todos os itens da coleção.
def get_all():
    # Converte a lusta 'items' para json e armazena em 'var_json'
    var_json = json.dumps(items, indent=2)
    
    # Imprime o json.
    print(var_json)

# Função que lê um item específico, identificado pelo índice.
def get_one(id):
    
    # Converte o dicionario 'items[id]' para json e armazena em 'var_json'
    var_json = json.dumps(items[id], indent=2)
    
    # Imprime o json.
    print(var_json)
    
# Chama (call) a função get_all().
get_all()

# Chama a função get_one(), passando o índice como parâmetro.
get_one(1)
