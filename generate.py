#!/usr/bin/env python3
"""Gera 9 HTMLs (1 hub painel pra Patrick+Mateus + 8 apresentações pros médicos)."""
import os, html, re
from data import (CIRURGIOES, iniciais, OFERTA, IG_ANALISE,
                  OFERTA_VALOR_TOTAL_MENSURAVEL, OFERTA_TOTAL_ELEMENTOS, OFERTA_INTANGIVEIS,
                  PRECO_PADRAO, PRECO_DESCONTO_PCT, PRECO_EXCLUSIVO)

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
      <span class="brand-text">Cirurgião Particular Premium · <span class="accent">{label}</span></span>
    </a>
    {nav}
  </div>
</header>
"""

FOOT_PUBLIC = """
<footer class="foot">
  <div class="wrap">
    <p class="small">Cirurgião Particular Premium · Diagnóstico individual com Patrick Suyti + Dr. Mateus Jerônimo</p>
    <p class="gold" style="margin-top:8px">06 de Maio · 2026</p>
  </div>
</footer>
</body>
</html>
"""

FOOT_OPS = """
<footer class="foot">
  <div class="wrap">
    <p class="small">Painel operacional · Patrick Suyti + Dr. Mateus Jerônimo</p>
    <p class="gold" style="margin-top:8px">Diagnóstico CPP · 06 de Maio · 2026</p>
  </div>
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

# ============================================================================
# MAPA DA OFERTA — usado nas individuais como pitch ancorado
# ============================================================================
def render_oferta_mapa():
    cards = []
    for i, item in enumerate(OFERTA, 1):
        valor_class = "imensuravel" if item["imensuravel"] else "tangible"
        highlight_class = " highlight" if item.get("highlight") else ""
        cards.append(f"""
      <div class="oferta-card {valor_class}{highlight_class}">
        <div class="oferta-icon">{item['icon']}</div>
        <div class="oferta-cat">{item['cat']}</div>
        <div class="oferta-nome">{safe(item['nome'])}</div>
        <div class="oferta-valor">{safe(item['valor'])}</div>
      </div>""")

    total_str = f"R$ {OFERTA_VALOR_TOTAL_MENSURAVEL:,}".replace(",",".")
    padrao_str = f"R$ {PRECO_PADRAO:,}".replace(",",".")
    exclusivo_str = f"R$ {PRECO_EXCLUSIVO:,}".replace(",",".")
    economia_str = f"R$ {PRECO_PADRAO - PRECO_EXCLUSIVO:,}".replace(",",".")

    return f"""
<section class="oferta-section">
  <div class="wrap-narrow">
    <div class="section-head" style="text-align: center; margin-bottom: 56px;">
      <span class="eyebrow">O que está dentro</span>
      <h2>O programa <em class="gold-accent">Cirurgião Particular Premium</em></h2>
      <p style="font-family: var(--serif); font-style: italic; font-size: 1.2rem; color: var(--text-2); margin-top: 16px; max-width: 60ch; margin-left: auto; margin-right: auto;">{OFERTA_TOTAL_ELEMENTOS} elementos. {OFERTA_TOTAL_ELEMENTOS - OFERTA_INTANGIVEIS} com preço de mercado declarado. {OFERTA_INTANGIVEIS} intangíveis que não cabem em planilha.</p>
    </div>

    <div class="oferta-grid">{''.join(cards)}
    </div>

    <div class="oferta-totals">
      <div class="oferta-total">
        <div class="oferta-total-label">Soma do que cabe em planilha</div>
        <div class="oferta-total-value">{total_str}</div>
        <div class="oferta-total-sub">{OFERTA_TOTAL_ELEMENTOS - OFERTA_INTANGIVEIS} elementos com preço declarado</div>
      </div>
      <div class="oferta-total intangible">
        <div class="oferta-total-label">O que não cabe em valor</div>
        <div class="oferta-total-value gold">Imensurável</div>
        <div class="oferta-total-sub">{OFERTA_INTANGIVEIS} elementos · marca, comunidade, ritual, elite</div>
      </div>
    </div>
  </div>
</section>

<section class="fechamento-section">
  <div class="wrap-narrow">
    <div class="section-head" style="text-align: center; margin-bottom: 60px;">
      <span class="eyebrow gold">Sua condição</span>
      <h2 style="margin-top: 14px;">Em reconhecimento à <em class="gold-accent">decisão de hoje</em></h2>
      <p style="font-family: var(--serif); font-style: italic; font-size: 1.15rem; color: var(--text-2); margin-top: 16px; max-width: 56ch; margin-left: auto; margin-right: auto;">Você não chegou aqui por acaso. Pagou um sinal antes de ter qualquer garantia. Confiou primeiro.</p>
    </div>

    <div class="precos-stack">
      <!-- Etapa 1: ancoragem -->
      <div class="preco-step preco-anchor">
        <div class="preco-step-label">Valor entregue · soma do programa</div>
        <div class="preco-step-value strike">{total_str}</div>
        <div class="preco-step-sub">{OFERTA_TOTAL_ELEMENTOS} elementos · {OFERTA_INTANGIVEIS} intangíveis</div>
      </div>

      <div class="preco-arrow">↓</div>

      <!-- Etapa 2: padrão -->
      <div class="preco-step preco-standard">
        <div class="preco-step-label">Investimento padrão da mentoria</div>
        <div class="preco-step-value strike">{padrao_str}</div>
        <div class="preco-step-sub">acesso pleno · 6 meses de acompanhamento</div>
      </div>

      <div class="preco-arrow gold">↓</div>

      <!-- Etapa 3: sua condição -->
      <div class="preco-step preco-final">
        <div class="preco-final-badge">SUA CONDIÇÃO · −{PRECO_DESCONTO_PCT}%</div>
        <div class="preco-step-label" style="color: var(--gold-bright);">Investimento exclusivo</div>
        <div class="preco-step-value gold">{exclusivo_str}</div>
        <div class="preco-step-sub">economia de {economia_str} · porque você confiou primeiro</div>
      </div>
    </div>

    <div class="cta-final">
      <p class="cta-final-eyebrow">A pergunta agora é simples</p>
      <h2 class="cta-final-h">Você está pronto para <em class="gold-accent">o próximo capítulo</em>?</h2>
      <p class="cta-final-sub">06 de Maio · com Patrick Suyti &amp; Dr. Mateus Jerônimo</p>
    </div>
  </div>
</section>"""

# ============================================================================
# HUB · PAINEL DETALHADO PRA PATRICK + MATEUS
# ============================================================================
def render_hub():
    title = "Painel operacional · Diagnóstico CPP · 06 Maio 2026"
    desc = "Painel detalhado dos 8 cirurgiões agendados para diagnóstico CPP em 06/05/2026 — uso interno Patrick Suyti + Dr. Mateus Jerônimo"

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

    # cards-fila
    fila_cards = []
    for c in CIRURGIOES:
        pc = perfil_class(c.get('perfil_cpp'))
        pl = perfil_label(c.get('perfil_cpp')).split(' ')[0]
        score_str = f'<span class="op-score">{c["score_compra"]}</span>' if c.get('score_compra') else '<span class="op-score muted">—</span>'

        ig = IG_ANALISE.get(c['slug'], {})
        verificado_badge = '<span class="op-verified" title="Selo azul de verificação">✓</span>' if ig.get('verificado') else ''

        # dores rápidas
        dores_short = []
        for dor, _ in (c.get('dores_top3') or [])[:3]:
            dores_short.append(f'<li>{safe(dor)}</li>')

        # hook 1
        hook = (c.get('hooks_abertura') or [None])[0] or ""

        ig_line = ""
        if c.get('instagram'):
            ig_line = f'<a href="{c["instagram_url"]}" target="_blank" rel="noopener" class="op-link">{safe(c["instagram"])}</a>'
            if c.get('instagram_seguidores'):
                ig_line += f' <span class="muted">· {safe(c["instagram_seguidores"])} seg · {safe(c["instagram_posts"] or "")} posts</span>'
        else:
            ig_line = '<span class="muted">sem IG pessoal</span>'

        site_line = f'<a href="{c["site"]}" target="_blank" rel="noopener" class="op-link">{safe(c["site"])}</a>' if c.get("site") else '<span class="muted">sem site</span>'

        alerta_html = f'<div class="op-alerta">⚠️ {safe(c.get("alerta_homonimo"))}</div>' if c.get("alerta_homonimo") and "97%" not in (c.get("alerta_homonimo") or "") and "100%" not in (c.get("alerta_homonimo") or "") and "95%" not in (c.get("alerta_homonimo") or "") and "90%" not in (c.get("alerta_homonimo") or "") else ""

        correcao_html = f'<div class="op-correcao">🔁 {safe(c["correcao_grafia"])}</div>' if c.get("correcao_grafia") else ""

        # ============== ANÁLISE PROFUNDA DO INSTAGRAM ==============
        ig_block_html = ""
        if ig:
            conteudo_li = "\n".join(f'<li>{safe(x)}</li>' for x in ig.get('conteudo',[]))
            gaps_li = "\n".join(f'<li>{safe(g)}</li>' for g in ig.get('gaps_ig',[]))
            score_visual = ig.get('score_visual', 0)
            score_class = "high" if score_visual >= 70 else ("mid" if score_visual >= 40 else "low")
            verif_text = '<span class="ig-verified">✓ Verificado</span>' if ig.get('verificado') else '<span class="ig-not-verified">sem verificação</span>'

            ig_block_html = f"""
      <div class="op-block op-block-wide ig-deep">
        <div class="ig-deep-head">
          <img src="{safe(ig.get('foto'))}" alt="{safe(ig.get('handle'))}" class="ig-avatar" loading="lazy" onerror="this.style.display='none'">
          <div class="ig-deep-meta">
            <h5 style="margin-bottom: 4px;">📱 Análise profunda do Instagram</h5>
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
          <div class="ig-deep-row">
            <div class="ig-k">Bio literal</div>
            <div class="ig-v ig-quote">{safe(ig.get('bio_literal'))}</div>
          </div>
          <div class="ig-deep-row">
            <div class="ig-k">Tom</div>
            <div class="ig-v">{safe(ig.get('tom'))}</div>
          </div>
          <div class="ig-deep-row">
            <div class="ig-k">Conteúdo</div>
            <div class="ig-v"><ul class="ig-list">{conteudo_li}</ul></div>
          </div>
          <div class="ig-deep-row">
            <div class="ig-k">Branding</div>
            <div class="ig-v">{safe(ig.get('branding'))}</div>
          </div>
          <div class="ig-deep-row">
            <div class="ig-k">Diagnóstico</div>
            <div class="ig-v ig-diag">{safe(ig.get('diagnostico'))}</div>
          </div>
          <div class="ig-deep-row">
            <div class="ig-k">Gaps cirúrgicos</div>
            <div class="ig-v"><ul class="ig-gaps">{gaps_li}</ul></div>
          </div>
        </div>
      </div>"""

        avatar_head = f'<img src="{safe(ig.get("foto"))}" alt="" class="op-head-avatar" loading="lazy" onerror="this.style.display=\'none\'">' if ig.get("foto") else ''

        fila_cards.append(f"""
    <article class="op-card" id="op-{c['slug']}">
      <header class="op-card-head">
        <div class="op-time">{c['hora']}</div>
        {avatar_head}
        <div class="op-id">
          <h3>{safe(c['nome'])} {verificado_badge}</h3>
          <div class="op-meta">
            <span class="op-perfil {pc}">{safe(pl)}</span>
            {score_str}
            <span class="op-spec">{safe(c['especialidade'])}{(' · ' + safe(c['subespecialidade'])) if c.get('subespecialidade') else ''}</span>
            <span class="op-loc">📍 {safe(c['cidade'])}/{safe(c['estado'])}</span>
          </div>
        </div>
        <a href="{c['slug']}.html" class="op-link-mapa" target="_blank" title="abrir página de apresentação">↗ apresentação</a>
      </header>

      {correcao_html}
      {alerta_html}

      {ig_block_html}

      <div class="op-grid">
        <div class="op-block">
          <h5>📋 Identidade</h5>
          <div class="op-kv">
            <div class="k">CRM</div><div class="v">{safe(c.get('crm') or '—')}</div>
            <div class="k">Site</div><div class="v">{site_line}</div>
            <div class="k">Tagline</div><div class="v small">{safe(c.get('tagline_atual') or '—')}</div>
            <div class="k">Zoom</div><div class="v"><a href="{c['zoom']}" target="_blank" rel="noopener" class="op-link">link da call</a></div>
          </div>
        </div>

        <div class="op-block">
          <h5>🎯 Posicionamento atual</h5>
          <p class="op-p">{safe(c.get('posicionamento_atual_publico') or '—')}</p>
        </div>

        <div class="op-block">
          <h5>💢 Top 3 dores</h5>
          <ol class="op-num">{''.join(dores_short)}</ol>
        </div>

        <div class="op-block">
          <h5>🔧 Top 3 gaps</h5>
          <ul class="op-bul">{''.join(f'<li><strong>{safe(area)}</strong> — {safe(desc)}</li>' for area, desc in (c.get('gaps') or []))}</ul>
        </div>

        <div class="op-block op-block-wide">
          <h5>🎤 Hooks de abertura · primeiros 60s</h5>
          {''.join(f'<p class="op-hook"><span class="hook-num">HOOK {i}</span>"{safe(h)}"</p>' for i, h in enumerate(c.get('hooks_abertura') or [], 1))}
        </div>

        <div class="op-block">
          <h5>🛡️ Objeções esperadas</h5>
          <ul class="op-bul">{''.join(f'<li>{safe(o)}</li>' for o in (c.get('objecoes_esperadas') or []))}</ul>
        </div>

        <div class="op-block">
          <h5>🧭 Abordagem recomendada</h5>
          <p class="op-p">{safe(c.get('abordagem_recomendada') or '—')}</p>
        </div>
      </div>
    </article>""")

    # composição visual
    composicao_pieces = []
    for k, label in [('aguia','Águias'),('gaviao','Gaviões'),('urubu','Urubus'),('pato','Patos'),('incerto','A confirmar')]:
        n = perfis.get(k, 0)
        if n: composicao_pieces.append(f'<span class="tag {("gold" if k=="aguia" else "")}">{n} {label}</span>')

    composicao_html = " ".join(composicao_pieces)

    # quick nav
    quick_nav = []
    for c in CIRURGIOES:
        pc = perfil_class(c.get('perfil_cpp'))
        quick_nav.append(f'<a href="#op-{c["slug"]}" class="quick-nav-link"><span class="qn-time">{c["hora"]}</span><span class="qn-dot {pc}"></span><span class="qn-name">{safe(c["nome"].replace("Dr. ","").replace("Dra. ","").split(" ")[0])} {safe(c["nome"].split(" ")[-1])}</span></a>')

    body = f"""
{TOPBAR.format(label='Painel operacional', nav='<span class="ops-badge">🔒 Patrick + Mateus</span>')}

<section class="hero" style="padding: 80px 0 50px;">
  <div class="wrap-narrow">
    <span class="hero-eyebrow" style="background: rgba(212,175,55,0.06); border-color: var(--gold-dark); color: var(--gold-bright);">Painel operacional · uso interno</span>
    <h1 class="hero-title" style="margin-bottom: 18px;">Diagnóstico CPP · <span class="gold">06 de Maio</span></h1>
    <p class="hero-sub">8 cirurgiões. 8 perfis. Tudo o que você precisa saber antes de cada call — em uma única página.</p>
    <div style="margin-top: 24px; color: var(--text-3); font-family: var(--serif); font-size: 1rem;">
      <strong style="color: var(--gold-soft)">Patrick Suyti</strong> &amp; <strong style="color: var(--gold-soft)">Dr. Mateus Jerônimo</strong>
    </div>
  </div>
</section>

<section style="padding: 30px 0 50px;">
  <div class="wrap">
    <div class="stats-grid">
      <div class="stat">
        <div class="stat-label">Cirurgiões</div>
        <div class="stat-value">8</div>
        <div class="stat-sub">um a cada hora · 11h-18h</div>
      </div>
      <div class="stat">
        <div class="stat-label">Identidade confirmada</div>
        <div class="stat-value">{confirmados}<span style="color: var(--text-4); font-size: 1.4rem">/8</span></div>
        <div class="stat-sub">prints + base + cruzamento</div>
      </div>
      <div class="stat">
        <div class="stat-label">Score médio</div>
        <div class="stat-value">{score_med}<span style="color: var(--text-4); font-size: 1.4rem">/100</span></div>
        <div class="stat-sub">{score_n} dos 8 já dossiados na base</div>
      </div>
      <div class="stat">
        <div class="stat-label">Composição</div>
        <div class="tags" style="margin-top: 6px;">{composicao_html}</div>
      </div>
    </div>
  </div>
</section>

<section style="padding: 0 0 40px; border-top: 0;">
  <div class="wrap">
    <div class="quick-nav">{''.join(quick_nav)}</div>
  </div>
</section>

<section style="padding: 30px 0 80px; border-top: 1px solid var(--border);">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">A fila do dia</span>
      <h2>Os 8 cirurgiões · em ordem cronológica</h2>
    </div>
    {''.join(fila_cards)}
  </div>
</section>

<section style="padding: 60px 0; border-top: 1px solid var(--border); background: rgba(212,175,55,0.02);">
  <div class="wrap-narrow">
    <div class="section-head">
      <span class="eyebrow">Estratégia do dia</span>
      <h2>Como calibrar tom por perfil</h2>
    </div>

    <div class="block">
      <span class="block-eyebrow">Pitches premium imediatos · 4 cirurgiões</span>
      <h3>Águias e quasi-Águias — peer-to-peer, NUNCA "aprenda do zero"</h3>
      <ul class="bullets">
        <li><strong>Rafael Bozzo Tacino</strong> · 12h · Águia · score 84 — Sloan-Kettering, 100% particular, R$400 underprice. Tom: "você venceu fase 1, está na fase 2"</li>
        <li><strong>Tarik Soares Suleiman</strong> · 14h · Águia digital · score 78 · 31,6k seguidores · verificado · Mateus já segue. Posicionamento "vesícula" cravado</li>
        <li><strong>Marina Marangon Melhado</strong> · 16h · Águia · score 84 · CNN+selo azul mas 100 seguidores. Dor: "casa não cabe a visita"</li>
        <li><strong>Eduardo Watanabe Castanheira</strong> · 17h · Águia/Urubu digital · score 82 · 30 anos · 6,8k seg · 2 RQEs. Pitch de LEGADO</li>
      </ul>
    </div>

    <div class="block">
      <span class="block-eyebrow">Águia em construção · ABORDAGEM CORRIGIDA pós-print</span>
      <h3>Felipe de Bulhões Ojeda · 18h</h3>
      <p>NÃO é Pato cansado como dossiê inicial achou. <strong>É Águia em construção</strong>: verificado azul, IDOR-SP, 2 RQEs, site felipebulhoes.com, posicionamento "Tech, Performance, Saúde do Homem". Tom: pares acelerando, não fundação.</p>
    </div>

    <div class="block">
      <span class="block-eyebrow">Gavião com tração</span>
      <h3>Tatiana Patruni · 11h · Curitiba · sem score na base</h3>
      <p>Gavião com casca de Pato. 14 anos de carreira, preceptora, rinoplastia · MAS 9k seg + 0 reviews Doctoralia + aceita Unimed. Tom: espelho duro.</p>
    </div>

    <div class="block">
      <span class="block-eyebrow">Gavião que descobrimos pela planilha · sócio ICOD Brasília</span>
      <h3>Paulo Victor de Souza Pereira · 13h</h3>
      <p>97% identidade após cruzar planilha. Ortopedia pé/tornozelo, sócio ICOD Brasília (ICOD ≠ ICOD do Tarik · siglas iguais, instituições diferentes). 151 reviews 5⭐ Doctoralia · sem IG pessoal · diluído na sociedade. Tom: "caso de sucesso clínico que ainda não virou negócio".</p>
    </div>

    <div class="block">
      <span class="block-eyebrow">Qualificação financeira ANTES do pitch</span>
      <h3>2 cirurgiões com risco de ROI longo</h3>
      <ul class="bullets">
        <li><strong>Júlio Fran da Silva Pinto</strong> · 15h · Urubu · score 45 · Timbó/SC · Unimed dominante · IG fechado/inativo</li>
      </ul>
      <p style="margin-top:14px">Pitch deve ser visão de 12-18 meses, parcelamento longo. Cuidado: pode ser Pato fingindo Gavião — verificar capital próprio.</p>
    </div>

    <div class="block">
      <span class="block-eyebrow">Achados críticos via prints + planilha</span>
      <ul class="bullets">
        <li><strong>Felipe Ojeda</strong> não é cirurgião geral plantonista — é UROLOGISTA fellow IDOR-SP, verificado azul. Dossiê inicial errou. Pitch corrigido pra Águia em construção.</li>
        <li><strong>Marina Marangon</strong> tem só 100 seguidores no @dramarinamelhado apesar do selo azul + CNN. Perfil recém-aberto/migrado. Dor central: autoridade externa &gt; audiência interna.</li>
        <li><strong>Tarik Suleiman</strong> tem 31,6k seg + verificado azul + Mateus já segue. É Águia digital, não Gavião. Posicionamento já cravado: "Cirurgião de vesícula".</li>
        <li><strong>Eduardo Watanabe</strong>: 6.808 seg / 672 posts (não 5.300/592) · 2 RQEs (12516 + 12515)</li>
        <li><strong>Paulo Victor</strong>: confirmado 97% via planilha — Paulo Victor DE SOUZA Pereira, sócio ICOD Brasília</li>
      </ul>
    </div>

    <div class="block">
      <span class="block-eyebrow">Correções de grafia</span>
      <ul class="bullets">
        <li>Patrick listou <strong>Patrubi</strong> · grafia oficial: <strong>Patruni</strong> (com N)</li>
        <li>Patrick listou <strong>Tarick</strong> · grafia oficial: <strong>Tarik</strong> (sem C)</li>
        <li>Patrick listou <strong>Mariana Marangon</strong> · nome correto: <strong>Marina Marangon Melhado</strong></li>
      </ul>
    </div>
  </div>
</section>

{FOOT_OPS}
"""
    out = HEAD.format(title=title, desc=desc) + body
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"  ✓ index.html (painel operacional)")

# ============================================================================
# INDIVIDUAL · APRESENTAÇÃO PRO MÉDICO + PITCH NO FINAL
# ============================================================================
def render_individual(c):
    title = f"{c['nome']} · Diagnóstico CPP · 06/05"
    desc = f"Mapa diagnóstico individual para {c['nome']} — Cirurgião Particular Premium · 06 de Maio 2026"

    correcao_html = ""
    # correção de grafia só aparece pra alguns (não confunde médico com nota interna)
    if c.get('correcao_grafia') and ('CORREÇÃO MASSIVA' not in c['correcao_grafia']):
        correcao_html = f'<div class="note"><h5>Nota</h5><p>{safe(c["correcao_grafia"])}</p></div>'

    formacao_li = li(c.get('formacao'))
    estruturas_li = li(c.get('estruturas'))
    credenciais_li = li(c.get('credenciais'))

    redes_rows = []
    if c.get('instagram'):
        ig_status = "aberto" if c.get('instagram_aberto') else "fechado / inativo"
        seg = c.get('instagram_seguidores')
        seg_str = f" · {seg} seguidores" if seg and seg != "—" else ""
        redes_rows.append(('Instagram', f'<a href="{c["instagram_url"]}" target="_blank" rel="noopener">{safe(c["instagram"])}</a> · <span class="muted">{ig_status}{seg_str}</span>'))
    if c.get('site'):
        redes_rows.append(('Site', f'<a href="{c["site"]}" target="_blank" rel="noopener">{safe(c["site"])}</a>'))
    if c.get('doctoralia'):
        redes_rows.append(('Doctoralia', f'<a href="{c["doctoralia"]}" target="_blank" rel="noopener">ver perfil</a>'))
    if c.get('linkedin'):
        redes_rows.append(('LinkedIn', f'<a href="{c["linkedin"]}" target="_blank" rel="noopener">ver perfil</a>'))

    redes_kv_html = ""
    if redes_rows:
        redes_kv_html = '<div class="kv">' + ''.join(f'<div class="k">{k}</div><div class="v">{v}</div>' for k,v in redes_rows) + '</div>'

    posicao_atual_html = c.get('posicionamento_atual_publico') or ""
    potencial_html = c.get('potencial_publico') or ""

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

    gaps_html = ""
    for area, descricao in c.get('gaps') or []:
        gaps_html += f'''
      <div class="duo-card">
        <h5>{safe(area)}</h5>
        <p>{safe(descricao)}</p>
      </div>'''

    # LEITURA DO INSTAGRAM (pública · elegante · alinhada à promessa da live)
    ig = IG_ANALISE.get(c['slug'], {})
    ig_public_html = ""
    if ig:
        verif_html = '<span class="ig-pub-verified">✓ Verificado</span>' if ig.get('verificado') else ''
        sub_stats = []
        if ig.get('seguidores') and ig.get('seguidores') != "—": sub_stats.append(f'<div class="ig-pub-stat"><div class="num">{safe(ig["seguidores"])}</div><div class="label">seguidores</div></div>')
        if ig.get('posts') and ig.get('posts') != "—": sub_stats.append(f'<div class="ig-pub-stat"><div class="num">{safe(ig["posts"])}</div><div class="label">posts</div></div>')
        if ig.get('seguindo') and ig.get('seguindo') != "—": sub_stats.append(f'<div class="ig-pub-stat"><div class="num">{safe(ig["seguindo"])}</div><div class="label">seguindo</div></div>')

        ig_public_html = f"""
<section class="ig-public-section">
  <div class="wrap-narrow">
    <div class="section-head">
      <span class="eyebrow">Leitura da sua presença digital</span>
      <h2>O que o seu <em class="gold-accent">Instagram</em> conta sobre você hoje</h2>
    </div>

    <div class="ig-public-card">
      <div class="ig-public-head">
        <img src="{safe(ig.get('foto'))}" alt="{safe(ig.get('handle'))}" class="ig-pub-avatar" loading="lazy" onerror="this.style.display='none'">
        <div class="ig-public-info">
          <div class="ig-pub-handle-row">
            <a href="{safe(ig.get('url'))}" target="_blank" rel="noopener" class="ig-pub-handle">{safe(ig.get('handle'))}</a>
            {verif_html}
          </div>
          <div class="ig-pub-bio">{safe(ig.get('bio_literal'))}</div>
        </div>
      </div>

      {('<div class="ig-pub-stats">' + ''.join(sub_stats) + '</div>') if sub_stats else ''}

      <div class="ig-public-readout">
        <div class="ig-pub-row">
          <h5>Tom de comunicação</h5>
          <p>{safe(ig.get('tom'))}</p>
        </div>
        <div class="ig-pub-row">
          <h5>Branding atual</h5>
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

    # PRÉ-DIAGNÓSTICO
    pre_diag = c.get('pre_diagnostico') or {}
    pre_diag_html = ""
    if pre_diag:
        pontos = pre_diag.get('pontos') or []
        pontos_html = "\n".join(f'<li>{safe(p)}</li>' for p in pontos)
        pre_diag_html = f"""
<section class="pre-diag-section">
  <div class="wrap-narrow">
    <div class="section-head">
      <span class="eyebrow">Pré-diagnóstico</span>
      <h2>O retrato em uma frase</h2>
    </div>

    <blockquote class="pre-diag-frase">
      <p>"{safe(pre_diag.get('frase_central'))}"</p>
    </blockquote>

    <div class="pre-diag-pontos">
      <h4 class="pre-diag-titulo">Os quatro pontos que se conectam</h4>
      <ol>{pontos_html}</ol>
    </div>

    <div class="pre-diag-no">
      <span class="pre-diag-no-label">O nó central</span>
      <p>{safe(pre_diag.get('no_central'))}</p>
    </div>
  </div>
</section>"""

    # PLANO DE AÇÃO
    plano = c.get('plano_acao') or []
    plano_html = ""
    if plano:
        fases_html = ""
        for i, f in enumerate(plano, 1):
            acoes_li = "\n".join(f'<li>{safe(a)}</li>' for a in f.get('acoes',[]))
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
<section class="plano-section">
  <div class="wrap-narrow">
    <div class="section-head">
      <span class="eyebrow">Plano de ação · resumido</span>
      <h2>O que você faria <em class="gold-accent">como Cirurgião Particular Premium</em></h2>
      <p style="font-family: var(--serif); font-style: italic; font-size: 1.1rem; color: var(--text-2); margin-top: 14px; max-width: 56ch;">Três fases. Três decisões. Cada uma constrói sobre a anterior.</p>
    </div>

    <div class="fases-grid">{fases_html}
    </div>
  </div>
</section>"""

    # mapa da oferta
    oferta_section = render_oferta_mapa()

    body = f"""
{TOPBAR.format(label='Mapa Diagnóstico', nav=nav_back_button())}

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
          {('<span class="dot"></span><span>🆔 <strong>' + safe(c['crm']) + '</strong></span>') if c.get('crm') and '[A CONFIRMAR' not in (c.get('crm') or '') else ''}
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

{ig_public_html}

{pre_diag_html}

{plano_html}

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
  </div>
</section>

{oferta_section}

{FOOT_PUBLIC}
"""
    out = HEAD.format(title=title, desc=desc) + body
    fname = f"{c['slug']}.html"
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"  ✓ {fname}")

if __name__ == "__main__":
    print("Gerando 9 HTMLs (1 painel operacional + 8 apresentações)...")
    render_hub()
    for c in CIRURGIOES:
        render_individual(c)
    print(f"\n✅ Gerados em {OUT}")
