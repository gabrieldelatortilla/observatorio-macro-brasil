import os
import sys
import json
import urllib.request
import urllib.error
import time

# Garante UTF-8 no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_DIR = os.path.join(BASE_DIR, "dados")
os.makedirs(DADOS_DIR, exist_ok=True)

SERIES_BCB = {
    "ipca_mensal": {"id": 433, "nome": "IPCA - Variação mensal (%)", "unidade": "%"},
    "selic_anualizada": {"id": 4189, "nome": "Taxa Selic acumulada no mês anualizada (% a.a.)", "unidade": "% a.a."},
    "dolar_comercial": {"id": 3698, "nome": "Dólar Comercial (média mensal R$/US$)", "unidade": "R$"},
    "divida_bruta_pib": {"id": 13762, "nome": "Dívida Bruta do Governo Geral (% PIB)", "unidade": "% PIB"},
    "divida_liquida_pib": {"id": 4505, "nome": "Dívida Líquida do Setor Público (% PIB)", "unidade": "% PIB"},
    "salario_minimo": {"id": 1619, "nome": "Salário Mínimo Nominal", "unidade": "R$"},
    "desemprego_pnad": {"id": 24369, "nome": "Taxa de Desocupação (PNAD Contínua)", "unidade": "%"},
    "pib_acumulado_12m": {"id": 4380, "nome": "PIB Acumulado últimos 12 meses (R$ mi)", "unidade": "R$ mi"},
    "balanca_comercial_saldo": {"id": 28526, "nome": "Balança Comercial - Saldo Mensal (US$ mi)", "unidade": "US$ mi"},
    "resultado_primario_mensal": {"id": 5081, "nome": "Resultado Primário Setor Público Consolidado (R$ mi)", "unidade": "R$ mi"}
}

GOVERNOS = {
    "lula_1_e_2": {
        "nome": "Lula (1º e 2º Mandatos)",
        "presidente": "Luiz Inácio Lula da Silva",
        "inicio": "2003-01-01",
        "fim": "2010-12-31",
        "partido": "PT",
        "vice": "José Alencar (PL/PRB)",
        "duracao_anos": 8
    },
    "dilma_1_e_2": {
        "nome": "Dilma Rousseff (1º e 2º Mandatos)",
        "presidente": "Dilma Vana Rousseff",
        "inicio": "2011-01-01",
        "fim": "2016-08-31",
        "partido": "PT",
        "vice": "Michel Temer (PMDB)",
        "duracao_anos": 5.67
    },
    "temer": {
        "nome": "Michel Temer",
        "presidente": "Michel Miguel Elias Temer Lulia",
        "inicio": "2016-09-01",
        "fim": "2018-12-31",
        "partido": "MDB",
        "vice": "Nenhum (Linha Sucessória)",
        "duracao_anos": 2.33
    },
    "bolsonaro": {
        "nome": "Jair Bolsonaro",
        "presidente": "Jair Messias Bolsonaro",
        "inicio": "2019-01-01",
        "fim": "2022-12-31",
        "partido": "PSL / PL",
        "vice": "Antônio Hamilton Martins Mourão (PRTB)",
        "duracao_anos": 4
    },
    "lula_3": {
        "nome": "Lula (3º Mandato)",
        "presidente": "Luiz Inácio Lula da Silva",
        "inicio": "2023-01-01",
        "fim": "2026-12-31",
        "partido": "PT",
        "vice": "Geraldo José Rodrigues Alckmin Filho (PSB)",
        "duracao_anos": 4
    }
}

def fetch_bcb_series(serie_id, data_inicial="01/01/2003", data_final="31/12/2026", max_tentativas=3):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie_id}/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"
    headers = {"User-Agent": "ObservatorioBrasil/1.0 (MonitoramentoPublico)"}
    req = urllib.request.Request(url, headers=headers)
    
    for tentativa in range(1, max_tentativas + 1):
        try:
            with urllib.request.urlopen(req, timeout=35) as response:
                data = json.loads(response.read().decode("utf-8"))
                return data
        except Exception as e:
            if tentativa == max_tentativas:
                print(f"⚠️ Erro ao coletar série {serie_id} após {max_tentativas} tentativas: {e}")
                return []
            time.sleep(2)
    return []

def parse_date(date_str):
    """Converte 'DD/MM/YYYY' para 'YYYY-MM-DD'"""
    try:
        parts = date_str.split("/")
        if len(parts) == 3:
            return f"{parts[2]}-{parts[1]}-{parts[0]}"
    except:
        pass
    return date_str

def to_float(val):
    if val is None:
        return None
    try:
        return float(str(val).replace(",", "."))
    except:
        return None

def coletar_todas_as_series():
    print("=" * 70)
    print("🛰️  OBSERVATÓRIO BRASIL - COLETA AUTÔNOMA DE DADOS OFICIAIS (BCB)")
    print("=" * 70)
    
    dados_brutos = {}
    
    for chave, meta in SERIES_BCB.items():
        print(f"📥 Coletando: {meta['nome']} [SGS {meta['id']}]...")
        raw_items = fetch_bcb_series(meta["id"])
        
        serie_normalizada = []
        for item in raw_items:
            iso_date = parse_date(item.get("data", ""))
            val = to_float(item.get("valor"))
            if val is not None:
                serie_normalizada.append({"data": iso_date, "valor": val})
                
        dados_brutos[chave] = {
            "metadata": meta,
            "total_pontos": len(serie_normalizada),
            "dados": serie_normalizada
        }
        print(f"   ✓ {len(serie_normalizada)} registros processados.")
        
    caminho_series = os.path.join(DADOS_DIR, "series_historicas.json")
    with open(caminho_series, "w", encoding="utf-8") as f:
        json.dump(dados_brutos, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Séries históricas brutas salvas em: {caminho_series}")
    
    return dados_brutos

def analisar_por_governo(dados_brutos):
    print("\n📊 Processando cruzamento analítico por governo...")
    
    matriz = {}
    
    for gov_key, gov_info in GOVERNOS.items():
        inicio = gov_info["inicio"]
        fim = gov_info["fim"]
        
        analise_gov = {
            "info": gov_info,
            "metricas": {}
        }
        
        for serie_key, serie_obj in dados_brutos.items():
            pts = [p for p in serie_obj["dados"] if inicio <= p["data"] <= fim]
            if not pts:
                continue
                
            valores = [p["valor"] for p in pts]
            val_inicio = valores[0]
            val_fim = valores[-1]
            media = sum(valores) / len(valores)
            
            # Tratamento de IPCA (composição mensal)
            if serie_key == "ipca_mensal":
                fator = 1.0
                for v in valores:
                    fator *= (1.0 + v / 100.0)
                ipca_acumulado = (fator - 1.0) * 100.0
                analise_gov["metricas"][serie_key] = {
                    "tipo": "composto",
                    "total_meses": len(valores),
                    "acumulado_periodo_pct": round(ipca_acumulado, 2),
                    "media_mensal_pct": round(media, 2),
                    "min": round(min(valores), 2),
                    "max": round(max(valores), 2)
                }
            # Tratamento de Nível com variação (Salário Mínimo, Dólar, Dívida, PIB)
            elif serie_key in ["salario_minimo", "dolar_comercial", "divida_bruta_pib", "divida_liquida_pib", "pib_acumulado_12m"]:
                variacao_nominal = ((val_fim / val_inicio) - 1.0) * 100.0 if val_inicio else 0
                analise_gov["metricas"][serie_key] = {
                    "tipo": "nivel",
                    "inicio": val_inicio,
                    "fim": val_fim,
                    "variacao_pct": round(variacao_nominal, 2),
                    "media_periodo": round(media, 2),
                    "min": min(valores),
                    "max": max(valores)
                }
            # Taxas e fluxos médios (Selic, Desemprego, Resultado Primário, Balança Comercial)
            else:
                total_acumulado = sum(valores) if serie_key in ["resultado_primario_mensal", "balanca_comercial_saldo"] else None
                analise_gov["metricas"][serie_key] = {
                    "tipo": "taxa_ou_fluxo",
                    "inicio": val_inicio,
                    "fim": val_fim,
                    "media_periodo": round(media, 2),
                    "total_acumulado": round(total_acumulado, 2) if total_acumulado is not None else None,
                    "min": min(valores),
                    "max": max(valores)
                }
                
        # Cálculo derivado especial: Ganho Real do Salário Mínimo (Descontando IPCA)
        if "salario_minimo" in analise_gov["metricas"] and "ipca_mensal" in analise_gov["metricas"]:
            var_sm = analise_gov["metricas"]["salario_minimo"]["variacao_pct"]
            ipca_acum = analise_gov["metricas"]["ipca_mensal"]["acumulado_periodo_pct"]
            # Fórmula de Fisher: (1 + var_nom) / (1 + ipca) - 1
            ganho_real = (((1.0 + var_sm / 100.0) / (1.0 + ipca_acum / 100.0)) - 1.0) * 100.0
            analise_gov["metricas"]["ganho_real_salario_minimo"] = {
                "tipo": "derivado",
                "ganho_real_pct": round(ganho_real, 2),
                "formula": "Fórmula de Fisher [(1 + VarNom) / (1 + IPCA) - 1]"
            }
            
        matriz[gov_key] = analise_gov
        
    caminho_matriz = os.path.join(DADOS_DIR, "matriz_comparativa.json")
    with open(caminho_matriz, "w", encoding="utf-8") as f:
        json.dump(matriz, f, ensure_ascii=False, indent=2)
    print(f"💾 Matriz comparativa salva em: {caminho_matriz}")
    
    return matriz

def main():
    dados = coletar_todas_as_series()
    analisar_por_governo(dados)
    print("\n✅ Coleta e segmentação histórica concluídas com sucesso!")

if __name__ == "__main__":
    main()
