# 五款游戏的提现机制拆解

一份可分享的中文研究网页，对比 Happy Mahjong、Solitaire Money Tree、Rings Cash、Smash Cash、Pixel Sand Puzzle 的提现机制、结构优点与关键问题。

线上页面：https://zyz9408.github.io/withdrawal-patterns/

## 内容与功能

- 五款同版本研究的对比总览与详细拆解。
- 机制筛选、文字搜索、可展开的代码依据。
- 整页与单款锚点分享、文字版下载、打印/PDF布局。
- 响应式布局、键盘导航和减少动效支持。
- 结论限定同版本代码、配置和已有取证，经营效果单独标为未知。

## 编辑

内容维护在 `data/research.json`。修改后使用 Python 3 运行：

```powershell
python build.py
```

`build.py` 只依赖标准库，生成 `index.html` 与 `report.md`。样式在 `styles.css`，交互在 `app.js`。网页运行不需要构建工具、框架、数据库或外部CDN。

## GitHub Pages

从 `main` 分支根目录发布；`.nojekyll` 保持静态文件直接提供。更新后提交并推送即可触发GitHub Pages部署。

## 研究边界

历史受控状态不等于自然达标、实际收款或真实配送。部分结论只针对已追踪的本地路径。没有各款实际CPI、净eCPM和成熟留存数据，不作LTV、ROI或回本能力排名。
