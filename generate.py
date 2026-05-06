#!/usr/bin/env python3
"""Gera 9 HTMLs (1 hub + 8 individuais) a partir de data.py."""
import os, sys, html
from data import CIRURGIOES, iniciais

OUT = os.path.dirname(os.path.abspath(__file__))
DATA_DIA = "06 de Maio · 2026"
TITULO_DIA = "Diagnóstico CPP"

# ============ HEAD COMPARTILHADO ============
HEAD = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0a0908">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
"""

TOPBAR = """
<header class="topbar">
  <div class="topbar-inner">
    <a href="index.html" class="brand">
      <span class="brand-mark">CPP</span>
      <span class="brand-text">Cirurgião Particular Premium · <span class="accent">Diagnóstico</span></span>
    </a>
    {nav}
  </div>
</header>
"""

FOOT = """
<footer class="foot">
  <div class="wrap">
    <p class="small">Cirurgião Particular Premium · Diagnóstico individual com Patrick Suyti + Dr. Mateus Jerônimo</p>
    <p class="gold" style="margin-top:8px">06 de Maio · 2026</p>
  </div>
</footer>
<button class="cirurgico-toggle" onclick="toggleModo()">Modo cirúrgico</button>
<script>
function toggleModo() {
  document.body.classList.toggle('cirurgico-on');
  const url = new URL(window.location);
  if (document.body.classList.contains('cirurgico-on')) {
    url.searchParams.set('modo','cirurgico');
  } else {
    url.searchParams.delete('modo');
  }
  history.replaceState(null,'',url);
}
const params = new URLSearchParams(window.location.search);
if (params.get('modo') === 'cirurgico') document.body.classList.add('cirurgico-on');
document.addEventListener('keydown', function(e) {
  if ((e.key === 'c' || e.key === 'C') && !e.ctrlKey && !e.metaKey && !e.altKey && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
    toggleModo();
  }
});
</script>
</body>
</html>
"""

def perfil_class(perfil):
    if not perfil: return "incerto"
    p = perfil.upper()
    if "ÁGUIA" in p or "AGUIA" in p: return "aguia"
    if "GAVIÃO" in p or "GAVIAO" in p: return "gaviao"
    if "URUBU" in p: return "urubu"
    if "PATO" in p: return "pato"
    return "incerto"

def perfil_label(perfil):
    if not perfil: return "A confirmar"
    return perfil

def safe(s):
    if s is None: return ""
    return html.escape(str(s))

def li(items):
    return "\n".join(f"      <li>{safe(it)}</li>" for it in (items or []))

def nav_back_button(text="← voltar ao painel"):
    return f'<a href="index.html" class="nav-back">{text}</a>'

# ============ HUB ============
def render_hub():
    title = "Diagnóstico CPP · 06 de Maio · 2026"
    desc = "Diagnóstico individual de 8 cirurgiões com Patrick Suyti e Dr. Mateus Jerônimo · Cirurgião Particular Premium"

    # estatísticas
    perfis = {}
    confirmados = 0
    score_sum = 0
    score_n = 0
    for c in CIRURGIOES:
        p = perfil_class(c.get('perfil_cpp'))
        perfis[p] = perfis.get(p,0) + 1
        if c.get('crm') and "[A CONFIRMAR" not in (c.get('crm') or ""):
            confirmados += 1
        if c.get('score_compra'):
            score_sum += c['score_compra']
            score_n += 1
    score_med = round(score_sum / score_n) if score_n else 0

    cards_html = []
    for c in CIRURGIOES:
        pc = perfil_class(c.get('perfil_cpp'))
        pl = perfil_label(c.get('perfil_cpp')).split(' ')[0]
        cards_html.append(f"""
    <a href="{c['slug']}.html" class="card">
      <div class="card-row">
        <span class="card-time">{c['hora']}</span>
        <span class="card-perfil {pc}">{safe(pl)}</span>
      </div>
      <div>
        <div class="card-name">{safe(c['nome'])}</div>
        <div class="card-spec">{safe(c['especialidade'])}</div>
      </div>
      <div class="card-loc">📍 {safe(c['cidade'])} · {safe(c['estado'])}</div>
      <div class="card-cta">Abrir mapa</div>
    </a>""")

    # composição do dia
    composicao_pieces = []
    for k, label in [('aguia','Águias'),('gaviao','Gaviões'),('urubu','Urubus'),('pato','Patos'),('incerto','Incertos')]:
        n = perfis.get(k, 0)
        if n: composicao_pieces.append(f'<span class="tag {("gold" if k=="aguia" else "")}">{n} {label}</span>')

    composicao_html = " ".join(composicao_pieces)

    body = f"""
{TOPBAR.format(nav='')}

<section class="hero">
  <div class="wrap-narrow">
    <span class="hero-eyebrow">Cirurgião Particular Premium</span>
    <h1 class="hero-title">Diagnóstico individual · <span class="gold">06 de Maio</span></h1>
    <p class="hero-sub">8 cirurgiões. Uma janela de oito horas. Um propósito único: enxergar com precisão onde cada um está hoje — e onde poderia estar amanhã.</p>
    <div style="margin-top: 28px; color: var(--text-3); font-family: var(--serif); font-size: 1.05rem;">
      Conduzido por <strong style="color: var(--gold-soft)">Patrick Suyti</strong> &amp; <strong style="color: var(--gold-soft)">Dr. Mateus Jerônimo</strong>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Visão de grupo</span>
      <h2>O que esse dia significa</h2>
    </div>

    <div class="stats-grid">
      <div class="stat">
        <div class="stat-label">Cirurgiões</div>
        <div class="stat-value">8</div>
        <div class="stat-sub">um a cada hora</div>
      </div>
      <div class="stat">
        <div class="stat-label">Identidade confirmada</div>
        <div class="stat-value">{confirmados}<span style="color: var(--text-4); font-size: 1.4rem">/8</span></div>
        <div class="stat-sub">cruzamento CRM + redes</div>
      </div>
      <div class="stat">
        <div class="stat-label">Score médio · base CPP</div>
        <div class="stat-value">{score_med}<span style="color: var(--text-4); font-size: 1.4rem">/100</span></div>
        <div class="stat-sub">{score_n} dos 8 já dossiados</div>
      </div>
      <div class="stat">
        <div class="stat-label">Janela</div>
        <div class="stat-value">8h</div>
        <div class="stat-sub">11h às 18h</div>
      </div>
    </div>

    <div class="block" style="margin-top: 32px">
      <span class="block-eyebrow">Composição do dia</span>
      <h3>A mistura é deliberadamente assimétrica</h3>
      <p style="margin-top: 12px">Você não vai entrar oito vezes no mesmo cirurgião. Cada call exige uma postura diferente — e o painel ao lado mostra qual.</p>
      <div class="tags" style="margin-top: 18px">{composicao_html}</div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="hub-grid-head">
      <div>
        <span class="eyebrow">Agenda do dia</span>
        <h2>Os 8 mapas individuais</h2>
      </div>
      <p class="muted" style="font-size: 0.9rem">Clique no card para abrir o diagnóstico em detalhe</p>
    </div>
    <div class="cards-grid">{''.join(cards_html)}
    </div>
  </div>
</section>

<section class="cirurgico-section cirurgico" style="display:none">
  <div class="wrap-narrow">
    <div class="section-head">
      <span class="eyebrow" style="color: var(--gold)">Painel cirúrgico do dia</span>
      <h2>O que olhar antes de cada call</h2>
    </div>

    <div class="block">
      <span class="block-eyebrow">Pitches premium imediatos</span>
      <h3>4 cirurgiões podem fechar hoje (perfil Águia/Gavião alto)</h3>
      <ul class="bullets">
        <li><strong>Rafael Bozzo Tacino</strong> · 12h · Águia · score 84 — peer-to-peer, NUNCA tom de "aprenda do zero"</li>
        <li><strong>Marina Marangon Melhado</strong> · 16h · Águia · score 84 — elite-para-elite, vender escala não convênio</li>
        <li><strong>Eduardo Watanabe Castanheira</strong> · 17h · Águia/Urubu · score 82 — pitch de LEGADO, sênior 30 anos</li>
        <li><strong>Tatiana Patruni</strong> · 11h · Gavião · espelho duro, ela é Gavião com casca de Pato</li>
      </ul>
    </div>

    <div class="block">
      <span class="block-eyebrow">Qualificação financeira antes do pitch</span>
      <h3>2 cirurgiões: ROI de 3-5 anos, não retorno imediato</h3>
      <ul class="bullets">
        <li><strong>Júlio Fran da Silva Pinto</strong> · 15h · Urubu · score 45 — Timbó/SC, Unimed dominante, verificar capital</li>
        <li><strong>Felipe (Fellype) de Bulhões Ojeda</strong> · 18h · Pato → Urubu · score 48 — plantonista, sem clínica, verificar capital próprio</li>
      </ul>
    </div>

    <div class="block">
      <span class="block-eyebrow">Crítico</span>
      <h3>Tarik Soares Suleiman · 14h · Gavião · score 78</h3>
      <p>Lead AAA estrutural. Tom técnico+ambicioso. Bariátrica como produto premium, não como cirurgia.</p>
    </div>

    <div class="block">
      <span class="block-eyebrow">⚠️ Confirmação de identidade obrigatória nos primeiros 5min</span>
      <h3>Paulo Victor Pereira · 13h · &lt;30% confiança</h3>
      <p>Não está na base do desafio R$97. Múltiplos candidatos no Brasil. Pedir CRM + cidade + especialidade ANTES de qualquer pitch. Stephany pode puxar cadastro.</p>
    </div>

    <div class="block">
      <span class="block-eyebrow">Correções de grafia</span>
      <ul class="bullets">
        <li>Patrick listou <strong>Patrubi</strong> · grafia oficial: <strong>Patruni</strong> (com N)</li>
        <li>Patrick listou <strong>Tarick</strong> · grafia oficial: <strong>Tarik</strong> (sem C)</li>
        <li>Patrick listou <strong>Mariana Marangon</strong> · nome correto: <strong>Marina Marangon Melhado</strong></li>
        <li>Felipe Ojeda assina <strong>Fellype</strong> com Y em publicações acadêmicas</li>
      </ul>
    </div>
  </div>
</section>

{FOOT}
"""
    out = HEAD.format(title=title, desc=desc) + body
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"  ✓ index.html (hub)")

# ============ INDIVIDUAL ============
def render_individual(c):
    title = f"{c['nome']} · Diagnóstico CPP · 06/05"
    desc = f"Mapa diagnóstico individual para {c['nome']} — Cirurgião Particular Premium · 06 de Maio 2026"
    pc = perfil_class(c.get('perfil_cpp'))
    pl = perfil_label(c.get('perfil_cpp'))

    correcao_html = ""
    if c.get('correcao_grafia'):
        correcao_html = f'<div class="note"><h5>Nota de identidade</h5><p>{safe(c["correcao_grafia"])}</p></div>'

    # IDENTIDADE
    formacao_li = li(c.get('formacao'))
    estruturas_li = li(c.get('estruturas'))
    credenciais_li = li(c.get('credenciais'))

    redes_rows = []
    if c.get('instagram'):
        ig_status = "aberto" if c.get('instagram_aberto') else "fechado / inativo"
        seg = c.get('instagram_seguidores')
        seg_str = f" · {seg} seguidores" if seg and seg != "—" else ""
        redes_rows.append(f'<div class="kv-row"><span class="k">Instagram</span><span class="v"><a href="{c["instagram_url"]}" target="_blank" rel="noopener">{safe(c["instagram"])}</a> · <span class="muted">{ig_status}{seg_str}</span></span></div>')
    if c.get('site'):
        redes_rows.append(f'<div class="kv-row"><span class="k">Site</span><span class="v"><a href="{c["site"]}" target="_blank" rel="noopener">{safe(c["site"])}</a></span></div>')
    if c.get('doctoralia'):
        redes_rows.append(f'<div class="kv-row"><span class="k">Doctoralia</span><span class="v"><a href="{c["doctoralia"]}" target="_blank" rel="noopener">ver perfil</a></span></div>')
    if c.get('linkedin'):
        redes_rows.append(f'<div class="kv-row"><span class="k">LinkedIn</span><span class="v"><a href="{c["linkedin"]}" target="_blank" rel="noopener">ver perfil</a></span></div>')

    redes_kv_html = ""
    if redes_rows:
        redes_kv_html = '<div class="kv">' + "".join(redes_rows).replace('<div class="kv-row">','').replace('</div>','</span></span></div>').replace('<span class="k">','<div class="k">').replace('</span><span class="v">','</div><div class="v">') + '</div>'
        # simplificar — vou reconstruir manualmente
        redes_kv_html = '<div class="kv">'
        for r in redes_rows:
            # parse rapido
            import re
            m = re.search(r'<span class="k">(.*?)</span><span class="v">(.*?)</span></div>', r, re.S)
            if m:
                redes_kv_html += f'<div class="k">{m.group(1)}</div><div class="v">{m.group(2)}</div>'
        redes_kv_html += '</div>'

    # POTENCIAL (público)
    posicao_atual_html = c.get('posicionamento_atual_publico') or ""
    potencial_html = c.get('potencial_publico') or ""

    # DORES (3 tiles)
    dores_html = ""
    for i, (dor, evid) in enumerate(c.get('dores_top3') or [], 1):
        dores_html += f'''
      <div class="tile">
        <div class="tile-num">0{i}</div>
        <div class="tile-body">
          <h5>{safe(dor)}</h5>
          <p>{safe(evid)}</p>
        </div>
      </div>'''

    # GAPS
    gaps_html = ""
    for area, descricao in c.get('gaps') or []:
        gaps_html += f'''
      <div class="duo-card">
        <h5>{safe(area)}</h5>
        <p>{safe(descricao)}</p>
      </div>'''

    # HOOKS (cirúrgico)
    hooks_html = ""
    for i, h in enumerate(c.get('hooks_abertura') or [], 1):
        hooks_html += f'<p class="hook"><span class="hook-num">HOOK {i}</span>"{safe(h)}"</p>'

    # OBJEÇÕES (cirúrgico)
    objecoes_li = li(c.get('objecoes_esperadas') or [])

    # FONTES
    fontes_li = "\n".join(f'<li><a href="{f}" target="_blank" rel="noopener">{html.escape(f)}</a></li>' for f in (c.get('fontes') or []))

    # bio IG (cirúrgico)
    instagram_detail = ""
    if c.get('instagram'):
        bio = safe(c.get('instagram_bio'))
        tom = safe(c.get('instagram_tom'))
        instagram_detail = f"""
      <div class="kv">
        <div class="k">Bio</div><div class="v">{bio}</div>
        <div class="k">Tom</div><div class="v">{tom}</div>
        <div class="k">Posts</div><div class="v">{safe(c.get('instagram_posts'))}</div>
        <div class="k">Tagline atual</div><div class="v">{safe(c.get('tagline_atual') or "—")}</div>
      </div>"""

    score_html = ""
    if c.get('score_compra'):
        score_html = f'''
      <div class="score-block">
        <span class="score-num">{c["score_compra"]}</span>
        <span class="score-max">/100</span>
        <span class="score-label">· Score de compra · base CPP</span>
      </div>'''

    body = f"""
{TOPBAR.format(nav=nav_back_button())}

<section class="hero">
  <div class="wrap-narrow">
    <span class="hero-eyebrow">Mapa Diagnóstico · 06 Maio · {c['hora']}</span>
    <h1 class="hero-title">{safe(c['nome'])}</h1>
    <p class="hero-sub">{safe(c['especialidade'])}{(' · ' + safe(c['subespecialidade'])) if c.get('subespecialidade') else ''}</p>

    <div class="hero-card">
      <div class="hero-avatar">{iniciais(c['nome'])}</div>
      <div class="hero-meta">
        <div class="hero-meta-row">
          <span><strong>📍 {safe(c['cidade'])} · {safe(c['estado'])}</strong></span>
          <span class="dot"></span>
          <span>🕐 <strong>{c['hora']}</strong> · 6 de maio</span>
          {('<span class="dot"></span><span>🆔 <strong>' + safe(c['crm']) + '</strong></span>') if c.get('crm') else ''}
        </div>
        <div class="hero-meta-row">
          <span><a href="{c['zoom']}" target="_blank" rel="noopener">⚡ Sala Zoom da call</a></span>
        </div>
        {correcao_html}
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap-narrow">
    <div class="section-head">
      <span class="eyebrow">Identidade</span>
      <h2>Quem você é, em uma página</h2>
    </div>

    {redes_kv_html}

    <div class="block" style="margin-top: 32px">
      <span class="block-eyebrow">Trajetória</span>
      <h3>Formação</h3>
      <ul class="bullets">{formacao_li}</ul>
    </div>

    {('<div class="block"><span class="block-eyebrow">Estrutura atual</span><h3>Onde você atua</h3><ul class="bullets">' + estruturas_li + '</ul></div>') if estruturas_li else ''}

    {('<div class="block"><span class="block-eyebrow">Credenciais</span><h3>O que sua trajetória já provou</h3><ul class="bullets">' + credenciais_li + '</ul></div>') if credenciais_li else ''}
  </div>
</section>

<section>
  <div class="wrap-narrow">
    <div class="section-head">
      <span class="eyebrow">Onde você está hoje</span>
      <h2>Posicionamento atual</h2>
    </div>

    <div class="block">
      <p class="block-lead">"{safe(posicao_atual_html)}"</p>
    </div>
  </div>
</section>

<section>
  <div class="wrap-narrow">
    <div class="section-head">
      <span class="eyebrow">Mapa de potencial</span>
      <h2>O que escuta o seu próximo capítulo</h2>
    </div>

    <h4 style="color: var(--text-3); margin-bottom: 6px; font-size: 0.78rem; letter-spacing: 0.18em; text-transform: uppercase">Pontos de tensão</h4>
    {dores_html}

    <h4 style="color: var(--text-3); margin: 40px 0 6px; font-size: 0.78rem; letter-spacing: 0.18em; text-transform: uppercase">Gaps observáveis</h4>
    <div class="duo">{gaps_html}
    </div>
  </div>
</section>

<section>
  <div class="wrap-narrow">
    <div class="section-head">
      <span class="eyebrow">Próximo capítulo</span>
      <h2>O que poderia estar à sua frente</h2>
    </div>

    <div class="block">
      <p class="block-lead">{potencial_html}</p>
      <div class="gold-line"></div>
      <p style="font-family: var(--serif); font-size: 1.05rem; color: var(--text-2); font-style: italic;">É exatamente sobre isso que essa call de hoje existe.</p>
    </div>

    <div class="cta-block">
      <h2>06 de Maio · {c['hora']}</h2>
      <p>Patrick Suyti &amp; Dr. Mateus Jerônimo · 60 minutos · sua agenda</p>
    </div>
  </div>
</section>

<!-- ============ MODO CIRÚRGICO (Patrick + Mateus) ============ -->
<section class="cirurgico-section cirurgico" style="display: none">
  <div class="wrap-narrow">
    <div class="section-head">
      <span class="eyebrow" style="color: var(--gold)">Painel cirúrgico</span>
      <h2>Munição para a call</h2>
      <span class="perfil-badge {pc}">{safe(pl)}</span>
      {score_html}
    </div>

    <div class="block">
      <span class="block-eyebrow">Por que esse perfil</span>
      <h3>Evidências observáveis</h3>
      <ul class="bullets">{li(c.get('perfil_evidencias'))}</ul>
    </div>

    {('<div class="block"><span class="block-eyebrow">Instagram · leitura</span><h3>O que o perfil te conta</h3>' + instagram_detail + '</div>') if c.get('instagram') else ''}

    <div class="block">
      <span class="block-eyebrow">Hooks de abertura · primeiros 60s</span>
      <h3>Três entradas testadas</h3>
      {hooks_html}
    </div>

    <div class="block">
      <span class="block-eyebrow">Objeções esperadas</span>
      <h3>O que pode vir</h3>
      <ul class="bullets">{objecoes_li}</ul>
    </div>

    <div class="block">
      <span class="block-eyebrow">Abordagem recomendada</span>
      <h3>Como conduzir</h3>
      <p style="margin-top: 14px; color: var(--text-2)">{safe(c.get('abordagem_recomendada'))}</p>
    </div>

    {('<div class="alert"><h5>Alerta de identidade</h5><p>' + safe(c.get('alerta_homonimo')) + '</p></div>') if c.get('alerta_homonimo') else ''}

    <div class="block">
      <span class="block-eyebrow">Fontes</span>
      <h3>De onde veio cada dado</h3>
      <ul class="sources">{fontes_li}</ul>
    </div>
  </div>
</section>

{FOOT}
"""
    out = HEAD.format(title=title, desc=desc) + body
    fname = f"{c['slug']}.html"
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"  ✓ {fname}")

if __name__ == "__main__":
    print("Gerando 9 HTMLs...")
    render_hub()
    for c in CIRURGIOES:
        render_individual(c)
    print(f"\n✅ Gerados em {OUT}")
