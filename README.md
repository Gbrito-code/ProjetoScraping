# 📦 Projeto: Análise de Notebooks do Mercado Livre


## Descrição

Este projeto realiza uma **ETL completa** dos notebooks anunciados no [Mercado Livre](https://www.mercadolivre.com.br), extraindo dados automaticamente com `Scrapy`, transformando e armazenando com `pandas` + `SQLite`, e por fim apresentando os dados em um **dashboard interativo em Streamlit**.

---

## Estrutura do Projeto

```
├── .git/                  # Configurações do Git
├── .venv/                 # Ambiente virtual Python
├── data/
│   ├── mercadolivre.db   # Banco de dados SQLite com os produtos coletados
│   └── data.json         # Backup/exportação da coleta em JSON
├── src/
│   ├── dashboard/
│   │   └── app.py        # Dashboard interativo com Streamlit
│   ├── extraction/
│   │   └── spiders/
│   │       └── notebook.py # Spider Scrapy para coletar dados de notebooks
│   └── transformLoad/
│       └── main.py       # Tratamento e carregamento dos dados com pandas
```

---

## ⚙️ Tecnologias Utilizadas

- Python 3.11+
- Scrapy – Coleta de dados (web scraping)
- Pandas – Transformação de dados
- SQLite – Banco de dados local
- Streamlit – Dashboard interativo
- Seaborn + Matplotlib – Visualizações gráficas

---

## 🚀 Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

### 2. Crie o ambiente virtual e ative

```bash
python -m venv .venv
source  .venv\Scripts\activate # ou .venv/bin/activate no Linux
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Coleta de dados

```bash
cd src/extraction
scrapy crawl notebook -o ../../data/data.json
```

> Isso irá gerar ou atualizar `data.json` com os dados dos notebooks.

### 5. Transformação dos dados

```bash
cd ../../transformLoad
python main.py
```

> Esta etapa trata os dados e grava no banco `mercadolivre.db`.

### 6. Executar o dashboard

```bash
cd ../dashboard
streamlit run app.py
```

---

## 📊 O que o Dashboard mostra?

- Quantidade total de notebooks
- Preço médio e avaliação média
- Filtros por faixa de preço, avaliação e busca textual
- Gráficos interativos de dispersão, tendência e distribuição
- Tabela com os dados filtrados

---

## 🛡️ Aviso legal

Este projeto é de **uso educacional**. Não há fins comerciais nem automações agressivas.  
Recomendamos respeitar os termos de uso do Mercado Livre para coleta de dados.

---

