import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Lendo o arquivo Excel
file_path = 'Vendas_01.01.2023 a 30.06.2024_Boutique.xlsx'
df = pd.read_excel(file_path)

# Análises de dados
# 1. Identificação de Produtos Populares
vendas_por_produto = df.groupby('Produto')['Vendas'].sum()
total_vendas = vendas_por_produto.sum()
participacao_percentual = (vendas_por_produto / total_vendas) * 100
produto_mais_vendido = vendas_por_produto.idxmax()
participacao_produto_mais_vendido = participacao_percentual.max()

# Identificação de Produtos Menos Vendidos
produto_menos_vendido = vendas_por_produto.idxmin()
participacao_produto_menos_vendido = participacao_percentual.min()

# 2. Tendências Sazonais
df['Data'] = pd.to_datetime(df['Data'])
df['Mês'] = df['Data'].dt.month
df['Ano'] = df['Data'].dt.year
vendas_mensais = df.groupby(['Ano', 'Mês'])['Vendas'].sum().reset_index()
tendencia_mensal = vendas_mensais.groupby('Mês')['Vendas'].mean()

# 3. Desempenho ao Longo do Tempo
vendas_mensais = vendas_mensais.rename(columns={'Ano': 'Year', 'Mês': 'Month'})
vendas_mensais['Day'] = 1
vendas_mensais['Data_Completa'] = pd.to_datetime(vendas_mensais[['Year', 'Month', 'Day']])
vendas_mensais = vendas_mensais.sort_values('Data_Completa')
vendas_mensais['Crescimento_Mensal'] = vendas_mensais['Vendas'].pct_change() * 100
media_crescimento_mensal = vendas_mensais['Crescimento_Mensal'].mean()

# 4. Análise de Vendas por Categoria de Produto
vendas_por_categoria = df.groupby('Categoria')['Vendas'].sum()
total_vendas_categoria = vendas_por_categoria.sum()
participacao_categoria = (vendas_por_categoria / total_vendas_categoria) * 100
categoria_principal = participacao_categoria.idxmax()
participacao_principal = participacao_categoria.max()
categoria_secundaria = participacao_categoria.idxmin()
participacao_secundaria = participacao_categoria.min()

# 6. Produto com Maior Crescimento
crescimento_produtos = df.groupby(['Ano', 'Produto'])['Vendas'].sum().unstack().pct_change().iloc[-1] * 100
produto_maior_crescimento = crescimento_produtos.idxmax()
percentual_crescimento_produto = crescimento_produtos.max()

# 7. Categoria com Maior Crescimento
crescimento_categorias = df.groupby(['Ano', 'Categoria'])['Vendas'].sum().unstack().pct_change().iloc[-1] * 100
categoria_maior_crescimento = crescimento_categorias.idxmax()
percentual_crescimento_categoria = crescimento_categorias.max()

# 8. Distribuição de Vendas por Categoria
fig_pie = px.pie(vendas_por_categoria, values='Vendas', names=vendas_por_categoria.index, title='Distribuição de Vendas por Categoria')

# Gráfico de produtos mais vendidos
top_produtos = vendas_por_produto.nlargest(10)  
fig_top_produtos = px.bar(top_produtos, x=top_produtos.index, y='Vendas', title='Top 10 Produtos Mais Vendidos')

# Gráfico de produtos menos vendidos
bottom_produtos = vendas_por_produto.nsmallest(10)  
fig_bottom_produtos = px.bar(bottom_produtos, x=bottom_produtos.index, y='Vendas', title='Top 10 Produtos Menos Vendidos')

# Gráfico de crescimento mensal médio
fig_crescimento_mensal = px.line(vendas_mensais, x='Data_Completa', y='Crescimento_Mensal', title='Crescimento Mensal Médio')

# Encontrar o mês com mais vendas em 2023
vendas_2023 = df[df['Ano'] == 2023]
mes_com_mais_vendas_2023 = vendas_2023.groupby('Mês')['Vendas'].sum().idxmax()
vendas_mes_2023 = vendas_2023.groupby('Mês')['Vendas'].sum().max()

# Gráfico de barras para 2023
fig_vendas_2023 = px.bar(vendas_2023.groupby('Mês')['Vendas'].sum().reset_index(), 
                         x='Mês', y='Vendas', 
                         title='Vendas Mensais em 2023',
                         labels={'Mês': 'Mês', 'Vendas': 'Vendas'})
fig_vendas_2023.update_traces(marker_color='lightblue')
fig_vendas_2023.add_shape(
    type='rect',
    x0=mes_com_mais_vendas_2023 - 0.5, x1=mes_com_mais_vendas_2023 + 0.5,
    y0=0, y1=vendas_mes_2023,
    line=dict(color='red', width=2)
)

# Encontrar o mês com mais vendas em 2024
vendas_2024 = df[df['Ano'] == 2024]
if not vendas_2024.empty:
    mes_com_mais_vendas_2024 = vendas_2024.groupby('Mês')['Vendas'].sum().idxmax()
    vendas_mes_2024 = vendas_2024.groupby('Mês')['Vendas'].sum().max()
else:
    mes_com_mais_vendas_2024 = None
    vendas_mes_2024 = 0

# Gráfico de barras para 2024
fig_vendas_2024 = px.bar(vendas_2024.groupby('Mês')['Vendas'].sum().reset_index(), 
                         x='Mês', y='Vendas', 
                         title='Vendas Mensais em 2024',
                         labels={'Mês': 'Mês', 'Vendas': 'Vendas'})
fig_vendas_2024.update_traces(marker_color='lightgreen')
if mes_com_mais_vendas_2024 is not None:
    fig_vendas_2024.add_shape(
        type='rect',
        x0=mes_com_mais_vendas_2024 - 0.5, x1=mes_com_mais_vendas_2024 + 0.5,
        y0=0, y1=vendas_mes_2024,
        line=dict(color='red', width=2)
    )

# Comparação de Vendas entre o Primeiro e Segundo Semestre de 2023
vendas_primeiro_semestre_2023 = vendas_2023[vendas_2023['Mês'].isin([1, 2, 3, 4, 5, 6])]['Vendas'].sum()
vendas_segundo_semestre_2023 = vendas_2023[vendas_2023['Mês'].isin([7, 8, 9, 10, 11, 12])]['Vendas'].sum()
fig_comparacao_semestral_2023 = px.bar(
    x=['Primeiro Semestre 2023', 'Segundo Semestre 2023'], 
    y=[vendas_primeiro_semestre_2023, vendas_segundo_semestre_2023], 
    title='Comparação de Vendas entre o Primeiro e Segundo Semestre de 2023',
    labels={'x': 'Semestre', 'y': 'Vendas'}
)

# Top 10 produtos mais vendidos no primeiro semestre de 2023
top_produtos_primeiro_semestre_2023 = vendas_2023[vendas_2023['Mês'].isin([1, 2, 3, 4, 5, 6])]
top_produtos_primeiro_semestre_2023 = top_produtos_primeiro_semestre_2023.groupby('Produto')['Vendas'].sum().nlargest(10)
fig_top_produtos_primeiro_semestre_2023 = px.bar(top_produtos_primeiro_semestre_2023, 
                                                 x=top_produtos_primeiro_semestre_2023.index, 
                                                 y='Vendas', 
                                                 title='Top 10 Produtos Mais Vendidos no Primeiro Semestre de 2023')

# Top 10 produtos mais vendidos no segundo semestre de 2023
top_produtos_segundo_semestre_2023 = vendas_2023[vendas_2023['Mês'].isin([7, 8, 9, 10, 11, 12])]
top_produtos_segundo_semestre_2023 = top_produtos_segundo_semestre_2023.groupby('Produto')['Vendas'].sum().nlargest(10)
fig_top_produtos_segundo_semestre_2023 = px.bar(top_produtos_segundo_semestre_2023, 
                                                x=top_produtos_segundo_semestre_2023.index, 
                                                y='Vendas', 
                                                title='Top 10 Produtos Mais Vendidos no Segundo Semestre de 2023')

# Comparação de Vendas do Primeiro Semestre de 2023 e 2024
vendas_primeiro_semestre_2024 = vendas_2024[vendas_2024['Mês'].isin([1, 2, 3, 4, 5, 6])]['Vendas'].sum() if not vendas_2024.empty else 0
fig_comparacao_primeiro_semestre = px.bar(
    x=['Primeiro Semestre 2023', 'Primeiro Semestre 2024'], 
    y=[vendas_primeiro_semestre_2023, vendas_primeiro_semestre_2024], 
    title='Comparação de Vendas do Primeiro Semestre de 2023 e 2024',
    labels={'x': 'Ano', 'y': 'Vendas'}
)

# Top 10 produtos mais vendidos no primeiro semestre de 2024
top_produtos_primeiro_semestre_2024 = vendas_2024[vendas_2024['Mês'].isin([1, 2, 3, 4, 5, 6])]
if not top_produtos_primeiro_semestre_2024.empty:
    top_produtos_primeiro_semestre_2024 = top_produtos_primeiro_semestre_2024.groupby('Produto')['Vendas'].sum().nlargest(10)
    fig_top_produtos_primeiro_semestre_2024 = px.bar(top_produtos_primeiro_semestre_2024, 
                                                     x=top_produtos_primeiro_semestre_2024.index, 
                                                     y='Vendas', 
                                                     title='Top 10 Produtos Mais Vendidos no Primeiro Semestre de 2024')
else:
    fig_top_produtos_primeiro_semestre_2024 = px.bar(title='Sem dados disponíveis para o Primeiro Semestre de 2024')

# Iniciando o aplicativo Dash
app = dash.Dash(__name__)
server = app.server 

app.layout = html.Div([
    html.H1("Análise de Vendas da Boutique de Carro"),

    html.H3('''A análise foi realizada com dados obtidos no período de 01/01/2023 a 30/06/2024. 
            Apresentamos os resultados dos produtos mais vendidos durante esse intervalo e realizamos 
            comparações entre o primeiro e o segundo semestre de 2023, bem como entre o primeiro semestre
            de 2023 e o primeiro semestre de 2024.'''),

    html.H2("Produto mais vendido"),
    html.P(f"O produto mais vendido do período de 01/01/2023 a 30/06/2024 é {produto_mais_vendido}, contribuindo com {participacao_produto_mais_vendido:.2f}% das vendas totais."),
    dcc.Graph(
        figure=fig_top_produtos
    ),

    html.H2("Produto menos vendido"),
    html.P(f"O produto menos vendido 01/01/2023 a 30/06/2024 é {produto_menos_vendido}, contribuindo com {participacao_produto_menos_vendido:.2f}% das vendas totais."),
    dcc.Graph(
        figure=fig_bottom_produtos
    ),

    html.H2("Tendência das Vendas Mensais"),
    dcc.Graph(
        figure=px.line(vendas_mensais, x='Data_Completa', y='Vendas', title='Tendência das Vendas Mensais')
    ),

    html.H2("Crescimento Mensal Médio"),
    html.P(f"A média de crescimento mensal é de {media_crescimento_mensal:.2f}%."),
    dcc.Graph(
        figure=fig_crescimento_mensal
    ),

    html.H2("Vendas por Categoria"),
    dcc.Graph(
        figure=fig_pie
    ),

    html.H2("Produto com Maior Crescimento"),
    html.P(f"O produto com maior crescimento do período 01/01/2023 a 30/06/2024 é {produto_maior_crescimento}, com um crescimento de {percentual_crescimento_produto:.2f}%."),

    html.H2("Categoria com Maior Crescimento"),
    html.P(f"A categoria com maior crescimento é do período 01/01/2023 a 30/06/2024 {categoria_maior_crescimento}, com um crescimento de {percentual_crescimento_categoria:.2f}%."),

    html.H2("Mês com Mais Vendas em 2023"),
    html.P(f"O mês com mais vendas em 2023 foi o mês {mes_com_mais_vendas_2023}, com um total de {vendas_mes_2023} vendas."),
    dcc.Graph(
        figure=fig_vendas_2023
    ),

    html.H2("Mês com Mais Vendas em 2024"),
    html.P(f"O mês com mais vendas em 2024 do primeiro semestre foi o mês {mes_com_mais_vendas_2024}, com um total de {vendas_mes_2024} vendas." if mes_com_mais_vendas_2024 else "Não há dados de vendas para 2024."),
    dcc.Graph(
        figure=fig_vendas_2024
    ),

    html.H2("Comparação de Vendas entre o Primeiro e Segundo Semestre de 2023"),
    dcc.Graph(
        figure=fig_comparacao_semestral_2023
    ),
    dcc.Graph(
        figure=fig_top_produtos_primeiro_semestre_2023
    ),
    dcc.Graph(
        figure=fig_top_produtos_segundo_semestre_2023
    ),

    html.H2("Comparação de Vendas do Primeiro Semestre de 2023 e 2024"),
    dcc.Graph(
        figure=fig_comparacao_primeiro_semestre
    ),
    dcc.Graph(
        figure=fig_top_produtos_primeiro_semestre_2023
    ),
    dcc.Graph(
        figure=fig_top_produtos_primeiro_semestre_2024
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
