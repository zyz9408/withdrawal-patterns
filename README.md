# 六款游戏 · 假提现逐阶段图解

一份以原界面截图为主体的中文研究网页。覆盖 Happy Mahjong、Solitaire Money Tree、Rings Cash、Smash Cash、Pixel Sand Puzzle、Crazy Water Puzzle 的提现主线、账户确认、审核、队列与相关奖品物流。

线上页面：https://zyz9408.github.io/withdrawal-patterns/

## 内容与功能

- 六款游戏、14条流程、91个阶段、114张经过核对的原界面截图。
- 每步包括玩家看到的画面、实际条件、按钮动作和后续去向。
- 游戏与支线切换、阶段目录、阶段直达链接与分享。
- 多图切换、无损原尺寸大图、逐张查看与Markdown图文下载。
- 失败重申、取消/返回和最终状态分别说明；原有比较收进折叠附录。
- 响应式布局、键盘导航和减少动效支持。
- 结论限定同版本代码、配置和已有取证，经营效果单独标为未知。

## 编辑

阶段内容维护在 `data/flows.json`，附录依据在 `data/research.json`。修改后使用 Python 3 运行：

```powershell
python build.py
```

`build.py` 调用 `flow_page.py`，只依赖标准库，生成 `index.html` 与 `report.md`。样式在 `reader.css`，交互在 `reader.js`。网页运行不需要框架、数据库或外部CDN。

`assets/screens/` 仅保存已经挑选的公开图片。完整尺寸为无损WebP，缩略图用于预览；阶段数据附原PNG的SHA-256和版本。APK、提取代码、真实账号、设备信息和本地状态备份不进入此仓库。

## GitHub Pages

从 `main` 分支根目录发布；`.nojekyll` 保持静态文件直接提供。更新后提交并推送即可触发GitHub Pages部署。

## 研究边界

历史受控状态不等于自然达标、实际收款或真实配送。部分结论只针对已追踪的本地路径。没有各款实际CPI、净eCPM和成熟留存数据，不作LTV、ROI或回本能力排名。

Crazy Water Puzzle 1.0.0 已补充原版逐阶段受控回放，保留当前日语/日元界面并加中文说明。收款确认的0金额回放已单独说明，不能当作自然小额到账。

唯一没有原图的项是Pixel Sand Puzzle的签到/相册配置补充；未确认的入口不制作仿图。当前已追踪提现主线及Smash Cash存钱罐四任务均有对应截图。
