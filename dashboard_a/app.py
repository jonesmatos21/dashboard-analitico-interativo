import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Dashboard Analítico A")

st.title("📊 Dashboard de Vendas - Versão A")
st.markdown("---")

# Carregamento de dados
df = pd.read_csv('data/vendas.csv')
df['Data'] = pd.to_datetime(df['Data'])

# Filtros na Barra Lateral
st.sidebar.header("Filtros")
regiao_sel = st.sidebar.multiselect("Selecione a Região", options=df['Regiao'].unique(), default=df['Regiao'].unique())
cat_sel = st.sidebar.multiselect("Selecione a Categoria", options=df['Categoria'].unique(), default=df['Categoria'].unique())

# Filtragem dos dados
df_filtered = df[(df['Regiao'].isin(regiao_sel)) & (df['Categoria'].isin(cat_sel))]

# Layout de Colunas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribuição por Estado (Mapa)")
    # Simulação de mapa (usando barras para representar estados já que não temos lat/long)
    fig_map = px.bar(df_filtered, x='Estado', y='Valor', color='Regiao',
                     title="Total por Estado", labels={'Valor': 'Vendas (R$)'})
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.subheader("Evolução Temporal")
    df_time = df_filtered.groupby('Data')['Valor'].sum().reset_index()
    fig_time = px.line(df_time, x='Data', y='Valor', title="Vendas ao Longo do Tempo")
    st.plotly_chart(fig_time, use_container_width=True)

st.markdown("---")
col3, col4 = st.columns(2)

with col3:
    st.subheader("Análise de Categoria")
    fig_cat = px.bar(df_filtered, x='Categoria', y='Valor', color='Categoria',
                     title="Vendas por Categoria")
    st.plotly_chart(fig_cat, use_container_width=True)

with col4:
    st.subheader("Mapa de Calor (Região x Categoria)")
    pivot_df = df_filtered.pivot_table(index='Regiao', columns='Categoria', values='Valor', aggfunc='sum')
    fig_heat = px.imshow(pivot_df, text_auto=True, title="Heatmap Região vs Categoria")
    st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("---")
st.subheader("Detalhes dos Dados")
st.dataframe(df_filtered)
