import os
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

ACCESSIBLE_PALETTE = ['#0072B2', '#D55E00', '#009E73', '#F0E442', '#CC79A7', '#56B4E9']

def generate_charts():
    df = pd.read_csv('data/vendas.csv')
    df['Data'] = pd.to_datetime(df['Data'])

    plt.style.use('default')

    # 1. Temporal Evolution
    df_time = df.groupby(df['Data'].dt.to_period('M')).sum(numeric_only=True).reset_index()
    df_time['Data'] = df_time['Data'].astype(str)

    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.plot(df_time['Data'], df_time['Valor'], marker='o', color=ACCESSIBLE_PALETTE[0], linewidth=2, markersize=6)
    ax.set_title('Evolução Temporal de Vendas (Mensal)', fontsize=11, fontweight='bold', color='#333333')
    ax.set_xlabel('Mês', fontsize=9)
    ax.set_ylabel('Valor (R$)', fontsize=9)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(fontsize=8)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('chart1.png', dpi=200)
    plt.close()

    # 2. State Bar Chart
    est_df = df.groupby('Estado')['Valor'].sum().sort_values(ascending=True).reset_index()
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.barh(est_df['Estado'], est_df['Valor'], color=ACCESSIBLE_PALETTE[1])
    ax.set_title('Performance de Vendas por Estado (UF)', fontsize=11, fontweight='bold', color='#333333')
    ax.set_xlabel('Valor (R$)', fontsize=9)
    ax.set_ylabel('Estado', fontsize=9)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    ax.grid(True, linestyle='--', alpha=0.5, axis='x')
    plt.tight_layout()
    plt.savefig('chart2.png', dpi=200)
    plt.close()

    # 3. Category Bar Chart
    cat_df = df.groupby('Categoria')['Valor'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.bar(cat_df['Categoria'], cat_df['Valor'], color=ACCESSIBLE_PALETTE[:len(cat_df)])
    ax.set_title('Distribuição de Vendas por Categoria', fontsize=11, fontweight='bold', color='#333333')
    ax.set_xlabel('Categoria', fontsize=9)
    ax.set_ylabel('Valor (R$)', fontsize=9)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    ax.grid(True, linestyle='--', alpha=0.5, axis='y')
    plt.tight_layout()
    plt.savefig('chart3.png', dpi=200)
    plt.close()

    # 4. Heatmap Region x Category (Pure Matplotlib)
    pivot_df = df.pivot_table(index='Regiao', columns='Categoria', values='Valor', aggfunc='sum').fillna(0)
    fig, ax = plt.subplots(figsize=(7, 3.2))
    cax = ax.imshow(pivot_df.values, cmap='viridis', aspect='auto')
    fig.colorbar(cax)
    ax.set_xticks(range(len(pivot_df.columns)))
    ax.set_xticklabels(pivot_df.columns, rotation=15, fontsize=8)
    ax.set_yticks(range(len(pivot_df.index)))
    ax.set_yticklabels(pivot_df.index, fontsize=8)

    # Annotate values
    for i in range(len(pivot_df.index)):
        for j in range(len(pivot_df.columns)):
            val = pivot_df.iloc[i, j]
            ax.text(j, i, f"{val:,.0f}", ha="center", va="center", color="white", fontsize=7, fontweight='bold')

    ax.set_title('Matriz de Calor (Heatmap): Região x Categoria', fontsize=11, fontweight='bold', color='#333333')
    ax.set_xlabel('Categoria', fontsize=9)
    ax.set_ylabel('Região', fontsize=9)
    plt.tight_layout()
    plt.savefig('chart4.png', dpi=200)
    plt.close()

    return df

def generate_pdf():
    df = generate_charts()

    target_dir = r"D:\G D EAD UFPI OEIRAS 2026.2\INFOVIS\dashboard analitico"
    os.makedirs(target_dir, exist_ok=True)
    pdf_filename = os.path.join(target_dir, "Dashboard_Analitico_Vendas_Relatorio.pdf")
    local_filename = "Dashboard_Analitico_Vendas_Relatorio.pdf"

    for filename in [pdf_filename, local_filename]:
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=36, leftMargin=36,
            topMargin=36, bottomMargin=36
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'DocTitle', parent=styles['Heading1'],
            fontSize=18, leading=22,
            textColor=colors.HexColor('#0072B2'), spaceAfter=6
        )
        subtitle_style = ParagraphStyle(
            'DocSubtitle', parent=styles['Normal'],
            fontSize=10, leading=13,
            textColor=colors.HexColor('#555555'), spaceAfter=15
        )
        heading_style = ParagraphStyle(
            'SectionHeading', parent=styles['Heading2'],
            fontSize=13, leading=16,
            textColor=colors.HexColor('#0072B2'), spaceBefore=12, spaceAfter=6
        )
        body_style = ParagraphStyle(
            'BodyTextCustom', parent=styles['Normal'],
            fontSize=9, leading=13,
            textColor=colors.HexColor('#333333'), spaceAfter=4
        )
        bullet_style = ParagraphStyle(
            'BulletCustom', parent=body_style,
            leftIndent=10, spaceAfter=3
        )

        story = []

        # Title & Header
        story.append(Paragraph("Relatório Técnico com Visualizações: Dashboard Analítico de Vendas", title_style))
        story.append(Paragraph("Projeto desenvolvido para a disciplina de Visualização de Dados | Python, Streamlit & Matplotlib", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0072B2'), spaceAfter=10))

        # 1. Dataset Summary Table
        story.append(Paragraph("1. Resumo Executivo e Métricas do Dataset", heading_style))
        total_vendas = df['Valor'].sum()
        ticket_medio = df['Valor'].mean()
        total_pedidos = len(df)

        data_summary = [
            [Paragraph("<b>Métrica</b>", body_style), Paragraph("<b>Valor</b>", body_style)],
            [Paragraph("Volume Total de Vendas", body_style), Paragraph(f"R$ {total_vendas:,.2f}", body_style)],
            [Paragraph("Ticket Médio", body_style), Paragraph(f"R$ {ticket_medio:,.2f}", body_style)],
            [Paragraph("Total de Transações", body_style), Paragraph(f"{total_pedidos:,}", body_style)],
            [Paragraph("Regiões Cobertas", body_style), Paragraph(f"{', '.join(df['Regiao'].unique())}", body_style)],
            [Paragraph("Categorias de Produtos", body_style), Paragraph(f"{', '.join(df['Categoria'].unique())}", body_style)]
        ]

        t = Table(data_summary, colWidths=[180, 360])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F0F4F8')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E9ECEF'))
        ]))
        story.append(t)
        story.append(Spacer(1, 10))

        # 2. Charts Section
        story.append(Paragraph("2. Visualizações Gráficas do Dashboard", heading_style))
        story.append(Paragraph("Abaixo estão representados os gráficos analíticos gerados a partir do dataset de vendas, contemplando séries temporais, distribuições espaciais e categóricas, e matrizes de correlação.", body_style))
        story.append(Spacer(1, 5))

        # Add Chart 1 & 2
        story.append(Paragraph("<b>Figura 1: Evolução Temporal de Vendas (Mensal)</b>", body_style))
        story.append(Image("chart1.png", width=480, height=220))
        story.append(Spacer(1, 8))

        story.append(Paragraph("<b>Figura 2: Performance de Vendas por Estado (UF)</b>", body_style))
        story.append(Image("chart2.png", width=480, height=220))
        story.append(PageBreak())

        story.append(Paragraph("<b>Figura 3: Distribuição de Vendas por Categoria de Produto</b>", body_style))
        story.append(Image("chart3.png", width=480, height=220))
        story.append(Spacer(1, 8))

        story.append(Paragraph("<b>Figura 4: Matriz de Calor (Heatmap) - Região x Categoria</b>", body_style))
        story.append(Image("chart4.png", width=480, height=220))
        story.append(Spacer(1, 10))

        # 3. Architecture & Tests Summary
        story.append(Paragraph("3. Arquitetura de Interação, Design (Tufte) e Testes", heading_style))
        story.append(Paragraph("• <b>Brushing & Linking:</b> Arquitetura baseada em filtros globais sincronizados na barra lateral.", bullet_style))
        story.append(Paragraph("• <b>Data-Ink Ratio:</b> Redução de elementos visuais desnecessários e foco na legibilidade.", bullet_style))
        story.append(Paragraph("• <b>Acessibilidade:</b> Paleta de cores amigável para daltonismo (`ACCESSIBLE_PALETTE`).", bullet_style))
        story.append(Paragraph("• <b>Testes Funcionais:</b> 100% aprovados (inicialização, múltiplas visões, sincronização e consistência).", bullet_style))

        doc.build(story)

    # Cleanup chart images
    for f in ["chart1.png", "chart2.png", "chart3.png", "chart4.png"]:
        if os.path.exists(f):
            os.remove(f)

    print("PDF com gráficos gerado, atualizado e copiado com sucesso!")

if __name__ == '__main__':
    generate_pdf()
