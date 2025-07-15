import pandas as pd
import random

marcas_modelos = {
    "Toyota": ["Corolla", "Yaris", "Hilux"],
    "Honda": ["Civic", "Fit", "HR-V"],
    "Chevrolet": ["Onix", "Cruze", "Tracker"],
    "Ford": ["Ka", "Fiesta", "EcoSport"],
    "Volkswagen": ["Gol", "Polo", "T-Cross"],
    "Hyundai": ["HB20", "Creta", "Tucson"]
}

combustiveis = ["gasolina", "etanol", "flex", "diesel"]
transmissoes = ["manual", "automático", "CVT"]
cores = ["preto", "branco", "prata", "azul", "vermelho", "cinza"]

data = []

for _ in range(100):
    marca = random.choice(list(marcas_modelos.keys()))
    modelo = random.choice(marcas_modelos[marca])
    ano = random.randint(2015, 2023)
    motorizacao = f"{random.choice([1.0, 1.4, 1.6, 2.0]):.1f}"
    combustivel = random.choice(combustiveis)
    transmissao = random.choice(transmissoes)
    km = random.randint(10000, 90000)
    portas = random.choice([2, 4])
    cor = random.choice(cores)
    preco = random.randint(35000, 120000)

    data.append({
        "marca": marca,
        "modelo": modelo,
        "ano": ano,
        "motorizacao": motorizacao,
        "combustivel": combustivel,
        "transmissao": transmissao,
        "quilometragem": km,
        "portas": portas,
        "cor": cor,
        "preco": preco
    })

df = pd.DataFrame(data)
df.to_excel("base_veiculos.xlsx", index=False)
print("Excel salvo como base_veiculos.xlsx")
