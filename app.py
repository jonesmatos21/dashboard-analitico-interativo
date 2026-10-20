import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

ACCESSIBLE_PALETTE = ['#0072B2', '#D55E00', '#009E73', '#F0E442', '#CC79A7', '#56B4E9']

st.set_page_config(
    layout="wide",
    page_title="Dashboard - Analfabetismo Infantil no Brasil (2025)",
    page_icon="📚"
)

st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .stMetric { background-color: #F8F9FA; padding: 10px; border-radius: 10px; border: 1px solid #E9ECEF; }
    div[data-testid="stPlotlyChart"] { border: none !important; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('data/analfabetismo_infantil_2025.csv')
    return df

df = load_data()

st.title("🇧🇷 Monitor de Analfabetismo Infantil no Brasil (2025)")
st.markdown("Painel analítico coordenado para monitoramento das taxas de analfabetismo infantil por Estado, Região, Localização e Faixa Etária.")
st.markdown("---")

# Sidebar - Global Filters
st.sidebar.header("⚙️ Filtros Globais")
st.sidebar.markdown("Selecione os parâmetros para atualizar as visões coordenadas.")

regioes = df['Regiao'].unique().tolist()
regiao_sel = st.sidebar.multiselect("Regiões", options=regioes, default=regioes)

estados = df[df['Regiao'].isin(regiao_sel)]['Estado'].unique().tolist()
estado_sel = st.sidebar.multiselect("Estados (UFs)", options=estados, default=estados)

localizacoes = df['Localizacao'].unique().tolist()
local_sel = st.sidebar.multiselect("Localização", options=localizacoes, default=localizacoes)

faixas = df['Faixa_Etaria'].unique().tolist()
faixa_sel = st.sidebar.multiselect("Faixa Etária", options=faixas, default=faixas)

# Filter mask
mask = (
    (df['Regiao'].isin(regiao_sel)) &
    (df['Estado'].isin(estado_sel)) &
    (df['Localizacao'].isin(local_sel)) &
    (df['Faixa_Etaria'].isin(faixa_sel))
)
df_filtered = df.loc[mask]

# --- KPIs ---
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    taxa_media = df_filtered['Taxa_Analfabetismo'].mean() if not df_filtered.empty else 0
    st.metric("Taxa Média de Analfabetismo", f"{taxa_media:.2f}%")
with kpi2:
    total_criancas = df_filtered['Total_Criancas'].sum() if not df_filtered.empty else 0
    st.metric("Total de Crianças Analisadas", f"{total_criancas:,}")
with kpi3:
    total_nao_alf = df_filtered['Criancas_Nao_Alfabetizadas'].sum() if not df_filtered.empty else 0
    st.metric("Crianças Não Alfabetizadas", f"{total_nao_alf:,}")
with kpi4:
    estados_criticos = df_filtered[df_filtered['Taxa_Analfabetismo'] > 10]['Estado'].nunique()
    st.metric("UFs com Taxa > 10%", f"{estados_criticos}")

st.markdown("<br>", unsafe_allow_html=True)

# --- GRÁFICOS COORDENADOS ---
row1_col1, row1_col2 = st.columns([2, 1])

with row1_col1:
    st.subheader("📊 Taxa Média de Analfabetismo por Estado (%)")
    if not df_filtered.empty:
        df_est = df_filtered.groupby('Estado')['Taxa_Analfabetismo'].mean().sort_values(ascending=True).reset_index()
        fig_est = px.bar(df_est, x='Taxa_Analfabetismo', y='Estado', orientation='h',
                         color='Taxa_Analfabetismo', color_continuous_scale='Reds',
                         title="Taxa de Analfabetismo por UF (%)")
        fig_est.update_layout(plot_bgcolor='white', paper_bgcolor='white', title_x=0.05, xaxis=dict(showgrid=True, gridcolor='#E9ECEF'))
        st.plotly_chart(fig_est, use_container_width=True)
    else:
        st.warning("Nenhum dado para os filtros selecionados.")

with row1_col2:
    st.subheader("📍 Por Localização (Urbana vs Rural)")
    if not df_filtered.empty:
        df_loc = df_filtered.groupby('Localizacao')['Criancas_Nao_Alfabetizadas'].sum().reset_index()
        fig_loc = px.pie(df_loc, names='Localizacao', values='Criancas_Nao_Alfabetizadas',
                         color_discrete_sequence=ACCESSIBLE_PALETTE,
                         hole=0.4, title="Crianças Não Alfabetizadas")
        fig_loc.update_layout(plot_bgcolor='white', paper_bgcolor='white', title_x=0.05)
        st.plotly_chart(fig_loc, use_container_width=True)
    else:
        st.warning("Nenhum dado.")

row2_col1, row2_col2 = st.columns([1, 2])

with row2_col1:
    st.subheader("👶 Por Faixa Etária")
    if not df_filtered.empty:
        df_faixa = df_filtered.groupby('Faixa_Etaria')['Taxa_Analfabetismo'].mean().reset_index()
        fig_faixa = px.bar(df_faixa, x='Faixa_Etaria', y='Taxa_Analfabetismo',
                           color='Faixa_Etaria', color_discrete_sequence=ACCESSIBLE_PALETTE,
                           title="Taxa Média por Idade")
        fig_faixa.update_layout(showlegend=False, plot_bgcolor='white', paper_bgcolor='white', title_x=0.05)
        st.plotly_chart(fig_faixa, use_container_width=True)
    else:
        st.warning("Nenhum dado.")

with row2_col2:
    st.subheader("🌡️ Matriz de Calor: Região x Faixa Etária (Taxa Média %)")
    if not df_filtered.empty:
        pivot_heat = df_filtered.pivot_table(index='Regiao', columns='Faixa_Etaria', values='Taxa_Analfabetismo', aggfunc='mean').fillna(0)
        fig_heat = px.imshow(pivot_heat, text_auto='.1f', color_continuous_scale='OrRd',
                             title="Taxa Média por Região e Faixa Etária")
        fig_heat.update_layout(plot_bgcolor='white', paper_bgcolor='white', title_x=0.05)
        st.plotly_chart(fig_heat, use_container_width=True)
    else:
        st.warning("Nenhum dado.")

st.markdown("---")
st.subheader("📄 Detalhamento dos Dados Estaduais (2025)")
st.dataframe(df_filtered, use_container_width=True)

if df_filtered.empty:
    st.warning("⚠️ Nenhum registro encontrado para a combinação de filtros selecionada.")
