#!/usr/bin/env python3
"""
Converte um snapshot de acessibilidade da Biblioteca de Anuncios da Meta
(gerado pelo Playwright MCP) em dados estruturados.

Uso:
    python3 parse-adlib.py <snapshot.txt> [--json] [--csv saida.csv]

Saida padrao: ranking de anunciantes por numero de anuncios ativos,
com a data do anuncio mais antigo (= ha quanto tempo investe).
"""
import sys, re, json, csv
from collections import defaultdict

MESES = {"jan":1,"fev":2,"mar":3,"abr":4,"mai":5,"jun":6,
         "jul":7,"ago":8,"set":9,"out":10,"nov":11,"dez":12}

def parse(path):
    txt = open(path, encoding="utf-8", errors="replace").read()
    linhas = txt.splitlines()
    anuncios, atual = [], None

    for i, ln in enumerate(linhas):
        m = re.search(r'Identificação da biblioteca:\s*"?(\d+)"?', ln)
        if m:
            if atual and atual.get("anunciante"):
                anuncios.append(atual)
            atual = {"id": m.group(1), "inicio": None, "anunciante": None, "url": None}
            continue
        if atual is None:
            continue

        m = re.search(r'Veiculação iniciada em (\d{1,2}) de ([a-zç]{3})[a-zç.]* de (\d{4})', ln)
        if m and not atual["inicio"]:
            d, mes, a = int(m.group(1)), MESES.get(m.group(2), 0), int(m.group(3))
            atual["inicio"] = f"{a:04d}-{mes:02d}-{d:02d}" if mes else None
            continue

        m = re.search(r'link "([^"]+)"', ln)
        if m and not atual["anunciante"]:
            nome = m.group(1).strip()
            # descarta itens de interface que nao sao anunciantes
            if nome.lower() in ("cookies","biblioteca de anúncios da meta",
                                "api da biblioteca de anúncios","ver detalhes do anúncio"):
                continue
            atual["anunciante"] = nome
            for j in range(i, min(i + 4, len(linhas))):
                u = re.search(r'/url:\s*(\S+)', linhas[j])
                if u:
                    atual["url"] = u.group(1)
                    break

    if atual and atual.get("anunciante"):
        anuncios.append(atual)

    total = re.search(r'~?([\d.]+)\s+resultados?', txt)
    return anuncios, (total.group(1) if total else "?")

def agregar(anuncios):
    ag = defaultdict(lambda: {"anuncios": 0, "desde": None, "url": None})
    for a in anuncios:
        r = ag[a["anunciante"]]
        r["anuncios"] += 1
        r["url"] = r["url"] or a["url"]
        if a["inicio"] and (r["desde"] is None or a["inicio"] < r["desde"]):
            r["desde"] = a["inicio"]
    return sorted(
        ({"anunciante": k, **v} for k, v in ag.items()),
        key=lambda x: (-x["anuncios"], x["desde"] or "9999"),
    )

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    anuncios, total = parse(sys.argv[1])
    linhas = agregar(anuncios)

    if "--json" in sys.argv:
        print(json.dumps({"total_resultados": total, "anunciantes": linhas},
                         ensure_ascii=False, indent=2)); return

    if "--csv" in sys.argv:
        out = sys.argv[sys.argv.index("--csv") + 1]
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["anunciante", "anuncios", "desde", "url"])
            w.writeheader(); w.writerows(linhas)
        print(f"{len(linhas)} anunciantes -> {out}"); return

    print(f"Total de resultados na busca: {total}")
    print(f"Anuncios lidos nesta pagina : {len(anuncios)}")
    print(f"Anunciantes distintos       : {len(linhas)}\n")
    print(f"{'ANUNCIANTE':38s} {'ANUNCIOS':>8s}  {'ATIVO DESDE':11s}")
    print("-" * 62)
    for l in linhas:
        print(f"{l['anunciante'][:38]:38s} {l['anuncios']:>8d}  {l['desde'] or '-':11s}")

if __name__ == "__main__":
    main()
