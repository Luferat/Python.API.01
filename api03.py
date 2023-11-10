# Importa a biblioteca 'json'.
import json

# Coleção de dados.
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


def get_all():  # Função que lê e lista todos os itens da coleção.

    # Converte a lista 'items' para json e retorna para o chamador.
    return json.dumps(items, indent=2)


def get_one(id):  # Função que lê um item específico, identificado pelo "id".

    for item in items:  # Loop que 'itera' cada item de 'items' e armazena em 'item'.
        # Extrai o valor da chave "id" do item e compara com o "id" passado como parâmetro.
        if item.get("id") == id:
            # Se os "ids" coincidem (True) retorna o item atual para o chamador como JSON.
            return json.dumps(item, indent=2)
        # Se os "ids" não coincidem, roda o próximo loop.


# Chama (call) a função get_all().
# print(get_all())

# Chama a função get_one(), passando o índice como parâmetro e imprime o retorno.
print(get_one(4))
