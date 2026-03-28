import pandas as pd
from fpdf import FPDF

# ============================================================
# PASSO 1 — Cria uma planilha de vendas de exemplo
# ============================================================

dados = {
    "Vendedor": ["Ana", "Carlos", "Maria", "João", "Ana", "Carlos", "Maria", "João"],
    "Produto":  ["Notebook", "Mouse", "Teclado", "Monitor", "Mouse", "Notebook", "Monitor", "Teclado"],
    "Quantidade": [2, 5, 3, 1, 4, 1, 2, 6],
    "Preco_Unitario": [3500, 80, 150, 1200, 80, 3500, 1200, 150],
    "Mes": ["Janeiro", "Janeiro", "Janeiro", "Janeiro", "Fevereiro", "Fevereiro", "Fevereiro", "Fevereiro"]
}

df = pd.DataFrame(dados)
df["Total"] = df["Quantidade"] * df["Preco_Unitario"]
df.to_csv("vendas.csv", index=False)
print("[OK] Planilha vendas.csv criada!")


# ============================================================
# PASSO 2 — Le a planilha e calcula o relatorio
# ============================================================

df = pd.read_csv("vendas.csv")

total_geral = df["Total"].sum()
melhor_vendedor = df.groupby("Vendedor")["Total"].sum().idxmax()
produto_mais_vendido = df.groupby("Produto")["Quantidade"].sum().idxmax()
vendas_por_vendedor = df.groupby("Vendedor")["Total"].sum()


# ============================================================
# PASSO 3 — Gera o relatorio em PDF
# ============================================================

pdf = FPDF()
pdf.add_page()

pdf.set_font("Helvetica", "B", 16)
pdf.cell(0, 10, "Relatorio de Vendas", ln=True, align="C")
pdf.ln(5)

pdf.set_font("Helvetica", "", 12)
pdf.cell(0, 10, f"Total geral de vendas: R$ {total_geral:,.2f}", ln=True)
pdf.cell(0, 10, f"Melhor vendedor: {melhor_vendedor}", ln=True)
pdf.cell(0, 10, f"Produto mais vendido: {produto_mais_vendido}", ln=True)
pdf.ln(5)

pdf.set_font("Helvetica", "B", 12)
pdf.cell(0, 10, "Vendas por vendedor:", ln=True)
pdf.set_font("Helvetica", "", 12)
for vendedor, total in vendas_por_vendedor.items():
    pdf.cell(0, 10, f"  {vendedor}: R$ {total:,.2f}", ln=True)

pdf.ln(5)
pdf.set_font("Helvetica", "B", 12)
pdf.cell(0, 10, "Detalhamento de vendas:", ln=True)

pdf.set_font("Helvetica", "B", 10)
pdf.cell(40, 8, "Vendedor", border=1)
pdf.cell(40, 8, "Produto", border=1)
pdf.cell(30, 8, "Qtd", border=1)
pdf.cell(40, 8, "Preco Unit.", border=1)
pdf.cell(40, 8, "Total", border=1)
pdf.ln()

pdf.set_font("Helvetica", "", 10)
for _, row in df.iterrows():
    pdf.cell(40, 8, str(row["Vendedor"]), border=1)
    pdf.cell(40, 8, str(row["Produto"]), border=1)
    pdf.cell(30, 8, str(row["Quantidade"]), border=1)
    pdf.cell(40, 8, f"R$ {row['Preco_Unitario']:,.2f}", border=1)
    pdf.cell(40, 8, f"R$ {row['Total']:,.2f}", border=1)
    pdf.ln()

pdf.output("relatorio.pdf")
print("[OK] Relatorio relatorio.pdf gerado!")
print(f"\n--- RESUMO ---")
print(f"Total de vendas: R$ {total_geral:,.2f}")
print(f"Melhor vendedor: {melhor_vendedor}")
print(f"Produto mais vendido: {produto_mais_vendido}")