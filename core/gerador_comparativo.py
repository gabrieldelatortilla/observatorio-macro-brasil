import os
import sys
import json
from datetime import datetime

# Garante UTF-8 no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_DIR = os.path.join(BASE_DIR, "dados")
DOSSIE_DIR = os.path.join(BASE_DIR, "dossie_historico")
os.makedirs(DOSSIE_DIR, exist_ok=True)

def gerar_quadro_comparativo():
    caminho_matriz = os.path.join(DADOS_DIR, "matriz_comparativa.json")
    if not os.path.exists(caminho_matriz):
        print("❌ Matriz comparativa não encontrada. Execute coletor_bcb.py primeiro.")
        return
        
    with open(caminho_matriz, "r", encoding="utf-8") as f:
        matriz = json.load(f)
        
    md = []
    md.append("# 🏛️ Observatório Macro Brasil: Quadro Comparativo de Governos (2003 - 2026)")
    md.append(f"\n> **Data de Geração:** {datetime.now().strftime('%d/%m/%Y %H:%M')} | **Fonte Primária:** Banco Central do Brasil (SGS) e IBGE\n")
    md.append("Este documento apresenta uma consolidação puramente estatística e factual comparando os mandatos de **Lula (1 e 2)**, **Dilma Rousseff**, **Michel Temer**, **Jair Bolsonaro** e **Lula (3)** sob a ótica das principais variáveis macroeconômicas.\n")
    
    md.append("## 📊 1. Tabela Comparativa Consolidada\n")
    md.append("| Indicador Econômico | Lula 1 e 2 (2003-10) | Dilma 1 e 2 (2011-16) | Temer (2016-18) | Bolsonaro (2019-22) | Lula 3 (2023-Presente) |")
    md.append("| :--- | :---: | :---: | :---: | :---: | :---: |")
    
    # Linha: Duração
    md.append("| **Duração do Mandato** | 8 anos (96 meses) | 5,6 anos (68 meses) | 2,3 anos (28 meses) | 4 anos (48 meses) | ~4 anos (45 meses) |")
    
    # Linha: IPCA Acumulado
    ipca_l1 = matriz["lula_1_e_2"]["metricas"]["ipca_mensal"]["acumulado_periodo_pct"]
    ipca_d = matriz["dilma_1_e_2"]["metricas"]["ipca_mensal"]["acumulado_periodo_pct"]
    ipca_t = matriz["temer"]["metricas"]["ipca_mensal"]["acumulado_periodo_pct"]
    ipca_b = matriz["bolsonaro"]["metricas"]["ipca_mensal"]["acumulado_periodo_pct"]
    ipca_l3 = matriz["lula_3"]["metricas"]["ipca_mensal"]["acumulado_periodo_pct"]
    md.append(f"| **Inflação Acumulada (IPCA)** | **+{ipca_l1}%** | **+{ipca_d}%** | **+{ipca_t}%** | **+{ipca_b}%** | **+{ipca_l3}%** |")
    
    # Linha: Média Mensal IPCA
    md.append(f"| **Média Mensal IPCA** | {matriz['lula_1_e_2']['metricas']['ipca_mensal']['media_mensal_pct']}% | {matriz['dilma_1_e_2']['metricas']['ipca_mensal']['media_mensal_pct']}% | {matriz['temer']['metricas']['ipca_mensal']['media_mensal_pct']}% | {matriz['bolsonaro']['metricas']['ipca_mensal']['media_mensal_pct']}% | {matriz['lula_3']['metricas']['ipca_mensal']['media_mensal_pct']}% |")
    
    # Linha: Salário Mínimo (Início -> Fim)
    sm_l1 = f"R$ {matriz['lula_1_e_2']['metricas']['salario_minimo']['inicio']:.0f} → R$ {matriz['lula_1_e_2']['metricas']['salario_minimo']['fim']:.0f}"
    sm_d = f"R$ {matriz['dilma_1_e_2']['metricas']['salario_minimo']['inicio']:.0f} → R$ {matriz['dilma_1_e_2']['metricas']['salario_minimo']['fim']:.0f}"
    sm_t = f"R$ {matriz['temer']['metricas']['salario_minimo']['inicio']:.0f} → R$ {matriz['temer']['metricas']['salario_minimo']['fim']:.0f}"
    sm_b = f"R$ {matriz['bolsonaro']['metricas']['salario_minimo']['inicio']:.0f} → R$ {matriz['bolsonaro']['metricas']['salario_minimo']['fim']:.0f}"
    sm_l3 = f"R$ {matriz['lula_3']['metricas']['salario_minimo']['inicio']:.0f} → R$ {matriz['lula_3']['metricas']['salario_minimo']['fim']:.0f}"
    md.append(f"| **Salário Mínimo (Nominal)** | {sm_l1} | {sm_d} | {sm_t} | {sm_b} | {sm_l3} |")
    
    # Linha: Ganho Real do Salário Mínimo
    gr_l1 = matriz["lula_1_e_2"]["metricas"]["ganho_real_salario_minimo"]["ganho_real_pct"]
    gr_d = matriz["dilma_1_e_2"]["metricas"]["ganho_real_salario_minimo"]["ganho_real_pct"]
    gr_t = matriz["temer"]["metricas"]["ganho_real_salario_minimo"]["ganho_real_pct"]
    gr_b = matriz["bolsonaro"]["metricas"]["ganho_real_salario_minimo"]["ganho_real_pct"]
    gr_l3 = matriz["lula_3"]["metricas"]["ganho_real_salario_minimo"]["ganho_real_pct"]
    md.append(f"| **Ganho Real do Salário Mínimo** | **+{gr_l1}%** | **+{gr_d}%** | **+{gr_t}%** | **{gr_b}%** | **+{gr_l3}%** |")
    
    # Linha: Dólar (Início -> Fim)
    us_l1 = f"R$ {matriz['lula_1_e_2']['metricas']['dolar_comercial']['inicio']:.2f} → R$ {matriz['lula_1_e_2']['metricas']['dolar_comercial']['fim']:.2f}"
    us_d = f"R$ {matriz['dilma_1_e_2']['metricas']['dolar_comercial']['inicio']:.2f} → R$ {matriz['dilma_1_e_2']['metricas']['dolar_comercial']['fim']:.2f}"
    us_t = f"R$ {matriz['temer']['metricas']['dolar_comercial']['inicio']:.2f} → R$ {matriz['temer']['metricas']['dolar_comercial']['fim']:.2f}"
    us_b = f"R$ {matriz['bolsonaro']['metricas']['dolar_comercial']['inicio']:.2f} → R$ {matriz['bolsonaro']['metricas']['dolar_comercial']['fim']:.2f}"
    us_l3 = f"R$ {matriz['lula_3']['metricas']['dolar_comercial']['inicio']:.2f} → R$ {matriz['lula_3']['metricas']['dolar_comercial']['fim']:.2f}"
    md.append(f"| **Dólar Comercial (Início → Fim)** | {us_l1} (-50,7%) | {us_d} (+91,6%) | {us_t} (+19,3%) | {us_b} (+40,1%) | {us_l3} (-1,1%) |")
    
    # Linha: Selic Média Anualizada
    s_l1 = matriz["lula_1_e_2"]["metricas"]["selic_anualizada"]["media_periodo"]
    s_d = matriz["dilma_1_e_2"]["metricas"]["selic_anualizada"]["media_periodo"]
    s_t = matriz["temer"]["metricas"]["selic_anualizada"]["media_periodo"]
    s_b = matriz["bolsonaro"]["metricas"]["selic_anualizada"]["media_periodo"]
    s_l3 = matriz["lula_3"]["metricas"]["selic_anualizada"]["media_periodo"]
    md.append(f"| **Taxa Selic Média (% a.a.)** | {s_l1}% | {s_d}% | {s_t}% | {s_b}% | {s_l3}% |")
    
    # Linha: Dívida Bruta (% PIB)
    db_l1 = f"{matriz['lula_1_e_2']['metricas']['divida_bruta_pib']['inicio']}% → {matriz['lula_1_e_2']['metricas']['divida_bruta_pib']['fim']}%"
    db_d = f"{matriz['dilma_1_e_2']['metricas']['divida_bruta_pib']['inicio']}% → {matriz['dilma_1_e_2']['metricas']['divida_bruta_pib']['fim']}%"
    db_t = f"{matriz['temer']['metricas']['divida_bruta_pib']['inicio']}% → {matriz['temer']['metricas']['divida_bruta_pib']['fim']}%"
    db_b = f"{matriz['bolsonaro']['metricas']['divida_bruta_pib']['inicio']}% → {matriz['bolsonaro']['metricas']['divida_bruta_pib']['fim']}%"
    db_l3 = f"{matriz['lula_3']['metricas']['divida_bruta_pib']['inicio']}% → {matriz['lula_3']['metricas']['divida_bruta_pib']['fim']}%"
    md.append(f"| **Dívida Bruta (% PIB)** | {db_l1} | {db_d} | {db_t} | {db_b} | {db_l3} |")
    
    md.append("\n---\n")
    md.append("## 🔍 2. Raio-X Crítico de Cada Mandato\n")
    
    md.append("### A. Governos Lula 1 e 2 (2003 - 2010): O Superciclo das Commodities e Expansão")
    md.append("- **Pontos Fortes:** Maior ganho real do salário mínimo da história moderna (+62,75%); forte apreciação cambial (dólar caiu pela metade); acúmulo histórico de reservas internacionais (que blindaram o país contra choques cambiais externos); quitação da dívida com o FMI; forte redução da pobreza extrema com expansão do Bolsa Família.")
    md.append("- **Gargalos Estruturais:** Manutenção de juros reais elevadíssimos (Selic média de 14,78%); baixa taxa de investimento público em infraestrutura logística; expansão acelerada dos gastos correntes que plantou sementes da rigidez orçamentária futura.")
    md.append("- **Contexto Externo:** O maior 'vento a favor' da história econômica recente, impulsionado pela entrada da China na OMC e demanda voraz por minério de ferro e soja.")
    
    md.append("\n### B. Governos Dilma Rousseff (2011 - 2016): A Nova Matriz Econômica e a Crise Fiscal")
    md.append("- **Pontos Fortes:** Manutenção do desemprego baixo nos primeiros anos; expansão do Pronatec e FIES; início de programas de concessão de infraestrutura.")
    md.append("- **Gargalos e Colapso:** Adoção da 'Nova Matriz Econômica' (desonerações setoriais sem contrapartida, controle artificial de tarifas de energia e combustíveis); explosão da dívida bruta (+32,3% em relação ao PIB); queda na arrecadação federal gerando déficits primários consecutivos; perda do grau de investimento em 2015; recessão profunda de 2015-2016 (queda acumulada de ~7% do PIB) culminando no processo de impeachment.")
    
    md.append("\n### C. Governo Michel Temer (2016 - 2018): As Reformas Estruturantes de Transição")
    md.append("- **Pontos Fortes:** Queda abrupta da inflação (IPCA acumulado de apenas 7,68% em mais de 2 anos); aprovação da PEC do Teto de Gastos (EC 95); aprovação da Reforma Trabalhista (modernização das relações de trabalho e fim do imposto sindical obrigatório); redução agressiva da taxa Selic de 14,25% para 6,5%.")
    md.append("- **Gargalos:** Baixa legitimidade popular e crises políticas agudas (gravações de Joesley Batista); greve dos caminhoneiros em 2018 expondo a vulnerabilidade logística nacional; desemprego ainda em níveis de dois dígitos herdado da recessão.")
    
    md.append("\n### D. Governo Jair Bolsonaro (2019 - 2022): Choque Pandêmico, Reformas e Pressão Inflacionária")
    md.append("- **Pontos Fortes:** Aprovação da Nova Previdência (EC 103); Marco Legal do Saneamento Básico; Lei de Liberdade Econômica; autonomia formal do Banco Central; criação do PIX; privatização da Eletrobras; recuperação rápida do emprego em 2022; término do mandato com superávit primário e redução da dívida bruta para 71,68% do PIB.")
    md.append("- **Gargalos e Crises:** Impacto severo da pandemia da COVID-19 (queda do PIB em 2020 e gastos emergenciais massivos que levaram a dívida a 87% do PIB); surto inflacionário pós-pandemia (IPCA de +26,93%), resultando em perda real do poder de compra do salário mínimo (-4,33%); forte desvalorização cambial (dólar saindo de R$ 3,74 para R$ 5,24); PEC dos Precatórios e flexibilizações do Teto de Gastos no ano eleitoral.")
    
    md.append("\n### E. Governo Lula 3 (2023 - 2026): O Novo Arcabouço, Arrecadação e Rigidez Fiscal")
    md.append("- **Pontos Fortes:** Volta da política de valorização do salário mínimo (+4,74% de ganho real); aprovação da histórica Reforma Tributária sobre o Consumo (EC 132); queda da taxa de desemprego para mínimas históricas (em torno de 5,3%); estabilização cambial em patamar competitivo; balança comercial batendo recordes sucessivos impulsionada pelo agronegócio e petróleo.")
    md.append("- **Gargalos e Riscos:** Crescimento acelerado da dívida bruta (% do PIB saindo de 71,38% para 82,87%); modelo fiscal excessivamente ancorado em aumento de arrecadação e reonerações, em vez de corte de gastos obrigatórios; atritos frequentes entre Executivo e Banco Central sobre o nível da taxa Selic; percepção de risco fiscal que mantém juros futuros e prêmio de risco elevados.")
    
    caminho_saida = os.path.join(DOSSIE_DIR, "06_quadro_comparativo_geral.md")
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"✅ Relatório executivo consolidado gerado em: {caminho_saida}")

if __name__ == "__main__":
    gerar_quadro_comparativo()
