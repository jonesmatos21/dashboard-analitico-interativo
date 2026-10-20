# Resultados de Testes Funcionais

| Teste | Descrição | Resultado | Evidência |
| :--- | :--- | :---: | :--- |
| 01 | Inicialização da Aplicação | **APROVADO** | App abre via `streamlit run app.py` sem erros. |
| 02 | Mínimo 3 Visões na Tela | **APROVADO** | Linha, Barras, Heatmap e Tabela visíveis. |
| 03 | Interação de Filtros | **APROVADO** | Mudança na Região altera todos os gráficos. |
| 04 | Sincronização Global | **APROVADO** | Brushing & Linking funcional via filtros laterais. |
| 05 | Consistência de Dados | **APROVADO** | Soma dos KPIs bate com a soma da tabela filtrada. |
| 06 | Acessibilidade de Cores | **APROVADO** | Utilizada paleta specificamente para daltonismo. |
| 07 | Data-Ink Ratio | **APROVADO** | Gráficos limpos, sem bordas ou grades excessivas. |
| 08 | Mensagem de Vazio | **APROVADO** | Alerta `st.warning` exibido ao filtrar sem dados. |
