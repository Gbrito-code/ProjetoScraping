import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

# Estilo dos gráficos
# Define o estilo visual dos gráficos do Seaborn.
# "whitegrid" adiciona uma grade branca de fundo, útil para gráficos com valores numéricos
sns.set(style="whitegrid")
# Configura a página do Streamlit para usar layout "wide" (mais espaço horizontal na tela).
st.set_page_config(layout="wide")

# Conectar e carregar dados
conn = sqlite3.connect('data/mercadolivre.db')
df = pd.read_sql_query("SELECT * FROM notebooks", conn)
conn.close()



# Limpeza de dados (remove preços nulos ou inválidos)
# O resultado substitui o próprio df.
# Isso evita valores faltantes ou inválidos nos gráficos.
df = df[(df['preço_promocional'] > 0) & (df['avaliacao'] > 0)]

# Título
st.title("📊 Pesquisa Interativa - Notebooks no Mercado Livre")

# Filtros interativos
st.sidebar.header("🔍 Filtros")

# Faixa de preço 
# Esses valores serão os limites do slider de preço.
min_price = int(df['preço_promocional'].min())
max_price = int(df['preço_promocional'].max())
faixa_preco = st.sidebar.slider("Faixa de Preço (R$)", min_value=min_price, max_value=max_price, value=(min_price, max_price))

# Faixa de avaliação
# Cria um slider de avaliação (de 0 a 5 estrelas) com passo de 0.5.
faixa_avaliacao = st.sidebar.slider("Avaliação (estrelas)", 0.0, 5.0, (0.0, 5.0), step=0.5)

# Filtra os dados de acordo com os critérios selecionados pelo usuário
filtro_df = df[
    (df['preço_promocional'] >= faixa_preco[0]) & 
    (df['preço_promocional'] <= faixa_preco[1]) & 
    (df['avaliacao'] >= faixa_avaliacao[0]) & 
    (df['avaliacao'] <= faixa_avaliacao[1])
]


# Sugestões automáticas: modelos mais comuns
sugestoes_modelos = df['nome'].value_counts().head(30).index.tolist()

# Multiselect com sugestões populares
modelos_selecionados = st.sidebar.multiselect(
    "🧠 Escolha modelos populares (opcional)",
    options=sugestoes_modelos
)

# Campo de texto livre para busca por qualquer termo
termo_busca = st.sidebar.text_input("🔍 Buscar por nome, modelo ou palavra-chave (ex: 'i5', 'Ryzen', '512')")

# Aplica filtro por modelos específicos (caso selecionado)
if modelos_selecionados:
    filtro_df = filtro_df[filtro_df['nome'].isin(modelos_selecionados)]

# Aplica filtro por texto digitado
if termo_busca:
    filtro_df = filtro_df[filtro_df['nome'].str.contains(termo_busca, case=False, na=False)]



# Exibir KPIs
st.subheader("💡 Visão Geral")
col1, col2, col3 = st.columns(3)
col1.metric("🖥️ Produtos Filtrados", filtro_df.shape[0])
col2.metric("💰 Preço Médio", f"R$ {filtro_df['preço_promocional'].mean():.2f}")
col3.metric("⭐ Avaliação Média", f"{filtro_df['avaliacao'].mean():.2f}")

# 📊 Histograma de preços
st.subheader("📈 Distribuição de Preços")
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.histplot(filtro_df['preço_promocional'], bins=30, kde=True, ax=ax1, color="skyblue")
ax1.set_xlabel("Preço Promocional (R$)")
ax1.set_ylabel("Quantidade de produtos")
st.pyplot(fig1)


st.subheader("📊 Avaliação vs Preço Promocional")

col1, col2 = st.columns(2)

# 🎯 Gráfico de Dispersão (Scatterplot)
with col1:
    st.markdown("**🎯 Dispersão Avaliação x Preço**")
    fig_scatter, ax_scatter = plt.subplots(figsize=(5, 4))
    sns.scatterplot(
        data=filtro_df,
        x='avaliacao',
        y='preço_promocional',
        hue='avaliacao',
        palette='coolwarm',
        ax=ax_scatter,
        legend=False
    )
    ax_scatter.set_xlabel("Avaliação (estrelas)")
    ax_scatter.set_ylabel("Preço Promocional (R$)")
    st.pyplot(fig_scatter)

# 📈 Gráfico com Linha de Tendência (Regplot)
with col2:
    st.markdown("**📈 Tendência Linear: Avaliação x Preço**")
    fig_reg, ax_reg = plt.subplots(figsize=(5, 4))
    sns.regplot(
        data=filtro_df,
        x='avaliacao',
        y='preço_promocional',
        scatter_kws={"s": 40, "alpha": 0.6},
        line_kws={"color": "red"},
        ax=ax_reg
    )
    ax_reg.set_xlabel("Avaliação (estrelas)")
    ax_reg.set_ylabel("Preço Promocional (R$)")
    st.pyplot(fig_reg)


# 📋 Tabela com dados filtrados
st.subheader("📋 Tabela com os dados filtrados")
st.dataframe(filtro_df.reset_index(drop=True))
