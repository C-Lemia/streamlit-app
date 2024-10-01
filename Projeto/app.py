import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


# Configura o cabeçalho com a imagem à direita
col1, col2 = st.columns([3, 1])  # Define uma coluna maior à esquerda e uma menor à direita

with col1:
    st.title("Inteligência de Mercado")
    
with col2:
    # Exibe a imagem na coluna direita
    st.image('Captura de tela 2024-10-01 114828.png', use_column_width=True)
    #st.image('Captura de tela 2024-10-01 114828.png', use_column_width=False, width=200)  # Ajuste o valor de 'width' conforme necessário


# Aplicar cor de fundo personalizada no Strea
# Aplicar cor de fundo personalizada no Streamlit
# Aplicar estilos personalizados usando CSS
st.markdown(
    """
    <style>
    /* Importar a fonte Roboto do Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    /* Aplicar a fonte Roboto a todo o aplicativo */
    .stApp {
        font-family: 'Roboto', sans-serif;
        background-color: #F0F8FF; /* Cor de fundo personalizada */
    }

    /* Estilizar as abas não selecionadas */
    div[data-testid="stTabs"] button {
        color: #013A61; /* Cor das letras das abas não selecionadas */
    }

    /* Estilizar a aba selecionada */
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #013A61; /* Cor das letras da aba selecionada */
        border-bottom: 2px solid #013A61; /* Linha inferior da aba selecionada */
    }

    /* Estilizar as abas ao passar o cursor */
    div[data-testid="stTabs"] button:hover {
        color: #013A61; /* Cor das letras das abas ao passar o cursor */
    }

    /* Estilizar os widgets para melhor responsividade */
    .stSelectbox, .stMultiselect {
        width: 100% !important;
        box-sizing: border-box;
    }

    /* Garantir que os widgets sejam visíveis em telas menores */
    @media (max-width: 600px) {
        .stSelectbox, .stMultiselect {
            font-size: 16px !important;
        }
    }

    /* Opcional: Estilizar outros elementos conforme necessário */
    /* Exemplo: Alterar a cor dos títulos */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #013A61;
    }
    </style>
    """,
    unsafe_allow_html=True
)



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

# Unificar os dataframes de vendas com os produtos e filiais
vendas_produtos_df = pd.merge(vendas_df, produtos_df, on='ID_PRODUTO', how='left')
vendas_filiais_df = pd.merge(vendas_produtos_df, vendasf_df[['ID_VENDA', 'ID_FILIAL']], on='ID_VENDA', how='left')
vendas_filiais_df = pd.merge(vendas_filiais_df, filiais_df, on='ID_FILIAL', how='left')

# Agrupar as vendas por filial e produto, somando as quantidades
vendas_agrupadas = vendas_filiais_df.groupby(['NOME_FILIAL', 'NOME_PRODUTO']).agg({'QUANTIDADE': 'sum'}).reset_index()

# Criar as abas no Streamlit
abas = st.tabs(["Produtos Mais Vendidos", "Produtos Menos Vendidos", "Comparação entre Filiais", "Total de Vendas por Mês"])

# Primeira aba: Mostrar os 5 produtos mais vendidos por filial
with abas[0]:
    st.header("Produtos Mais Vendidos por Filial")
    
    filial_selecionada = st.selectbox('Selecione a Filial', vendas_agrupadas['NOME_FILIAL'].unique(), key="mais_vendidos")
    vendas_filial_selecionada = vendas_agrupadas[vendas_agrupadas['NOME_FILIAL'] == filial_selecionada]
    top_5_produtos = vendas_filial_selecionada.nlargest(5, 'QUANTIDADE')
    
    # Definir um índice de posição para o gráfico
    bar_width = 0.25
    indices = np.arange(len(top_5_produtos))

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Adicionar as barras no gráfico
    ax.bar(indices, top_5_produtos['QUANTIDADE'], width=bar_width, color='#013A61')

    # Definir detalhes do gráfico
    ax.set_ylabel('Quantidade Vendida')
    ax.set_title(f'Produtos Mais Vendidos - Filial {filial_selecionada}')
    ax.set_xticks(indices)
    ax.set_xticklabels(top_5_produtos['NOME_PRODUTO'], rotation=45, ha='right')
    
    # Exibir o gráfico no Streamlit
    st.pyplot(fig)

    # Análise e recomendações práticas
    st.subheader("Recomendações")

    # Aplicar a cor de fundo no texto
    st.markdown(f"""
        <div style="background-color:#013A61; padding:10px; border-radius:5px;">
            <p style="color:white;">A análise mostra os 5 produtos mais vendidos na Filial {filial_selecionada} e indicam uma preferência clara do público local. 
            Recomenda-se aumentar o estoque desses produtos para evitar rupturas e ajustar o marketing para focar nesses itens.
            Ofertas promocionais em torno desses produtos podem atrair mais clientes e fidelizar a base de consumidores.</p>
        </div>
        """, unsafe_allow_html=True)

# Segunda aba: Mostrar os 5 produtos menos vendidos por filial
with abas[1]:
    st.header("Produtos Menos Vendidos por Filial")
    
    filial_selecionada = st.selectbox('Selecione a Filial', vendas_agrupadas['NOME_FILIAL'].unique(), key="menos_vendidos")
    vendas_filial_selecionada = vendas_agrupadas[vendas_agrupadas['NOME_FILIAL'] == filial_selecionada]
    bottom_5_produtos = vendas_filial_selecionada.nsmallest(5, 'QUANTIDADE')
    
    # Definir um índice de posição para o gráfico
    bar_width = 0.25
    indices = np.arange(len(bottom_5_produtos))

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Adicionar as barras no gráfico
    ax.bar(indices, bottom_5_produtos['QUANTIDADE'], width=bar_width, color='#D2691E')

    # Definir detalhes do gráfico
    ax.set_ylabel('Quantidade Vendida')
    ax.set_title(f'Produtos Menos Vendidos - Filial {filial_selecionada}')
    ax.set_xticks(indices)
    ax.set_xticklabels(bottom_5_produtos['NOME_PRODUTO'], rotation=45, ha='right')
    
    # Exibir o gráfico no Streamlit
    st.pyplot(fig)

    # Análise e recomendações práticas
    st.subheader("Recomendações")

    # Aplicar a cor de fundo no texto
    st.markdown(f"""
        <div style="background-color:#013A61; padding:10px; border-radius:5px;">
            <p style="color:white;">Os produtos menos vendidos na Filial {filial_selecionada} e sugerem uma demanda reduzida ou uma oferta desajustada. 
            Recomenda-se investigar as razões para o baixo desempenho, como preço, localização dos produtos na loja ou falta de divulgação. 
            Se o produto não se alinhar com o público local, é possível reduzir o estoque ou substituí-lo por itens mais populares.</p>
        </div>
        """, unsafe_allow_html=True)

# Terceira aba: Comparar os 10 produtos mais vendidos entre até três filiais
with abas[2]:
    st.header("Comparação dos 10 Produtos Mais Vendidos entre Filiais")
    
    # Widget para seleção de até três filiais
    filiais_selecionadas = st.multiselect('Selecione até 3 Filiais para Comparar', vendas_agrupadas['NOME_FILIAL'].unique(), default=None, key="comparacao_filiais", max_selections=3)
    
    if filiais_selecionadas:
        # Filtrar os dados para as filiais selecionadas
        vendas_filiais_comparacao = vendas_agrupadas[vendas_agrupadas['NOME_FILIAL'].isin(filiais_selecionadas)]
        
        # Selecionar os 10 produtos mais vendidos no total para todas as filiais selecionadas
        produtos_top_10 = vendas_filiais_comparacao.groupby('NOME_PRODUTO')['QUANTIDADE'].sum().nlargest(10).index
        
        # Definir um índice de posição para o gráfico
        bar_width = 0.25
        indices = np.arange(len(produtos_top_10))

        fig, ax = plt.subplots(figsize=(10, 6))
        cores = ['#013A61', '#F57C00', '#F1E4D0'] 
        for i, filial in enumerate(filiais_selecionadas):
            vendas_filial = vendas_filiais_comparacao[vendas_filiais_comparacao['NOME_FILIAL'] == filial]
            vendas_filial = vendas_filial.set_index('NOME_PRODUTO').reindex(produtos_top_10).fillna(0)
            
            # Ajustar a posição das barras de acordo com a posição dos índices e bar_width
            ax.bar(indices + i * bar_width, vendas_filial['QUANTIDADE'], width=bar_width, label=filial)
        
        # Definir detalhes do gráfico
        ax.set_xlabel('Produtos')
        ax.set_ylabel('Quantidade Vendida')
        ax.set_title('Comparação dos 10 Produtos Mais Vendidos entre Filiais')
        ax.set_xticks(indices + bar_width / 2)
        ax.set_xticklabels(produtos_top_10, rotation=45, ha='right')
        ax.legend(title='Filiais')
        
        # Exibir o gráfico no Streamlit
        st.pyplot(fig)


        # Análise e recomendações práticas
        st.subheader("Recomendações")
        
        # Aplicar a cor de fundo no texto
        st.markdown(f"""
        <div style="background-color:#013A61; padding:10px; border-radius:5px;">
            <p style="color:white;">A comparação entre as filiais revela como os produtos têm diferentes desempenhos em diferentes localidades. 
            Considere ajustar a distribuição de produtos com base nas preferências locais. Produtos que são bem-sucedidos em uma filial 
            podem se beneficiar de campanhas de marketing e promoções direcionadas em outras filiais para aumentar as vendas.</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.write("Por favor, selecione até 3 filiais para comparação.")
    


# Conversão dos valores de venda para o formato correto
vendasf_df['VALOR_VENDA'] = vendasf_df['VALOR_VENDA'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
vendasf_df['VALOR_VENDA'] = vendasf_df['VALOR_VENDA'].astype(float)

# Criar uma nova coluna 'MES' a partir da data de venda
vendasf_df['DATA_VENDA'] = pd.to_datetime(vendasf_df['DATA_VENDA'], format='%d/%m/%Y')  # Alterado para o formato correto
vendasf_df['MES'] = vendasf_df['DATA_VENDA'].dt.to_period('M')

# Quarta aba: Gráfico de total de vendas em R$ por mês para uma filial selecionada
with abas[3]:
    st.header("Total de Vendas por Mês - Filial")
    
    # Widget para selecionar a filial
    filial_selecionada = st.selectbox('Selecione a Filial para ver as Vendas Mensais em R$', filiais_df['NOME_FILIAL'].unique(), key="vendas_mensais_reais")
    
    # Filtrar as vendas para a filial selecionada
    vendas_filial = vendasf_df[vendasf_df['ID_FILIAL'].isin(filiais_df[filiais_df['NOME_FILIAL'] == filial_selecionada]['ID_FILIAL'].values)]
    
    # Agrupar as vendas por mês, somando os valores
    total_vendas_mes = vendas_filial.groupby('MES').agg({'VALOR_VENDA': 'sum'}).reset_index()
    
    # Plotar o gráfico se houver dados
    if not total_vendas_mes.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(total_vendas_mes['MES'].astype(str), total_vendas_mes['VALOR_VENDA'], marker='o', linestyle='-', color='#013A61')

        # Definir detalhes do gráfico
        ax.set_xlabel('Mês')
        ax.set_ylabel('Total de Vendas (R$)')
        ax.set_title(f'Total de Vendas por Mês - Filial {filial_selecionada}')
        ax.tick_params(axis='x', rotation=45)

        # Exibir o gráfico no Streamlit
        st.pyplot(fig)

        # Análise e recomendações práticas
        st.subheader("Recomendações")
        st.markdown(f"""
        <div style="background-color:#013A61; padding:10px; border-radius:5px;">
            <p style="color:white;">Com base nas tendências de vendas mensais da Filial {filial_selecionada}, recomenda-se ajustar os estoques para prever períodos de alta demanda. 
            Além disso, promoções específicas podem ser planejadas para meses de baixa performance, incentivando as vendas.</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.write("Nenhum dado de vendas encontrado para a filial selecionada.")