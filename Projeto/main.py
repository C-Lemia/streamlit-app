import pandas as pd

# Carregar os arquivos CSV fornecidos
clientes_df = pd.read_csv('CLIENTES.csv', delimiter=';')
filiais_df = pd.read_csv('FILIAIS.csv', delimiter=';')
produtos_df = pd.read_csv('PRODUTOS.csv', delimiter=';')
vendas_df = pd.read_csv('VENDAS_PRODUTOS.csv', delimiter=';')
vendasf_df = pd.read_csv('VENDAS.csv', delimiter=';')

# Remover espaços em branco nos nomes das colunas de todos os dataframes
clientes_df.columns = clientes_df.columns.str.strip()
filiais_df.columns = filiais_df.columns.str.strip()
produtos_df.columns = produtos_df.columns.str.strip()
vendas_df.columns = vendas_df.columns.str.strip()
vendasf_df.columns = vendasf_df.columns.str.strip()

# Unificar os dataframes de clientes e filiais com base na coluna 'CIDADE'
cliente_filial_df = pd.merge(clientes_df, filiais_df, on='CIDADE', how='left')

# Exibir as primeiras linhas do dataframe resultante
print("DataFrame de Clientes e Filiais:")
print(cliente_filial_df.head())

# Unir vendas de produtos com as informações dos produtos usando a chave 'ID_PRODUTO'
vendas_produtos_df = pd.merge(vendas_df, produtos_df, on='ID_PRODUTO', how='left')

# Agrupar as vendas por filial e produto, somando as quantidades vendidas
vendas_por_filial = vendas_produtos_df.groupby(['ID_PRODUTO', 'NOME_PRODUTO']).agg({'QUANTIDADE': 'sum'}).reset_index()

# Exibir as primeiras linhas do dataframe de vendas por produto e quantidade total
print("\nVendas por Produto:")
print(vendas_por_filial.head())


# Unificar os dataframes de vendas com os produtos
vendas_produtos_df = pd.merge(vendas_df, produtos_df, on='ID_PRODUTO', how='left')

# Unificar os dataframes de vendas com as filiais, através de `ID_FILIAL`
vendas_filiais_df = pd.merge(vendas_produtos_df, vendasf_df[['ID_VENDA', 'ID_FILIAL']], on='ID_VENDA', how='left')
vendas_filiais_df = pd.merge(vendas_filiais_df, filiais_df, on='ID_FILIAL', how='left')

# Agrupar as vendas por filial e produto, somando as quantidades
vendas_agrupadas = vendas_filiais_df.groupby(['NOME_FILIAL', 'NOME_PRODUTO']).agg({'QUANTIDADE': 'sum'}).reset_index()

# Encontrar o produto mais vendido em cada filial
produto_mais_vendido_por_filial = vendas_agrupadas.loc[vendas_agrupadas.groupby('NOME_FILIAL')['QUANTIDADE'].idxmax()]

# Exibir as informações do produto mais vendido por filial
print("\nProduto mais vendido por filial:")
print(produto_mais_vendido_por_filial)


vendasf_df['VALOR_VENDA'] = vendasf_df['VALOR_VENDA'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
vendasf_df['VALOR_VENDA'] = vendasf_df['VALOR_VENDA'].astype(float)


vendasf_df['DATA_VENDA'] = pd.to_datetime(vendasf_df['DATA_VENDA'], format='%d/%m/%Y')

# Criar uma nova coluna 'MES' a partir da data de venda
vendasf_df['MES'] = vendasf_df['DATA_VENDA'].dt.to_period('M')

# Agrupar as vendas por filial e mês, somando os lucros (VALOR_VENDA)
lucro_por_filial_mes = vendasf_df.groupby(['ID_FILIAL', 'MES']).agg({'VALOR_VENDA': 'sum'}).reset_index()
lucro_por_filial_mes.head()

lucro_com_nome_filial = pd.merge(lucro_por_filial_mes, filiais_df[['ID_FILIAL', 'NOME_FILIAL']], on='ID_FILIAL', how='left')
print(lucro_com_nome_filial)