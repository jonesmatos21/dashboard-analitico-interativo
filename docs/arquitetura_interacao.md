# Arquitetura de Interação - Dashboard Analítico de Vendas

## 1. Visão Geral
O dashboard foi desenvolvido utilizando **Python** com as bibliotecas **Streamlit** para a interface e **Plotly** para as visualizações. O objetivo é fornecer uma análise coordenada de vendas, permitindo que o usuário explore os dados através de múltiplas dimensões simultaneamente.

## 2. Componentes de Visualização
O sistema implementa três categorias obrigatórias de visões:
1. **Visão Temporal/Espacial:** 
   - Série temporal de vendas mensais (linha).
   - Ranking de vendas por estado (barras horizontais), servindo como alternativa clara ao mapa coroplético para evitar ruído visual.
2. **Distribuição Categórica:**
   - Gráfico de barras por categoria de produto.
   - Mapa de calor (Heatmap) cruzando Região vs. Categoria.
3. **Detalhamento:**
   - Tabela de dados filtrada em tempo real e KPIs de resumo (Total, Ticket Médio, Volume e Share).

## 3. Mecanismo de Interação (Brushing & Linking)
A arquitetura de interação baseia-se em **filtros globais sincronizados**:
- **Fluxo de Dados:** Os filtros na barra lateral (Data, Região, Categoria) atuam como o "Driver" da aplicação.
- **Sincronização:** Qualquer alteração nos filtros dispara a re-execução do script Streamlit, que aplica uma máscara booleana ao DataFrame original.
- **Linking:** Todos os componentes (KPIs, Gráficos e Tabela) consomem o mesmo DataFrame filtrado (`df_filtered`), garantindo que a seleção em uma dimensão reflita instantaneamente em todas as outras visões na tela.

## 4. Decisões de Design e Acessibilidade
- **Data-Ink Ratio (Tufte):** 
  - Remoção de grades desnecessárias (*gridlines*) e bordas de gráficos.
  - Uso de fundos brancos e cores neutras para destacar apenas a informação relevante.
  - Substituição de elementos redundantes por KPIs claros.
- **Acessibilidade Visual:**
  - Implementação de uma paleta de cores baseada em padrões *color-blind friendly* (`ACCESSIBLE_PALETTE`).
  - Uso de textos automáticos no Heatmap para garantir que a informação seja legível mesmo sem a percepção exata da cor.

## 5. Como Executar
1. Instalar dependências: `pip install streamlit pandas plotly`
2. Executar app: `streamlit run app.py`
