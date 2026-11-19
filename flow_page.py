"""Build the screenshot-first research reader. Standard library only."""
import hashlib
import html
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'data/flows.json').read_text('utf-8'))
OLD=json.loads((ROOT/'data/research.json').read_text('utf-8'))
BASE='https://zyz9408.github.io/withdrawal-patterns/'
esc=lambda value:html.escape(str(value),quote=True)
MODE={
    'natural': '自然操作',
    'controlled': '受控回放',
    'counterfactual': '反事实回放',
    'user_reference': '用户原图',
    'design_reference': '方案截图',
}

def is_design(game):
    return game.get('evidence_type') == 'design'

def source_id(shot):
    reference = shot.get('source_label') or f"v{shot['version']}"
    return f"{shot['id']} · {reference}"

def version_label(game):
    return '设计文档' if is_design(game) else f"v{game['version']}"

def rev(file):return hashlib.sha256((ROOT/file).read_bytes()).hexdigest()[:10]
def image_html(shot):
    return f'''<a class="screen-shot" href="{esc(shot['src'])}" data-image="{esc(shot['id'])}" aria-label="放大：{esc(shot['caption'])}"><img src="{esc(shot['thumb'])}" width="{shot['width']}" height="{shot['height']}" alt="{esc(shot['caption'])}" loading="lazy" decoding="async"><span class="zoom-hint">↗ 查看原始尺寸</span></a>'''

def stage_html(stage,index,*,design=False):
    images=stage['images']
    if images:
        first=images[0]
        thumbs=''
        if len(images)>1:
            thumbs='<div class="filmstrip" aria-label="本阶段其他截图">'+''.join(f'<button class="thumb {"selected" if i==0 else ""}" type="button" data-shot="{esc(x["id"])}" aria-label="截图{i+1}：{esc(x["caption"])}" aria-pressed="{str(i==0).lower()}"><img src="{esc(x["thumb"])}" alt="" width="48" height="85" loading="lazy"><span>{i+1:02}</span></button>' for i,x in enumerate(images))+'</div>'
        media=f'''<div class="stage-media"><div class="screen-label"><span class="mode mode-{first['mode']}">{MODE.get(first['mode'],'受控回放')}</span><span class="shot-counter">01 / {len(images):02}</span></div><div class="screen-frame">{image_html(first)}</div>{thumbs}<p class="screen-caption">{esc(first['caption'])}</p><p class="source-id">{esc(source_id(first))}</p></div>'''
    else:
        material = '此项仅有方案文字' if design else '此项仅有代码 / 配置'
        media=f'<div class="stage-media code-only"><span class="code-symbol">{{ }}</span><strong>{material}</strong><p>尚无对应截图。具体缺口见本阶段说明。</p></div>'
    note=f'<p class="stage-note">{esc(stage["note"])}</p>' if stage.get('note') else ''
    terminal_label = '方案终点' if design else '已追踪终点'
    terminal = f'<span class="terminal-tag">{terminal_label}</span>' if stage.get('terminal') else ''
    condition_label = '方案条件' if design else '实际条件'
    index_label = '原文位置' if design else '本阶段代码索引'
    return f'''<article class="stage-card {"is-terminal" if stage.get('terminal') else ""}" id="{stage['id']}" data-stage="{stage['id']}">
      <div class="stage-heading"><span class="step-index">{index:02}</span><div><p class="step-eyebrow">STAGE {index:02}{terminal}</p><h3>{esc(stage['title'])}</h3></div><button class="copy-stage icon-button" data-share="{stage['id']}" aria-label="复制本阶段链接" title="复制本阶段链接">↗</button></div>
      <div class="stage-layout">{media}<div class="stage-detail"><dl><div><dt>玩家看到</dt><dd>{esc(stage['visible'])}</dd></div><div><dt>{condition_label}</dt><dd>{esc(stage['rule'])}</dd></div><div><dt>按钮与操作</dt><dd>{esc(stage['action'])}</dd></div><div class="next-state"><dt>接下来 <span aria-hidden="true">→</span></dt><dd>{esc(stage['after'])}</dd></div></dl>{note}<details class="stage-code"><summary>{index_label} <span>＋</span></summary><code>{esc(stage['code'])}</code></details></div></div></article>'''

def game_html(g,index):
    old=next(x for x in OLD['games'] if x['id']==g['id'])
    design = is_design(g)
    game_class = 'game-view design-case' if design else 'game-view'
    version = '设计文档' if design else f"已分析版本 {g['version']}"
    image_label = '张方案截图' if design else '张原界面截图'
    appendix_label = '附录：方案规则与待确认事项' if design else '附录：代码依据与原有比较说明'
    n=sum(len(b['stages']) for b in g['branches'])
    pics={s['id'] for b in g['branches'] for st in b['stages'] for s in st['images']}
    tabs=''.join(f'<a href="#{g["id"]}--{b["id"]}" class="branch-tab {"selected" if i==0 else ""}" data-branch="{g["id"]}--{b["id"]}" aria-current="{str(i==0).lower()}">{esc(b["title"])}<span>{len(b["stages"]):02}</span></a>' for i,b in enumerate(g['branches']))
    branches=[]
    for i,b in enumerate(g['branches']):
        bid=f'{g["id"]}--{b["id"]}'
        roadmap=''.join(f'<li><a href="#{s["id"]}"><span>{j:02}</span>{esc(s["title"])}</a></li>' for j,s in enumerate(b['stages'],1))
        stages=''.join(stage_html(s,j,design=design) for j,s in enumerate(b['stages'],1))
        branches.append(f'''<section class="branch-view" id="{bid}" {"hidden" if i else ""} aria-label="{esc(b['title'])}"><div class="branch-intro"><p>{esc(b['intro'])}</p><button class="text-button" data-share="{bid}">分享这条流程 ↗</button></div><details class="roadmap"><summary><span>流程目录</span><span>{len(b['stages'])} 个阶段 <i>＋</i></span></summary><ol>{roadmap}</ol></details><div class="stage-list">{stages}</div><div class="branch-end"><span>END OF FLOW</span><p>已读完「{esc(b['title'])}」</p><a href="#{g['id']}">回到游戏开头 ↑</a></div></section>''')
    findings=''.join(f'<li><span>{esc(x["id"])}</span><code>{esc(x["location"])}</code><p>{esc(x["claim"])}</p></li>' for x in old['findings'])
    strengths=''.join(f'<li>{esc(x)}</li>' for x in old['strengths'])
    weaknesses=''.join(f'<li>{esc(x)}</li>' for x in old['weaknesses'])
    return f'''<section class="{game_class}" id="{g['id']}" {"hidden" if index else ""} data-game="{g['id']}"><header class="game-heading"><div><p class="eyebrow">CASE {index+1:02} / {len(DATA['games']):02}<span>{esc(version)}</span></p><h2>{esc(g['name'])}</h2><p class="game-intro">{esc(g['intro'])}</p></div><div class="game-count"><strong>{len(pics):02}</strong><span>{image_label}</span><small>{n}个阶段 · {len(g['branches'])}条流程</small></div></header><nav class="branch-tabs" aria-label="{esc(g['name'])}的流程分支">{tabs}</nav>{''.join(branches)}<details class="appendix"><summary><span>{appendix_label}</span><span>＋</span></summary><div class="appendix-body"><p>{esc(old['correction'])}</p><div class="comparison"><section><h3>结构特点</h3><ul>{strengths}</ul></section><section><h3>问题与限制</h3><ul>{weaknesses}</ul></section></div><h3>发现索引</h3><ul class="findings">{findings}</ul></div></details></section>'''

shots={s['id']:s for g in DATA['games'] for b in g['branches'] for st in b['stages'] for s in st['images']}
for shot in shots.values():
    for key in ['src','thumb']:
        if not (ROOT/shot[key]).is_file():raise FileNotFoundError(shot[key])
stage_count=sum(len(b['stages']) for g in DATA['games'] for b in g['branches'])
missing=sum(not st['images'] for g in DATA['games'] for b in g['branches'] for st in b['stages'])
sidebar=''.join(f'<a class="game-link {"selected" if i==0 else ""}" href="#{g["id"]}" data-game-link="{g["id"]}" aria-current="{str(i==0).lower()}"><span class="game-number">{i+1:02}</span><span>{esc(g["name"])}<small>{esc(version_label(g))}</small></span><span class="game-arrow">↗</span></a>' for i,g in enumerate(DATA['games']))
options=''.join(f'<option value="{g["id"]}">{esc(g["name"])} · {esc(version_label(g))}</option>' for g in DATA['games'])
payload=json.dumps(DATA,ensure_ascii=False).replace('<','\\u003c')
page=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>{DATA['title']}</title><meta name="description" content="逐阶段查看原包界面与方案材料，沿着条件、操作与后续状态，阅读提现、审核、排队和物流流程。"><link rel="canonical" href="{BASE}"><meta property="og:type" content="website"><meta property="og:title" content="{DATA['title']}"><meta property="og:description" content="每个阶段附对应资料，沿着条件看接下来的状态。"><meta property="og:url" content="{BASE}"><meta property="og:image" content="{BASE}assets/share-card.png?v={rev('assets/share-card.png')}"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="assets/favicon.svg"><link rel="stylesheet" href="reader.css?v={rev('reader.css')}"><script src="reader.js?v={rev('reader.js')}" defer></script></head>
<body><a class="skip-link" href="#reader">跳到阶段截图</a><header class="site-header"><a class="brand" href="#happy-mahjong"><span class="brand-icon">↗</span><span>机制观察<small>WITHDRAWAL FLOW ARCHIVE</small></span></a><div class="header-note">阶段截图与流程</div><div class="header-actions"><button class="quiet-button" id="print-page">打印</button><button class="share-button" data-share="">分享网页 ↗</button></div></header>
<div class="workspace"><aside class="sidebar"><div class="sidebar-heading"><span>样本目录</span><span>{len(DATA['games']):02} CASES</span></div><nav aria-label="选择游戏">{sidebar}</nav><div class="sidebar-bottom"><a href="report.md" download>下载完整图文 Markdown ↓</a><a href="#method">截图与证据说明 ↘</a><a href="https://github.com/zyz9408/withdrawal-patterns" target="_blank" rel="noopener noreferrer">GitHub ↗</a></div><p class="updated">更新 {esc(DATA['updated'].replace('-', '.'))}</p></aside>
<main id="reader"><section class="reader-intro"><div><p class="eyebrow">SCREEN BY SCREEN / FIELD NOTES</p><h1>假提现，逐阶段看。</h1><p>从第一次承诺，到最后停留的那一屏。</p></div><div class="archive-count"><span><b>{len(DATA['games'])}</b> 个案例</span><span><b>{stage_count}</b> 个阶段</span><span><b>{len(shots)}</b> 张资料图</span></div></section><label class="mobile-picker">选择游戏<select id="game-select">{options}</select></label><div class="reading-key"><span><i class="natural-dot"></i>自然操作</span><span><i class="controlled-dot"></i>受控回放</span><span><i class="counter-dot"></i>反事实回放</span><span><i class="design-dot"></i>方案截图</span><a href="#method">标记说明 ↗</a></div><div id="games">{''.join(game_html(g,i) for i,g in enumerate(DATA['games']))}</div>
<section class="method" id="method"><p class="eyebrow">READ THE EVIDENCE</p><h2>原图与条件，一起读。</h2><div class="method-grid"><div><h3>自然操作</h3><p>原包中直接操作取得的界面；它只证明拍摄时看到的内容。</p></div><div><h3>受控回放</h3><p>在同版本原包上设置本地进度、日期或资格，展示后段原界面。代码算法保持原样；截图不代表自然通关或真实到账。</p></div><div><h3>反事实回放</h3><p>人为满足原路径无法提供的条件，用来检查下游界面。对应阶段单独标明。</p></div><div><h3>方案截图</h3><p>从设计文档的阶段表、流程图和界面画板截取。文案中的金额与时长随图标明。</p></div><div><h3>缺图与不可达</h3><p>目前有{missing}个仅代码或配置项。缺图处写清具体缺口；不会用其他阶段或自绘页面补作原图。</p></div></div><p class="method-foot">大图为原始像素的无损WebP副本，小图用于加载预览。页面包含虚构研究账户与示例资料，不包含真实收款或配送信息。结论限于标注版本与已追踪路径。</p></section><footer><span>机制观察 / 2026</span><div><a href="data/flows.json">阶段数据</a><a href="data/research.json">原研究数据</a><a href="#reader">回到顶部 ↑</a></div></footer></main></div>
<dialog id="image-viewer" aria-label="阶段图片查看器"><div class="viewer-top"><div><span id="viewer-mode"></span><p id="viewer-caption"></p></div><button class="viewer-close" aria-label="关闭大图">×</button></div><div class="viewer-body"><img id="viewer-image" alt=""></div><div class="viewer-bottom"><button id="viewer-prev" aria-label="上一张截图">← 上一张</button><span id="viewer-position"></span><a id="viewer-original" target="_blank" rel="noopener">打开原始尺寸 ↗</a><button id="viewer-next" aria-label="下一张截图">下一张 →</button></div></dialog><dialog id="share-dialog"><form method="dialog"><h2>复制分享链接</h2><input id="share-url" aria-label="分享链接" readonly><button class="share-button">完成</button></form></dialog><div class="toast" id="toast" role="status" aria-live="polite"></div><script id="flow-data" type="application/json">{payload}</script><noscript><style>.game-view[hidden],.branch-view[hidden]{{display:block!important}}</style></noscript></body></html>'''
(ROOT/'index.html').write_text(page,'utf-8')
report=['# '+DATA['title'],'',f"更新：{DATA['updated']}。在线阅读：{BASE}",'','图片分别标注自然操作、受控回放、反事实回放或方案截图。本地页面状态与真实付款记录分别归档。','']
for g in DATA['games']:
    report += ['## '+g['name']+' · '+version_label(g),'',g['intro'],'']
    for b in g['branches']:
        report += ['### '+b['title'],'',b['intro'],'']
        design = is_design(g)
        rule_label = '方案条件' if design else '实际条件'
        reference_label = '原文位置' if design else '代码索引'
        for i,s in enumerate(b['stages'],1):
            report += [f"#### {i:02} {s['title']}",'']
            for im in s['images']:
                report += [f"![{im['caption']}]({BASE}{im['src']})",f"{MODE.get(im['mode'],'受控回放')} · {source_id(im)}",'']
            if not s['images']:report += ['**仅代码/配置，尚无该项原图。**','']
            report += [f"- 玩家看到：{s['visible']}",f"- {rule_label}：{s['rule']}",f"- 按钮与操作：{s['action']}",f"- 接下来：{s['after']}",f"- {reference_label}：{s['code']}"]
            if s.get('note'):report += ['- 说明：'+s['note']]
            report += ['']
(ROOT/'report.md').write_text('\n'.join(report),'utf-8')
print(f"Built {len(DATA['games'])} games / {stage_count} stages / {len(shots)} screenshots / {missing} code-only items")
