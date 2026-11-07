import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime

# Garante UTF-8 no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_DIR = os.path.join(BASE_DIR, "dados")
DOSSIE_DIR = os.path.join(BASE_DIR, "dossie_historico")
os.makedirs(DADOS_DIR, exist_ok=True)
os.makedirs(DOSSIE_DIR, exist_ok=True)

def fetch_json(url):
    headers = {
        "User-Agent": "ObservatorioBrasil/1.0 (MonitoramentoPublico)",
        "Accept": "application/json"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"⚠️ Erro ao consultar API {url}: {e}")
        return None

def coletar_medidas_provisorias():
    print("📜 Coletando Medidas Provisórias recentes do Poder Executivo (Câmara Dados Abertos)...")
    ano_atual = datetime.now().year
    url = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes?siglaTipo=MPV&ano={ano_atual}&ordem=DESC&ordenarPor=id"
    data = fetch_json(url)
    
    mpvs = []
    if data and "dados" in data:
        for item in data["dados"][:15]:  # Pega as 15 mais recentes
            mpvs.append({
                "id": item.get("id"),
                "tipo": item.get("siglaTipo"),
                "numero": item.get("numero"),
                "ano": item.get("ano"),
                "ementa": item.get("ementa"),
                "data_apresentacao": item.get("dataApresentacao", "")[:10],
                "link": item.get("uri")
            })
    print(f"   ✓ {len(mpvs)} Medidas Provisórias mapeadas.")
    return mpvs

def coletar_projetos_executivo():
    print("📜 Coletando Projetos de Lei e PECs do Executivo em tramitação...")
    ano_atual = datetime.now().year
    # Busca PLs de relevância prioritária do ano corrente
    url = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes?siglaTipo=PL&ano={ano_atual}&itens=10&ordem=DESC&ordenarPor=id"
    data = fetch_json(url)
    
    pls = []
    if data and "dados" in data:
        for item in data["dados"][:10]:
            pls.append({
                "id": item.get("id"),
                "tipo": item.get("siglaTipo"),
                "numero": item.get("numero"),
                "ano": item.get("ano"),
                "ementa": item.get("ementa"),
                "data_apresentacao": item.get("dataApresentacao", "")[:10]
            })
    print(f"   ✓ {len(pls)} Projetos de Lei mapeados.")
    return pls

def compilar_auditoria_politicas(mpvs, pls):
    print("📊 Compilando dossiê de Atos do Executivo e Controvérsias de Políticas Públicas...")
    
    arquivo_json = os.path.join(DADOS_DIR, "atos_executivo_recentes.json")
    dados_compilados = {
        "ultima_atualizacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_mpvs_rastreadas": len(mpvs),
        "total_pls_rastreados": len(pls),
        "medidas_provisorias": mpvs,
        "projetos_lei": pls
    }
    with open(arquivo_json, "w", encoding="utf-8") as f:
        json.dump(dados_compilados, f, ensure_ascii=False, indent=2)
    print(f"💾 Dados salvos em: {arquivo_json}")
    
    # Gera documento em Markdown no dossie_historico
    caminho_md = os.path.join(DOSSIE_DIR, "07_atos_executivo_e_politicas.md")
    
    md = []
    md.append("# 🏛️ Observatório Brasil: Atos do Executivo, Decisões e Auditoria de Políticas Públicas")
    md.append(f"\n> **Última Atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M')} | **Fonte:** Câmara dos Deputados (Dados Abertos) e DOU\n")
    
    md.append("Este módulo audita as decisões normativas, decretos, medidas provisórias e as principais controvérsias regulatórias do mandato presidencial em curso.\n")
    
    md.append("## 🔍 1. Raio-X de Controvérsias Emblemáticas e Políticas de Arrecadação\n")
    
    md.append("### A. O Caso do PIX MEI e Fiscalização das Transações Digitais")
    md.append("- **A Medida e a Polêmica:** Movimentações regulatórias do Confaz e da Receita Federal visando cruzar dados de movimentações financeiras via PIX e cartões de crédito para microempresas e Microempreendedores Individuais (MEIs).")
    md.append("- **O Ruído Político:** A narrativa de 'taxação do PIX' e aperto fiscal gerou reação imediata do setor de pequenos negócios e da opinião pública. Na prática, a medida buscava fiscalizar a omissão de receita e desenquadramento de MEIs que faturavam acima do teto de R$ 81 mil/ano.")
    md.append("- **O Fiasco de Alcance e Recuos:** Devido à forte repercussão negativa e ao fato de atingir uma fração desproporcionalmente pequena de arrecadação efetiva comparada ao desgaste político, o governo recuou em declarações públicas e adiou exigências, evidenciando o padrão de atrito gerado por iniciativas de fiscalização microscópica enquanto grandes privilégios fiscais permanecem intocados.")
    
    md.append("\n### B. Remessa Conforme e a 'Taxa das Blusinhas' (Compras Internacionais até US$ 50)")
    md.append("- **A Medida:** Fim da isenção do imposto de importação federal para compras internacionais abaixo de US$ 50 (imposto de 20% somado a 17% de ICMS estadual).")
    md.append("- **Impacto Social e Desgaste:** Aprovada no Congresso Nacional como parte do projeto do Mover, a medida impactou diretamente o consumo das classes C, D e E em plataformas de e-commerce asiáticas (Shopee, Shein, AliExpress), gerando forte descontentamento popular contra a equipe econômica.")
    
    md.append("\n### C. Regulamentação do Imposto Seletivo e IVA Dual (Reforma Tributária)")
    md.append("- **A Medida:** Tramitação das leis complementares que fixam as alíquotas do IBS e da CBS, com definição da 'cesta básica nacional' isenta e do Imposto Seletivo ('imposto do pecado' sobre bebidas, cigarros, veículos e minerais).")
    md.append("- **Tensões:** Disputa acirrada de lobbies setoriais no Congresso (saúde privada, agronegócio, serviços) para obtenção de regimes diferenciados e alíquotas reduzidas, pressionando a alíquota padrão estimada para cerca de 27% a 28%, o que pode torná-la uma das maiores do mundo.")

    md.append("\n---\n")
    md.append("## 📜 2. Medidas Provisórias (MPVs) Recentes Editadas pelo Poder Executivo\n")
    md.append("| Número/Ano | Apresentação | Ementa Resumida |")
    md.append("| :---: | :---: | :--- |")
    
    for mp in mpvs[:10]:
        num_str = f"**MPV {mp['numero']}/{mp['ano']}**"
        data_str = mp['data_apresentacao']
        ementa = mp['ementa'].replace("\n", " ").strip()
        md.append(f"| {num_str} | {data_str} | {ementa} |")
        
    with open(caminho_md, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"✅ Relatório de Atos do Executivo gerado em: {caminho_md}")

def main():
    print("=" * 70)
    print("🛰️  OBSERVATÓRIO BRASIL - COLETA DE ATOS E POLÍTICAS DO EXECUTIVO")
    print("=" * 70)
    mpvs = coletar_medidas_provisorias()
    pls = coletar_projetos_executivo()
    compilar_auditoria_politicas(mpvs, pls)
    print("\n✅ Módulo de atos e políticas concluído com sucesso!")

if __name__ == "__main__":
    main()
