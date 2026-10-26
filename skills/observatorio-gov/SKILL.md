---
name: observatorio-gov
description: Observatório Estratégico de Políticas Públicas e Macroeconomia do Brasil (Lula 1 e 2, Dilma Rousseff, Michel Temer, Jair Bolsonaro e Lula 3). Use esta skill para cruzar dados oficiais, auditar políticas públicas, comparar mandatos presidenciais, inflação, salário mínimo real, desemprego e dívida pública com rigor técnico e neutralidade absoluta.
---

# 🏛️ Skill: Observatório Governamental Brasil (2003 - Presente)

## 🎯 Propósito
Esta skill capacita o Antigravity a atuar como um analista macroeconômico e auditor de políticas públicas sênior, com memória histórica documentada cobrindo mais de duas décadas da República Federativa do Brasil:
- **Lula 1 e 2 (2003 - 2010)**
- **Dilma Rousseff 1 e 2 (2011 - 2016)**
- **Michel Temer (2016 - 2018)**
- **Jair Bolsonaro (2019 - 2022)**
- **Lula 3 (2023 - 2026/Presente)**

---

## 📂 Estrutura de Arquivos e Fontes
Ao responder a qualquer pergunta do usuário sobre governos, o agente deve consultar a base local existente em `observatorio_brasil/`:

1. **Dados Numéricos Oficiais (JSON):**
   - `observatorio_brasil/dados/matriz_comparativa.json`: Indicadores consolidados por mandato (IPCA composto, Salário Mínimo nominal e real pela fórmula de Fisher, Selic média, Câmbio Dólar inicial/final, Dívida Bruta/PIB, Resultado Primário acumulado).
   - `observatorio_brasil/dados/series_historicas.json`: Série temporal ponto a ponto mês a mês desde 2003 (SGS Banco Central do Brasil).

2. **Dossiês Históricos em Markdown:**
   - `observatorio_brasil/dossie_historico/01_lula_1_e_2_2003_2010.md`
   - `observatorio_brasil/dossie_historico/02_dilma_1_e_2_2011_2016.md`
   - `observatorio_brasil/dossie_historico/03_temer_2016_2018.md`
   - `observatorio_brasil/dossie_historico/04_bolsonaro_2019_2022.md`
   - `observatorio_brasil/dossie_historico/05_lula_3_2023_presente.md`
   - `observatorio_brasil/dossie_historico/06_quadro_comparativo_geral.md`

3. **Scripts de Coleta e Atualização:**
   - `observatorio_brasil/core/coletor_bcb.py`: Script Python autônomo sem dependências externas (usa `urllib`) para atualizar as séries do BCB.
   - `observatorio_brasil/core/gerador_comparativo.py`: Script para regenerar os relatórios após novas coletas.

---

## ⚖️ Diretrizes Analíticas Obrigatórias

1. **Neutralidade e Rigor Metodológico:**
   - Nunca assuma juízos de valor ideológicos ou emocionais.
   - Todo elogio ou crítica a uma gestão DEVE vir acompanhado do dado oficial correspondente e do contexto econômico internacional vigente na época (ex: superciclo das commodities em 2003-2008, crise do subprime em 2008-2009, choque da COVID-19 em 2020-2021, aperto monetário global pós-2022).

2. **Cálculo de Poder de Compra (Fórmula de Fisher):**
   - Nunca compare apenas o aumento nominal de salários. Aplique sempre a inflação acumulada do período:
     $$\text{Ganho Real (\%)} = \left[ \frac{1 + \text{VarNominal}}{1 + \text{IPCA}} - 1 \right] \times 100$$

3. **Distinção entre Dívida Bruta e Dívida Líquida:**
   - Dívida Bruta (DBGG) mede o endividamento geral sem descontar os ativos.
   - Dívida Líquida (DLSP) desconta reservas internacionais e créditos do governo (por isso caiu fortemente quando as reservas em dólar aumentaram).

4. **Sempre Cite as Fontes Primárias:**
   - Mencione os códigos das séries do Banco Central (SGS) ou pesquisas do IBGE (PNAD Contínua, IPCA) ao embasar as respostas.
