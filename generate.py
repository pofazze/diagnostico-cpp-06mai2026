#!/usr/bin/env python3
"""Gera 9 HTMLs (1 painel operacional + 8 apresentações premium Apple Clean × CPP)."""
import os, html
from data import (CIRURGIOES, iniciais, OFERTA, IG_ANALISE,
                  OFERTA_VALOR_TOTAL_MENSURAVEL, OFERTA_TOTAL_ELEMENTOS, OFERTA_INTANGIVEIS,
                  PRECO_PADRAO, PRECO_DESCONTO_PCT, PRECO_EXCLUSIVO)
from fbi_data import FBI, BG_IMAGES

OUT = os.path.dirname(os.path.abspath(__file__))

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
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
"""

FOOT_PUBLIC = """
<footer class="foot-min">
  <div class="wrap-narrow">
    <p>Cirurgião Particular Premium · com Patrick Suyti &amp; Dr. Mateus Jerônimo</p>
  </div>
</footer>
</body>
</html>
"""

FOOT_OPS = """
<footer class="foot-min">
  <div class="wrap"><p class="ops-foot">Painel operacional · Patrick Suyti + Dr. Mateus Jerônimo · 06 de Maio · 2026</p></div>
</footer>
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

def safe(s):
    if s is None: return ""
    return html.escape(str(s))

def safe_html(s):
    """Permite tags HTML mínimas (em, strong, br) — ideal pra textos curados."""
    if s is None: return ""
    return str(s)  # já controlamos input no data — texto cuidadosamente escrito

def li(items):
    return "\n".join(f"      <li>{safe(it)}</li>" for it in (items or []))

# ============================================================================
# OFERTA — 13 elementos + stack fechamento
# ============================================================================
def render_oferta_e_fechamento():
    cards = []
    for item in OFERTA:
        valor_class = "imensuravel" if item["imensuravel"] else "tangible"
        highlight_class = " highlight" if item.get("highlight") else ""
        cards.append(f"""
      <div class="of-card {valor_class}{highlight_class}">
        <div class="of-cat">{item['cat']}</div>
        <div class="of-nome">{safe(item['nome'])}</div>
        <div class="of-valor">{safe(item['valor'])}</div>
      </div>""")

    total_str = f"R$ {OFERTA_VALOR_TOTAL_MENSURAVEL:,}".replace(",", ".")
    padrao_str = f"R$ {PRECO_PADRAO:,}".replace(",", ".")
    exclusivo_str = f"R$ {PRECO_EXCLUSIVO:,}".replace(",", ".")
    economia_str = f"R$ {PRECO_PADRAO - PRECO_EXCLUSIVO:,}".replace(",", ".")

    return f"""
<section class="sec sec-oferta">
  <div class="wrap-narrow">
    <div class="sec-head sec-head-center">
      <span class="eyebrow">O programa</span>
      <h2 class="sec-h2">Cirurgião Particular Premium</h2>
      <p class="sec-lead">{OFERTA_TOTAL_ELEMENTOS} elementos. {OFERTA_TOTAL_ELEMENTOS - OFERTA_INTANGIVEIS} com preço de mercado declarado. {OFERTA_INTANGIVEIS} intangíveis que não cabem em planilha.</p>
    </div>

    <div class="of-grid">{''.join(cards)}
    </div>

    <div class="of-totals">
      <div class="of-total">
        <div class="of-total-label">Soma do que cabe em planilha</div>
        <div class="of-total-value">{total_str}</div>
      </div>
      <div class="of-total intangible">
        <div class="of-total-label">O que não cabe em valor</div>
        <div class="of-total-value gold">Imensurável</div>
      </div>
    </div>
  </div>
</section>

<section class="sec sec-fechamento">
  <div class="wrap-narrow">
    <div class="sec-head sec-head-center">
      <span class="eyebrow gold-eyebrow">Sua condição</span>
      <h2 class="sec-h2">Em reconhecimento à <em>decisão de hoje</em></h2>
      <p class="sec-lead">Você não chegou aqui por acaso. Pagou um sinal antes de ter qualquer garantia. Confiou primeiro.</p>
    </div>

    <div class="precos-stack">
      <div class="preco-step preco-anchor">
        <div class="preco-step-label">Valor entregue · soma do programa</div>
        <div class="preco-step-value strike">{total_str}</div>
      </div>
      <div class="preco-arrow">↓</div>
      <div class="preco-step preco-standard">
        <div class="preco-step-label">Investimento padrão da mentoria</div>
        <div class="preco-step-value strike">{padrao_str}</div>
      </div>
      <div class="preco-arrow gold">↓</div>
      <div class="preco-step preco-final">
        <div class="preco-final-badge">SUA CONDIÇÃO · −{PRECO_DESCONTO_PCT}%</div>
        <div class="preco-step-label">Investimento exclusivo</div>
        <div class="preco-step-value gold">{exclusivo_str}</div>
        <div class="preco-step-sub">Economia de {economia_str} · porque você confiou primeiro</div>
      </div>
    </div>

    <div class="cta-final">
      <p class="cta-final-eyebrow">A pergunta agora é simples</p>
      <h2 class="cta-final-h">Você está pronto para <em>o próximo capítulo</em>?</h2>
      <p class="cta-final-sub">06 de Maio · com Patrick Suyti &amp; Dr. Mateus Jerônimo</p>
    </div>
  </div>
</section>
"""

# ============================================================================
# HUB · PAINEL OPERACIONAL — para Patrick + Mateus
# ============================================================================
def render_hub():
    title = "Painel operacional · Diagnóstico CPP · 06 Maio 2026"
    desc = "Painel operacional dos 8 cirurgiões agendados — uso interno"

    perfis = {}
    confirmados = 0
    score_sum = 0
    score_n = 0
    for c in CIRURGIOES:
        p = perfil_class(c.get('perfil_cpp'))
        perfis[p] = perfis.get(p, 0) + 1
        if c.get('crm') and "[A CONFIRMAR" not in (c.get('crm') or ""):
            confirmados += 1
        if c.get('score_compra'):
            score_sum += c['score_compra']
            score_n += 1
    score_med = round(score_sum / score_n) if score_n else 0

    fila_cards = []
    for c in CIRURGIOES:
        slug = c['slug']
        pc = perfil_class(c.get('perfil_cpp'))
        pl = (c.get('perfil_cpp') or "A confirmar").split(' ')[0]
        score_str = f'<span class="op-score">{c["score_compra"]}</span>' if c.get('score_compra') else '<span class="op-score muted">—</span>'

        ig = IG_ANALISE.get(slug, {})
        fbi = FBI.get(slug, {})
        bg = BG_IMAGES.get(slug, "")

        verificado_badge = '<span class="op-verified" title="Selo azul">✓</span>' if ig.get('verificado') else ''

        # avatar IG
        avatar_head = f'<img src="{safe(ig.get("foto", ""))}" alt="" class="op-head-avatar" loading="lazy" onerror="this.style.display=\'none\'">' if ig.get("foto") else ''

        # bloco IG profundo (analise estendida)
        ig_block = ""
        if ig:
            conteudo_li = "\n".join(f'<li>{safe(x)}</li>' for x in ig.get('conteudo', []))
            gaps_li = "\n".join(f'<li>{safe(g)}</li>' for g in ig.get('gaps_ig', []))
            score_visual = ig.get('score_visual', 0)
            score_class = "high" if score_visual >= 70 else ("mid" if score_visual >= 40 else "low")
            verif_text = '<span class="ig-verified">✓ Verificado</span>' if ig.get('verificado') else '<span class="ig-not-verified">sem verificação</span>'

            ig_block = f"""
      <div class="op-block op-block-wide ig-deep">
        <div class="ig-deep-head">
          <img src="{safe(ig.get('foto'))}" alt="" class="ig-avatar" loading="lazy" onerror="this.style.display='none'">
          <div class="ig-deep-meta">
            <h5>Análise profunda do Instagram</h5>
            <div class="ig-handle-row">
              <a href="{safe(ig.get('url'))}" target="_blank" rel="noopener" class="ig-handle-link">{safe(ig.get('handle'))}</a>
              {verif_text}
            </div>
            <div class="ig-stats">
              <span><strong>{safe(ig.get('seguidores'))}</strong> seguidores</span>
              <span class="dot"></span>
              <span><strong>{safe(ig.get('posts'))}</strong> posts</span>
              {('<span class="dot"></span><span><strong>' + safe(ig.get('seguindo')) + '</strong> seguindo</span>') if ig.get('seguindo') and ig.get('seguindo') != "—" else ''}
            </div>
            <div class="ig-score-bar">
              <div class="ig-score-label">Marca digital</div>
              <div class="ig-score-track"><div class="ig-score-fill {score_class}" style="width: {score_visual}%"></div></div>
              <div class="ig-score-num">{score_visual}<span class="muted">/100</span></div>
            </div>
          </div>
        </div>
        <div class="ig-deep-body">
          <div class="ig-deep-row"><div class="ig-k">Bio literal</div><div class="ig-v ig-quote">{safe(ig.get('bio_literal'))}</div></div>
          <div class="ig-deep-row"><div class="ig-k">Tom</div><div class="ig-v">{safe(ig.get('tom'))}</div></div>
          <div class="ig-deep-row"><div class="ig-k">Conteúdo</div><div class="ig-v"><ul class="ig-list">{conteudo_li}</ul></div></div>
          <div class="ig-deep-row"><div class="ig-k">Branding</div><div class="ig-v">{safe(ig.get('branding'))}</div></div>
          <div class="ig-deep-row"><div class="ig-k">Diagnóstico</div><div class="ig-v ig-diag">{safe(ig.get('diagnostico'))}</div></div>
          <div class="ig-deep-row"><div class="ig-k">Gaps cirúrgicos</div><div class="ig-v"><ul class="ig-gaps">{gaps_li}</ul></div></div>
        </div>
      </div>"""

        # FBI — pontos internos cirúrgicos
        fbi_internos = ""
        if fbi.get('pontos_internos'):
            internos_li = "\n".join(f"<li>{safe(p)}</li>" for p in fbi['pontos_internos'])
            fbi_internos = f"""
      <div class="op-block op-block-wide fbi-internal">
        <h5>Inteligência interna · só Patrick + Mateus</h5>
        <ul class="op-bul">{internos_li}</ul>
      </div>"""

        # dores rápidas
        dores_short = []
        for dor, _ in (c.get('dores_top3') or [])[:3]:
            dores_short.append(f'<li>{safe(dor)}</li>')

        # gaps
        gaps_html = ''.join(f'<li><strong>{safe(area)}</strong> — {safe(desc)}</li>' for area, desc in (c.get('gaps') or []))

        # hooks
        hooks_html = ''.join(f'<p class="op-hook"><span class="hook-num">HOOK {i}</span>"{safe(h)}"</p>' for i, h in enumerate(c.get('hooks_abertura') or [], 1))

        # objeções
        objecoes_li = ''.join(f"<li>{safe(o)}</li>" for o in (c.get('objecoes_esperadas') or []))

        fila_cards.append(f"""
    <article class="op-card" id="op-{slug}">
      <header class="op-card-head">
        <div class="op-time">{c['hora']}</div>
        {avatar_head}
        <div class="op-id">
          <h3>{safe(c['nome'])} {verificado_badge}</h3>
          <div class="op-meta">
            <span class="op-perfil {pc}">{safe(pl)}</span>
            {score_str}
            <span class="op-spec">{safe(c['especialidade'])}{(' · ' + safe(c['subespecialidade'])) if c.get('subespecialidade') else ''}</span>
            <span class="op-loc">{safe(c['cidade'])}/{safe(c['estado'])}</span>
          </div>
        </div>
        <a href="{slug}.html" class="op-link-mapa" target="_blank">↗ apresentação</a>
      </header>

      {ig_block}

      {fbi_internos}

      <div class="op-grid">
        <div class="op-block">
          <h5>Identidade essencial</h5>
          <div class="op-kv">
            <div class="k">CRM</div><div class="v">{safe(c.get('crm') or '—')}</div>
            <div class="k">Site</div><div class="v">{(f'<a href="{c["site"]}" target="_blank" rel="noopener" class="op-link">' + safe(c["site"]) + '</a>') if c.get("site") else '<span class="muted">sem site</span>'}</div>
            <div class="k">Tagline</div><div class="v small">{safe(c.get('tagline_atual') or '—')}</div>
            <div class="k">Zoom</div><div class="v"><a href="{c['zoom']}" target="_blank" rel="noopener" class="op-link">link da call</a></div>
          </div>
        </div>

        <div class="op-block">
          <h5>Posicionamento atual</h5>
          <p class="op-p">{safe(c.get('posicionamento_atual_publico') or '—')}</p>
        </div>

        <div class="op-block">
          <h5>Top 3 dores</h5>
          <ol class="op-num">{''.join(dores_short)}</ol>
        </div>

        <div class="op-block">
          <h5>Top 3 gaps</h5>
          <ul class="op-bul">{gaps_html}</ul>
        </div>

        <div class="op-block op-block-wide">
          <h5>Hooks de abertura · primeiros 60s</h5>
          {hooks_html}
        </div>

        <div class="op-block">
          <h5>Objeções esperadas</h5>
          <ul class="op-bul">{objecoes_li}</ul>
        </div>

        <div class="op-block">
          <h5>Abordagem recomendada</h5>
          <p class="op-p">{safe(c.get('abordagem_recomendada') or '—')}</p>
        </div>

        {('<div class="op-block op-block-wide alerta-callout"><h5>Alerta de identidade</h5><p>' + safe(c.get('alerta_homonimo')) + '</p></div>') if c.get('alerta_homonimo') else ''}
      </div>
    </article>""")

    composicao_pieces = []
    for k, label in [('aguia', 'Águias'), ('gaviao', 'Gaviões'), ('urubu', 'Urubus'), ('pato', 'Patos'), ('incerto', 'A confirmar')]:
        n = perfis.get(k, 0)
        if n: composicao_pieces.append(f'<span class="tag {("gold" if k=="aguia" else "")}">{n} {label}</span>')

    # quick nav
    quick_nav = []
    for c in CIRURGIOES:
        pc = perfil_class(c.get('perfil_cpp'))
        nome_curto = c['nome'].replace("Dr. ", "").replace("Dra. ", "").replace("(Fellype) ", "").split(' ')[0]
        sobrenome = c['nome'].replace("(Fellype) ", "").split(' ')[-1]
        quick_nav.append(f'<a href="#op-{c["slug"]}" class="quick-nav-link"><span class="qn-time">{c["hora"]}</span><span class="qn-dot {pc}"></span><span class="qn-name">{safe(nome_curto)} {safe(sobrenome)}</span></a>')

    body = f"""
<header class="topbar">
  <div class="topbar-inner">
    <a href="index.html" class="brand">
      <span class="brand-mark">CPP</span>
      <span class="brand-text">Cirurgião Particular Premium · <span class="accent">Painel</span></span>
    </a>
    <span class="ops-badge">Patrick + Mateus</span>
  </div>
</header>

<section class="hero hero-ops">
  <div class="wrap-narrow">
    <span class="hero-eyebrow gold-eyebrow">Painel operacional · uso interno</span>
    <h1 class="hero-title">Diagnóstico CPP · <span class="gold">06 de Maio</span></h1>
    <p class="hero-sub">8 cirurgiões. 8 perfis. Tudo o que você precisa saber antes de cada call — em uma única página.</p>
  </div>
</section>

<section class="sec sec-stats">
  <div class="wrap">
    <div class="stats-grid">
      <div class="stat">
        <div class="stat-label">Cirurgiões</div>
        <div class="stat-value">8</div>
        <div class="stat-sub">um a cada hora · 11h-18h</div>
      </div>
      <div class="stat">
        <div class="stat-label">Identidade confirmada</div>
        <div class="stat-value">{confirmados}<span class="stat-frac">/8</span></div>
        <div class="stat-sub">prints + base + cruzamento + FBI</div>
      </div>
      <div class="stat">
        <div class="stat-label">Score médio</div>
        <div class="stat-value">{score_med}<span class="stat-frac">/100</span></div>
        <div class="stat-sub">{score_n} dos 8 dossiados</div>
      </div>
      <div class="stat">
        <div class="stat-label">Composição</div>
        <div class="tags" style="margin-top: 6px;">{' '.join(composicao_pieces)}</div>
      </div>
    </div>
  </div>
</section>

<section class="sec sec-quicknav">
  <div class="wrap">
    <div class="quick-nav">{''.join(quick_nav)}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">A fila do dia</span>
      <h2 class="sec-h2">Os 8 cirurgiões · ordem cronológica</h2>
    </div>
    {''.join(fila_cards)}
  </div>
</section>

{FOOT_OPS}
"""
    out = HEAD.format(title=title, desc=desc) + body
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"  ✓ index.html (painel operacional)")


# ============================================================================
# INDIVIDUAL · APRESENTAÇÃO PREMIUM PARA O MÉDICO
# ============================================================================
def render_individual(c):
    slug = c['slug']
    title = f"{c['nome']} · Diagnóstico CPP · 06/05"
    desc = f"Mapa diagnóstico individual · {c['nome']} · Cirurgião Particular Premium · 06 de Maio 2026"

    fbi = FBI.get(slug, {})
    ig = IG_ANALISE.get(slug, {})
    bg = BG_IMAGES.get(slug, "")

    bg_style = f'style="--hero-bg: url(\'{bg}\');"' if bg else ''

    # ============= HERO CINEMATOGRÁFICO =============
    quote_manifesto = fbi.get('quote_manifesto', '')

    # ============= NARRATIVA + DESCOBERTAS =============
    narrativa_html = fbi.get('narrativa_publica', c.get('posicionamento_atual_publico', ''))

    descobertas_html = ""
    if fbi.get('descobertas_publicas'):
        items = "".join(f'<li>{d}</li>' for d in fbi['descobertas_publicas'])
        descobertas_html = f"""
<section class="sec sec-descobertas">
  <div class="wrap-narrow">
    <div class="sec-head">
      <span class="eyebrow">O que pesquisamos sobre você</span>
      <h2 class="sec-h2">A trajetória, ponto a ponto</h2>
      <p class="sec-lead">Antes de qualquer pergunta, queríamos chegar com lição de casa feita. Aqui está o que encontramos.</p>
    </div>
    <ul class="descoberta-list">{items}</ul>
  </div>
</section>"""

    # ============= LEITURA DO INSTAGRAM (público) =============
    ig_public_html = ""
    if ig and ig.get('foto'):
        verif_html = '<span class="ig-pub-verified">✓ Verificado</span>' if ig.get('verificado') else ''
        sub_stats = []
        if ig.get('seguidores') and ig.get('seguidores') != "—":
            sub_stats.append(f'<div class="ig-pub-stat"><div class="num">{safe(ig["seguidores"])}</div><div class="label">seguidores</div></div>')
        if ig.get('posts') and ig.get('posts') != "—":
            sub_stats.append(f'<div class="ig-pub-stat"><div class="num">{safe(ig["posts"])}</div><div class="label">posts</div></div>')
        if ig.get('seguindo') and ig.get('seguindo') != "—":
            sub_stats.append(f'<div class="ig-pub-stat"><div class="num">{safe(ig["seguindo"])}</div><div class="label">seguindo</div></div>')

        ig_public_html = f"""
<section class="sec sec-ig-public">
  <div class="wrap-narrow">
    <div class="sec-head">
      <span class="eyebrow">Leitura da sua presença digital</span>
      <h2 class="sec-h2">O que o seu <em>Instagram</em> conta hoje</h2>
    </div>

    <div class="ig-pub-card">
      <div class="ig-pub-head">
        <img src="{safe(ig.get('foto'))}" alt="" class="ig-pub-avatar" loading="lazy" onerror="this.style.display='none'">
        <div class="ig-pub-info">
          <div class="ig-pub-handle-row">
            <span class="ig-pub-handle">{safe(ig.get('handle'))}</span>
            {verif_html}
          </div>
          <div class="ig-pub-bio">{safe(ig.get('bio_literal'))}</div>
        </div>
      </div>

      {('<div class="ig-pub-stats">' + ''.join(sub_stats) + '</div>') if sub_stats else ''}

      <div class="ig-pub-readout">
        <div class="ig-pub-row">
          <h5>Tom de comunicação</h5>
          <p>{safe(ig.get('tom'))}</p>
        </div>
        <div class="ig-pub-row">
          <h5>Linha editorial</h5>
          <p>{safe(ig.get('branding'))}</p>
        </div>
        <div class="ig-pub-row ig-pub-row-diag">
          <h5>O que isso significa</h5>
          <p>{safe(ig.get('diagnostico'))}</p>
        </div>
      </div>
    </div>
  </div>
</section>"""

    # ============= PRÉ-DIAGNÓSTICO =============
    pre_diag = c.get('pre_diagnostico') or {}
    pre_diag_html = ""
    if pre_diag:
        pontos_html = "\n".join(f'<li>{safe(p)}</li>' for p in pre_diag.get('pontos', []))
        pre_diag_html = f"""
<section class="sec sec-prediag">
  <div class="wrap-narrow">
    <div class="sec-head">
      <span class="eyebrow">Pré-diagnóstico</span>
      <h2 class="sec-h2">O retrato em uma frase</h2>
    </div>

    <blockquote class="pre-diag-frase">
      <p>{safe(pre_diag.get('frase_central'))}</p>
    </blockquote>

    <div class="pre-diag-pontos">
      <h4 class="pre-diag-titulo">Os pontos que se conectam</h4>
      <ol>{pontos_html}</ol>
    </div>

    <div class="pre-diag-no">
      <span class="pre-diag-no-label">O nó central</span>
      <p>{safe(pre_diag.get('no_central'))}</p>
    </div>
  </div>
</section>"""

    # ============= PLANO DE AÇÃO =============
    plano = c.get('plano_acao') or []
    plano_html = ""
    if plano:
        fases_html = ""
        for i, f in enumerate(plano, 1):
            acoes_li = "\n".join(f'<li>{safe(a)}</li>' for a in f.get('acoes', []))
            fases_html += f"""
      <article class="fase-card">
        <div class="fase-num">0{i}</div>
        <div class="fase-body">
          <div class="fase-prazo">{safe(f.get('fase'))}</div>
          <h3 class="fase-titulo">{safe(f.get('titulo'))}</h3>
          <ul class="fase-acoes">{acoes_li}</ul>
        </div>
      </article>"""

        plano_html = f"""
<section class="sec sec-plano">
  <div class="wrap-narrow">
    <div class="sec-head">
      <span class="eyebrow">Plano de ação</span>
      <h2 class="sec-h2">O que você faria <em>como Cirurgião Particular Premium</em></h2>
      <p class="sec-lead">Três fases. Três decisões. Cada uma constrói sobre a anterior.</p>
    </div>

    <div class="fases-grid">{fases_html}
    </div>
  </div>
</section>"""

    # ============= PITCH DIRECIONADO =============
    pitch_html = ""
    if fbi.get('pitch_direcionado'):
        etapas_html = ""
        for i, (titulo, desc_etapa) in enumerate(fbi['pitch_direcionado'], 1):
            etapas_html += f"""
      <article class="pitch-step">
        <div class="pitch-num">{i:02d}</div>
        <div class="pitch-body">
          <h3 class="pitch-titulo">{safe(titulo)}</h3>
          <p class="pitch-desc">{desc_etapa}</p>
        </div>
      </article>"""

        pitch_html = f"""
<section class="sec sec-pitch">
  <div class="wrap-narrow">
    <div class="sec-head">
      <span class="eyebrow">Estrutura do pitch</span>
      <h2 class="sec-h2">Como o programa <em>vai mudar a sua próxima fase</em></h2>
      <p class="sec-lead">Não é teoria. É o caminho específico que faz sentido para o ponto onde você está.</p>
    </div>
    <div class="pitch-stack">{etapas_html}
    </div>
  </div>
</section>"""

    # ============= OFERTA + FECHAMENTO =============
    oferta_section = render_oferta_e_fechamento()

    # ============= MONTAGEM =============
    body = f"""
<header class="topbar topbar-public">
  <div class="topbar-inner">
    <span class="brand">
      <span class="brand-mark">CPP</span>
      <span class="brand-text">Cirurgião Particular Premium</span>
    </span>
    <span class="hora-tag">{c['hora']} · 06 de Maio</span>
  </div>
</header>

<section class="hero-cinema" {bg_style}>
  <div class="hero-cinema-overlay"></div>
  <div class="hero-cinema-content">
    <div class="wrap-narrow">
      <span class="hero-eyebrow gold-eyebrow">Mapa Diagnóstico Premium · {c['hora']}</span>
      <h1 class="hero-name">{safe(c['nome'])}</h1>
      <p class="hero-spec">{safe(c['especialidade'])}{(' · ' + safe(c['subespecialidade'])) if c.get('subespecialidade') else ''}</p>
      <p class="hero-local">{safe(c['cidade'])} · {safe(c['estado'])}{(' · ' + safe(c['crm'])) if c.get('crm') and '[A CONFIRMAR' not in (c.get('crm') or '') else ''}</p>

      {('<blockquote class="hero-quote"><p>' + safe(quote_manifesto) + '</p></blockquote>') if quote_manifesto else ''}

      <div class="hero-conduzido">
        <span class="hero-conduzido-label">conduzido por</span>
        <strong>Patrick Suyti</strong> &amp; <strong>Dr. Mateus Jerônimo</strong>
      </div>
    </div>
  </div>
</section>

<section class="sec sec-narrativa">
  <div class="wrap-narrow">
    <div class="sec-head">
      <span class="eyebrow">Quem você é</span>
      <h2 class="sec-h2">Em uma única página</h2>
    </div>
    <p class="narrativa-text">{narrativa_html}</p>
  </div>
</section>

{descobertas_html}

{ig_public_html}

{pre_diag_html}

{plano_html}

{pitch_html}

{oferta_section}

{FOOT_PUBLIC}
"""
    out = HEAD.format(title=title, desc=desc) + body
    fname = f"{slug}.html"
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"  ✓ {fname}")


if __name__ == "__main__":
    print("Gerando 9 HTMLs (Apple Clean × CPP Premium)...")
    render_hub()
    for c in CIRURGIOES:
        render_individual(c)
    print(f"\n✅ Gerados em {OUT}")
