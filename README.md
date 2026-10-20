# Monitor de Analfabetismo Infantil no Brasil (2025)

Projeto desenvolvido para a disciplina de Visualização de Dados, replicando a estrutura de dashboard analítico interativo e relatório técnico.

## 🚀 Como Executar
1. Clone o repositório.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute a aplicação Streamlit:
   ```bash
   streamlit run app.py --server.headless true --browser.gatherUsageStats false
   ```

## 🛠️ Tecnologias
- **Python 3.x**
- **Streamlit** (Interface e Interatividade)
- **Plotly** (Gráficos Interativos)
- **Pandas** (Manipulação de Dados)
- **ReportLab & Matplotlib** (Geração de Relatórios PDF)

## 📂 Estrutura do Projeto
- `app.py`: Código principal da aplicação do monitor de analfabetismo infantil.
- `data/analfabetismo_infantil_2025.csv`: Dataset com índices por estado, região, localização e faixa etária.
- `docs/`: Documentação de arquitetura, interação e testes.
- `Dashboard_Analitico_Vendas_Relatorio.pdf`: Relatório técnico gerado em PDF com gráficos e métricas.
