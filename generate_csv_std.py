import csv
import random
from datetime import datetime, timedelta

regioes = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
categorias = ['Eletrônicos', 'Vestuário', 'Alimentos', 'Casa e Jardim', 'Beleza']
estados = {
    'Norte': ['AM', 'PA', 'AC', 'RO', 'RR', 'AP', 'TO'],
    'Nordeste': ['BA', 'PE', 'CE', 'RN', 'PB', 'AL', 'SE', 'MA', 'PI'],
    'Centro-Oeste': ['MT', 'MS', 'GO', 'DF'],
    'Sudeste': ['SP', 'RJ', 'MG', 'ES'],
    'Sul': ['RS', 'SC', 'PR']
}

with open('data/vendas.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Data', 'Regiao', 'Estado', 'Categoria', 'Valor'])

    start_date = datetime(2023, 1, 1)
    for i in range(1000):
        reg = random.choice(regioes)
        est = random.choice(estados[reg])
        cat = random.choice(categorias)
        val = round(random.uniform(100, 5000), 2)
        date = (start_date + timedelta(days=random.randint(0, 364))).strftime('%Y-%m-%d')
        writer.writerow([date, reg, est, cat, val])
