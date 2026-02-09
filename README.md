# Engetrol Engenharia — Sistema de Orçamentação de Obras v3.0

Sistema web interativo para orçamentação de obras industriais, desenvolvido em **Streamlit** com foco no regime tributário do **Lucro Real**.

## Funcionalidades

- **Configuração Inicial**: Impostos individuais (PIS, COFINS, ISS), encargos sociais detalhados (CLT/Lei 8.212), IRPJ progressivo (15% + 10% adicional), CSLL 9%
- **Banco de Recursos**: 11 funções pré-cadastradas com periculosidade NR-10 (30%)
- **Materiais e Insumos (BOM)**: Cadastro com margem de perda técnica e créditos PIS/COFINS 9,25%
- **Cronograma e Alocação**: Etapas com datas, produtividade HH, histograma de efetivo (Plotly)
- **Custos Indiretos**: Refeição, hospedagem, combustível, pedágio, veículos, mobilização
- **Fechamento**: DRE Gerencial, BDI reverso, Simulador de Negociação, Lucro Líquido Alvo (Gross-up)
- **Persistência**: SQLite com versionamento de orçamentos
- **Exportação**: PDF com logo, Excel (.xlsx) com abas, Markdown para IA

## Como Rodar Localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Tecnologias

- Python 3.11+
- Streamlit
- Pandas, Plotly, OpenPyXL
- WeasyPrint (PDF)
- SQLite

## Licença

Uso exclusivo Engetrol Engenharia.
