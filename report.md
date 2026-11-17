# 六款游戏 · 假提现逐阶段图解

更新：2026-11-17。在线阅读：https://zyz9408.github.io/withdrawal-patterns/

自然操作、受控回放与反事实回放分别标注；本地页面状态不等于付款或配送。

## Happy Mahjong · 2.4

从显示8关开始，依次追加在线时长、金额、活跃日期与玩家等级。下面把首段等待、奖励过渡和最终空记录也接回同一条流程。

### 提现主线

按原流程的推进顺序阅读。不同本地状态的回放不构成同一个自然玩家的连续实录。

#### 01 第一阶段：显示8关，实际目标40关

![第一阶段实际目标满足后的八个勾](https://zyz9408.github.io/withdrawal-patterns/assets/screens/HM-072-after-phase1-original-completion.webp)
受控回放 · HM-072-after-phase1-original-completion · v2.4

- 玩家看到：满足后，页面显示八个勾。原文承诺完成第8关即可提现全部余额。
- 实际条件：显示目标8；PhaseTask中的实际目标为40个实际关卡。
- 按钮与操作：点击 Withdraw Cash；满足实际目标才启动本阶段的提现表现。
- 接下来：进入 WITHDRAWING 等待页。
- 代码索引：Level8 / actualTargetLevel=40 / displayTargetLevel=8
- 说明：此图为第一段目标已完成的受控原版画面。

#### 02 达标后先显示提现处理中

![第一阶段衔接：WITHDRAWING约20分钟](https://zyz9408.github.io/withdrawal-patterns/assets/screens/HM-073-phase1-completion-original-flow.webp)
受控回放 · HM-073-phase1-completion-original-flow · v2.4

- 玩家看到：WITHDRAWING 与约20分钟倒计时。
- 实际条件：这段计时属于第一阶段后的原版衔接，不等于后面的20分钟活跃任务。
- 按钮与操作：等待原计时完成，按原版后续提示继续。
- 接下来：弹出 Special Bonus 奖励。
- 代码索引：PhaseTask pendingFlow / withdrawing flow

#### 03 提现衔接成新的奖励

![第一阶段Special Bonus27.85](https://zyz9408.github.io/withdrawal-patterns/assets/screens/HM-074-phase1-continue-reward.webp)
受控回放 · HM-074-phase1-continue-reward · v2.4

![领取后进入20分钟第二任务及飞钱动画](https://zyz9408.github.io/withdrawal-patterns/assets/screens/HM-075-phase1-claimed-reward.webp)
受控回放 · HM-075-phase1-claimed-reward · v2.4

- 玩家看到：Special Bonus 27.85；领取后有飞钱表现，钱包改成新的时长任务。
- 实际条件：领取奖励与阶段推进是本地流程；不等于该金额转入支付平台。
- 按钮与操作：领取 Special Bonus。
- 接下来：进入“再玩20分钟提现全部”。
- 代码索引：RunFlow / reward continuation

#### 04 第二阶段：20分钟与消除数量

![第二阶段：20分钟与消除数量](https://zyz9408.github.io/withdrawal-patterns/assets/screens/HM-032-phase2-minute-withdraw-loaded.webp)
受控回放 · HM-032-phase2-minute-withdraw-loaded · v2.4

- 玩家看到：Play 20 more minutes to withdraw all；截图进度为1/20。
- 实际条件：后端是19个60秒在线段；每段还要满足成功消除数量20、21、22、23、25、27、29、32、35、38、42、46、50、55、60、65、71、77、83，合计821次；本段多出的次数不顺延。
- 按钮与操作：继续实际游戏；未满足时点击 Withdraw Cash 只提示当前条件。
- 接下来：时长段和各段消除条件完成后，进入2000金额门槛。
- 代码索引：ActiveMinutes20 / carryEscapesToNextSlot=false

#### 05 第三阶段：累计金额2000

![第三阶段：累计金额2000](https://zyz9408.github.io/withdrawal-patterns/assets/screens/HM-041-Coin2000-withdraw.webp)
受控回放 · HM-041-Coin2000-withdraw · v2.4

- 玩家看到：Reach $2000 to withdraw all instantly；进度为9.09/2000。
- 实际条件：目标是本提现阶段的金额口径2000；不能按 Coin 方法名当作另一套普通金币。
- 按钮与操作：继续积累；条件满足后点击 Withdraw Cash。
- 接下来：追加7天活跃要求。
- 代码索引：Coin2000 / targetCoin=2000

#### 06 第四阶段：7个有效活跃日

![第四阶段：7个有效活跃日](https://zyz9408.github.io/withdrawal-patterns/assets/screens/HM-046-ActiveDays7-withdraw.webp)
受控回放 · HM-046-ActiveDays7-withdraw · v2.4

- 玩家看到：Stay active for 7 days to withdraw all；进度0/7。
- 实际条件：每天至少5次胜利才计作有效日期；按已完成日期去重，不要求连续7天。
- 按钮与操作：跨日期完成每日胜利要求，再点提现。
- 接下来：追加玩家等级30要求。
- 代码索引：ActiveDays7 / requiredWinsPerDay=5

#### 07 第五阶段：要求玩家30级

![第五阶段钱包：要求玩家30级](https://zyz9408.github.io/withdrawal-patterns/assets/screens/HM-061-fifth-phase-withdraw-direct.webp)
受控回放 · HM-061-fifth-phase-withdraw-direct · v2.4

- 玩家看到：Reach Lv.30 to withdraw all instantly；钱包显示1/30。
- 实际条件：玩家等级与提现SDK显示的进度分离。29级累计约745次，29→30还需99999次，累计100744次。
- 按钮与操作：继续升级后重开钱包。
- 接下来：后台等级变化，但钱包进度不跟随变化。
- 代码索引：PlayerLevel30 / BuildWithdrawContext

#### 08 后台29级，钱包仍是1/30

![后台29级时钱包仍1/30](https://zyz9408.github.io/withdrawal-patterns/assets/screens/HM-065-player29-wallet-stable.webp)
受控回放 · HM-065-player29-wallet-stable · v2.4

- 玩家看到：页面继续显示1/30。
- 实际条件：第五阶段传入SDK的 Current 固定为1，Target=30，Normalized=0；截图不是后台等级证明，后台值另有本地状态证据。
- 按钮与操作：达到原等级条件后重新打开钱包。
- 接下来：后台30级时仍保留相同进度。
- 代码索引：Current=1 / Target=30 / Normalized=0

#### 09 后台30级，钱包仍是1/30

![后台已达30时钱包仍1/30](https://zyz9408.github.io/withdrawal-patterns/assets/screens/HM-067-after-original-level30-event.webp)
受控回放 · HM-067-after-original-level30-event · v2.4

- 玩家看到：后台已触发原版30级事件后，页面仍是1/30。
- 实际条件：后台阶段资格可以标记完成，但SDK文本使用固定进度；两种状态不能混为一谈。
- 按钮与操作：点击最终领取。
- 接下来：关闭钱包，回到游戏，阶段条隐藏。
- 代码索引：TryCompleteCurrentPhase / finalQualified

#### 10 最终点击：返回游戏

![最终领取点击后回到游戏、阶段条隐藏](https://zyz9408.github.io/withdrawal-patterns/assets/screens/HM-069-qualified-records.webp)
受控回放 · HM-069-qualified-records · v2.4

- 玩家看到：点击后回到游戏，原阶段任务条隐藏。
- 实际条件：完成最终阶段会置资格标志；当前最终分支没有生成 pendingFlow。RunFlow 收到空流程后返回。
- 按钮与操作：从游戏再次点钱包入口。
- 接下来：重开钱包继续核对记录，而不是出现付款凭证。
- 代码索引：Claim / pendingFlow=null / RunFlow(null)

#### 11 重开钱包与最终记录

![最终资格完成后重开钱包](https://zyz9408.github.io/withdrawal-patterns/assets/screens/HM-070-all-complete-wallet-reopen.webp)
受控回放 · HM-070-all-complete-wallet-reopen · v2.4

![最终仍为空的Records](https://zyz9408.github.io/withdrawal-patterns/assets/screens/HM-071-final-records-entry.webp)
受控回放 · HM-071-final-records-entry · v2.4

- 玩家看到：重新打开钱包，再点 Records，记录页仍为空。
- 实际条件：当前 RecordPop 只绑定关闭操作，没有查到此主线写入真实付款记录的步骤。
- 按钮与操作：关闭 Records 可返回钱包；重开不产生一笔已付款记录。
- 接下来：已追踪客户端路径结束于资格完成与空记录页。
- 代码索引：RecordPop / close binding
- 说明：本地资格、页面关闭和真实到账分别看待。

### 收款信息与返回

这是主线共用的账户编辑分支，完成后回到原阶段。

#### 01 选择收款渠道并填写资料

![选择收款渠道并填写资料](https://zyz9408.github.io/withdrawal-patterns/assets/screens/HM-016-not-qualified.webp)
自然操作 · HM-016-not-qualified · v2.4

![选择收款渠道并填写资料](https://zyz9408.github.io/withdrawal-patterns/assets/screens/HM-019-channel-visa.webp)
自然操作 · HM-019-channel-visa · v2.4

- 玩家看到：Enter details，PayPal / Cash App / VISA / venmo；账户与姓名输入框。
- 实际条件：界面允许切换渠道；研究截图使用虚构资料。
- 按钮与操作：填写账户和姓名，点 Confirm；右上角×取消编辑。
- 接下来：进入二次确认。
- 代码索引：Account detail input

#### 02 二次确认与取消

![二次确认与取消](https://zyz9408.github.io/withdrawal-patterns/assets/screens/HM-023-account-confirm-review.webp)
自然操作 · HM-023-account-confirm-review · v2.4

- 玩家看到：Confirm Details 展示所选平台、账户与姓名。
- 实际条件：这里只确认本地收款资料，未出现支付平台收款证明。
- 按钮与操作：Confirm 保存后回钱包；×取消当前确认弹窗。
- 接下来：回到提现主线的当前阶段，后续条件仍需完成。
- 代码索引：Account confirmation

## Solitaire Money Tree · 1.6

进度能够到100%，之后改为集齐GREAT五个字母。关键卡点在A权重与最后的领取逻辑。

### 进度 → GREAT → 领取

账户编辑、99.99%、100%与最终字母页依次展开。

#### 01 余额与初始提现进度

![提现主页：0%与30美元](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SMT-012-withdraw-direct.webp)
自然操作 · SMT-012-withdraw-direct · v1.6

- 玩家看到：WITHDRAW页面显示30美元、0%进度与账户入口。
- 实际条件：金额显示与提现进度是独立条件，余额并不是立即可支付金额。
- 按钮与操作：先编辑收款账户，再随关卡推进进度。
- 接下来：进入收款平台选择与两次账户输入。
- 代码索引：Withdraw progress

#### 02 八种渠道，账户输入两遍

![八种收款渠道与两次账户输入](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SMT-013-account-selector.webp)
自然操作 · SMT-013-account-selector · v1.6

- 玩家看到：账户选择页有8种渠道与两次账户输入。
- 实际条件：两次账户需一致；截图中的空表单不含真实收款信息。
- 按钮与操作：选择渠道，输入两遍相同账户，点确认。
- 接下来：不一致会提示错误，一致则保存本地账户。
- 代码索引：Account input / repeated value validation

#### 03 账户不一致的错误分支

![两次虚构账户不一致提示](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SMT-015-account-mismatch.webp)
受控回放 · SMT-015-account-mismatch · v1.6

- 玩家看到：两次虚构研究账户不一致时的提示。
- 实际条件：错误不推进提现阶段。
- 按钮与操作：修改为一致的两次输入；关闭则返回编辑。
- 接下来：验证通过后回到提现主页。
- 代码索引：Input mismatch

#### 04 资料保存，继续推进关卡

![本地显示研究账户](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SMT-017-account-saved.webp)
受控回放 · SMT-017-account-saved · v1.6

- 玩家看到：提现主页显示已保存的研究账户。
- 实际条件：保存资料不跳过进度与字母条件。
- 按钮与操作：继续过关，推进顶部进度。
- 接下来：50级显示99.99%，51级到100%。
- 代码索引：Account local save

#### 05 50级：99.99%

![50级：99.99%](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SMT-019-withdraw-99point99.webp)
受控回放 · SMT-019-withdraw-99point99 · v1.6

- 玩家看到：日历页面上方的提现提示显示99.99%。
- 实际条件：50级=99.99%；不是100%永远不可达。截图为顶部进度提示，未把日历误当提现页。
- 按钮与操作：再完成所需关卡，达到51级。
- 接下来：进度到100%，可进入最终步骤。
- 代码索引：GetWithdrawProgress / level50

#### 06 51级：100%，点击提现

![100%进度后WITHDRAW可见](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SMT-020-withdraw-100.webp)
受控回放 · SMT-020-withdraw-100 · v1.6

- 玩家看到：提现进度100%，WITHDRAW按钮可见。
- 实际条件：100%只是前置进度完成。
- 按钮与操作：点击 WITHDRAW。
- 接下来：打开 FINAL STEP 的GREAT字母收集页。
- 代码索引：level51 / progress=100

#### 07 FINAL STEP：集齐GREAT

![最终收集GREAT：五字母灰色](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SMT-021-withdraw-at-full.webp)
受控回放 · SMT-021-withdraw-at-full · v1.6

- 玩家看到：G、R、E、A、T五个字母均灰色，底部CLAIM灰色。
- 实际条件：追踪到的五个字母权重依次为5、4、3、0、1；A的权重为0。
- 按钮与操作：通过原字母奖励入口继续收集。
- 接下来：可以得到其余字母，但当前奖池没有A的自然抽中路径。
- 代码索引：Letter weights [5,4,3,0,1]

#### 08 四个字母点亮，缺A

![四字母已得、A未得](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SMT-022-four-letters-missing-A.webp)
受控回放 · SMT-022-four-letters-missing-A · v1.6

- 玩家看到：G、R、E、T已得到，A仍灰色。
- 实际条件：这张图是本地受控状态展示；“A权重0”来自代码与配置，并非仅靠截图推断。
- 按钮与操作：继续触发同一奖池仍受原权重约束。
- 接下来：无法由已追踪奖池补齐A。
- 代码索引：Letter collection / A=0

#### 09 反事实：五个全齐，CLAIM仍灰

![反事实五字母全得后CLAIM仍灰](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SMT-024-all-five-claim-tap.webp)
反事实回放 · SMT-024-all-five-claim-tap · v1.6

- 玩家看到：即使受控设置五个字母全得，CLAIM仍是灰色。
- 实际条件：此版本最终页没有建立可执行的领奖绑定，只查到关闭操作。受控全齐不能当作自然可达。
- 按钮与操作：尝试原CLAIM入口；关闭按钮可退出。
- 接下来：当前已追踪页面没有继续走到付款完成的回调。
- 代码索引：Final claim UI / close-only binding
- 说明：反事实回放：人为满足原本无法从该奖池获得的全字母状态。

### 关联入口：Money Tree

该入口展示收取与升级；没有把它包装成另一条已证明可付款的提现链。

#### 01 Money Tree：收取与升级

![Money Tree收现升级后的主页](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SMT-026-money-tree-details.webp)
受控回放 · SMT-026-money-tree-details · v1.6

- 玩家看到：树园主页显示收取、升级和货币信息。
- 实际条件：原图支持本地奖励与树升级表现；当前证据不支持将此页当作付款结果。
- 按钮与操作：收取或升级后留在相关奖励系统。
- 接下来：提现仍回到主线进度与GREAT条件。
- 代码索引：Money Tree reward UI

## Rings Cash · 1.0.2

现金主线之外还有手机碎片兑奖和独立转盘礼品，两条奖品线都要继续追到物流终点。

### 现金主线

从关卡资格到VIP、三天视频、审核、付款倒计时、100关与最终队列。

#### 01 入口资格：常见30关，特定状态20关

![30/30达标Cash Out](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-037-wallet-direct.webp)
受控回放 · RC-037-wallet-direct · v1.0.2

![同版本福利1状态下20关提现入口](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-104-online-reward-entry.webp)
受控回放 · RC-104-online-reward-entry · v1.0.2

- 玩家看到：Cash Out显示30/30；同版本福利状态下另有20关入口。
- 实际条件：Enhanced且Welfare1Claimed时使用20关；否则30关。两个画面是不同状态，不是不同版本。
- 按钮与操作：满足当前入口门槛，点击Cash Out。
- 接下来：打开收款账户绑定。
- 代码索引：Enhanced / Welfare1Claimed / level gate

#### 02 输入收款账户

![Mastercard账号输入](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-038-redeem-after-level30.webp)
受控回放 · RC-038-redeem-after-level30 · v1.0.2

- 玩家看到：ORDER或Redeem中的Mastercard账户表单。
- 实际条件：选择的渠道会进入后续账户验证和订单显示。
- 按钮与操作：填写虚构研究账户并确认；×取消则回Cash Out。
- 接下来：不是立即付款，而是出现长队与VIP挑战。
- 代码索引：Account binding

#### 03 验证后长队，转入VIP挑战

![账号验证后长队与VIP挑战](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-043-bind-verification-result.webp)
受控回放 · RC-043-bind-verification-result · v1.0.2

- 玩家看到：账户验证后的长队提示与VIP入口。
- 实际条件：验证成功仅推进本地资格。
- 按钮与操作：点击VIP挑战/继续。
- 接下来：打开1000美元门槛与500美元补偿的界面。
- 代码索引：Bind verification / VIP challenge

#### 04 小额暂停，要求1000美元

![小额暂停、1000美元门槛与500补偿](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-045-vip-stable.webp)
受控回放 · RC-045-vip-stable · v1.0.2

- 玩家看到：小额暂停提示；达到1000美元可提，并显示500美元补偿。
- 实际条件：目标从最初关卡要求转成余额与补偿引导。
- 按钮与操作：完成原补偿领取条件后继续。
- 接下来：弹出500美元补偿确认。
- 代码索引：VIP target=1000 / compensation=500

#### 05 500补偿确认，再回Cash Out

![500美元补偿确认](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-050-compensation-completed.webp)
受控回放 · RC-050-compensation-completed · v1.0.2

![补偿到账户余额后的Cash Out入口](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-051-after-compensation-confirm.webp)
受控回放 · RC-051-after-compensation-confirm · v1.0.2

- 玩家看到：500美元补偿确认；确认后余额增加并返回Cash Out。
- 实际条件：本地余额增加不是收款平台到账。
- 按钮与操作：确认补偿，再点提现。
- 接下来：创建订单，进入120小时45关任务。
- 代码索引：Compensation confirmation

#### 06 120小时内完成45个大关

![120h内达到45大关：已满足](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-057-order45-ready.webp)
受控回放 · RC-057-order45-ready · v1.0.2

- 玩家看到：ORDER REQUEST，45关条件已满足的原版画面。
- 实际条件：订单第一段限120小时；超时会进入失败分支。
- 按钮与操作：条件完成后按原领取/继续按钮。
- 接下来：进入三天任务第1天。
- 代码索引：Order stage1 / 45 levels / 120h
- 说明：图为条件已经满足的受控回放。

#### 07 三天任务：第1天20视频

![三天任务第1天：20视频](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-058-order-stage2-after-redeem.webp)
受控回放 · RC-058-order-stage2-after-redeem · v1.0.2

- 玩家看到：Day 1 task: watch 20 videos。
- 实际条件：第1天视频目标20；另有按日时序的跳过条件10。
- 按钮与操作：完成原视频/时序条件，点击对应继续入口。
- 接下来：进入第2天30视频。
- 代码索引：Day1 / videos20 / skip10

#### 08 三天任务：第2天30视频

![三天任务：第2天30视频](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-059-after-day1-original-advance.webp)
受控回放 · RC-059-after-day1-original-advance · v1.0.2

- 玩家看到：Day 2 task: watch 30 videos。
- 实际条件：第2天视频目标30；对应时序阈值30。
- 按钮与操作：满足第2天条件。
- 接下来：进入第3天100视频。
- 代码索引：Day2 / videos30 / skip30

#### 09 三天任务：第3天100视频

![三天任务：第3天100视频](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-060-after-day2-original-advance.webp)
受控回放 · RC-060-after-day2-original-advance · v1.0.2

- 玩家看到：Day 3 task: watch 100 videos。
- 实际条件：第3天视频目标100；对应时序阈值60。
- 按钮与操作：满足第3天条件。
- 接下来：追加120小时审核。
- 代码索引：Day3 / videos100 / skip60

#### 10 审核：120小时或120视频

![120h审核或120视频](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-061-after-day3-original-advance.webp)
受控回放 · RC-061-after-day3-original-advance · v1.0.2

- 玩家看到：订单审核页显示等待/视频完成路径。
- 实际条件：审核等待120小时，也可按原视频条件推进；完成三天任务并未付款。
- 按钮与操作：等待或满足120视频条件。
- 接下来：进入发送付款的360小时倒计时。
- 代码索引：Review stage / 120h or 120 ads

#### 11 发送付款：360小时

![发送付款：360h倒计时及广告减时](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-063-stage4-after-review.webp)
受控回放 · RC-063-stage4-after-review · v1.0.2

- 玩家看到：Sending payment 与360小时倒计时，视频可缩短等待。
- 实际条件：每次对应广告回调减1小时；这是新的本地等待阶段。
- 按钮与操作：等待倒计时结束或按原广告减时。
- 接下来：继续追加100个大关要求。
- 代码索引：Payment countdown / 360h / 1h per ad

#### 12 倒计时结束，再要求100关

![付款倒计时结束后再要求100大关](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-064-after-payment-countdown.webp)
受控回放 · RC-064-after-payment-countdown · v1.0.2

- 玩家看到：原订单改为完成100个大关才能领取。
- 实际条件：主玩法超过100会回到1；不能随意把MainLevel设置成101来当100关完成证据。
- 按钮与操作：按原Main100与Endless衔接完成条件。
- 接下来：Get按钮可见。
- 代码索引：Main100 / Endless progression

#### 13 100关完成：点击Get

![完成100大关后Get按钮](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-069-completed100-order-open.webp)
受控回放 · RC-069-completed100-order-open · v1.0.2

- 玩家看到：条件完成后Get按钮出现。
- 实际条件：此步骤只通向下一个订单状态。
- 按钮与操作：点击Get。
- 接下来：出现7952人的最终队列。
- 代码索引：Order stage5 → stage6

#### 14 最终队列：7952人

![最终7952人队列](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-070-final-queue-stage6.webp)
受控回放 · RC-070-final-queue-stage6 · v1.0.2

- 玩家看到：排队人数7952，等待提现。
- 实际条件：队列显示=7952−floor(已过毫秒/600000)，约每10分钟减1。
- 按钮与操作：等待原版刷新。
- 接下来：人数可以归零，但没有因此进入已付款状态。
- 代码索引：queue=7952-floor(elapsedMs/600000)

#### 15 队列归零后仍等待

![排队归零仍等待](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-071-final-queue-after365days.webp)
受控回放 · RC-071-final-queue-after365days · v1.0.2

- 玩家看到：把本地订单日期前移365天后，人数归零，仍是等待页面。
- 实际条件：当前已追踪终态没有“队列0→真实付款完成”的客户端分支。
- 按钮与操作：重开订单仍查看该队列状态。
- 接下来：此现金主线停留在等待队列。
- 代码索引：Final queue stage
- 说明：日期前移属于受控回放，不是实际等待365天。

#### 16 失败分支：订单超时

![订单任务超时失败，要求重新申请](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-101-original-order-timeout-failure.webp)
受控回放 · RC-101-original-order-timeout-failure · v1.0.2

![原版重新申请后返回45关任务](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-102-reapply-after-timeout.webp)
受控回放 · RC-102-reapply-after-timeout · v1.0.2

- 玩家看到：任务超时失败，重新申请后又回45关任务。
- 实际条件：过期不会自动结算；重申会重置对应订单任务。
- 按钮与操作：点击重新申请。
- 接下来：回到本主线的120小时45关阶段，重新推进。
- 代码索引：Order timeout / Reapply
- 说明：此步骤是失败回路，不接在最终队列之后。

### 手机碎片兑奖

0→100碎片→地址→20视频审核→物流→退回。

#### 01 碎片从0开始，地图奖励与广告补齐

![手机兑奖中心：0/100及广告碎片](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-072-phone-prize-zero.webp)
受控回放 · RC-072-phone-prize-zero · v1.0.2

- 玩家看到：手机兑奖中心显示0/100，广告碎片入口。
- 实际条件：90以上地图碎片来源停止；广告次数按日期限制，次日仍能补至100，不应概括成永远卡90。
- 按钮与操作：收集地图碎片，在原广告次数限制下继续补齐。
- 接下来：达到100/100，Redeem可用。
- 代码索引：Phone17 fragment reward

#### 02 100碎片：点击Redeem

![手机100/100与Redeem](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-074-phone-fragments100.webp)
受控回放 · RC-074-phone-fragments100 · v1.0.2

- 玩家看到：100/100与Redeem按钮。
- 实际条件：100只满足兑换申请资格。
- 按钮与操作：点Redeem。
- 接下来：打开配送地址表单。
- 代码索引：Phone redeem threshold=100

#### 03 填写配送地址与地区

![配送地址表单上半部](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-075-phone-address-form.webp)
受控回放 · RC-075-phone-address-form · v1.0.2

![配送州/地区选择列表](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-077-address-country-selector.webp)
受控回放 · RC-077-address-country-selector · v1.0.2

![配送地址空字段逐项校验](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-078-address-validation-position.webp)
受控回放 · RC-078-address-validation-position · v1.0.2

- 玩家看到：地址上半部、地区选择、空字段校验。
- 实际条件：必填项校验通过后才保存本地订单；研究不使用真实地址。
- 按钮与操作：填写虚构研究资料并确认；返回可继续编辑。
- 接下来：进入20次广告审核。
- 代码索引：Address validation

#### 04 提交地址后再看20次广告

![手机兑奖广告审核0/20](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-081-phone-review-after-address.webp)
受控回放 · RC-081-phone-review-after-address · v1.0.2

![手机广告审核20/20完成](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-082-phone-ad-review20.webp)
受控回放 · RC-082-phone-ad-review20 · v1.0.2

- 玩家看到：审核进度从0/20到20/20。
- 实际条件：当前版本在该分支激活的是20广告条件；没有把旧72小时分支当作本版本活跃要求。
- 按钮与操作：按原广告回调满足20次，确认继续。
- 接下来：开放原物流入口。
- 代码索引：Current phone review / ads20

#### 05 查看物流：订单已接收

![原物流页：订单已接收](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-087-phone-logistics-stable.webp)
受控回放 · RC-087-phone-logistics-stable · v1.0.2

- 玩家看到：物流初始状态为订单已接收。
- 实际条件：查看物流还包含原广告入口；画面是本地物流模板，不是快递公司扫描证明。
- 按钮与操作：进入Tracking，等待日期推进。
- 接下来：显示运输中节点。
- 代码索引：Local logistics template

#### 06 中段物流：新加坡转运

![同一订单日期前移15天：新加坡转运](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-088-phone-tracking-day15.webp)
受控回放 · RC-088-phone-tracking-day15 · v1.0.2

- 玩家看到：同一订单日期前移15天后，显示新加坡转运节点。
- 实际条件：时间变化驱动本地预置节点。
- 按钮与操作：继续等待。
- 接下来：进入最后的地址错误退回。
- 代码索引：15-day controlled aging

#### 07 终点：地址错误，包裹退回

![同一订单日期前移60天：地址错误退回](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-089-phone-tracking-day60-returned.webp)
受控回放 · RC-089-phone-tracking-day60-returned · v1.0.2

- 玩家看到：同一订单日期前移60天，显示地址错误/退回。
- 实际条件：53个地区的本地时序均终止于地址错误退回；美国模板约61920分钟，另存10–100秒偏移。
- 按钮与操作：再次查看仍按原时间表展示物流节点。
- 接下来：该客户端奖品链的已追踪终点为退回。
- 代码索引：Local shipping timelines
- 说明：受控日期回放不证明真实发货或真实地址校验。

### 独立转盘礼品

SIM/GAID资格入口下的独立系统；不是手机碎片线的下一阶段。

#### 01 转盘入口与环境资格

![受控开放的独立八奖转盘](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-092-sdk-lottery-controlled-entry.webp)
受控回放 · RC-092-sdk-lottery-controlled-entry · v1.0.2

- 玩家看到：原SDK八奖转盘。
- 实际条件：默认无SIM模拟器受SIM/GAID判定限制；此图只受控开放入口资格缓存。当前轮盘8项，配置奖品目录56项。
- 按钮与操作：点击Spin。
- 接下来：首抽得到完整iPhone16Pro礼品弹窗。
- 代码索引：MonetizationServices.OpenLuckyLottery / SIM-GAID gate
- 说明：受控环境资格，不证明自然玩家一定看到该入口。

#### 02 首抽：完整iPhone16Pro

![首抽iPhone16Pro完整礼品弹窗](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-093-lottery-first-spin-result.webp)
受控回放 · RC-093-lottery-first-spin-result · v1.0.2

- 玩家看到：中奖弹窗显示iPhone16Pro。
- 实际条件：此入口首抽使用固定礼品；后续奖励节点为2/5/10/15/20/30/40/50/75/100。
- 按钮与操作：领取/填写配送信息。
- 接下来：打开独立中奖地址表单。
- 代码索引：First-spin fixed prize

#### 03 地址表单与错误提示

![独立转盘中奖地址表单](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-094-lottery-prize-address.webp)
受控回放 · RC-094-lottery-prize-address · v1.0.2

![独立转盘空地址统一错误提示](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-095-lottery-empty-address-validation.webp)
受控回放 · RC-095-lottery-empty-address-validation · v1.0.2

- 玩家看到：独立转盘地址表单；空地址统一错误提示。
- 实际条件：这是转盘SDK自己的表单，与手机碎片线分开保存。
- 按钮与操作：填写虚构研究地址并保存。
- 接下来：My Prizes出现订单入口。
- 代码索引：Lottery address form

#### 04 地址保存，生成奖品订单

![地址保存后My Prizes订单状态入口](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-097-lottery-address-submit-result.webp)
受控回放 · RC-097-lottery-address-submit-result · v1.0.2

![原订单提交成功通知与物流入口](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-098-lottery-first-view-tracking.webp)
受控回放 · RC-098-lottery-first-view-tracking · v1.0.2

- 玩家看到：My Prizes中出现订单；初次查看有原提交成功通知。
- 实际条件：提交成功通知表示本地订单状态变化，不能当作发货凭证。
- 按钮与操作：点击查看Tracking。
- 接下来：进入本地物流页。
- 代码索引：Prize order / My Prizes

#### 05 初始物流与最终退回

![独立转盘首次物流页](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-099-lottery-logistics-initial.webp)
受控回放 · RC-099-lottery-logistics-initial · v1.0.2

![独立转盘60天后固定退回](https://zyz9408.github.io/withdrawal-patterns/assets/screens/RC-100-lottery-order-day60.webp)
受控回放 · RC-100-lottery-order-day60 · v1.0.2

- 玩家看到：初始物流；日期前移60天后同样显示退回。
- 实际条件：转盘礼品也使用本地固定时序，末端为地址错误退回。
- 按钮与操作：按原时间推进再次查看。
- 接下来：奖品链停留在退回状态。
- 代码索引：Lottery local shipping
- 说明：不同入口共用终端模板，不等于同一笔订单。

## Smash Cash · 1.0.3

现金提现与存钱罐利息分开看：现金在审核中不断换状态；利息还要经过四项任务。

### 现金提现与审核

先看余额和账户，再看每一个审核状态。

#### 01 余额入口与高额提现档位

![余额入口与高额提现档位](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SC-003-withdraw-entry.webp)
自然操作 · SC-003-withdraw-entry · v1.0.3

![余额入口与高额提现档位](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SC-004-withdraw-main.webp)
自然操作 · SC-004-withdraw-main · v1.0.3

- 玩家看到：HUD提示距1000美元还有差额；钱包显示2000/3000/4000的后续档位。
- 实际条件：美国主档1000/2000/3000/4000；新手奖励100/60/40。余额≥999.5后奖励区间缩至0–0.01，广告基础0–0.02；区间允许正数，不能证明恒为0。
- 按钮与操作：点Withdraw进入钱包。
- 接下来：先设置收款账户。
- 代码索引：Cash tiers / late reward ranges

#### 02 平台与账户

![平台与账户](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SC-007-account-channels.webp)
自然操作 · SC-007-account-channels · v1.0.3

- 玩家看到：PayPal、amazon、Mastercard与账户输入。
- 实际条件：未填资料时Confirm灰色；可切换平台。
- 按钮与操作：填写虚构研究账号并确认。
- 接下来：回到钱包，满足余额后可申请。
- 代码索引：Monetization account UI

#### 03 1000美元余额：申请确认

![1000美元余额：申请确认](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SC-021-qualified1000-wallet.webp)
受控回放 · SC-021-qualified1000-wallet · v1.0.3

![1000美元余额：申请确认](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SC-024-qualified-withdraw-confirm.webp)
受控回放 · SC-024-qualified-withdraw-confirm · v1.0.3

- 玩家看到：1000美元钱包与Withdraw二次确认，显示平台、账户与时间。
- 实际条件：此图通过本地余额回放达到门槛；不是自然积累1000美元的证据。
- 按钮与操作：点Confirm提交。
- 接下来：余额扣除，出现In Progress。
- 代码索引：Withdraw confirmation / target1000

#### 04 审核0：In Progress

![审核0：In Progress](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SC-025-submission-response.webp)
受控回放 · SC-025-submission-response · v1.0.3

- 玩家看到：已提交申请，提示等待审核1–7天。
- 实际条件：原本地申请有requestId与stageStartedUtc；阶段0等待，每次检查重新抽12–24小时门槛。
- 按钮与操作：关闭弹窗，稍后通过View重看。
- 接下来：条件满足后变成Account Under Review。
- 代码索引：reviewStage0 / [12,24)h

#### 05 审核1：Account Under Review

![审核1：Account Under Review](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SC-040-review-aging1-detail.webp)
受控回放 · SC-040-review-aging1-detail · v1.0.3

- 玩家看到：首档出现Account Under Review与View。
- 实际条件：只前移本地阶段开始时间，阶段由原版检查推进；阶段1每次检查重新抽24–48小时。
- 按钮与操作：点View查看；达到时序门槛继续推进。
- 接下来：变为Bank Review状态。
- 代码索引：reviewStage1 / [24,48)h

#### 06 审核2：Bank Review

![审核2：Bank Review](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SC-051-bank-top.webp)
受控回放 · SC-051-bank-top · v1.0.3

- 玩家看到：原代码的银行审核阶段。
- 实际条件：阶段2每次检查重新抽48–72小时门槛。
- 按钮与操作：通过原View/刷新触发检查。
- 接下来：推进到Approved Payment Pending。
- 代码索引：reviewStage2 / [48,72)h
- 说明：原版阶段2界面已补采；本地状态受控，不代表银行真实审核。

#### 07 审核3：Approved Payment Pending

![审核3：Approved Payment Pending](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SC-042-review-aging3-detail.webp)
受控回放 · SC-042-review-aging3-detail · v1.0.3

- 玩家看到：首档显示Approved Payment Pending与View。
- 实际条件：阶段3后当前推进逻辑停止；Approved与Paid不是一个状态。
- 按钮与操作：继续等待、重开钱包仍由本地状态渲染。
- 接下来：当前已追踪现金链停在“批准，待支付”。
- 代码索引：reviewStage3 / terminal pending
- 说明：截图为受控日期推进后的原版显示。

### 存钱罐利息提现

利息任务与现金审核是两条不同链。四项任务、最终确认和提交记录均附原版回放截图。

#### 01 利息累积

![利息累积](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SC-052-interest-entry.webp)
受控回放 · SC-052-interest-entry · v1.0.3

- 玩家看到：主界面Interest入口与存钱罐余额。
- 实际条件：每次增加max(float32(0.01), float32(奖励)×0.1)；提交后停止继续累计。
- 按钮与操作：打开Interest查看提现任务。
- 接下来：先进入100次奖励任务。
- 代码索引：PiggyIncrement

#### 02 任务1：领取奖励100次

![任务1：领取奖励100次](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SC-053-piggy-task1.webp)
受控回放 · SC-053-piggy-task1 · v1.0.3

- 玩家看到：第一项任务是奖励次数。
- 实际条件：目标是100次reward事件。
- 按钮与操作：完成后触发原任务刷新。
- 接下来：下一次调用才推进下一项任务。
- 代码索引：Piggy rewardCount100

#### 03 任务2：存钱罐广告30次

![任务2：存钱罐广告30次](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SC-061-piggy-ads-ready.webp)
受控回放 · SC-061-piggy-ads-ready · v1.0.3

- 玩家看到：第二项任务是存钱罐广告。
- 实际条件：只计此处的广告计数，目标30。
- 按钮与操作：按原广告回调完成。
- 接下来：追加存钱罐金额门槛。
- 代码索引：Piggy adCount30

#### 04 任务3：存钱罐余额

![任务3：存钱罐余额](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SC-055-piggy-balance.webp)
受控回放 · SC-055-piggy-balance · v1.0.3

- 玩家看到：第三项检查存钱罐余额。
- 实际条件：目标按国家配置，美国为170；不是主钱包1000美元余额。
- 按钮与操作：累积至对应金额并刷新任务。
- 接下来：追加7天登录。
- 代码索引：Piggy country target / US170

#### 05 任务4：登录7天

![任务4：登录7天](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SC-056-piggy-login.webp)
受控回放 · SC-056-piggy-login · v1.0.3

![任务4：登录7天](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SC-058-piggy-ready-clean.webp)
受控回放 · SC-058-piggy-ready-clean · v1.0.3

- 玩家看到：最后一项任务是登录天数。
- 实际条件：完整链包含4项；一次推进调用最多前进一项。
- 按钮与操作：满足7天后按原提交按钮。
- 接下来：本地记录InProgress并清空存钱罐余额。
- 代码索引：Piggy loginDays7

#### 06 提交后的付款展示

![提交后的付款展示](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SC-059-piggy-submit.webp)
受控回放 · SC-059-piggy-submit · v1.0.3

![提交后的付款展示](https://zyz9408.github.io/withdrawal-patterns/assets/screens/SC-060-piggy-local-record.webp)
受控回放 · SC-060-piggy-local-record · v1.0.3

- 玩家看到：利息申请处于处理中/支付展示。
- 实际条件：保存金额、日期、submitted=true，余额清零；InterestUIActiveStage固定返回2，不能当作实际转账。
- 按钮与操作：重开Interest查看本地已提交状态。
- 接下来：已追踪链只证明本地提交与展示。
- 代码索引：InterestUIActiveStage=2
- 说明：该分支未证明自然任务全达标与真实支付。

## Pixel Sand Puzzle · 1.0.4

从0.01提示到5关、20分钟、48小时，再以额度已满重新申请，最后进入要求玩家30级的队列。

### 提现主线

把账户往返、首次申请、失败后的二次审核和队列连起来。

#### 01 首关出现0.01美元提示

![首关可提0.01美元提示](https://zyz9408.github.io/withdrawal-patterns/assets/screens/PSP-006-cashout-page.webp)
自然操作 · PSP-006-cashout-page · v1.0.4

- 玩家看到：首关可提0.01美元的原版弹窗。
- 实际条件：这是小额提现引导，不能从提示推断已到账。
- 按钮与操作：点提现进入账户表单；关闭则返回游戏。
- 接下来：设置支付渠道与资料。
- 代码索引：First-level small cash prompt

#### 02 选择渠道并输入资料

![PayPal收款信息输入](https://zyz9408.github.io/withdrawal-patterns/assets/screens/PSP-043-direct-current.webp)
受控回放 · PSP-043-direct-current · v1.0.4

![Revolut渠道输入字段](https://zyz9408.github.io/withdrawal-patterns/assets/screens/PSP-044-revolut-fields.webp)
受控回放 · PSP-044-revolut-fields · v1.0.4

![Cash App渠道输入字段](https://zyz9408.github.io/withdrawal-patterns/assets/screens/PSP-045-cashapp-fields.webp)
受控回放 · PSP-045-cashapp-fields · v1.0.4

- 玩家看到：PayPal、Revolut、Cash App各自输入页。
- 实际条件：不同渠道字段不同。
- 按钮与操作：填入虚构研究账户；点击继续。
- 接下来：空值会被校验，合法形式进入确认页。
- 代码索引：Account channel input

#### 03 空值校验与二次确认

![空收款信息校验](https://zyz9408.github.io/withdrawal-patterns/assets/screens/PSP-046-empty-account-validation.webp)
受控回放 · PSP-046-empty-account-validation · v1.0.4

![Confirm again二次账户确认](https://zyz9408.github.io/withdrawal-patterns/assets/screens/PSP-054-account-next-state.webp)
受控回放 · PSP-054-account-next-state · v1.0.4

![Re-enter返回并保留信息](https://zyz9408.github.io/withdrawal-patterns/assets/screens/PSP-055-account-reenter.webp)
受控回放 · PSP-055-account-reenter · v1.0.4

- 玩家看到：空资料错误；Confirm again；Re-enter返回时保留原输入。
- 实际条件：二次确认可取消回编辑，不重置填写内容。
- 按钮与操作：Confirm继续；Re-enter返回修改。
- 接下来：创建本地申请，展示5关审核条件。
- 代码索引：Confirm again / Re-enter

#### 04 提交后要求先完成5个显示关

![审核中：要求先过第5显示关](https://zyz9408.github.io/withdrawal-patterns/assets/screens/PSP-058-payout-processing-settled.webp)
受控回放 · PSP-058-payout-processing-settled · v1.0.4

![Cash主页面：1/5进度与1.95美元余额](https://zyz9408.github.io/withdrawal-patterns/assets/screens/PSP-026-cash-main-confirmed.webp)
受控回放 · PSP-026-cash-main-confirmed · v1.0.4

- 玩家看到：审核中要求先过第5显示关；Cash主页进度1/5。
- 实际条件：前5个显示关实际分配16个原始关卡；显示5覆盖原始6–16。
- 按钮与操作：完成原始关卡，重看申请记录。
- 接下来：申请记录追加20分钟有效时长。
- 代码索引：Display-level map / raw level6–16

#### 05 记录追加20分钟

![原参数记录显示追加20分钟要求](https://zyz9408.github.io/withdrawal-patterns/assets/screens/PSP-068-full-record-replay-list.webp)
受控回放 · PSP-068-full-record-replay-list · v1.0.4

- 玩家看到：原申请记录显示在线/有效游戏20分钟要求。
- 实际条件：有效时间=floor(活跃秒数×0.7)；累计1200有效秒约需28分35秒实际活跃。
- 按钮与操作：继续在原有效计时范围内游戏。
- 接下来：原回调将记录起始时间重置，再显示48小时等待。
- 代码索引：TimeStageManager / valid=floor(active×0.7)

#### 06 时长完成：再等48小时

![有效时长完成后改为48小时内成功](https://zyz9408.github.io/withdrawal-patterns/assets/screens/PSP-077-record-review-after-time.webp)
受控回放 · PSP-077-record-review-after-time · v1.0.4

- 玩家看到：记录改为48小时内成功/处理中。
- 实际条件：48小时从完成有效时长时重新计起，不能把最初申请时间直接算作已满足。
- 按钮与操作：等待，重开申请记录。
- 接下来：以额度已满失败，要求换银行。
- 代码索引：recordTime reset / wait48h

#### 07 48小时后：额度已满

![额度已满失败，更换银行重新申请](https://zyz9408.github.io/withdrawal-patterns/assets/screens/PSP-081-expired-full-record-entry.webp)
受控回放 · PSP-081-expired-full-record-entry · v1.0.4

- 玩家看到：额度已满或银行限额的失败提示。
- 实际条件：失败不会结束条件链，原路径提供换银行重新申请。
- 按钮与操作：点击换银行/重新申请。
- 接下来：开启第二次银行审核，追加显示18关要求。
- 代码索引：Quota fail / change bank

#### 08 二次申请：要求显示18关

![银行审核：追加第18显示关要求](https://zyz9408.github.io/withdrawal-patterns/assets/screens/PSP-083-retry-requirements.webp)
受控回放 · PSP-083-retry-requirements · v1.0.4

- 玩家看到：银行审核提示需达到第18显示关。
- 实际条件：该要求与最初5关不同，是失败后新增门槛。
- 按钮与操作：达标后进入原申请记录继续。
- 接下来：进入固定人数队列，同时要求玩家30级。
- 代码索引：Bank review / display level18

#### 09 进入队列：还需玩家30级

![固定队列：当前玩家13/30级](https://zyz9408.github.io/withdrawal-patterns/assets/screens/PSP-087-after-eighteen-record-click.webp)
受控回放 · PSP-087-after-eighteen-record-click · v1.0.4

- 玩家看到：队列页与当前玩家13/30级。
- 实际条件：队列人数使用固定9812/8632显示，不是已证明存在的真实用户队列。
- 按钮与操作：继续升级后重看该记录。
- 接下来：原等级函数的返回上限成为最终阻断。
- 代码索引：Queue fixed9812/8632 / required user level30

#### 10 最终：最高返回28，仍要求30

![最终排队要求30级，原函数最高只能28级](https://zyz9408.github.io/withdrawal-patterns/assets/screens/PSP-091-level28-final-queue.webp)
受控回放 · PSP-091-level28-final-queue · v1.0.4

- 玩家看到：原版队列中当前玩家28级，目标仍30级。
- 实际条件：等级表29与30的TotalLevel都为1000002380；函数返回首个更大阈值的前一级，耗尽返回1，因此当前表最高可返回28。
- 按钮与操作：继续套用当前原表无法得到30级。
- 接下来：此已追踪分支无法跨过玩家30级条件。
- 代码索引：UserLv.GetUserLv / duplicated terminal thresholds
- 说明：这与“升级非常慢”不同，是当前函数与表的返回域不包含30。

### 关联奖励与额外门槛

保留奖励入口与提现资格的关联，不把未找到入口的配置做成假页面。

#### 01 Lucky reward：广告档与普通档

![Lucky reward广告高额与普通低额领取](https://zyz9408.github.io/withdrawal-patterns/assets/screens/PSP-074-record-after-time-progress.webp)
受控回放 · PSP-074-record-after-time-progress · v1.0.4

![普通奖励领取动画](https://zyz9408.github.io/withdrawal-patterns/assets/screens/PSP-075-after-lucky-base-claim.webp)
受控回放 · PSP-075-after-lucky-base-claim · v1.0.4

- 玩家看到：Lucky reward有广告高额与普通领取；普通领取后出现奖励动画。
- 实际条件：普通基础奖励与广告奖励不同，不是付款结果。
- 按钮与操作：选择普通领取可继续游戏。
- 接下来：仍回到上面的提现条件链。
- 代码索引：Lucky reward UI

#### 02 签到与相册配置的边界

**仅代码/配置，尚无该项原图。**

- 玩家看到：签到奖励的提现资格还有玩家30级要求；相册未确认独立入口。
- 实际条件：美国签到配置显示20/50/100/200/300，实际奖励配置为0.01/0/0/0/0，后四档再要求玩家30级。相册仅发现配置。
- 按钮与操作：当前等级函数不能返回30；不能假设相册配置一定有玩家可见的独立流程。
- 接下来：未发现的原UI保留为空，不制作仿图。
- 代码索引：Sign-in config / album config
- 说明：此项仅代码与配置，缺少对应原界面。

## Crazy Water Puzzle · 1.0.0

原版当前显示日语、日元，旁注提供中文解释。主线先用关卡与小额申请引导，再追加隐藏关卡、动态金额、有效天数和玩家等级。

### 关卡 → 金额 → 天数 → 等级

保留原版语言与货币。US配置金额与本次日语截图分开注明；回放不是一段自然连续通关记录。

#### 01 首次欢迎：承诺全阶段后全额提现

![首次欢迎：承诺全阶段后全额提现](https://zyz9408.github.io/withdrawal-patterns/assets/screens/CW-001-first-hud.webp)
自然操作 · CW-001-first-hud · v1.0.0

- 玩家看到：欢迎页画出1–5阶段路线，几个节点标“全额出金”。
- 实际条件：界面展示的5个节点，不等于后端只有5个枚举状态；EMergeSortStep有9个值，引导另有57个状态。
- 按钮与操作：点开始，按原版倒水引导进入游戏。
- 接下来：主界面显示余额、出金按钮与当前关卡。
- 代码索引：EMergeSortStep / EGuideType

#### 02 早期第1段：过关与小额申请

![早期第1段：过关与小额申请](https://zyz9408.github.io/withdrawal-patterns/assets/screens/CW-020-stage1.webp)
受控回放 · CW-020-stage1 · v1.0.0

- 玩家看到：Lv1钱包，1关目标与出金按钮。
- 实际条件：包内US第1段金额0.18、Condition_1=1；当前原版日语货币显示日元，图中18是受控余额，不是已到账。
- 按钮与操作：满足原关卡/引导后点击出金。
- 接下来：进入账户、二次确认与本地成功展示；完整表单见“收款确认”分支。
- 代码索引：Step1 / US value0.18

#### 03 早期第2段：再次要求过关

![早期第2段：再次要求过关](https://zyz9408.github.io/withdrawal-patterns/assets/screens/CW-021-stage2.webp)
受控回放 · CW-021-stage2 · v1.0.0

- 玩家看到：Lv2钱包，进度1/2，再过1关。
- 实际条件：包内US第2段value0.24、Condition_1=2；小额申请与本地记录有独立引导状态。
- 按钮与操作：完成对应条件后再次申请。
- 接下来：后面继续出现5关、15关和全额目标，不以小额成功页结束。
- 代码索引：Step2 / US value0.24

#### 04 Step3：先达到显示5关

![Step3：先达到显示5关](https://zyz9408.github.io/withdrawal-patterns/assets/screens/CW-016-stage3-ready.webp)
受控回放 · CW-016-stage3-ready · v1.0.0

- 玩家看到：当前Lv3，提现进度2/5，提示还需3关。
- 实际条件：隐藏关卡表用max(1,实际关卡−3)查询；显示5覆盖查表原始7–22，对实际关卡还要加入口偏移3。
- 按钮与操作：按原关卡条件继续完成。
- 接下来：下一段改成显示15关。
- 代码索引：GetHideLevelData / HideMax1=5

#### 05 Step4：门槛改成显示15关

![Step4：门槛改成显示15关](https://zyz9408.github.io/withdrawal-patterns/assets/screens/CW-022-stage4.webp)
受控回放 · CW-022-stage4 · v1.0.0

- 玩家看到：Lv6钱包，进度5/15，还需10关。
- 实际条件：显示15覆盖表内原始39–50，实际入口同样另有−3偏移；不能把显示15当作只玩15个实际关卡。
- 按钮与操作：继续过关。
- 接下来：过完显示15段后，追加动态金额目标。
- 代码索引：HideMax2=15 / hidden-level map

#### 06 Step5：追加动态金额

![Step5：追加动态金额](https://zyz9408.github.io/withdrawal-patterns/assets/screens/CW-023-stage5.webp)
受控回放 · CW-023-stage5 · v1.0.0

- 玩家看到：提现页要求余额达到200000日元；当前25/200000。
- 实际条件：目标由GameYETargetManager依当前余额及地区参数生成；不是所有玩家固定这个数。还要求引导枚举>45。
- 按钮与操作：积累到当前原目标，再点出金。
- 接下来：转入5个有效日期与每天10关任务。
- 代码索引：TargetCoinData / IsCompleteTargetLimit

#### 07 Step6：5天，每天10关

![Step6：5天，每天10关](https://zyz9408.github.io/withdrawal-patterns/assets/screens/CW-026-stage6-open.webp)
受控回放 · CW-026-stage6-open · v1.0.0

![Step6：5天，每天10关](https://zyz9408.github.io/withdrawal-patterns/assets/screens/CW-027-daily-task.webp)
受控回放 · CW-027-daily-task · v1.0.0

- 玩家看到：0/5天；今天还需10关。审核弹窗已经画出“批准”“本人确认完成”，最后再挂5天认证。
- 实际条件：总有效日期目标5，每日通关目标10。原AddTotal_LoginDayCount只在Step6/7计入，并按日期去重；只打开游戏不算当天完成。
- 按钮与操作：完成今日10关；关闭弹窗回游戏可继续累计。
- 接下来：今日满足而总天数不足时进入Step7等待后续日期。
- 代码索引：MaxLoginDay=5 / Total_ToDay_Level=10

#### 08 Step7：当天完成，等待后续日期

![Step7：当天完成，等待后续日期](https://zyz9408.github.io/withdrawal-patterns/assets/screens/CW-044-day1-wallet.webp)
受控回放 · CW-044-day1-wallet · v1.0.0

- 玩家看到：当天条件完成后的原版登录任务/等待显示。
- 实际条件：这是第6、7枚举间的日循环；次日重置当天关卡计数，完成后再增加一个有效日。
- 按钮与操作：跨日期完成任务，直到5个有效日。
- 接下来：又追加玩家等级30。
- 代码索引：Step6 ↔ Step7 / date deduplication

#### 09 Step8：天数完成后再要求玩家30级

![Step8：天数完成后再要求玩家30级](https://zyz9408.github.io/withdrawal-patterns/assets/screens/CW-029-user-level30.webp)
受控回放 · CW-029-user-level30 · v1.0.0

- 玩家看到：主钱包进度6/30；继续承诺达到Lv30全额出金。
- 实际条件：此处的玩家等级由UserLv配置计算，与标题上的关卡Lv16分开。
- 按钮与操作：继续提升实际关卡数，查看原等级函数能返回的最高值。
- 接下来：原表最高返回28，门槛仍未满足。
- 代码索引：GetGameUserLV / UserMaxLv30

#### 10 最终阻断：28/30，与严格大于30

![最终阻断：28/30，与严格大于30](https://zyz9408.github.io/withdrawal-patterns/assets/screens/CW-030-user-level28.webp)
受控回放 · CW-030-user-level28 · v1.0.0

![最终阻断：28/30，与严格大于30](https://zyz9408.github.io/withdrawal-patterns/assets/screens/CW-031-level-final-check.webp)
受控回放 · CW-031-level-final-check · v1.0.0

- 玩家看到：钱包进度28/30；点击后仍显示“最后一步，马上入金”，并要求Lv30认证。
- 实际条件：表中29与30的TotalLevel都为1000002804；首个更大阈值返回lv−1，耗尽返回1，最高返回28。GetIsFinishGameLevel更要求玩家等级严格>30；GetEMergeSortStep在≤30时保持Step8。
- 按钮与操作：继续使用当前原表无法得到30或>30。
- 接下来：Step9不能由这份包内等级表自然推进；没有伪造一张可达Step9截图。
- 代码索引：GetUserLv0xEC7CA8 / GetIsFinishGameLevel0xEDF2D0
- 说明：原钱包已补拍；只修改运行数据展示边界，未修改原算法。

### 收款确认与“成功”页

这是早期申请共用的原版页面。此回放使用全0无效号码，提交金额为0，不能当作小额到账实录。

#### 01 选择渠道与填写资料

![选择渠道与填写资料](https://zyz9408.github.io/withdrawal-patterns/assets/screens/CW-034-first-account.webp)
受控回放 · CW-034-first-account · v1.0.0

- 玩家看到：当前地区提供LINE Pay、PayPay；姓名与+81号码输入框。
- 实际条件：原版按地区选择渠道和字段。研究使用ResearchStudy与全0无效号码。
- 按钮与操作：填写后按确认；×关闭可取消。
- 接下来：进入二次核对。
- 代码索引：UserTakeOutInfoData / regional input rules

#### 02 二次确认，允许重新输入

![二次确认，允许重新输入](https://zyz9408.github.io/withdrawal-patterns/assets/screens/CW-038-second-confirm.webp)
受控回放 · CW-038-second-confirm · v1.0.0

- 玩家看到：展示虚构姓名、全0号码；绿色立即出金、蓝色重新输入。
- 实际条件：重新输入返回表单；确认继续本地申请流程。
- 按钮与操作：点立即出金。
- 接下来：进入本地审核表现。
- 代码索引：Confirm input / Re-enter

#### 03 审核勾选与出金按钮

![审核勾选与出金按钮](https://zyz9408.github.io/withdrawal-patterns/assets/screens/CW-040-first-result.webp)
受控回放 · CW-040-first-result · v1.0.0

- 玩家看到：三项审核出现完成标记和出金按钮；本次回放金额0。
- 实际条件：原界面可以显示审核完成；实际执行的确认代码先设置record.isTx=true，再SetTakeOutLogData保存PlayerPrefs。
- 按钮与操作：点击原出金按钮。
- 接下来：打开出金成功面板。
- 代码索引：Confirm callback0xF24B10 / SetTakeOutLogData0xEFD688
- 说明：0金额受控回放，只展示本地UI与回调，不代表早期默认奖励金额。

#### 04 “出金成功”，再写1–7天到账

![“出金成功”，再写1–7天到账](https://zyz9408.github.io/withdrawal-patterns/assets/screens/CW-041-day-ready.webp)
受控回放 · CW-041-day-ready · v1.0.0

- 玩家看到：成功页金额0，文案说申请完成、预计1–7日内到账。
- 实际条件：这张原界面支持“出现成功显示”；追踪回调是本地记录，并未证明支付平台完成转账。
- 按钮与操作：OK关闭成功页并衔接后续关卡。
- 接下来：主线继续5关、15关、金额、天数、等级条件。
- 代码索引：Success button0xF22A5C / local saved record
- 说明：受控0金额原版页面，不能作为自然提现或到账证明。

### 关联展示：他人提现播报

这些播报与本人申请记录分开。

#### 01 他人成功播报由本地拼接

![他人成功播报由本地拼接](https://zyz9408.github.io/withdrawal-patterns/assets/screens/CW-004-first-stage-next.webp)
自然操作 · CW-004-first-stage-next · v1.0.0

- 玩家看到：顶部庆祝弹条称某Player提取了一笔钱。
- 实际条件：SetNoticeData使用RandomChannel、两次随机字母拼接用户名与本地DM配置金额，不能作为其他玩家真实收到钱的证据。
- 按钮与操作：播报自动出现/消失。
- 接下来：与本人提现条件没有真实付款校验关系。
- 代码索引：SetNoticeData0xF2E6C8 / GetUserName0xEBCF2C
