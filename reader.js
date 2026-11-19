'use strict';
(() => {
  const data = JSON.parse(document.getElementById('flow-data').textContent);
  const modes = {
    natural: '自然操作',
    controlled: '受控回放',
    counterfactual: '反事实回放',
    user_reference: '用户原图',
    design_reference: '方案截图',
  };
  const sourceId = image => `${image.id} · ${image.source_label || `v${image.version}`}`;
  const stages = new Map();
  const shots = new Map();
  data.games.forEach(g => g.branches.forEach(b => b.stages.forEach(s => {
    stages.set(s.id, {game:g, branch:b, stage:s});
    s.images.forEach(im => shots.set(im.id, im));
  })));
  let currentGame = data.games[0];
  let currentBranch = currentGame.branches[0];
  const viewer = document.getElementById('image-viewer');
  let viewerImages = [];
  let viewerIndex = 0;
  let focusBeforeViewer;
  let toastTimer;
  function toast(message) {
    const el = document.getElementById('toast');
    el.textContent = message; el.classList.add('show');
    clearTimeout(toastTimer); toastTimer = setTimeout(() => el.classList.remove('show'), 2400);
  }
  function route(initial = false) {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { id = ''; }
    if (id === 'method' || id === 'reader') return;
    const parts = id.split('--');
    const g = data.games.find(x => x.id === parts[0]) || data.games[0];
    const b = g.branches.find(x => x.id === parts[1]) || g.branches[0];
    currentGame = g; currentBranch = b;
    document.querySelectorAll('.game-view').forEach(el => { el.hidden = el.id !== g.id; });
    document.querySelectorAll('.game-link').forEach(el => {
      const selected = el.dataset.gameLink === g.id;
      el.classList.toggle('selected', selected); el.setAttribute('aria-current', String(selected));
    });
    document.getElementById('game-select').value = g.id;
    const pane = document.getElementById(g.id);
    pane.querySelectorAll('.branch-view').forEach(el => { el.hidden = el.id !== `${g.id}--${b.id}`; });
    pane.querySelectorAll('.branch-tab').forEach(el => {
      const selected = el.dataset.branch === `${g.id}--${b.id}`;
      el.classList.toggle('selected', selected); el.setAttribute('aria-current', String(selected));
    });
    if (!initial || id) requestAnimationFrame(() => {
      const target = document.getElementById(id);
      if (target && !target.hidden) target.scrollIntoView({block:'start', behavior:'instant'});
      else if (!initial) document.getElementById(g.id).scrollIntoView({block:'start', behavior:'instant'});
    });
  }
  window.addEventListener('hashchange', () => route());
  document.getElementById('game-select').addEventListener('change', e => { location.hash = e.target.value; });
  route(true);
  function selectShot(card, im) {
    const link = card.querySelector('.screen-shot');
    link.href = im.src; link.dataset.image = im.id;
    link.setAttribute('aria-label', `放大：${im.caption}`);
    const image = link.querySelector('img');
    image.src = im.thumb; image.alt = im.caption; image.width = im.width; image.height = im.height;
    card.querySelector('.screen-caption').textContent = im.caption;
    card.querySelector('.source-id').textContent = sourceId(im);
    const mode = card.querySelector('.mode');
    mode.className = `mode mode-${im.mode}`; mode.textContent = modes[im.mode] || '受控回放';
    const list = stages.get(card.id).stage.images;
    card.querySelector('.shot-counter').textContent = `${String(list.findIndex(x => x.id === im.id)+1).padStart(2,'0')} / ${String(list.length).padStart(2,'0')}`;
    card.querySelectorAll('.thumb').forEach(el => {
      const selected = el.dataset.shot === im.id;
      el.classList.toggle('selected', selected); el.setAttribute('aria-pressed', String(selected));
    });
  }
  function renderViewer() {
    const im = viewerImages[viewerIndex];
    document.getElementById('viewer-image').src = im.src;
    document.getElementById('viewer-image').alt = im.caption;
    document.getElementById('viewer-caption').textContent = im.caption;
    document.getElementById('viewer-mode').textContent = `${modes[im.mode] || '受控回放'} · ${sourceId(im)}`;
    document.getElementById('viewer-position').textContent = `${viewerIndex+1} / ${viewerImages.length}`;
    document.getElementById('viewer-original').href = im.src;
    document.getElementById('viewer-prev').disabled = viewerIndex === 0;
    document.getElementById('viewer-next').disabled = viewerIndex === viewerImages.length-1;
  }
  function changeViewer(delta) {
    const next = viewerIndex + delta;
    if (next < 0 || next >= viewerImages.length) return;
    viewerIndex = next; renderViewer();
  }
  document.addEventListener('click', async e => {
    const thumb = e.target.closest('[data-shot]');
    if (thumb) { selectShot(thumb.closest('.stage-card'), shots.get(thumb.dataset.shot)); return; }
    const shotLink = e.target.closest('.screen-shot');
    if (shotLink) {
      e.preventDefault(); focusBeforeViewer = shotLink;
      const branch = stages.get(shotLink.closest('.stage-card').id).branch;
      viewerImages = branch.stages.flatMap(s => s.images);
      viewerIndex = viewerImages.findIndex(x => x.id === shotLink.dataset.image);
      renderViewer(); viewer.showModal(); return;
    }
    const share = e.target.closest('[data-share]');
    if (share) {
      const url = new URL(location.href); url.hash = share.dataset.share;
      try { await navigator.clipboard.writeText(url.href); toast('分享链接已复制'); }
      catch {
        const input = document.getElementById('share-url'); input.value = url.href;
        document.getElementById('share-dialog').showModal(); input.select();
      }
    }
  });
  document.getElementById('viewer-prev').addEventListener('click', () => changeViewer(-1));
  document.getElementById('viewer-next').addEventListener('click', () => changeViewer(1));
  viewer.querySelector('.viewer-close').addEventListener('click', () => viewer.close());
  viewer.addEventListener('close', () => { if (focusBeforeViewer) focusBeforeViewer.focus({preventScroll:true}); });
  viewer.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft') { e.preventDefault(); changeViewer(-1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); changeViewer(1); }
  });
  document.getElementById('print-page').addEventListener('click', () => window.print());
})();
