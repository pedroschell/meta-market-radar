// Extrai anunciantes da Biblioteca de Anuncios da Meta direto do DOM.
// Cole como o parametro `function` de mcp__playwright__browser_evaluate.
// Retorna: total de resultados da busca + anunciantes agregados
// (numero de anuncios ativos e data do mais antigo = ha quanto tempo investe).
() => {
  const total = (document.body.innerText.match(/~?[\d.]+\s+resultados?/i) || ['?'])[0];
  const M = {jan:1,fev:2,mar:3,abr:4,mai:5,jun:6,jul:7,ago:8,set:9,out:10,nov:11,dez:12};
  const vistos = {}, ag = {};

  document.querySelectorAll('a[href*="facebook.com/"]').forEach(a => {
    const nome = (a.innerText || '').trim();
    if (!nome || nome.length < 3 || nome.length > 60) return;
    // descarta rotulos da propria interface da Meta
    if (/^(Ver|Abrir|Saiba|Cadastre|Enviar|Comprar|Reservar|Biblioteca|API|Cookies|Entrar|Criar|Relatório)/i.test(nome)) return;

    // sobe ate o card do anuncio
    let n = a, card = null;
    for (let i = 0; i < 12 && n; i++, n = n.parentElement) {
      if (n.innerText && /Identificação da biblioteca/.test(n.innerText)) { card = n; break; }
    }
    if (!card) return;

    const id = (card.innerText.match(/Identificação da biblioteca:\s*(\d+)/) || [])[1];
    if (!id || vistos[id]) return;      // deduplica: um card tem varios links
    vistos[id] = 1;

    const m = card.innerText.match(/Veiculação iniciada em (\d{1,2}) de ([a-zç]+)\.? de (\d{4})/i);
    const iso = m
      ? `${m[3]}-${String(M[m[2].slice(0,3)] || 0).padStart(2,'0')}-${String(m[1]).padStart(2,'0')}`
      : null;

    ag[nome] = ag[nome] || { anuncios: 0, desde: null, url: a.getAttribute('href') };
    ag[nome].anuncios++;
    if (iso && (!ag[nome].desde || iso < ag[nome].desde)) ag[nome].desde = iso;
  });

  return {
    total,
    cards_lidos: Object.keys(vistos).length,
    anunciantes: Object.entries(ag)
      .map(([nome, v]) => ({ nome, ...v }))
      .sort((a, b) => b.anuncios - a.anuncios || (a.desde || '9').localeCompare(b.desde || '9'))
  };
}
