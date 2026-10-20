import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Gerando dados sintéticos para auditoria
np.random.seed(42)
n_rows = 1000

regioes = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
categorias = ['Eletrônicos', 'Vestuário', 'Alimentos', 'Casa e Jardim', 'Beleza']
estados = {
    'Norte': ['AM', 'PA', 'AC', 'RO', 'RR', 'AP', 'TO'],
    'Nordeste': ['BA', 'PE', 'CE', 'RN', 'PB', 'AL', 'SE', 'MA', 'PI'],
    'Centro-Oeste': ['MT', 'MS', 'GO', 'DF'],
    'Sudeste': ['SP', 'RJ', 'MG', 'ES'],
    'Sul': ['RS', 'SC', 'PR']
}

start_date = datetime(2023, 1, 1)
dates = [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(n_rows)]
regiao_list = np.random.choice(regioes, n_rows)
cat_list = np.random.choice(categorias, n_rows)
valores = np.random.uniform(100, 5000, n_rows)

data = []
for i in range(n_rows):
    reg = regioes[np.random.randint(0, 5)] # Re-sorting for state consistency
    est = np.random.choice(estados[reg])
    data.append([dates[i], reg, est, cat_list[i], valores[i]])

df = pd.DataFrame(data, columns=['Data', 'Regiao', 'Estado', 'Categoria', 'Valor'])
df.to_csv('data/vendas.csv', index=False)
