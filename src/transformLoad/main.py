#importar as bibliotecas
import pandas as pd
import sqlite3
from datetime import datetime


#Definir o caminho para o arquivo JSON ou CSV 
df = pd.read_json("data/data.json")


#Setar o pandas para exibir todas as colunas
pd.set_option('display.max_columns', None)

#Precisamos saber da onde veio esse arquivo, ou seja, de onde foi coletado.
#E vamos precisar da data de extração, ou seja, a data e hora que foi coletado.

#adicionar a coluna _source com o nome do arquivo
df['_source'] = "https://lista.mercadolivre.com.br/notebook#"

#adicionar a colina data de extração com a data e hora atual
df['data_extracao'] = datetime.now()

#tratar os valores nulos
df['preço_antigo'] = df['preço_antigo'].fillna('0')
df['preço_promocional'] = df['preço_promocional'].fillna('0')
df['avaliacao'] = df['avaliacao'].fillna('0')
df['quantidade_de_avaliacao'] = df['quantidade_de_avaliacao'].fillna('(0)')

#tratar os valores nulos para colunas numéricas e de texto
df['preço_antigo'] = df['preço_antigo'].astype(str).str.replace('.', '', regex=False)
df['preço_promocional'] = df['preço_promocional'].astype(str).str.replace('.', '', regex=False)
df['quantidade_de_avaliacao'] = df['quantidade_de_avaliacao'].astype(str).str.replace('[\(\)]', '', regex=True)

# Converter para números
df['preço_antigo'] = df['preço_antigo'].astype(float)
df['preço_promocional'] = df['preço_promocional'].astype(float)
df['avaliacao'] = df['avaliacao'].astype(float)
df['quantidade_de_avaliacao'] = df['quantidade_de_avaliacao'].astype(int)


# Tratar os preços como floats e calcular os valores totais
# Manter apenas produtos com preço entre 1000 e 10000 reais
df = df[
    (df['preço_antigo'] >= 1000) & (df['preço_antigo'] <= 10000) &
    (df['preço_promocional'] >= 1000) & (df['preço_promocional'] <= 10000)
]

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('data/mercadolivre.db')

#Salvar o DataFrame no banco de dados
df.to_sql('notebooks', conn, if_exists='replace', index=False)

#fechar a conexão com o banco de dados
conn.close()