import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURAÇÕES DE ACESSIBILIDADE E DESIGN (Tufte & Color-Blind Friendly) ---
# Paleta de cores amigável para daltonismo (Colorblind-safe palette)
ACCESSIBLE_PALETTE = ['#0072B2', '#D55E00', '#009E73', '#F0E442', '#CC79A7', '#56B4E9']

st.set_page_config(
    layout="wide",
    page_title="Dashboard Analítico de Vendas",
    page_icon="📊"
)

# Estilo customizado para reduzir Data-Ink Ratio (remover bordas desnecessárias, etc)
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .stMetric { background-color: #F8F9FA; padding: 10px; border-radius: 10px; border: 1px solid #E9ECEF; }
    div[data-testid="stPlotlyChart"] { border: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CARREGAMENTO E TRATAMENTO DE DADOS ---
@st.cache_data
def load_data():
    df = pd.read_csv('data/vendas.csv')
    df['Data'] = pd.to_datetime(df['Data'])
    return df

df = load_data()

# --- ARQUITETURA DE INTERAÇÃO (Brushing & Linking) ---
st.title("📊 Análise de Performance de Vendas")
st.markdown("Interatividade coordenada: Utilize os filtros laterais para sincronizar todas as visões.")
st.markdown("---")

# Sidebar para Filtros Globais (Sincronização)
st.sidebar.header("⚙️ Painel de Controle")
st.sidebar.markdown("Filtre os dados para atualizar a visão coordenada.")

# Filtro de Período (Visão Temporal)
min_date = df['Data'].min().to_datetime_64() if hasattr(df['Data'], 'min') else df['Data'].min()
max_date = df['Data'].max().to_datetime_64() if hasattr(df['Data'], 'max') else df['Data'].max()
date_range = st.sidebar.date_input("Período de Análise", [min_date, max_date])

# Filtro de Região (Visão Espacial/Regional)
regioes = df['Regiao'].unique().tolist()
regiao_sel = st.sidebar.multiselect("Regiões", options=regioes, default=regioes)

# Filtro de Categoria (Visão Categórica)
categorias = df['Categoria'].unique().tolist()
cat_sel = st.sidebar.multiselect("Categorias", options=categorias, default=categorias)

# Aplicação do Filtro Sincronizado (Brushing & Linking Global)
mask = (
    (df['Data'].dt.date >= pd.to_datetime(date_range[0]).date()) &
    (df['Data'].dt.date <= pd.to_datetime(date_range[1]).date()) &
    (df['Regiao'].isin(regiao_sel)) &
    (df['Categoria'].isin(cat_sel))
)
df_filtered = df.loc[mask]

# --- VISUALIZAÇÕES COORDENADAS ---

# 1. Camada de KPIs (Indicadores Rápidos)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("Vendas Totais", f"R$ {df_filtered['Valor'].sum():,.2f}")
with kpi2:
    st.metric("Ticket Médio", f"R$ {df_filtered['Valor'].mean():,.2f}")
with kpi3:
    st.metric("Volume de Pedidos", f"{len(df_filtered)}")
with kpi4:
    # Comparativo simples com o total geral para contexto
    perc = (df_filtered['Valor'].sum() / df['Valor'].sum()) * 100
    st.metric("Share do Total", f"{perc:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)

# 2. Visão Temporal e Regional (Linha Superior)
row1_col1, row1_col2 = st.columns([2, 1])

with row1_col1:
    st.subheader("📈 Evolução Temporal de Vendas")
    df_time = df_filtered.groupby(df_filtered['Data'].dt.to_period('M')).sum(numeric_only=True).reset_index()
    df_time['Data'] = df_time['Data'].astype(str)
    fig_time = px.line(df_time, x='Data', y='Valor',
                       color_discrete_sequence=[ACCESSIBLE_PALETTE[0]],
                       title="Soma de Vendas por Mês")
    fig_time.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#E9ECEF'),
        title_x=0.05
    )
    st.plotly_chart(fig_time, use_container_width=True)

with row1_col2:
    st.subheader("🗺️ Performance por Estado")
    # Usando gráfico de barras ordenadas como substituto eficiente de mapa coroplético para clareza (Tufte)
    est_df = df_filtered.groupby('Estado')['Valor'].sum().sort_values(ascending=True).reset_index()
    fig_est = px.bar(est_df, x='Valor', y='Estado', orientation='h',
                     color='Valor', color_continuous_scale=[ACCESSIBLE_PALETTE[0], ACCESSIBLE_PALETTE[1]],
                     title="Total por UF")
    fig_est.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=False),
        title_x=0.05
    )
    st.plotly_chart(fig_est, use_container_width=True)

# 3. Visão Categórica e Cruzada (Linha Inferior)
row2_col1, row2_col2 = st.columns([1, 2])

with row2_col1:
    st.subheader("📊 Distribuição por Categoria")
    fig_cat = px.bar(df_filtered, x='Categoria', y='Valor', color='Categoria',
                     color_discrete_sequence=ACCESSIBLE_PALETTE,
                     title="Vendas por Categoria")
    fig_cat.update_layout(
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=False),
        title_x=0.05
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with row2_col2:
    st.subheader("🌡️ Intensidade Região x Categoria")
    pivot_df = df_filtered.pivot_table(index='Regiao', columns='Categoria', values='Valor', aggfunc='sum').fillna(0)
    fig_heat = px.imshow(pivot_df,
                         text_auto='.2s',
                         color_continuous_scale='Viridis', # Paleta percebida uniformemente
                         title="Matriz de Calor de Vendas")
    fig_heat.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_x=0.05
    )
    st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("---")

# 4. Detalhamento sob Demanda
st.subheader("📄 Detalhamento dos Registros")
st.markdown("Tabela filtrada dinamicamente com base nas seleções acima.")
st.dataframe(df_filtered.sort_values(by='Data', ascending=False), use_container_width=True)

# Mensagem de ausência de dados
if df_filtered.empty:
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados. Tente ajustar os parâmetros na barra lateral.")
