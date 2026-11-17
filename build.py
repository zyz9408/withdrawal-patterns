"""Render the shareable static research page. Python standard library only."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "data/research.json").read_text(encoding="utf-8"))
BASE_URL = "https://zyz9408.github.io/withdrawal-patterns/"
REPO_URL = "https://github.com/zyz9408/withdrawal-patterns"


def esc(value):
    return html.escape(str(value), quote=True)


def icon(kind):
    shapes = {
        "mahjong": '<rect x="18" y="19" width="43" height="60" rx="7" fill="#b6cfc0" transform="rotate(-12 40 49)"/><rect x="36" y="22" width="43" height="60" rx="7" fill="#fffdf5" stroke="currentColor" stroke-width="2"/><text x="57.5" y="62" text-anchor="middle" fill="currentColor" font-size="28" font-weight="700">發</text>',
        "solitaire": '<rect x="18" y="17" width="46" height="66" rx="6" fill="#c5b8d9" transform="rotate(-12 41 50)"/><rect x="35" y="18" width="46" height="66" rx="6" fill="#fffdf5" stroke="currentColor" stroke-width="2"/><path d="M58 34c-4 8-14 11-14 19a8 8 0 0 0 13 6l-4 10h10l-4-10a8 8 0 0 0 13-6c0-8-10-11-14-19Z" fill="currentColor"/>',
        "rings": '<ellipse cx="47" cy="66" rx="29" ry="16" fill="none" stroke="#cf9a67" stroke-width="11"/><ellipse cx="50" cy="48" rx="29" ry="16" fill="none" stroke="#6b9e89" stroke-width="11"/><ellipse cx="53" cy="30" rx="29" ry="16" fill="none" stroke="#d5bb69" stroke-width="11"/>',
        "smash": '<rect x="15" y="15" width="32" height="32" rx="8" fill="#cc8d69"/><rect x="53" y="15" width="32" height="32" rx="8" fill="#edbb8d"/><rect x="15" y="53" width="32" height="32" rx="8" fill="#edbb8d"/><rect x="53" y="53" width="32" height="32" rx="8" fill="#cc8d69"/><path d="M44 36 54 48 45 62" fill="none" stroke="#fffaf0" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',
        "pixel": ''.join(f'<rect x="{18+x*9}" y="{18+y*9}" width="8" height="8" rx="1" fill="{color}"/>' for y, row in enumerate(["1111111", "0111110", "0022200", "0002000", "0022200", "0222220", "1111111"]) for x, digit in enumerate(row) if digit != "0" for color in [{"1": "#668fb0", "2": "#e8bb67"}[digit]]),
    }
    return f'<svg viewBox="0 0 100 100" aria-hidden="true" focusable="false">{shapes[kind]}</svg>'


def case_card(game, index):
    facts = ''.join(f'<div class="fact"><strong>{esc(f["value"])}</strong><span>{esc(f["label"])}</span><p>{esc(f["note"])}</p></div>' for f in game["facts"])
    flow = ''.join(f'<li><span class="flow-dot"></span>{esc(step)}</li>' for step in game["flow"])
    strengths = ''.join(f'<li>{esc(v)}</li>' for v in game["strengths"])
    weaknesses = ''.join(f'<li>{esc(v)}</li>' for v in game["weaknesses"])
    evidence = ''.join(f'<div class="evidence-item"><span class="finding-id">{esc(f["id"])}</span><code>{esc(f["location"])}</code><p>{esc(f["claim"])}</p></div>' for f in game["findings"])
    search = esc(' '.join([game["name"], game["kind"], game["summary"], game["terminal"], *game["weaknesses"]]))
    return f'''<article class="case theme-{game['theme']}" id="{game['id']}" data-tags="{' '.join(game['tags'])}" data-search="{search}">
      <div class="case-identity"><span class="case-index">CASE / {index:02}</span><div class="game-art">{icon(game['theme'])}</div><span class="kind-label">{esc(game['kind'])}</span><span class="version">已分析版本 {esc(game['version'])}</span></div>
      <div class="case-body"><header class="case-heading"><div><h3>{esc(game['name'])}</h3><p>{esc(game['subtitle'])}</p></div><button class="icon-button case-share" data-share="{game['id']}" aria-label="分享{esc(game['name'])}的单款链接" title="分享单款链接"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 4h5v5M20 4l-9 9M10 5H6a2 2 0 0 0-2 2v11a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2v-4"/></svg></button></header>
      <p class="case-summary">{esc(game['summary'])}</p>
      <div class="flow-label"><span>机制路径</span><span>以当前已追踪流程为准</span></div><ol class="mechanism-flow">{flow}</ol>
      <div class="facts">{facts}</div>
      <div class="assessment"><section><h4><span class="small-mark">＋</span>结构优点</h4><ul>{strengths}</ul></section><section><h4><span class="small-mark risk-mark">↳</span>主要问题</h4><ul>{weaknesses}</ul></section></div>
      <aside class="correction-note"><span>读对这一点</span><p>{esc(game['correction'])}</p></aside>
      <details class="evidence"><summary><span><span class="evidence-dot"></span>查看代码依据与结论边界</span><span class="plus-sign" aria-hidden="true">＋</span></summary><div class="evidence-body">{evidence}<div class="interpretation"><strong>设计判断 · 非经营实测</strong><p>{esc(game['business'])}</p></div></div></details>
      </div></article>'''


overview_rows = ''.join(f'<tr><th scope="row"><a href="#{g["id"]}"><span class="table-index">{i:02}</span><span>{esc(g["name"])}<small>v{esc(g["version"])}</small></span><span class="table-arrow" aria-hidden="true">↗</span></a></th><td>{esc(g["kind"])}</td><td>{esc(g["short"])}</td><td><span class="endpoint"><i></i>{esc(g["terminal"])}</span></td></tr>' for i, g in enumerate(DATA["games"], 1))
cards = ''.join(case_card(g, i) for i, g in enumerate(DATA["games"], 1))
sheet_rows = ''.join(f'<a class="sheet-row" href="#{g["id"]}"><span class="sheet-num">{i:02}</span><span class="sheet-game">{esc(g["name"])}</span><span class="sheet-type">{esc(g["kind"])}</span><span aria-hidden="true">↗</span></a>' for i, g in enumerate(DATA["games"], 1))

page = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light">
<title>五款游戏的提现机制拆解 · 机制观察</title><meta name="description" content="从阶段任务、字母收集到审核、队列与等级，比较五款游戏的提现机制、结构优点、关键问题和代码证据。">
<link rel="canonical" href="{BASE_URL}"><meta property="og:type" content="website"><meta property="og:locale" content="zh_CN"><meta property="og:title" content="五款游戏，五种提现机制。"><meta property="og:description" content="把显示目标、实际条件和最终状态，放在同一张图里看清楚。"><meta property="og:url" content="{BASE_URL}"><meta property="og:image" content="{BASE_URL}assets/share-card.png"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="五款游戏的提现机制拆解"><meta name="twitter:image" content="{BASE_URL}assets/share-card.png">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg"><link rel="stylesheet" href="styles.css"><script src="app.js" defer></script></head>
<body><a class="skip-link" href="#overview">跳到研究内容</a><div class="read-progress" aria-hidden="true"><span id="read-progress"></span></div>
<header class="site-header"><div class="header-inner"><a class="brand" href="#top" aria-label="机制观察首页"><span class="brand-mark" aria-hidden="true">↗</span><span>机制观察<small>GAME MECHANICS NOTES</small></span></a><nav aria-label="页面导航"><a href="#overview">对比总览</a><a href="#cases">逐款拆解</a><a href="#corrections">关键纠错</a><a href="#method">证据边界</a></nav><button class="share-button" data-share="" aria-label="分享整个研究页面"><span>分享研究</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 15V3m-4 4 4-4 4 4M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/></svg></button></div></header>
<main id="top"><section class="hero container"><div class="hero-copy"><p class="eyebrow"><span class="live-dot"></span>FIELD NOTES <span class="eyebrow-slash">/</span> NO. 001</p><h1>五款游戏，<br>五种<span>提现机制。</span></h1><p class="hero-description">把显示目标、实际条件和最终状态，<br class="desktop-break">放在同一张图里看清楚。</p><div class="hero-actions"><a class="button primary" href="#overview">开始阅读 <span aria-hidden="true">↘</span></a><a class="text-link" href="report.md" download="五款提现机制对比.md">下载文字版 <span aria-hidden="true">↓</span></a></div><p class="hero-meta"><span>更新于 2026.11.17</span><span>基于同版本代码与配置</span></p></div>
<div class="reading-sheet" aria-label="五款研究样本"><div class="sheet-top"><span>RESEARCH INDEX</span><span>05 SAMPLES</span></div><div class="sheet-heading"><span>“完成条件”之后，<br>流程还会去哪里？</span><svg viewBox="0 0 80 80" aria-hidden="true"><path d="M15 57h48V9M18 54 62 10"/><circle cx="17" cy="56" r="8"/></svg></div><div class="sheet-rows">{sheet_rows}</div><div class="sheet-bottom"><span class="bracket">[</span><p>余额 · 资格 · 申请 · 付款<br><strong>四种状态，分别看待。</strong></p><span class="bracket">]</span></div></div></section>
<div class="basis-strip"><div class="container basis-inner"><span><i></i>同版本客户端代码</span><span><i></i>包内配置与历史取证</span><span><i></i>结构比较 · 非收益排名</span><a href="#method">阅读分析边界 <span aria-hidden="true">↗</span></a></div></div>
<section class="section container" id="overview" data-nav><div class="section-heading"><div><p class="eyebrow muted">01 / THE BIG PICTURE</p><h2>先看五种不同的终点。</h2></div><p class="section-intro">“显示达标”不等于“付款完成”。<br>不同机制，需要检查不同的最后一步。</p></div><div class="table-scroll" role="region" aria-label="五款游戏机制对比表" tabindex="0"><table class="overview-table"><thead><tr><th scope="col">游戏 / 已分析版本</th><th scope="col">机制类型</th><th scope="col">主要路径</th><th scope="col">代码中的关键状态</th></tr></thead><tbody>{overview_rows}</tbody></table></div><p class="table-footnote">点击游戏名称，可直接跳转到对应拆解。以下“优点”评价任务与工程结构，不代表真实支付能力。</p></section>
<section class="cases-section" id="cases" data-nav><div class="container"><div class="section-heading"><div><p class="eyebrow muted">02 / CASE BY CASE</p><h2>拆开流程，再看优缺点。</h2></div><p class="section-intro">先还原条件，再区分设计判断。<br>每款均附方法与发现编号。</p></div><div class="explore-bar"><div class="filters" role="group" aria-label="按机制筛选"><button class="filter active" data-filter="all" aria-pressed="true">全部五款</button><button class="filter" data-filter="tasks" aria-pressed="false">阶段任务</button><button class="filter" data-filter="collection" aria-pressed="false">收集机制</button><button class="filter" data-filter="queue" aria-pressed="false">订单与队列</button><button class="filter" data-filter="review" aria-pressed="false">审核机制</button></div><label class="search-label"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4.5 4.5"/></svg><span class="sr-only">搜索游戏或机制</span><input id="case-search" type="search" placeholder="搜索游戏或机制" autocomplete="off"></label></div><div class="result-line"><span id="result-count" aria-live="polite">显示全部 5 款研究</span><button class="text-link" id="expand-evidence" type="button" aria-pressed="false">展开全部代码依据 <span aria-hidden="true">＋</span></button></div><div class="case-list">{cards}</div><div class="empty-state" id="empty-state" hidden><span aria-hidden="true">⌕</span><h3>没有匹配的研究</h3><p>试试其他游戏名或机制关键词。</p><button class="button" id="reset-filters">清除筛选</button></div></div></section>
<section class="section corrections-section container" id="corrections" data-nav><div class="section-heading"><div><p class="eyebrow muted">03 / READ IT RIGHT</p><h2>四个容易误读的结论。</h2></div><p class="section-intro">定位真正的卡点，<br>比笼统地说“永远达不到”更重要。</p></div><div class="correction-grid"><article><span class="note-number">01</span><span class="note-game">SOLITAIRE MONEY TREE</span><h3>100%本身能达到。</h3><p>50级99.99%，51级100%。应继续追踪后置字母收集与最终领取页。</p><a href="#solitaire-money-tree">回看证据 <span aria-hidden="true">↗</span></a></article><article><span class="note-number">02</span><span class="note-game">RINGS CASH</span><h3>碎片并非永久卡90。</h3><p>部分广告限制与日期相关，次日仍可补到100。关键问题在下游订单与物流。</p><a href="#rings-cash">回看证据 <span aria-hidden="true">↗</span></a></article><article><span class="note-number">03</span><span class="note-game">SMASH CASH</span><h3>允许0，不等于恒为0。</h3><p>最后奖励区间也允许正数。不能仅凭区间中的0证明金额永远不可达。</p><a href="#smash-cash">回看证据 <span aria-hidden="true">↗</span></a></article><article><span class="note-number">04</span><span class="note-game">HAPPY / PIXEL SAND</span><h3>“很难”与“不能返回”。</h3><p>Happy末级需要极多完成次数；Pixel当前函数最高返回28却要求30，性质不同。</p><a href="#pixel-sand-puzzle">回看证据 <span aria-hidden="true">↗</span></a></article></div></section>
<section class="method-section" id="method" data-nav><div class="container method-layout"><div><p class="eyebrow light">04 / EVIDENCE & SCOPE</p><h2>看得见流程，<br>不替代真实结果。</h2><p>分析范围为上述五个版本的客户端代码、配置与已标记的历史取证。结论限定已追踪路径；未来版本或远端变化需要重新判断。</p><a class="button light-button" href="report.md" download="五款提现机制对比.md">保存研究文字版 <span aria-hidden="true">↓</span></a></div><div class="scope-list"><div><span>01</span><section><h3>代码与配置</h3><p>支持条件、奖池权重、状态迁移和数值返回域的结论。各款技术旁注保留发现编号与方法名。</p></section></div><div><span>02</span><section><h3>历史受控观察</h3><p>部分后续页面使用受控状态回放。它们不代表自然通关、真实提现或真实配送。</p></section></div><div><span>03</span><section><h3>经营效果仍未知</h3><p>没有对应CPI、净eCPM、实际展示与成熟留存数据，不能据此排列LTV、ROI或回本能力。</p></section></div></div></div></section>
</main><footer class="site-footer container"><a class="footer-brand" href="#top">机制观察 <span>↗</span></a><p>五款游戏提现机制研究 · 2026.11.17</p><div><a href="data/research.json">研究数据</a><a href="{REPO_URL}" target="_blank" rel="noopener noreferrer">GitHub <span aria-hidden="true">↗</span></a><button id="print-page" type="button">打印 / 存为PDF</button></div></footer>
<div class="toast" id="toast" role="status" aria-live="polite"></div><dialog id="share-dialog"><form method="dialog"><div class="dialog-heading"><h2>分享这份研究</h2><button class="icon-button" aria-label="关闭分享窗口">×</button></div><p>复制下方链接，即可分享当前内容。</p><label class="sr-only" for="share-url">分享链接</label><input id="share-url" type="url" readonly><button class="button primary" value="done">完成</button></form></dialog><script type="application/json" id="research-data">{json.dumps(DATA, ensure_ascii=False).replace('<', '&lt;')}</script>
</body></html>'''
(ROOT / "index.html").write_text(page, encoding="utf-8")

report = ["# 五款游戏的提现机制拆解", "", "更新：2026-11-17。范围：同版本客户端代码、配置与已标记的历史取证。", "", DATA["scope"], ""]
for g in DATA["games"]:
    report += [f"## {g['name']} {g['version']} · {g['kind']}", "", g["summary"], "", "路径：" + " → ".join(g["flow"]), "", "### 关键事实", ""]
    report += [f"- {f['label']}：{f['value']}。{f['note']}" for f in g["facts"]]
    report += ["", "### 结构优点", ""] + [f"- {v}" for v in g["strengths"]]
    report += ["", "### 主要问题", ""] + [f"- {v}" for v in g["weaknesses"]]
    report += ["", "关键纠错：" + g["correction"], "", "设计判断（非经营实测）：" + g["business"], "", "### 证据索引", ""]
    report += [f"- {f['id']} / {f['location']}：{f['claim']}" for f in g["findings"]]
    report += [""]
report += ["## 结论边界", "", "历史受控状态不代表自然可达、真实收款或真实配送。结论限定当前已追踪的客户端路径与配置。没有五款对应的CPI、实际收益展示、净eCPM和成熟留存数据，因此不作经营收益排序。", ""]
(ROOT / "report.md").write_text("\n".join(report), encoding="utf-8")
print(f"Built {len(DATA['games'])} cases → index.html and report.md")
