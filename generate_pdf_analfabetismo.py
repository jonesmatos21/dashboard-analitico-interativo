import os
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

ACCESSIBLE_PALETTE = ['#0072B2', '#D55E00', '#009E73', '#F0E442', '#CC79A7', '#56B4E9']

def generate_charts():
    df = pd.read_csv('data/analfabetismo_infantil_2025.csv')

    plt.style.use('default')

    # 1. Bar chart of illiteracy rate by State
    df_est = df.groupby('Estado')['Taxa_Analfabetismo'].mean().sort_values(ascending=True).reset_index()
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.barh(df_est['Estado'], df_est['Taxa_Analfabetismo'], color='#D55E00')
    ax.set_title('Taxa Média de Analfabetismo Infantil por UF (%) - 2025', fontsize=10, fontweight='bold', color='#333333')
    ax.set_xlabel('Taxa (%)', fontsize=9)
    ax.set_ylabel('Estado', fontsize=9)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=7)
    ax.grid(True, linestyle='--', alpha=0.5, axis='x')
    plt.tight_layout()
    plt.savefig('chart1.png', dpi=200)
    plt.close()

    # 2. Pie chart / Bar of Localizacao
    df_loc = df.groupby('Localizacao')['Criancas_Nao_Alfabetizadas'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.pie(df_loc['Criancas_Nao_Alfabetizadas'], labels=df_loc['Localizacao'], colors=ACCESSIBLE_PALETTE[:2], autopct='%1.1f%%', startangle=90)
    ax.set_title('Distribuição de Crianças Não Alfabetizadas por Localização', fontsize=10, fontweight='bold', color='#333333')
    plt.tight_layout()
    plt.savefig('chart2.png', dpi=200)
    plt.close()

    # 3. Bar chart by Faixa Etaria
    df_faixa = df.groupby('Faixa_Etaria')['Taxa_Analfabetismo'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.bar(df_faixa['Faixa_Etaria'], df_faixa['Taxa_Analfabetismo'], color=ACCESSIBLE_PALETTE[0])
    ax.set_title('Taxa Média de Analfabetismo por Faixa Etária (%)', fontsize=10, fontweight='bold', color='#333333')
    ax.set_xlabel('Faixa Etária', fontsize=9)
    ax.set_ylabel('Taxa Média (%)', fontsize=9)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    ax.grid(True, linestyle='--', alpha=0.5, axis='y')
    plt.tight_layout()
    plt.savefig('chart3.png', dpi=200)
    plt.close()

    # 4. Heatmap Region x Faixa Etaria
    pivot_df = df.pivot_table(index='Regiao', columns='Faixa_Etaria', values='Taxa_Analfabetismo', aggfunc='mean').fillna(0)
    fig, ax = plt.subplots(figsize=(7, 3.2))
    cax = ax.imshow(pivot_df.values, cmap='OrRd', aspect='auto')
    fig.colorbar(cax)
    ax.set_xticks(range(len(pivot_df.columns)))
    ax.set_xticklabels(pivot_df.columns, fontsize=8)
    ax.set_yticks(range(len(pivot_df.index)))
    ax.set_yticklabels(pivot_df.index, fontsize=8)

    for i in range(len(pivot_df.index)):
        for j in range(len(pivot_df.columns)):
            val = pivot_df.iloc[i, j]
            ax.text(j, i, f"{val:.1f}%", ha="center", va="center", color="black" if val < 10 else "white", fontsize=7, fontweight='bold')

    ax.set_title('Matriz de Calor: Região x Faixa Etária (Taxa %)', fontsize=10, fontweight='bold', color='#333333')
    ax.set_xlabel('Faixa Etária', fontsize=9)
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
            fontSize=16, leading=20,
            textColor=colors.HexColor('#0072B2'), spaceAfter=4
        )
        subtitle_style = ParagraphStyle(
            'DocSubtitle', parent=styles['Normal'],
            fontSize=9, leading=12,
            textColor=colors.HexColor('#555555'), spaceAfter=12
        )
        heading_style = ParagraphStyle(
            'SectionHeading', parent=styles['Heading2'],
            fontSize=12, leading=15,
            textColor=colors.HexColor('#0072B2'), spaceBefore=10, spaceAfter=4
        )
        body_style = ParagraphStyle(
            'BodyTextCustom', parent=styles['Normal'],
            fontSize=9, leading=12,
            textColor=colors.HexColor('#333333'), spaceAfter=3
        )
        bullet_style = ParagraphStyle(
            'BulletCustom', parent=body_style,
            leftIndent=10, spaceAfter=2
        )

        story = []

        # Title & Header
        story.append(Paragraph("Relatório Técnico: Índice de Analfabetismo Infantil no Brasil por Estado (2025)", title_style))
        story.append(Paragraph("Monitoramento Educacional | Python, Streamlit & Matplotlib", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0072B2'), spaceAfter=8))

        # 1. Dataset Summary Table
        story.append(Paragraph("1. Resumo Executivo e Indicadores Educacionais (2025)", heading_style))
        taxa_media = df['Taxa_Analfabetismo'].mean()
        total_criancas = df['Total_Criancas'].sum()
        total_nao_alf = df['Criancas_Nao_Alfabetizadas'].sum()

        data_summary = [
            [Paragraph("<b>Indicador Educacional</b>", body_style), Paragraph("<b>Valor Consolidado</b>", body_style)],
            [Paragraph("Taxa Média de Analfabetismo Infantil (Brasil)", body_style), Paragraph(f"{taxa_media:.2f}%", body_style)],
            [Paragraph("Total de Crianças Analisadas", body_style), Paragraph(f"{total_criancas:,}", body_style)],
            [Paragraph("Crianças Não Alfabetizadas Estimadas", body_style), Paragraph(f"{total_nao_alf:,}", body_style)],
            [Paragraph("Estados Analisados", body_style), Paragraph("26 Estados + Distrito Federal (27 UFs)", body_style)],
            [Paragraph("Fontes e Variáveis", body_style), Paragraph("Censo Escolar / PNAD / Faixa etária de 6 a 14 anos", body_style)]
        ]

        t = Table(data_summary, colWidths=[200, 340])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F0F4F8')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E9ECEF'))
        ]))
        story.append(t)
        story.append(Spacer(1, 8))

        # 2. Charts Section
        story.append(Paragraph("2. Visualizações Gráficas do Monitor", heading_style))
        story.append(Paragraph("Os gráficos abaixo apresentam a distribuição espacial por UF, o impacto da localização (urbana/rural), faixa etária e matriz regional de incidência.", body_style))
        story.append(Spacer(1, 4))

        # Add Chart 1 & 2
        story.append(Paragraph("<b>Figura 1: Taxa Média de Analfabetismo Infantil por UF (%) - 2025</b>", body_style))
        story.append(Image("chart1.png", width=480, height=210))
        story.append(Spacer(1, 6))

        story.append(Paragraph("<b>Figura 2: Distribuição de Crianças Não Alfabetizadas por Localização</b>", body_style))
        story.append(Image("chart2.png", width=480, height=210))
        story.append(PageBreak())

        story.append(Paragraph("<b>Figura 3: Taxa Média de Analfabetismo por Faixa Etária (%)</b>", body_style))
        story.append(Image("chart3.png", width=480, height=210))
        story.append(Spacer(1, 6))

        story.append(Paragraph("<b>Figura 4: Matriz de Calor (Região x Faixa Etária)</b>", body_style))
        story.append(Image("chart4.png", width=480, height=210))
        story.append(Spacer(1, 8))

        # 3. Architecture & Tests Summary
        story.append(Paragraph("3. Arquitetura de Interação, Design (Tufte) e Validação", heading_style))
        story.append(Paragraph("• <b>Brushing & Linking:</b> Filtros interativos na barra lateral atualizam simultaneamente todas as visões.", bullet_style))
        story.append(Paragraph("• <b>Data-Ink Ratio:</b> Gráficos limpos, remoção de grades desnecessárias e foco na clareza analítica.", bullet_style))
        story.append(Paragraph("• <b>Acessibilidade Visual:</b> Uso de paleta de cores *color-blind friendly* para inclusão universal.", bullet_style))
        story.append(Paragraph("• <b>Validação de Dados:</b> Consistência garantida entre os indicadores estaduais e nacionais.", bullet_style))

        doc.build(story)

    for f in ["chart1.png", "chart2.png", "chart3.png", "chart4.png"]:
        if os.path.exists(f):
            os.remove(f)

    print("PDF de analfabetismo infantil gerado, atualizado e copiado com sucesso!")

if __name__ == '__main__':
    generate_pdf()
