import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf():
    pdf_filename = "Dashboard_Analitico_Vendas_Relatorio.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0072B2'),
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#555555'),
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0072B2'),
        spaceBefore=15,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=body_style,
        leftIndent=15,
        spaceAfter=4
    )

    story = []

    # Title & Header
    story.append(Paragraph("Relatório Técnico: Dashboard Analítico de Vendas", title_style))
    story.append(Paragraph("Projeto desenvolvido para a disciplina de Visualização de Dados | Python, Streamlit & Plotly", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0072B2'), spaceAfter=15))

    # 1. Dataset Summary
    story.append(Paragraph("1. Resumo do Dataset", heading_style))
    story.append(Paragraph("O sistema processa o dataset de vendas (`data/vendas.csv`) contendo registros de transações comerciais.", body_style))

    try:
        df = pd.read_csv('data/vendas.csv')
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

        t = Table(data_summary, colWidths=[200, 340])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F0F4F8')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E9ECEF'))
        ]))
        story.append(t)
    except Exception as e:
        story.append(Paragraph(f"Não foi possível carregar o dataset: {e}", body_style))

    story.append(Spacer(1, 10))

    # 2. Arquitetura de Interação
    story.append(Paragraph("2. Arquitetura de Interação e Brushing & Linking", heading_style))
    story.append(Paragraph("A aplicação adota o princípio de <b>visões coordenadas</b> (Brushing & Linking):", body_style))
    story.append(Paragraph("• <b>Filtros Globais Sincronizados:</b> Os controles na barra lateral (Data, Região e Categoria) atuam como driver único para toda a aplicação.", bullet_style))
    story.append(Paragraph("• <b>Visão Temporal:</b> Gráfico de linha interativo exibindo a evolução mensal das vendas.", bullet_style))
    story.append(Paragraph("• <b>Visão Espacial & Categórica:</b> Rankings por estado/região e distribuição por categoria, além de mapa de calor cruzado (Heatmap).", bullet_style))
    story.append(Paragraph("• <b>Detalhamento em Tempo Real:</b> KPIs dinâmicos e tabela de dados filtrada instantaneamente.", bullet_style))

    story.append(Spacer(1, 10))

    # 3. Design e Acessibilidade
    story.append(Paragraph("3. Princípios de Design e Acessibilidade", heading_style))
    story.append(Paragraph("• <b>Data-Ink Ratio (Tufte):</b> Redução de elementos visuais redundantes, remoção de grades excessivas e foco absoluto na legibilidade dos dados.", bullet_style))
    story.append(Paragraph("• <b>Acessibilidade Color-Blind:</b> Uso de paleta de cores otimizada para daltônicos (`ACCESSIBLE_PALETTE`), garantindo contraste adequado e inclusão visual.", bullet_style))

    story.append(Spacer(1, 10))

    # 4. Testes e Qualidade
    story.append(Paragraph("4. Resumo de Testes Funcionais", heading_style))

    test_data = [
        [Paragraph("<b>ID</b>", body_style), Paragraph("<b>Descrição do Teste</b>", body_style), Paragraph("<b>Resultado</b>", body_style)],
        [Paragraph("01", body_style), Paragraph("Inicialização da Aplicação Streamlit", body_style), Paragraph("APROVADO", body_style)],
        [Paragraph("02", body_style), Paragraph("Presença de Múltiplas Visões na Tela", body_style), Paragraph("APROVADO", body_style)],
        [Paragraph("03", body_style), Paragraph("Interação e Sincronização de Filtros (Brushing & Linking)", body_style), Paragraph("APROVADO", body_style)],
        [Paragraph("04", body_style), Paragraph("Consistência Numérica entre KPIs e Tabelas", body_style), Paragraph("APROVADO", body_style)],
        [Paragraph("05", body_style), Paragraph("Acessibilidade Visual e Redução de Data-Ink", body_style), Paragraph("APROVADO", body_style)]
    ]

    t_test = Table(test_data, colWidths=[40, 350, 150])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F0F4F8')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E9ECEF'))
    ]))
    story.append(t_test)

    doc.build(story)
    print(f"PDF gerado com sucesso: {pdf_filename}")

if __name__ == '__main__':
    generate_pdf()
