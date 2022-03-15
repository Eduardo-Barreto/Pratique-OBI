# Desafio disponível em: https://olimpiada.ic.unicamp.br/pratique/p2/2007/f1/choc/

# Entradas
divisoes_original = int(input())
pedacos = input()

# Tratamento
pedacos = pedacos.split(' ')
for i in range(len(pedacos)):
  pedacos[i] = int(pedacos[i])


# Lógica
armazenados = 0

for corte in pedacos:
  armazenados += corte -1

# Saída
print(armazenados)
