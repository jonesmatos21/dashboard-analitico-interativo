import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Dashboard Analítico B")

st.title("📉 Relatório Executivo de Vendas - Versão B")
st.markdown("---")

# Carregamento de dados
df = pd.read_csv('data/vendas.csv')
df['Data'] = pd.to_datetime(df['Data'])

# Filtros
st.sidebar.header("Filtros de Relatório")
regiao_sel = st.sidebar.selectbox("Região", options=df['Regiao'].unique())

df_filtered = df[df['Regiao'] == regiao_sel]

# KPIs
total_vendas = df_filtered['Valor'].sum()
avg_vendas = df_filtered['Valor'].mean()
count_vendas = df_filtered.shape[0]

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total de Vendas", f"R$ {total_vendas:,.2f}")
kpi2.metric("Ticket Médio", f"R$ {avg_vendas:,.2f}")
kpi3.metric("Qtd Transações", count_vendas)

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Vendas por Categoria")
    fig_bar = px.bar(df_filtered, x='Categoria', y='Valor', title=f"Categorias em {regiao_sel}")
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("Top Estados")
    est_df = df_filtered.groupby('Estado')['Valor'].sum().sort_values(ascending=False).reset_index()
    fig_est = px.pie(est_df, values='Valor', names='Estado', title="Share por Estado")
    st.plotly_chart(fig_est, use_container_width=True)

st.markdown("---")
st.subheader("Tabela de Registros Filtrados")
st.table(df_filtered.head(20))
