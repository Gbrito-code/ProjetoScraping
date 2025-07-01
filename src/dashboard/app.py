import streamlit as st
import pandas as pd
import sqlite3

#conectar ao banco de dados SQLite
conn = sqlite3.connect('data/mercadolivre.db')

#carregar os dados do banco de dados
df = pd.read_sql_query("SELECT * FROM notebooks", conn)

#fechar a conexão com o banco de dados
conn.close()

# Título da aplicação
st.title('📊 Pesquisa de Mercado - Notebooks no Mercado Livre')

# Melhorar o layout com colunas para KPIs
st.subheader('💡 KPIs principais')
col1, col2, col3 = st.columns(3)

# KPI 1: Número total de itens
total_itens = df.shape[0]
col1.metric(label="🖥️ Total de Notebooks", value=total_itens)

# KPI 2: Número de marcas únicas
unique_brands = df['marca'].nunique()
col2.metric(label="🏷️ Marcas Únicas", value=unique_brands)

# KPI 3: Preço médio novo (em reais)
average_new_price = df['preço_promocional'].mean()
col3.metric(label="💰 Preço Médio (R$)", value=f"{average_new_price:.2f}")

# Marcas mais frequentes
st.subheader('🏆 Marcas mais encontradas até a 10ª página')
col1, col2 = st.columns([4, 2])
top_brands = df['marca'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_brands)
col2.write(top_brands)

# Preço médio por marca
st.subheader('💵 Preço médio por marca')
col1, col2 = st.columns([4, 2])
df_non_zero_prices = df[df['preço_promocional'] > 0]
average_price_by_brand = df_non_zero_prices.groupby('marca')['preço_promocional'].mean().sort_values(ascending=False)
col1.bar_chart(average_price_by_brand)
col2.write(average_price_by_brand)

# Satisfação média por marca
st.subheader('⭐ Satisfação média por marca')
col1, col2 = st.columns([4, 2])
df_non_zero_reviews = df[df['avaliacao'] > 0]
satisfaction_by_brand = df_non_zero_reviews.groupby('marca')['avaliacao'].mean().sort_values(ascending=False)
col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)