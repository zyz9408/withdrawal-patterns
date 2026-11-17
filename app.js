"use strict";

(() => {
  const data = JSON.parse(document.getElementById("research-data").textContent);
  const cards = [...document.querySelectorAll(".case")];
  const filters = [...document.querySelectorAll("[data-filter]")];
  const search = document.getElementById("case-search");
  const empty = document.getElementById("empty-state");
  const count = document.getElementById("result-count");
  const expand = document.getElementById("expand-evidence");
  let selected = "all";
  let toastTimer;

  function update() {
    const query = search.value.trim().toLocaleLowerCase();
    let matches = 0;
    cards.forEach(card => {
      const tagMatch = selected === "all" || card.dataset.tags.split(" ").includes(selected);
      const textMatch = !query || card.dataset.search.toLocaleLowerCase().includes(query);
      card.hidden = !(tagMatch && textMatch);
      if (!card.hidden) matches++;
    });
    filters.forEach(button => {
      const active = button.dataset.filter === selected;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    count.textContent = matches === data.games.length ? `显示全部 ${data.games.length} 款研究` : `显示 ${matches} / ${data.games.length} 款研究`;
    empty.hidden = matches !== 0;
    updateProgress();
  }

  filters.forEach(button => button.addEventListener("click", () => {
    selected = button.dataset.filter;
    update();
  }));
  search.addEventListener("input", update);
  document.getElementById("reset-filters").addEventListener("click", () => {
    selected = "all";
    search.value = "";
    update();
    search.focus();
  });

  function showHashCase() {
    const id = location.hash.slice(1);
    if (!cards.some(card => card.id === id)) return;
    selected = "all";
    search.value = "";
    update();
    requestAnimationFrame(() => document.getElementById(id).scrollIntoView({block: "start"}));
  }
  addEventListener("hashchange", showHashCase);
  document.querySelectorAll('a[href^="#"]').forEach(link => link.addEventListener("click", () => {
    const id = link.getAttribute("href").slice(1);
    const target = cards.find(card => card.id === id);
    if (target && target.hidden) {
      selected = "all";
      search.value = "";
      update();
    }
  }));

  expand.addEventListener("click", () => {
    const open = expand.getAttribute("aria-pressed") !== "true";
    document.querySelectorAll(".case:not([hidden]) details.evidence").forEach(detail => detail.open = open);
    expand.setAttribute("aria-pressed", String(open));
    expand.innerHTML = open ? '收起全部代码依据 <span aria-hidden="true">−</span>' : '展开全部代码依据 <span aria-hidden="true">＋</span>';
  });

  function toast(message) {
    const element = document.getElementById("toast");
    clearTimeout(toastTimer);
    element.textContent = message;
    element.classList.add("visible");
    toastTimer = setTimeout(() => element.classList.remove("visible"), 3000);
  }

  async function share(id) {
    const url = new URL(location.href);
    url.hash = id || "";
    url.search = "";
    const game = data.games.find(item => item.id === id);
    const title = game ? `${game.name} · 提现机制拆解` : data.title;
    const text = game ? `${game.kind}：${game.subtitle}` : `${data.games.length}款游戏的提现机制、结构优点与关键问题。`;
    try {
      await navigator.clipboard.writeText(url.href);
      toast(game ? `${game.name} 单款链接已复制` : "研究页面链接已复制");
    } catch {
      if (navigator.share) {
        try {
          await navigator.share({title, text, url: url.href});
          return;
        } catch (error) {
          if (error.name === "AbortError") return;
        }
      }
      const dialog = document.getElementById("share-dialog");
      const field = document.getElementById("share-url");
      field.value = url.href;
      dialog.showModal();
      field.focus();
      field.select();
    }
  }
  document.querySelectorAll("[data-share]").forEach(button => button.addEventListener("click", () => share(button.dataset.share)));

  function updateProgress() {
    const height = document.documentElement.scrollHeight - innerHeight;
    const progress = height > 0 ? Math.min(100, Math.max(0, scrollY / height * 100)) : 0;
    document.getElementById("read-progress").style.width = `${progress}%`;
  }
  addEventListener("scroll", updateProgress, {passive: true});
  addEventListener("resize", updateProgress);
  document.querySelectorAll("details").forEach(detail => detail.addEventListener("toggle", updateProgress));

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(entries => {
      const visible = entries.filter(entry => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (!visible.length) return;
      const id = visible[0].target.id;
      document.querySelectorAll(".header-inner nav a").forEach(link => {
        if (link.hash === `#${id}`) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      });
    }, {rootMargin: "-15% 0px -55% 0px"});
    document.querySelectorAll("[data-nav]").forEach(section => observer.observe(section));
  }

  let printState;
  addEventListener("beforeprint", () => {
    printState = [...document.querySelectorAll("details")].map(detail => ({detail, open: detail.open}));
    printState.forEach(item => item.detail.open = true);
    cards.forEach(card => card.dataset.printWasHidden = String(card.hidden));
    cards.forEach(card => card.hidden = false);
  });
  addEventListener("afterprint", () => {
    printState?.forEach(item => item.detail.open = item.open);
    cards.forEach(card => card.hidden = card.dataset.printWasHidden === "true");
    updateProgress();
  });
  document.getElementById("print-page").addEventListener("click", () => print());
  update();
  if (location.hash) showHashCase();
})();
