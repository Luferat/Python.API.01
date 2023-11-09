import json

# Seu dicionário
meu_dict = {'nome': 'Luferat', 'idade': 40, 'linguagem': 'Python'}

# Converter o dicionário em uma representação JSON
json_str = json.dumps(meu_dict)

# Exibir o JSON
print(json_str)
