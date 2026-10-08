# DormMate 综合工程作品 · 任务解读与实施指南

> 依据：《NOVA C01｜DormMate 综合工程作品任务书》V0.8R5（2026 年 9 月）
> 说明：文中的阈值、Topic、文件名、权重等都是**建议方案**，可以按自己的设计调整，但必须能说清"为什么这样做"。**状态阈值请替换为 C01 统一练习规则。**

---

## 0. 一句话看懂这份任务书

**你要一个人**把 C01 学过的 Web、Python 数据分析、MQTT/JSON、移动端（小程序/H5）、Three.js 3D、Camera/ASR/TTS、Isolation Forest，重新组织成**一个**真正能运行的 DormMate 系统；用"三个宿舍在线 → 某宿舍持续异常 → 系统判定优先关注 → 用户处理 → 后续数据验证恢复 → 复盘"这一条完整故事证明系统成立；最后交齐 GitHub 仓库、README、Evidence、PPT、技术文档、演示视频，并通过现场 **Run / Explain / Modify / Debug / Verify** 核验。

| 项目 | 内容 |
|---|---|
| 作品题目 | DormMate：面向多宿舍节点的环境状态感知、事件响应与多端协同系统 |
| 完成方式 | 个人独立完成、独立提交 |
| 允许 | 查文档、搜资料、用 AI、参考开源、和同学交流思路 |
| 前提 | 所有提交物必须本人能完整运行、解释、修改、排错、验证 |
| 不提供 | 逐步教程、成品代码、统一界面（不要求大家做得一样） |
| 评价顺序 | 先"基本完成"（门槛）→ 再看"高质量表现" → 再看"竞赛亮点" |

---

## 1. 任务要求总览（它到底要你做什么）

### 1.1 作品公式

```
1 个完整系统 + 2 条真实数据链 + 多个协同入口 + 1 套事件处理机制
```

关键词：**不是多个作业拼起来**，而是所有模块围绕同一个 DormMate 系统、同一套实时状态协同工作。

### 1.2 数据基础

- 至少 3 个模拟宿舍节点：`dorm-a`、`dorm-b`、`dorm-c`
- 每条节点数据至少包含：`nodeId`、`temperature`、`humidity`、`status`、`time`
- 状态规则沿用 C01 统一练习规则；如果改进，必须明确、可解释、可验证

### 1.3 两条必须真正跑通的数据链

| 数据链 | 路径 | 硬性要求 |
|---|---|---|
| A · 离线分析链 | Web/历史记录 → CSV → Python → 统计/趋势 → `report.html` | 数据来自真实运行或**明确标注**的模拟运行；换一份 CSV 能重新生成报告；报告**不能手工改结果** |
| B · 实时系统链 | 模拟节点 → MQTT/JSON → 共享实时状态 → Web/Dashboard + 移动端 + 3D | ≥3 节点；节点数据**不串线**；新消息到达后多端围绕同一状态更新；各端**共享同一数据源** |

### 1.4 多端分工（不是复制页面）

| 入口 | 承担的任务 |
|---|---|
| Web / Dashboard | 多节点实时总览、重点节点、趋势、事件状态 |
| 移动端 | 快速查看当前重点、最新状态、必要操作 |
| 3D | 节点与空间对象对应，用可视方式表达重点、状态和处理过程 |
| TTS | 朗读当前真实状态或事件信息 |
| Camera | 记录与当前节点/事件相关的现场快照 |
| report.html | 历史分析、事件时间线、今日摘要与复盘 |

> 界面可以调整，但要能解释为什么这样分工。

### 1.5 全部必做：5 个场景 + 3 个增强

| 编号 | 名称 | 核心要求 | 做到这里才算完成 |
|---|---|---|---|
| D1 | 多节点稳定运行 | 3 节点同时在线；Web、移动端、3D 看到同一批节点的最新状态；不串线 | 现场随机改任意节点数据后，三端都能识别为同一节点的新状态，核心数据一致 |
| D2 | 持续异常与优先关注 | 多个宿舍不同程度异常时，按**写在程序里**的规则给出"当前优先关注：xxx"并说明理由 | 准备 3 组不同的三节点情况，优先对象和依据都跟着变；**不能写死 dorm-b** |
| D3 | 处理—验证—恢复 | 发现 → 优先关注 → 用户处理 → 后续数据验证 → 恢复/未恢复 → 记录复盘 | 演示 1 次：异常 → 处理 → **至少 2 组后续新数据** → 恢复/未恢复 → 事件记录 |
| D4 | 实时链路故障与修复 | 主动制造 ≥1 类故障（停 Broker、写错 Topic、错误 JSON、改错字段名、节点长时间不发数据） | 观察现象 → 定位原因 → 修复 → 重新运行 → 验证恢复，并在文档/视频中保留过程 |
| D5 | 固定规则 + ML 辅助判断 | Rule 与轻量 ML 并列，同时显示温湿度、Rule 判断、ML 判断、是否一致 | 至少保留 1 个"值得分析"的案例并解释原因 |
| E1 | 3D 数字空间增强 | 实时数据驱动、可交互、有展示亮点的多节点 3D | 满足 7 条最低完成线（见 Phase 5） |
| E2 | Camera/ASR/TTS 交互增强 | 语音、图像、系统状态围绕同一节点/事件联动 | 满足 6 条最低完成线，至少 1 条完整交互链（见 Phase 6） |
| E3 | Web—移动端实时同步与协同 | 数据同源、状态一致、变化同步、终端分工明确 | 发布新消息两端自动同步 + 至少 1 项跨端联动（见 Phase 4） |

### 1.6 最终提交物

| 提交物 | 要求 |
|---|---|
| 可运行作品 + GitHub 仓库 | 含 Web/Dashboard、Python 分析、移动端、3D、数据/示例、report、README、Evidence、真实 Commit 历史 |
| Git Commit | **≥5 次有意义的 Commit**，能看出"基础可运行版本 → 关键功能推进 → 问题修复/调整 → 最终稳定版本"；现场会随机抽 2 次让你讲 |
| Evidence/ | D1–D5、E1–E3、Debug、Reproduce、Open 子目录 + 索引 README |
| README | 陌生人不靠你口头指导，只看仓库就能搭环境、启动组件、复现至少一条核心数据链 |
| README 交叉复现 | **必做**：找一位没参与开发的同学按 README 复现，留下"遇到问题 → 修订 README → 再次复现"的证据 |
| PPT | 建议 10–15 页，围绕"作品"讲，不按模块讲 |
| 技术文档 | 建议 10–15 页正文，重点是"为什么这样设计、怎样实现、怎样验证" |
| 演示视频 | 建议 5–8 分钟，用一条完整故事演示，以真实运行为主 |

### 1.7 现场验收五关

| 关卡 | 内容 |
|---|---|
| Run | 从关闭状态启动主要组件，跑通至少一条完整链路 |
| Explain | 随机选一个功能，讲清：数据从哪来 → 经过什么处理 → 为什么得到现在的结果 |
| Modify | 现场临时小需求：改状态阈值 / 改移动端显示字段 / 加 ASR 指令 / 改 3D 状态映射 / 调整优先规则 |
| Debug | 现场可控故障：Topic 错、JSON 字段错、Broker 停止、3D 节点映射错、移动端不同步 |
| Verify | 每次修改或修复后，重新运行证明结果真的变了 |

### 1.8 任务书的 8 个核心问题 → 由哪部分回答

| # | 问题 | 回答它的模块 |
|---|---|---|
| 1 | 现在多个宿舍分别什么状态？ | D1 + Dashboard 总览 |
| 2 | 哪个宿舍更值得优先关注？ | D2 优先规则 |
| 3 | 发现问题后用户做了什么？ | D3 事件记录中的处理动作 |
| 4 | 采取措施后数据是否真的改善？ | D3 后续验证数据 + 恢复判定 |
| 5 | Web、移动端、3D 看到的是不是同一套实时状态？ | E3 + D1 |
| 6 | 一次事件能否从"发现"追踪到"恢复/未恢复"？ | D3 + report 事件时间线 |
| 7 | 实时链路故障时能否发现、定位、修复、验证？ | D4 |
| 8 | Rule 和 ML 结果不同时能否讲清两种依据？ | D5 |

> 建议把这张表放进 PPT 前两页：它就是你的"需求说明"。

---

## 2. 深度分析：这份任务书真正在考什么

### 2.1 三层能力

1. **系统集成**：多个入口是否围绕同一数据源、同一套业务状态工作——**一致性是最核心的考点**。
2. **工程闭环**：事件闭环（D3）、故障闭环（D4）、复现闭环（README 交叉复现）、修改闭环（现场 Modify → Verify）。
3. **真实掌握**：允许用 AI，但现场五关就是检验你是否真正理解自己作品的地方。

### 2.2 最关键的设计决策：建立"统一状态中心"

任务书反复强调"同一套实时状态""不由两端分别维护互不一致的结果"。如果 Web、移动端、3D 各自计算状态、优先级和事件，只要某一端逻辑略有不同、或打开时间不同，就会出现不一致——这正是 E3 第 5 条和 D3"重要要求"所禁止的。

**建议做法**：写一个 Python 程序 `core.py` 作为唯一的"业务大脑"：

- 订阅所有节点原始数据 → 校验 JSON → 计算 `status` → 计算优先关注 → 推进事件状态机 → 计算 ML 判断 → 写入历史 CSV
- 把结果作为**一份完整的状态快照**发布到 `dormmate/v1/state`（retained 消息，新打开的页面立刻拿到最新状态）
- 各前端**只渲染、不判断**；用户操作（处理、切换节点、快照登记）以命令形式发给 core，由 core 统一修改状态再广播

好处：一致性天然成立；现场 Modify（改阈值、改优先规则）只需改一个地方；D4 排错时日志集中；它本身就是任务书"统一状态中心"亮点方向的一种实现，而且只用到 C01 已学的 Python + MQTT。

### 2.3 硬性红线（踩了就不达标）

| 红线 | 出处 |
|---|---|
| 点击"处理"按钮**不能**直接把事件改成"已恢复"，恢复必须由后续新数据触发 | D3 |
| 优先规则不能把 dorm-b 写死，换数据后结果要能变 | D2 |
| Web 和移动端分别手工输入相同数据，**不算**同步 | E3 |
| "当前重点 / 处理中 / 已恢复"等共享状态不能两端各自维护 | E3、D3 |
| report 不能靠手工修改结果；换 CSV 要能重新生成 | 数据链 A |
| 模拟数据必须明确标注；构造的 ML 测试输入必须标注"构造测试样本" | 数据链 A、D5 |
| 不能手工改 ML 输出，也不能为得到想要的答案反复改模型参数 | D5 |
| 开放拓展不能替代共同完成线 | 3.2、7.3 |
| E2 不以人脸识别、身份识别、个人敏感信息分析为目标 | E2 |
| 只换颜色、背景图、标题不算自主设计 | 6 |

### 2.4 评价逻辑

```
基本完成（第 10 章清单全部满足）= 门槛
      ↓
高质量表现 → 决定是否值得重点培养
      ↓
竞赛亮点   → 决定是否值得进一步冲赛
```

评价矩阵的 5 个维度：系统整体与协同、工程质量与可靠性、交互与作品呈现、数据与智能应用、自主设计与竞赛潜力。

注意：**"用了 LLM、YOLO、数字孪生"不自动等于亮点**。真正的亮点要满足：有问题来源 → 有实际增量 → 有运行证据 → 可解释、可修改 → 可继续深化。

**策略建议**：先把共同完成线做扎实（尤其是一致性、事件闭环、故障处理、README 复现），再挑 1 个与 DormMate 真实问题相关的点深挖成亮点，而不是铺很多浅层的"高级词"。

---

## 3. 推荐总体架构

### 3.1 架构图

```
[simulator.py] 三个模拟节点 dorm-a / dorm-b / dorm-c
      │  publish  dormmate/v1/nodes/{nodeId}/telemetry
      ▼
[Mosquitto Broker]  1883 (MQTT)  /  9001 (WebSocket，给浏览器和小程序用)
      │
      ▼
[core.py 状态中心 —— 唯一的业务大脑]
   ① 校验 JSON、防串线    ② 状态规则 status    ③ 优先关注 priority
   ④ 事件状态机 OPEN → HANDLING → RECOVERED / UNRESOLVED
   ⑤ ML 判断（Isolation Forest）    ⑥ 写 data/history.csv 与 data/events.json
      │  publish  dormmate/v1/state   （retained，完整状态快照）
      ▼
[Broker] ──▶ Web Dashboard ───────┐
         ──▶ 移动端 (H5/小程序) ───┤  用户操作 publish dormmate/v1/cmd ──▶ core.py
         ──▶ 3D (Three.js) ────────┤  （开始处理 / 切换关注节点 / 快照登记）
         ──▶ 语音·TTS·Camera ──────┘  模拟器也订阅 cmd，用于模拟"开风扇后温度下降"

离线链 A：data/history.csv ──▶ analysis/make_report.py ──▶ report/report.html
D5 训练 ：data/history.csv ──▶ analysis/train_iforest.py ──▶ models/*.joblib ──▶ core.py
```

### 3.2 技术选型（全部在 C01 范围内即可完成）

| 部分 | 选择 | 说明 |
|---|---|---|
| Broker | Mosquitto（或 C01 用过的 Broker） | 同时开 1883 (MQTT) 和 9001 (WebSocket) |
| 状态中心 | Python + paho-mqtt | 统一状态、事件、ML、写 CSV |
| 模拟器 | Python + paho-mqtt | 支持随机模式和"剧本回放"模式 |
| Web/Dashboard | HTML/CSS/JS + mqtt.js + Chart.js | 只渲染 state，不自己判断 |
| 移动端 | H5 移动页面（最省事）或微信小程序 | 二选一即可满足最低线 |
| 3D | Three.js（CSS2DRenderer 做标签） | 订阅同一份 state |
| 语音/图像 | 沿用 C01 的 ASR 方案或 Web Speech API、speechSynthesis、getUserMedia | 放在 Web 端或独立页面 |
| 离线分析 | pandas + matplotlib | 生成单文件 report.html |
| ML | scikit-learn IsolationForest + joblib | 按节点分别训练 |
| 版本管理 | Git + GitHub | 按阶段提交 |

> 建议把 mqtt.js、Chart.js、three.js 下载到仓库的 `lib/` 目录，而不是只依赖 CDN——现场网络不稳时也能跑，交叉复现也更可靠（在 README 中注明来源与许可证）。

### 3.3 建议目录结构

```
DormMate/
├── README.md                  # 复现指南（最重要的文档）
├── requirements.txt           # Python 依赖及版本
├── start_all.bat / .sh        # 可选：一键启动
├── broker/
│   └── mosquitto.conf
├── lib/                       # mqtt.min.js、chart.umd.js、three 等本地副本
├── shared/
│   └── config.js              # 前端共用：Broker 地址、Topic、节点名称映射
├── core/
│   ├── config.json            # 阈值、优先权重、恢复判定参数（现场 Modify 主要改这里）
│   ├── core.py                # 状态中心主程序
│   ├── rules.py               # 状态规则 + 优先规则
│   ├── events.py              # 事件状态机
│   └── ml.py                  # 加载模型、ML 判断
├── simulator/
│   ├── simulator.py           # 三节点模拟器
│   ├── publish_one.py         # 手动发一条消息（现场核验 / 故障注入）
│   └── scenarios/             # D2 三组情况、D3 事件、D5 构造样本等剧本
├── web/                       # Dashboard + 语音/TTS/Camera 面板
├── mobile/                    # H5 移动端（或 miniprogram/）
├── three/                     # 3D 数字空间
├── analysis/
│   ├── make_report.py
│   └── train_iforest.py
├── models/                    # 训练好的 Isolation Forest
├── data/
│   ├── history.csv            # 运行时自动追加
│   ├── events.json            # 事件记录
│   └── sample_history.csv     # 示例数据（给复现者用）
├── report/
│   └── report.html
├── docs/                      # 技术文档、PPT、架构图
└── Evidence/
    ├── README.md              # 证据索引
    ├── D1/ D2/ D3/ D4/ D5/
    ├── E1/ E2/ E3/
    └── Debug/ Reproduce/ Open/
```

### 3.4 Topic 设计

| Topic | 发布者 | 订阅者 | retained | 内容 |
|---|---|---|---|---|
| `dormmate/v1/nodes/{nodeId}/telemetry` | 模拟器 | core | 否 | 节点原始数据 |
| `dormmate/v1/state` | core | 所有前端 | **是** | 全局状态快照 |
| `dormmate/v1/cmd` | 各前端 | core、模拟器 | 否 | 用户操作命令 |
| `dormmate/v1/core/online` | core（含遗嘱 LWT） | 所有前端 | 是 | 状态中心在线/离线 |
| `dormmate/v1/log/reject` | core | Dashboard | 否 | 被拒绝的消息及原因（D4 可视化） |

core 订阅 `dormmate/v1/nodes/+/telemetry`，并检查 **Topic 中的 nodeId 与 JSON 中的 nodeId 是否一致**——这是"不串线"的关键保障之一。

### 3.5 JSON 数据结构

**① 节点原始数据（telemetry）**

```json
{
  "nodeId": "dorm-b",
  "temperature": 30.6,
  "humidity": 58.0,
  "time": "2026-10-08T14:03:21+08:00",
  "seq": 128,
  "source": "simulated"
}
```

`status` 由 core 统一计算后写入状态快照（也可以让模拟器带上 status，但以 core 的判断为准，保证全系统只有一套规则）。

**② 状态快照（state，由 core 发布）**

```json
{
  "updatedAt": "2026-10-08T14:03:21+08:00",
  "focus": "dorm-b",
  "nodes": {
    "dorm-a": {
      "nodeId": "dorm-a", "temperature": 24.1, "humidity": 52.0,
      "status": "NORMAL", "time": "2026-10-08T14:03:20+08:00", "seq": 127,
      "online": true, "last_seen": "2026-10-08T14:03:20+08:00",
      "ml": { "label": "NORMAL", "score": 0.08 }, "agree": true,
      "recent": [[24.0, 51.0, "NORMAL"], [24.1, 52.0, "NORMAL"]]
    }
  },
  "priority": {
    "nodeId": "dorm-b", "score": 22,
    "reasons": ["已连续异常 4 次", "最近 10 条中异常 6 次", "当前状态 HOT，严重度 2"]
  },
  "events": [
    { "event_id": "EVT-20261008-dorm-b-001", "nodeId": "dorm-b", "state": "HANDLING" }
  ]
}
```

说明：`nodes` 中还有 dorm-b、dorm-c（此处省略）；`recent` 为最近 N 条数据，供趋势图使用；`events` 只放未关闭事件和最近几条已关闭事件，完整记录保存在 `events.json`。

**③ 用户命令（cmd）—— 三种示例**

```json
{ "cmd": "handle",   "event_id": "EVT-20261008-dorm-b-001", "action": "开启风扇", "by": "mobile", "cmd_id": "k3x9a", "time": "..." }
{ "cmd": "focus",    "nodeId": "dorm-c", "by": "voice" }
{ "cmd": "snapshot", "nodeId": "dorm-b", "event_id": "EVT-20261008-dorm-b-001", "file": "snap_dorm-b_EVT-20261008-dorm-b-001_1760000000000.png", "by": "web" }
```

**④ 事件记录（events.json 中的一条）**

```json
{
  "event_id": "EVT-20261008-dorm-b-001",
  "nodeId": "dorm-b",
  "state": "RECOVERED",
  "problem": "HOT",
  "start_time": "2026-10-08T14:02:00+08:00",
  "priority_reasons": ["已连续异常 4 次", "最近 10 条中异常 6 次"],
  "actions": [{ "action": "开启风扇", "by": "mobile", "time": "2026-10-08T14:05:10+08:00" }],
  "verify": [
    { "time": "2026-10-08T14:05:30+08:00", "temperature": 28.9, "humidity": 56, "status": "HOT" },
    { "time": "2026-10-08T14:05:50+08:00", "temperature": 27.6, "humidity": 55, "status": "NORMAL" },
    { "time": "2026-10-08T14:06:10+08:00", "temperature": 27.1, "humidity": 55, "status": "NORMAL" }
  ],
  "verify_from": 0,
  "snapshots": ["snap_dorm-b_EVT-20261008-dorm-b-001_1760000000000.png"],
  "recovered_at": "2026-10-08T14:06:10+08:00",
  "result": "处理后连续 2 条数据正常，判定已恢复"
}
```

### 3.6 状态规则（占位示例）

> ⚠ 下面阈值只是示例，请替换为 C01 统一练习规则。

| status | 条件（示例） | 中文 |
|---|---|---|
| HOT | temperature > 28 | 偏热 |
| HUMID | humidity > 70 | 偏湿 |
| COLD | temperature < 16 | 偏冷 |
| NORMAL | 其余情况 | 正常 |
| 离线 | 超过 10 秒未收到数据（由 `last_seen` 判断，单独用 `online` 字段表示） | 离线 |

多个条件同时满足时（例如又热又湿）按什么顺序判定，也是你的设计决策，需要写进文档。

---

## 4. 分阶段详细操作

每个阶段都按 **目标 → 步骤 → 验证 → 留证据 → 提交** 来做。做完一个阶段就 commit 一次，Commit 历史自然就形成"版本演进"。

### Phase 0｜环境与仓库准备

**步骤**

1. 安装：Python 3.10+、Git、VS Code、Chrome 或 Edge、Mosquitto（或沿用 C01 的 Broker）；如果移动端用小程序，再装微信开发者工具。
2. 安装 Python 依赖并锁定版本：
   ```bash
   pip install paho-mqtt pandas matplotlib scikit-learn joblib
   pip freeze > requirements.txt
   ```
   > 注意：paho-mqtt 2.x 创建客户端要写 `mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)`，回调函数参数也和 1.x 不同。网上很多旧教程是 1.x 写法，README 中要写明版本。
3. 编写 `broker/mosquitto.conf`：
   ```conf
   listener 1883
   protocol mqtt

   listener 9001
   protocol websockets

   allow_anonymous true
   ```
   > Mosquitto 2.x 不写配置时只监听本机、且没有 WebSocket；一旦自己配置了 listener，必须显式写 `allow_anonymous true`，否则匿名连接会被拒绝。Windows 上如果 Mosquitto 服务已在后台运行，会占用 1883 端口，需要先停掉服务再用自己的配置启动。
4. 启动：`mosquitto -c broker/mosquitto.conf -v`
5. 按第 3.3 节建目录、写 `.gitignore`（忽略 `__pycache__/`、大体积视频等），在 GitHub 建仓库并推送。

**验证**：开两个终端，分别运行 `mosquitto_sub -h localhost -t "dormmate/#" -v` 和 `mosquitto_pub -h localhost -t dormmate/test -m hello`，能收到消息。

**提交**：`chore: 初始化项目结构与 Broker 配置`

---

### Phase 1｜打通实时链路（D1 雏形）

**目标**：三个节点的数据从模拟器 → Broker → 网页实时显示。

**步骤**

1. 写 `simulator/simulator.py`：
   - 每 2 秒为 dorm-a/b/c 各发一条 telemetry，Topic 为 `dormmate/v1/nodes/{nodeId}/telemetry`
   - 每个节点有自己的 `mode`（normal / hot / humid / cooling / silent），温湿度在基准值附近小幅随机波动
   - 每条数据带 `seq`（递增序号）和 `"source": "simulated"`
   - 支持 `--scenario 文件` 参数，按剧本逐步发送（保证演示和 D2 测试可重复）
   - 订阅 `dormmate/v1/cmd`：收到某节点的"开启风扇/开窗通风"处理命令后，把该节点 mode 切到 `cooling`（每次降 0.5～1℃），模拟处理效果；加一个 `--ineffective` 参数让处理无效，用于演示"未恢复"
2. 写 `simulator/publish_one.py`，从命令行手动发一条消息：
   ```bash
   python simulator/publish_one.py dorm-b 31.2 58
   ```
   再加两个故障注入参数：`--topic 自定义Topic`、`--raw '任意字符串'`（发送错误 JSON）。这个工具在 D1 现场核验、D4 故障和现场 Debug 时都会用到。
3. 先写一个最简网页，用 mqtt.js 直接订阅 telemetry、显示三张卡片（Phase 4 会改为订阅 state）：
   ```js
   const client = mqtt.connect("ws://localhost:9001", { reconnectPeriod: 2000 });
   client.on("connect", () => client.subscribe("dormmate/v1/nodes/+/telemetry"));
   client.on("message", (topic, payload) => {
     const d = JSON.parse(payload.toString());
     document.querySelector(`#card-${d.nodeId}`).textContent =
       `${d.nodeId}  ${d.temperature}℃  ${d.humidity}%  ${d.time}`;
   });
   ```
4. 在仓库根目录运行 `python -m http.server 8000`，打开 `http://localhost:8000/web/`。

**验证**：三张卡片各自刷新、互不串线；用 `publish_one.py` 改 dorm-b，只有 dorm-b 卡片变化。

**提交**：`feat: 三节点模拟器与实时 Dashboard 雏形（基础可运行版本）`

---

### Phase 2｜状态中心：校验 + 状态规则 + 优先关注（D2）

**目标**：core.py 成为唯一的业务大脑，给出"当前优先关注"及理由。

**步骤**

1. `core/config.json` 集中放参数：
   ```json
   {
     "nodes": ["dorm-a", "dorm-b", "dorm-c"],
     "thresholds": { "temp_high": 28.0, "temp_low": 16.0, "hum_high": 70.0 },
     "priority_weights": { "consecutive": 3, "count": 1, "severity": 2 },
     "priority_window": 10,
     "offline_timeout_sec": 10,
     "recover_consecutive_normal": 2,
     "unresolved_after": 5
   }
   ```
2. core.py 主结构（paho-mqtt 2.x 写法，`handle_reading`、`handle_cmd`、`reject`、`publish_state`、`check_offline` 需要你自己实现）：
   ```python
   import json, time
   import paho.mqtt.client as mqtt

   CFG = json.load(open("core/config.json", encoding="utf-8"))

   def validate(topic, d):
       for k, t in {"nodeId": str, "temperature": (int, float),
                    "humidity": (int, float), "time": str}.items():
           if k not in d:              return f"缺少字段 {k}"
           if not isinstance(d[k], t): return f"字段 {k} 类型错误"
       topic_node = topic.split("/")[3]
       if d["nodeId"] != topic_node:
           return f"nodeId({d['nodeId']}) 与 Topic({topic_node}) 不一致"
       if d["nodeId"] not in CFG["nodes"]:
           return f"未知节点 {d['nodeId']}"
       return None

   def on_connect(client, userdata, flags, reason_code, properties):
       client.subscribe([("dormmate/v1/nodes/+/telemetry", 0), ("dormmate/v1/cmd", 0)])
       client.publish("dormmate/v1/core/online", "online", retain=True)
       print("[CORE] 已连接 Broker")

   def on_message(client, userdata, msg):
       try:
           d = json.loads(msg.payload.decode("utf-8"))
       except (json.JSONDecodeError, UnicodeDecodeError) as e:
           reject(client, msg.topic, f"JSON 解析失败: {e}"); return
       if msg.topic == "dormmate/v1/cmd":
           handle_cmd(d)                # 处理 / 切换焦点 / 快照登记
       else:
           err = validate(msg.topic, d)
           if err:
               reject(client, msg.topic, err); return
           handle_reading(d)            # 状态规则 → 事件状态机 → ML → 写 CSV → 算优先
       publish_state(client)            # 发布完整快照，retain=True

   client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="dormmate-core")
   client.will_set("dormmate/v1/core/online", "offline", retain=True)   # 遗嘱：core 异常退出时通知前端
   client.on_connect, client.on_message = on_connect, on_message
   client.connect("localhost", 1883)
   client.loop_start()
   while True:                          # 主线程负责离线检测
       if check_offline(CFG["offline_timeout_sec"]):
           publish_state(client)
       time.sleep(1)
   ```
   `reject()` 负责打印日志 `[REJECT] 原因` 并发布到 `dormmate/v1/log/reject`。
3. `rules.py` 状态规则（阈值来自 config）：
   ```python
   def judge_status(t, h, th):
       if t > th["temp_high"]: return "HOT"
       if h > th["hum_high"]:  return "HUMID"
       if t < th["temp_low"]:  return "COLD"
       return "NORMAL"
   ```
4. `rules.py` 优先规则（写在程序里、可解释、可重复、不写死任何节点）：
   ```python
   def severity(r, th):
       over = max(r["temperature"] - th["temp_high"],
                  (r["humidity"] - th["hum_high"]) / 5,     # 湿度每超 5% 折算为 1
                  th["temp_low"] - r["temperature"], 0)
       return 0 if over <= 0 else (1 if over < 2 else 2)

   def rank_priority(history, online, cfg):
       w, th, n = cfg["priority_weights"], cfg["thresholds"], cfg["priority_window"]
       ranking = []
       for node_id, hist in history.items():
           recent = hist[-n:]
           if not recent or not online[node_id] or recent[-1]["status"] == "NORMAL":
               continue                     # 当前正常或离线的节点不参与"优先关注"
           consec = 0
           for r in reversed(recent):
               if r["status"] == "NORMAL":
                   break
               consec += 1
           count = sum(r["status"] != "NORMAL" for r in recent)
           sev = severity(recent[-1], th)
           score = w["consecutive"] * consec + w["count"] * count + w["severity"] * sev
           ranking.append({"nodeId": node_id, "score": score, "reasons": [
               f"已连续异常 {consec} 次",
               f"最近 {len(recent)} 条中异常 {count} 次",
               f"当前状态 {recent[-1]['status']}，严重度 {sev}"]})
       ranking.sort(key=lambda x: x["score"], reverse=True)
       return ranking    # 为空 → "当前无需优先关注"；ranking[0] → 当前优先关注
   ```
   > 同分时怎么排（例如异常开始更早者优先）、离线节点是否单独告警，都是你的设计决策，要写进文档。
5. 写三组 D2 剧本，例如 `simulator/scenarios/d2_case1.json`（每步给出三个节点的 [温度, 湿度]）：
   ```json
   {
     "name": "D2-情况1：a 正常，b 连续偏热，c 刚出现一次偏湿",
     "interval_sec": 2,
     "steps": [
       {"dorm-a": [24.0, 50], "dorm-b": [29.5, 55], "dorm-c": [25.0, 60]},
       {"dorm-a": [24.2, 51], "dorm-b": [29.8, 56], "dorm-c": [25.1, 62]},
       {"dorm-a": [24.1, 50], "dorm-b": [30.2, 55], "dorm-c": [25.3, 74]}
     ]
   }
   ```
   建议的三组情况：

   | 情况 | 设计 | 期望优先 |
   |---|---|---|
   | 1 | a 正常；b 连续偏热 3 次以上；c 刚出现一次偏湿 | dorm-b |
   | 2 | a 连续偏湿且湿度严重超标；b 正常；c 偶发偏热 | dorm-a |
   | 3 | b、c 都持续偏热，c 持续更久、超标更多 | dorm-c |

   还可以加第 4 组"三节点全部正常 → 暂无需优先关注"。

**验证**：分别回放三组剧本，截图"优先对象 + 理由"，三次结果不同。

**留证据**：`Evidence/D2/`：三张截图 + 三个剧本文件 + 一份 `rule.md`（公式、权重、为什么这样设计）。

**提交**：`feat: 状态中心 core——JSON 校验、统一状态规则与可解释优先规则`

---

### Phase 3｜事件闭环（D3）

**目标**：异常 → OPEN → 用户处理 → HANDLING → 后续数据判定 RECOVERED / UNRESOLVED → 记录复盘。

**状态机**

```
节点出现异常 ──▶ OPEN（待处理）
                   │ 用户点击"开始处理"（按钮只能推进到这里）
                   ▼
              HANDLING（处理中）
                   │ 收到后续新数据，由 core 判定
         ┌─────────┴──────────┐
         ▼                    ▼
  处理后连续 K 条正常     处理后 M 条仍未恢复
         │                    │
         ▼                    ▼
  RECOVERED（已恢复）    UNRESOLVED（未恢复·仍需关注）
                              │ 可再次处理 → HANDLING；之后连续 K 条正常 → RECOVERED
```

**步骤**

1. `events.py` 核心逻辑：
   ```python
   K = CFG["recover_consecutive_normal"]   # 处理后连续 K 条正常 → 已恢复
   M = CFG["unresolved_after"]             # 处理后收到 M 条仍未恢复 → 未恢复

   def on_reading(node_id, r):
       ev = active_event(node_id)                       # 该节点尚未 RECOVERED 的事件
       if ev is None:
           if r["status"] != "NORMAL":
               create_event(node_id, r)                 # state="OPEN"，记录 start_time、problem、priority_reasons
           return
       if ev["state"] in ("HANDLING", "UNRESOLVED"):
           ev["verify"].append({k: r[k] for k in ("time", "temperature", "humidity", "status")})
           since = ev["verify"][ev["verify_from"]:]     # 最近一次处理之后收到的数据
           if len(since) >= K and all(x["status"] == "NORMAL" for x in since[-K:]):
               ev["state"], ev["recovered_at"] = "RECOVERED", r["time"]
               ev["result"] = f"处理后连续 {K} 条数据正常，判定已恢复"
           elif ev["state"] == "HANDLING" and len(since) >= M:
               ev["state"] = "UNRESOLVED"
               ev["result"] = f"处理后 {M} 条数据仍未恢复，仍需关注"
       save_events()

   def on_handle(cmd):
       ev = find_event(cmd["event_id"])
       if ev and ev["state"] in ("OPEN", "UNRESOLVED"):
           ev["state"] = "HANDLING"                     # ⚠ 按钮最多只能推进到 HANDLING
           ev["actions"].append({"action": cmd["action"], "by": cmd["by"], "time": cmd["time"]})
           ev["verify_from"] = len(ev["verify"])        # 从这次处理之后重新计数验证数据
       save_events()
   ```
2. Web 和移动端都放"开始处理"按钮，点击后发送 `{"cmd": "handle", "event_id": ..., "action": "开启风扇"}`，由 core 改为 HANDLING。
3. 每次事件变化后 core 写 `data/events.json`；启动时读回，保证重启不丢事件。
4. 事件字段与任务书要求对照：

   | 任务书要求 | 字段 |
   |---|---|
   | event_id 或等价事件标识 | `event_id` |
   | nodeId | `nodeId` |
   | 开始时间 | `start_time` |
   | 问题/异常 | `problem` |
   | 为什么被优先关注 | `priority_reasons`（事件开启/被处理时的优先理由快照） |
   | 用户采取的动作 | `actions[]` |
   | 后续验证数据 | `verify[]` |
   | 当前事件状态 | `state` |
   | 恢复时间/最终结果 | `recovered_at`、`result` |
   | （E2 用）现场快照 | `snapshots[]` |

5. 需要你自己做的设计决策（写进文档）：事件处于 OPEN、用户还没处理、数据就自己恢复了怎么办？可以记为"未处理·自行恢复"并关闭，也可以保持 OPEN 等待确认。二选一并说明理由。

**验证**：回放 `d3_event.json`：dorm-b 持续偏热 → OPEN → 移动端点"开启风扇" → 三端显示"处理中" → 模拟器降温 → 至少 2 条后续数据 → RECOVERED。再用 `--ineffective` 跑一次，得到 UNRESOLVED。

**留证据**：`Evidence/D3/`：完整事件录屏、对应的 events.json 片段、状态流转截图。

**提交**：`feat: 事件生命周期 OPEN/HANDLING/RECOVERED，恢复由后续数据触发`

---

### Phase 4｜Web Dashboard + 移动端协同（E3 + D1 完整版）

**目标**：两端读同一份 state，自动同步，分工不同，并至少实现 1 项跨端联动。

**步骤**

1. 把 Phase 1 的网页改为订阅 `dormmate/v1/state`，**前端只渲染，不做状态判断**：
   ```js
   // BROKER_WS、CLIENT_NAME 来自 shared/config.js
   const client = mqtt.connect(BROKER_WS, { reconnectPeriod: 2000 });
   client.on("connect", () => {
     setConn("已连接");
     client.subscribe(["dormmate/v1/state", "dormmate/v1/core/online"]);
   });
   client.on("reconnect", () => setConn("重连中…"));
   client.on("close",     () => setConn("Broker 已断开"));
   client.on("message", (topic, payload) => {
     if (topic === "dormmate/v1/state")       render(JSON.parse(payload.toString()));
     if (topic === "dormmate/v1/core/online") setCore(payload.toString());
   });
   function sendCmd(cmd) {
     Object.assign(cmd, { by: CLIENT_NAME, cmd_id: Date.now().toString(36), time: new Date().toISOString() });
     client.publish("dormmate/v1/cmd", JSON.stringify(cmd));
   }
   ```
2. **Dashboard 布局建议**：顶部连接状态条（Broker / 状态中心）→ 优先关注横幅（节点 + 理由）→ 三节点卡片（温度、湿度、status、time、在线状态、Rule/ML）→ Chart.js 趋势图（用 state 中的 `recent`）→ 事件列表/时间线 → 处理按钮 → Rule vs ML 对照表 → 最近被拒绝的消息（D4 可视化）。
3. **移动端布局建议**（同一份 state，不同的信息组织）：
   - 顶部：连接状态
   - 大卡片：当前优先关注节点 + 理由 + 最新数据 + 事件状态 + "开始处理"按钮（可选动作：开启风扇 / 开窗通风）
   - 三节点迷你列表：点击某节点 → 发送 `focus` 命令
   - 最近 1～3 条事件
4. 移动端实现方式二选一：
   - **H5（推荐）**：`mobile/index.html`，复用 `shared/config.js`；在电脑上用浏览器开发者工具的"设备模拟"预览即可。
   - **微信小程序**：沿用 C01 中已跑通的小程序 MQTT 方案；本地开发时在开发者工具中勾选"不校验合法域名、web-view（业务域名）、TLS 版本以及 HTTPS 证书"（通常在"详情 → 本地设置"，以当前版本为准）。
   - ⚠ 真机里的 `localhost` 指手机自己，不是电脑。真机访问要改成电脑的局域网 IP（如 `ws://192.168.1.23:9001`），并保证在同一网络。**最低完成线不强制真机**，用开发者工具模拟器或 H5 证明同步即可；真机、跨网络、云端 MQTT/WSS 可作为 Open Enhancement。
5. **跨端联动**（至少做一项，建议两项都做）：
   - 移动端点"开始处理" → core 改为 HANDLING → Web、3D 同步显示"处理中"
   - 移动端或语音切换关注节点 → core 更新 `focus` → Web 高亮该卡片、3D 镜头飞向该房间
6. 为了让"一致"一眼可见：两端都显示 `time` 和 `seq`，现场核验时直接比对。

**验证**（模拟现场核验）：
```bash
python simulator/publish_one.py dorm-b 31.5 62
```
两端同时变化，dorm-b 的 nodeId / temperature / humidity / status / time 完全一致。

**留证据**：
- `Evidence/D1/`：三节点同时在线截图；一条消息同时驱动 Web、移动端、3D 更新的录屏（画面里同时出现终端命令和三个窗口）；`dataflow.md` 说明 nodeId、Topic、实时数据流。
- `Evidence/E3/`：同步录屏 + 跨端联动录屏 + 两端信息组织不同的原因说明。

**提交**：`feat: Web 与移动端订阅统一状态快照，实现跨端处理与节点联动`

---

### Phase 5｜3D 数字空间（E1）

**最低完成线 → 建议实现**

| # | 最低要求 | 建议实现 |
|---|---|---|
| 1 | ≥3 宿舍/区域与 nodeId 明确映射 | 用一个 `NODE_MAP` 对象集中定义映射 |
| 2 | 能在 3D 中区分并选择节点 | Raycaster 点击房间 → 高亮 + 信息面板 + 发送 focus 命令 |
| 3 | ≥2 类对象随状态动态变化 | 房间颜色（status）、风扇旋转（HANDLING）、标签文字（温湿度）、光圈（优先关注） |
| 4 | MQTT 新消息到达后 3D 无需刷新即更新 | 3D 页面直接订阅 `dormmate/v1/state` |
| 5 | 优先关注节点有明显表达 | 房间上方脉冲光圈 + 标签加"优先关注" |
| 6 | "处理中/已恢复"至少一种在 3D 中体现 | 处理中：风扇转动 + 黄色边框；已恢复：绿色闪烁 2 秒 |
| 7 | ≥1 项展示亮点 | 镜头聚焦飞行动画 / 动态标签 / 视角切换 / 事件动画 / 历史回放 / 状态面板联动（选 1～2 项做精） |

**步骤**

1. 场景：一栋简化宿舍楼、三个房间（BoxGeometry 地板 + 半透明墙），每个房间放一个风扇（圆柱 + 叶片）、一扇窗户、一个 CSS2D 标签。
2. 映射与颜色集中定义（现场"修改 3D 状态映射"只改这里）：
   ```js
   export const NODE_MAP = {
     "dorm-a": { label: "A 宿舍", pos: [-6, 0, 0] },
     "dorm-b": { label: "B 宿舍", pos: [ 0, 0, 0] },
     "dorm-c": { label: "C 宿舍", pos: [ 6, 0, 0] },
   };
   export const STATUS_COLOR = {
     NORMAL: 0x3fb950, HOT: 0xf85149, HUMID: 0x388bfd, COLD: 0x79c0ff, OFFLINE: 0x6e7681,
   };
   ```
3. 状态驱动更新：
   ```js
   let lastFocus = null;
   function render3D(state) {
     for (const [id, n] of Object.entries(state.nodes)) {
       const room = rooms[id];
       room.box.material.color.setHex(STATUS_COLOR[n.online ? n.status : "OFFLINE"]);
       room.label.element.textContent = `${NODE_MAP[id].label}  ${n.temperature}℃  ${n.humidity}%`;
       const ev = state.events.find(e => e.nodeId === id && e.state !== "RECOVERED");
       room.fanSpinning = ev?.state === "HANDLING";
     }
     for (const id in rooms) rooms[id].ring.visible = (id === state.priority?.nodeId);
     if (state.focus && state.focus !== lastFocus) {     // 只在焦点变化时飞行，避免每次刷新都移动镜头
       lastFocus = state.focus;
       flyTo(rooms[state.focus]);
     }
   }
   ```
   在动画循环中：`fanSpinning` 为真时旋转风扇；光圈做缩放脉冲；`flyTo` 用插值平滑移动相机。"已恢复"动画可通过比较前后两次 state 中事件状态（HANDLING → RECOVERED）来触发。
4. 进阶（任选）：用 GLTFLoader 加载 Blender 自建或开源宿舍模型；按 events.json 回放"异常 → 处理 → 恢复"动画；在 3D 旁嵌入状态卡片和事件时间线联动。

**留证据**：`Evidence/E1/`：选择节点、优先光圈、处理中风扇、恢复动画的截图/短视频，以及 `NODE_MAP` 映射说明。

**提交**：`feat: 3D 数字空间——节点映射、状态驱动、优先与处理状态可视化`

---

### Phase 6｜Camera / ASR / TTS 多模态交互（E2）

**最低完成线 → 建议实现**

| # | 最低要求 | 建议实现 |
|---|---|---|
| 1 | ASR 支持 ≥2 条有意义的 DormMate 指令 | 下表 5 条指令 |
| 2 | ≥1 条语音指令真实改变操作对象或触发功能 | "查看 dorm-b" → 发送 focus 命令，三端联动 |
| 3 | TTS 朗读内容来自当前真实节点/事件状态 | 从当前 state 拼接播报文本 |
| 4 | Camera 保存 ≥1 张与节点/事件关联的快照 | canvas 截图 + 水印 |
| 5 | 快照能说明属于哪个节点、什么时间、什么事件 | 水印 + 文件名 + 登记到事件的 `snapshots[]` |
| 6 | ≥1 条完整交互链 | "查看 dorm-b → 朗读状态 → 记录现场" |

**指令设计**

| 语音指令 | 同义说法（示例） | 系统动作 |
|---|---|---|
| 查看 dorm-b | 看一下 B 宿舍、切换到二号宿舍 | 发送 focus 命令 → Web/移动端/3D 同步切换 |
| 查看重点节点 | 谁最需要关注 | focus 到 `state.priority.nodeId` |
| 朗读状态 | 播报一下、读一下 | TTS 播报当前 focus 节点的数据与事件状态 |
| 记录现场 | 拍一张、拍照 | Camera 抓拍，关联当前节点和活动事件 |
| 开始处理 | 开风扇、通风 | 对当前节点的活动事件发送 handle 命令 |

**步骤**

1. 指令解析（先做文本规范化，提高识别容错）：
   ```js
   const ALIAS = {           // 规范化后的别名：已去空格、去连字符、转小写
     "dorm-a": ["dorma", "a宿舍", "一号宿舍"],
     "dorm-b": ["dormb", "b宿舍", "二号宿舍"],
     "dorm-c": ["dormc", "c宿舍", "三号宿舍"],
   };
   function parseCommand(text) {
     const t = text.toLowerCase().replace(/[\s\-，。,.]/g, "");
     if (/重点|优先|最需要/.test(t))     return { type: "focusPriority" };
     if (/朗读|播报|读一下/.test(t))     return { type: "speak" };
     if (/记录现场|拍照|拍一张/.test(t)) return { type: "snapshot" };
     if (/开始处理|开风扇|通风/.test(t))
       return { type: "handle", action: t.includes("通风") ? "开窗通风" : "开启风扇" };
     for (const [id, words] of Object.entries(ALIAS))
       if (words.some(w => t.includes(w))) return { type: "focus", nodeId: id };
     return { type: "unknown", text };
   }
   ```
2. ASR：沿用 C01 的实现。若使用浏览器 `webkitSpeechRecognition`（设 `lang = "zh-CN"`），注意 Chrome 的识别依赖在线服务，现场网络环境要提前测试；建议页面上再保留一个"文字指令"输入框，走同一个 `parseCommand`，方便调试和兜底（但它不能代替 ASR 本身）。
3. TTS 文本来自真实 state：
   ```js
   function speakNode(state, id) {
     const n = state.nodes[id];
     const ev = state.events.find(e => e.nodeId === id && e.state !== "RECOVERED");
     const text = `${NODE_MAP[id].label}，温度${n.temperature}度，湿度百分之${n.humidity}，` +
                  `状态${STATUS_CN[n.status]}，` +
                  (ev ? `事件${EVENT_CN[ev.state]}` : "当前没有未关闭的事件");
     const u = new SpeechSynthesisUtterance(text);
     u.lang = "zh-CN";
     speechSynthesis.speak(u);
   }
   ```
4. Camera 快照（带水印，并登记到事件）：
   ```js
   // 页面加载时：video.srcObject = await navigator.mediaDevices.getUserMedia({ video: true });
   function snapshot(state, id) {
     const ev = state.events.find(e => e.nodeId === id && e.state !== "RECOVERED");
     const c = document.createElement("canvas");
     c.width = video.videoWidth; c.height = video.videoHeight;
     const g = c.getContext("2d");
     g.drawImage(video, 0, 0);
     const now = new Date();
     const tag = `${id} | ${ev ? ev.event_id + " " + ev.state : "无活动事件"} | ${now.toLocaleString()}`;
     g.fillStyle = "rgba(0,0,0,.6)"; g.fillRect(0, c.height - 36, c.width, 36);
     g.fillStyle = "#fff"; g.font = "20px sans-serif"; g.fillText(tag, 10, c.height - 12);
     const file = `snap_${id}_${ev ? ev.event_id : "none"}_${now.getTime()}.png`;
     const a = document.createElement("a");
     a.href = c.toDataURL("image/png"); a.download = file; a.click();                    // 保存图片
     sendCmd({ cmd: "snapshot", nodeId: id, event_id: ev ? ev.event_id : null, file });  // 登记到事件
   }
   ```
   > 摄像头只能在 `localhost` 或 HTTPS 页面中使用；通过局域网 IP 打开的 http 页面会被浏览器拒绝。
   > 拍摄对象应是环境（窗户、风扇、温湿度计等），尽量避免拍人——任务书明确不以人脸/身份识别为目标。
5. 进阶（可选）：节点进入重点、处理中、恢复、离线时自动 TTS 播报；快照自动进入事件卡片并在 report 中显示；LLM 自然语言查询；VLM 描述快照中的环境。

**留证据**：`Evidence/E2/`：完整交互链录屏（带声音）、快照图片、包含 `snapshots` 字段的事件记录。

**提交**：`feat: 语音指令、状态播报与事件关联快照`

---

### Phase 7｜离线分析链 → report.html（数据链 A）

**步骤**

1. core 每收到一条合法数据，就追加一行到 `data/history.csv`：
   ```
   time,nodeId,temperature,humidity,status,ml_label,event_id,event_state,source
   ```
   （可选：Dashboard 增加"导出 CSV"按钮，对应任务书中的"Web/历史记录 → CSV"。）
2. `analysis/make_report.py` 支持命令行参数，换一份 CSV 就能重新生成：
   ```bash
   python analysis/make_report.py --csv data/history.csv --events data/events.json --out report/report.html
   ```
3. 报告内容建议：
   - **数据来源说明**：时间范围、记录数、`source` 构成（真实运行 / 模拟运行 / 构造样本，必须标注）
   - **各节点统计表**：平均 / 最高 / 最低温湿度、异常占比
   - **趋势图**：每个节点的温度、湿度曲线，画出阈值线并标出事件区间
   - **事件时间线**：event_id、节点、开始时间、处理动作、处理时间、恢复时间、持续时长、结果、快照
   - **今日摘要**：由程序自动生成文字，例如"今日共 3 个事件，2 个已恢复，平均恢复用时 4 分钟，dorm-b 异常最多"
   - **Rule vs ML 统计**：一致率、不一致样本列表
4. 关键代码点：
   ```python
   import base64, io
   import matplotlib
   matplotlib.use("Agg")
   import matplotlib.pyplot as plt
   plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC"]
   plt.rcParams["axes.unicode_minus"] = False        # 解决中文和负号显示问题

   def fig_to_img(fig):                               # 图片内嵌为 base64，report.html 单文件即可打开
       buf = io.BytesIO()
       fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
       plt.close(fig)
       return f'<img src="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}">'
   ```
   统计表可用 `df.groupby("nodeId").agg(...)` 再 `.to_html()`，最后用字符串模板拼成完整 HTML。

**验证**：分别用 `data/history.csv` 和 `data/sample_history.csv` 两份不同数据生成报告，内容随之变化。

**留证据**：两份报告截图 + 生成命令记录。可自建 `Evidence/ChainA/`，或并入 `Evidence/D3/`（事件时间线部分），并在证据索引中注明"数据链 A"。

**提交**：`feat: 历史 CSV 自动记录与 report.html 自动生成`

---

### Phase 8｜固定规则 vs ML（D5）

**步骤**

1. 先让系统正常运行一段时间（或用模拟器生成足够的历史，建议每个节点 ≥100 条），得到训练用的历史数据。模拟数据要在 `source` 中标注。
2. `analysis/train_iforest.py`（按节点分别训练，关注"与该宿舍自身历史是否不同"）：
   ```python
   import pandas as pd, joblib
   from sklearn.ensemble import IsolationForest

   df = pd.read_csv("data/history.csv")
   df = df[df["source"] != "constructed"]             # 构造测试样本不能进入训练集
   for node, g in df.groupby("nodeId"):
       X = g[["temperature", "humidity"]]
       model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42).fit(X)
       joblib.dump(model, f"models/iforest_{node}.joblib")
       print(node, "训练样本数:", len(X))
   ```
   参数一次定好并写进文档，之后**不再为了得到某个答案去改**。
3. core 中实时判断，结果写入 state，Dashboard 显示"温湿度 | Rule | ML | 是否一致"：
   ```python
   X = pd.DataFrame([[t, h]], columns=["temperature", "humidity"])
   ml_label = "ANOMALY" if model.predict(X)[0] == -1 else "NORMAL"
   ml_score = float(model.decision_function(X)[0])    # 越小越"不像该宿舍的历史"
   agree = (rule_status == "NORMAL") == (ml_label == "NORMAL")
   ```
4. 寻找"值得分析"的案例。如果自然运行中没出现不一致，在**规则和模型都保持不变**的前提下设计输入，并标注 `"source": "constructed"`（界面上显示"构造测试样本"）：

   | 案例 | 构造思路 | 预期结果 | 解释 |
   |---|---|---|---|
   | A：Rule 正常、ML 异常 | dorm-a 历史一直在 22–25℃ / 45–55%，发送 27.0℃ / 66% | 未超阈值 → Rule 正常；远离 dorm-a 自身历史 → ML 异常 | Rule 看的是绝对舒适阈值，ML 看的是是否偏离"这个宿舍平时的样子" |
   | B：Rule 异常、ML 正常 | dorm-b 历史中经常处于 28.5–30℃（例如西晒），发送 29.0℃ | 超阈值 → Rule 偏热；在 dorm-b 历史中很常见 → ML 正常 | 历史本身包含异常，ML 把"常见的异常"学成了常态 |

   如果经过合理测试仍然一致，就如实记录实际结果，并解释为什么两种方法当前表现一致。
5. 原因分析可参考任务书给出的方向：历史数据太少；历史数据太单一；历史本身包含异常；当前环境模式已变化；固定阈值与该宿舍自身历史分布关注的是不同问题。另外要能解释：`contamination=0.05` 意味着模型默认把训练数据中约 5% 最"孤立"的点视为异常。

**边界**：本任务不需要 Label、Train/Test 划分、Accuracy/F1、混淆矩阵、模型版本管理、复杂调参、模型服务。

**留证据**：`Evidence/D5/`：对照界面截图、构造样本文件、`case.md`（输入、两种结果、原因分析）。

**提交**：`feat: Isolation Forest 与固定规则并列判断及对照案例`

---

### Phase 9｜故障制造与修复（D4）

**步骤**

1. 先把"可观测性"做好，故障才看得见：
   - 三端顶部显示 Broker 连接状态（mqtt.js 的 connect / reconnect / close 事件）
   - 显示状态中心在线状态（遗嘱消息 LWT）
   - core 日志打印每条被拒绝的消息及原因，并在 Dashboard 列出
   - 节点 `last_seen` 超时后显示"离线"
2. 至少真实做一次下面的故障，建议做 2～3 种：

   | 故障 | 制造方式 | 现象 | 定位方法 | 修复 |
   |---|---|---|---|---|
   | 写错 Topic | 模拟器 Topic 改成 `dormmate/v1/node/...`（少了 s） | 该节点不再更新，超时后显示离线，前端没有报错 | `mosquitto_sub -v -t "dormmate/#"` 发现消息发到了错误 Topic，和 core 的订阅对不上 | 改回正确 Topic |
   | 错误 JSON | `publish_one.py --raw '{"nodeId":"dorm-a",'` | 数据不更新；core 日志显示 JSON 解析失败 | 查 core 日志 / Dashboard 拒绝列表 | 修正消息格式 |
   | 字段名写错 | 用 `temp` 代替 `temperature` | core 日志显示缺少字段 temperature | 查日志，对照 JSON 规范 | 改回字段名 |
   | 停止 Broker | 在终端 Ctrl+C 停掉 mosquitto | 三端显示"Broker 已断开"，数据停止 | 检查 mosquitto 进程和 1883/9001 端口 | 重启 Broker，确认各端自动重连 |
   | 节点停发 | 模拟器把某节点设为 silent | 超时后该节点显示离线 | 查看 `last_seen` | 恢复发送，确认重新上线 |

3. 每次都走完整流程：**观察现象 → 定位原因 → 修复 → 重新跑同一链路 → 验证恢复**。
4. 记录模板（`Evidence/Debug/fault_01_topic.md`）：
   ```markdown
   ## 故障 01：Topic 写错
   - 制造方式：……
   - 现象：……（截图）
   - 定位过程：……（日志 / mosquitto_sub 输出）
   - 原因：……
   - 修复：……（对应 commit：xxxxxxx）
   - 重新运行与验证：……（修复后截图 / 录屏）
   ```

**可加分**：节点在线/离线、`last_seen`、错误 JSON 拒绝、Broker 断开提示、自动重连——前面已顺带实现的部分，可以在文档中作为工程可靠性亮点来写。

**提交**：`fix: JSON 字段校验、节点离线检测与 Broker 断线提示`

---

### Phase 10｜README 与交叉复现（必做）

**步骤**

1. 按第 5.3 节模板写 README。
2. 自己先在一个"干净"的环境（或新建目录重新 clone）按 README 从零跑一遍。
3. 找一位**没有参与开发**的同学，只给他仓库地址。他只能依据 GitHub 仓库、README、仓库中的配置说明和示例数据；你**不能逐步口头指导**。
4. 记录他实际遇到的卡点（例如"不知道要先停掉 Mosquitto 服务""装成了 paho-mqtt 1.x""不知道移动端怎么打开"）。
5. 根据卡点修订 README 并 commit。
6. 让他（或另一位同学）按修订后的 README 再复现一次，记录结果。

**留证据**：`Evidence/Reproduce/`：复现者信息、卡点截图、README 修订前后对比（或 commit 链接）、再次复现成功的截图。

**提交**：`docs: 根据交叉复现反馈修订 README`

---

### Phase 11｜PPT、技术文档、演示视频

按第 5.4～5.6 节的大纲与脚本完成。

**提交**：`docs: 技术文档、PPT 与 Evidence 索引`，最后 `release: v1.0 最终稳定版本`（可打 tag）。

---

### Phase 12｜模拟现场验收

找同学扮演评委，按第 6 章逐项演练，尤其是：从关机状态计时启动、随机 Modify、随机 Debug。

---

## 5. 交付物规范与模板

### 5.1 Commit 规划示例（≥5 次有意义提交）

| # | Commit | 对应阶段 |
|---|---|---|
| 1 | feat: 三节点模拟器与实时 Dashboard 雏形 | 基础可运行版本 |
| 2 | feat: 状态中心 core——统一状态规则与可解释优先规则 | 关键功能推进 |
| 3 | feat: 事件生命周期，恢复由后续数据触发 | 关键功能推进 |
| 4 | feat: 移动端协同与跨端处理 | 关键功能推进 |
| 5 | feat: 3D 数字空间状态联动 | 关键功能推进 |
| 6 | feat: 语音指令、播报与事件快照 | 关键功能推进 |
| 7 | feat: report.html 自动生成与 Isolation Forest 对照 | 关键功能推进 |
| 8 | fix: JSON 校验、离线检测与断线提示 | 问题修复/调整 |
| 9 | docs: 根据交叉复现修订 README | 问题修复/调整 |
| 10 | release: v1.0 最终稳定版本 | 最终稳定版本 |

> 现场会随机抽 2 次 Commit，让你讲"改了什么、为什么改、改后怎么验证"。建议在 commit 正文里把这三点写清楚。不要为凑数反复提交没有实际变化的版本。

### 5.2 Evidence 目录与索引

```
Evidence/
├── README.md        # 证据索引
├── D1/  D2/  D3/  D4/  D5/
├── E1/  E2/  E3/
├── Debug/           # 真实故障与修复记录
├── Reproduce/       # 交叉复现记录
└── Open/            # 有开放拓展时使用
```

不需要堆大量截图，每项保留**最能证明结果**的截图、短视频、JSON、日志或测试记录，并配一句简要说明。

`Evidence/README.md` 索引模板：

```markdown
| 编号 | 文件 | 证明什么 | 视频时间点 |
|---|---|---|---|
| D1-1 | D1/three_nodes_online.png | 三节点同时在线，三端显示一致 | 00:35 |
| D1-2 | D1/one_msg_three_ends.mp4 | 一条 MQTT 消息同时驱动 Web/移动端/3D 更新 | 00:50 |
| D2-1 | D2/case1_dorm-b.png | 情况 1：优先关注 dorm-b 及理由 | 01:20 |
| ...  | ... | ... | ... |
```

### 5.3 README 模板

README 的首要目标：**让一个从未接触过该项目的人，不需要你口头指导，仅根据仓库和 README 就能准备环境、启动主要组件，并复现至少一条核心数据链。**

```markdown
# DormMate：面向多宿舍节点的环境状态感知、事件响应与多端协同系统

## 1. 项目简介
解决什么问题；一张架构图；两条数据链。

## 2. 环境要求
操作系统、Python 版本、Mosquitto 版本、浏览器、（微信开发者工具版本）、关键库版本（见 requirements.txt）。

## 3. 目录结构
每个目录的用途。

## 4. 安装与配置
pip install -r requirements.txt；Broker 配置说明；如 Mosquitto 服务已在后台运行需先停止。

## 5. 启动顺序
1) Broker：mosquitto -c broker/mosquitto.conf -v
2) 状态中心：python core/core.py
3) 模拟器：python simulator/simulator.py
4) 静态服务：python -m http.server 8000（在仓库根目录）
5) 打开 Web / 移动端 / 3D 的地址

## 6. 关键配置
Broker 地址、MQTT 端口 1883、WebSocket 端口 9001、Topic 结构、JSON 字段说明。

## 7. 怎样产生一条测试数据
python simulator/publish_one.py dorm-b 31.5 62

## 8. 怎样验证 Web—移动端实时同步
操作步骤 + 应该看到什么。

## 9. D1–D5 快速复现
每个场景一条命令（剧本回放）+ 预期结果。

## 10. 正常情况下应看到的结果
关键截图。

## 11. 常见问题与排查
端口占用、paho-mqtt 版本、摄像头权限、真机上 localhost 的含义、ASR 对网络的依赖……

## 12. 已知限制

## 13. 使用的开源库与资料来源
```

### 5.4 PPT 大纲（14 页）

| 页 | 内容 |
|---|---|
| 1 | 封面：作品名 + 一句话定位 |
| 2 | 项目问题与目标（8 个核心问题） |
| 3 | 最终产品长什么样（三端 + 3D 同屏截图） |
| 4 | 系统架构与两条数据链 |
| 5 | 多端协同方式：统一状态中心 + 各端分工及理由 |
| 6 | D1 多节点 & D2 优先规则（公式 + 3 组情况对比） |
| 7 | D3 事件生命周期状态图 + 一次完整事件 |
| 8 | E1 3D 数字空间 |
| 9 | E2 多模态交互链 |
| 10 | E3 跨端联动 |
| 11 | 一次真实故障与修复 |
| 12 | Rule / ML 对照案例 |
| 13 | 自主设计与作品亮点 / Open Enhancement |
| 14 | 已知限制与后续想法 |

核心：讲清"为什么做、做成什么、系统怎样工作、怎样证明它成立、有哪些自主创新与限制"。

### 5.5 技术文档大纲（10–15 页正文）

| 部分 | 建议篇幅 | 内容 |
|---|---|---|
| 1 项目与需求 | 1–1.5 页 | 目标、使用场景、8 个核心问题 |
| 2 系统架构与数据链 | 2 页 | 整体架构图、离线分析链、实时系统链 |
| 3 核心数据与系统机制 | 2.5 页 | 数据结构、Topic/JSON、事件状态机、Web—移动端同步机制 |
| 4 D1–D5 与 E1–E3 关键实现 | 4 页 | 只写关键设计与核心实现，配必要代码片段 |
| 5 测试、故障与验证 | 2.5 页 | D1–D5 测试、真实故障与修复、Rule/ML 对照、README 交叉复现 |
| 6 自主设计与开放拓展 | 1.5 页 | 设计决策表、新增技术的作用、验证证据、已知限制、参考来源 |

鼓励放：系统架构图、数据流图、关键界面截图、事件状态图、必要代码片段、测试与 Evidence 引用。**不要整段复制代码代替说明。**

### 5.6 演示视频脚本（约 7 分钟）

| 时间 | 画面 | 对应要求 |
|---|---|---|
| 0:00–0:30 | 一句话介绍问题与系统，快速展示架构图 | — |
| 0:30–1:15 | 三宿舍同时在线；终端发布一条消息，Web/移动端/3D 同时更新 | D1、E3 |
| 1:15–2:00 | dorm-b 持续偏热，系统给出"优先关注 dorm-b"及理由，三端同步突出 | D2、E1 |
| 2:00–2:45 | 语音"查看重点节点" → "朗读状态" → "记录现场"，3D 镜头聚焦 | E2、E1 |
| 2:45–3:45 | 移动端"开始处理" → 三端显示处理中 → 后续数据进入 → 已恢复 | D3、E3 |
| 3:45–4:15 | 打开 report.html，查看事件时间线和今日摘要 | 数据链 A |
| 4:15–5:15 | 制造 Topic/Broker/JSON 故障 → 观察 → 定位 → 修复 → 验证 | D4 |
| 5:15–6:15 | Rule/ML 对照案例与解释 | D5 |
| 6:15–7:00 | 自主设计 / 开放拓展亮点，总结 | 亮点 |

录制建议：用 OBS 等工具录屏，把 Web、移动端（模拟器）、3D 三个窗口并排；**以真实系统运行画面为主**，PPT 只用于必要说明；不要按"这是 M1、这是 M2……"逐个介绍模块。

---

## 6. 现场验收预案

### 6.1 Run（从关闭状态启动）

- 准备一键启动脚本，或把启动顺序写在 README 最前面
- 提前演练并计时，目标是 3 分钟内三端都显示实时数据
- 现场先检查：端口是否被占用、摄像头/麦克风权限、网络（如 ASR 需要）

### 6.2 Explain（随机功能讲数据流）

用固定句式练习：**数据从哪里来 → 经过什么处理 → 为什么得到现在的结果**。例如：

> Dashboard 上 dorm-b 显示"优先关注"：模拟器向 `dormmate/v1/nodes/dorm-b/telemetry` 发布 JSON → core 校验字段和 nodeId → 按阈值判定为 HOT → 优先规则计算得分：连续异常 4 次 × 3 + 最近 10 条中异常 6 次 × 1 + 严重度 2 × 2 = 22，高于其他节点 → core 发布 state → Dashboard 渲染横幅和理由。

### 6.3 Modify（现场改需求速查表）

| 可能的需求 | 改哪里 | 验证方法 |
|---|---|---|
| 改状态阈值 | `core/config.json` → `thresholds` | 重启 core，用 `publish_one.py` 发一条临界值数据，看三端状态 |
| 改移动端显示字段 | `mobile/` 中的 render 函数 | 刷新移动端，对比 Web |
| 增加 ASR 指令 | `parseCommand` 中加一条规则 + 对应动作 | 说出新指令（或用文字输入框测试） |
| 修改 3D 状态映射 | `STATUS_COLOR` / `NODE_MAP` | 发送异常数据，看颜色/位置 |
| 调整优先规则 | `config.json` → `priority_weights`，或 `rank_priority` 函数 | 回放 D2 剧本，看优先对象/理由的变化 |

> 提前把每一项都亲手演练一遍，并确保改完能**重新运行证明结果真的变了**。

### 6.4 Debug（可控故障预案）

| 现场故障 | 排查思路 |
|---|---|
| Topic 错误 | `mosquitto_sub -v -t "dormmate/#"` 看消息实际发到哪；对比 core 的订阅 |
| JSON 字段错误 | 看 core 日志和 Dashboard 拒绝列表中的原因 |
| Broker 停止 | 三端顶部出现断线提示；检查 mosquitto 进程与 1883/9001 端口 |
| 3D 节点映射错误 | 点击房间看显示的 nodeId；检查 `NODE_MAP` |
| 移动端没有同步 | 看移动端连接状态；检查 ws 地址（真机不能用 localhost）、端口 9001、订阅的 Topic |

### 6.5 Verify

每次修改/修复后：重新运行同一条链路 → 截图或当场演示前后对比。

### 6.6 可能被追问的问题（提前准备答案）

- 为什么要单独做一个状态中心，而不是让各端自己计算？
- 点击"处理"后为什么不能直接恢复？你的恢复判定条件是什么？为什么是连续 2 条？
- 优先规则的权重为什么这样定？换一组数据会怎样？
- 三个节点怎样保证不串线？
- Isolation Forest 为什么会和规则判断不一致？contamination 是什么意思？
- Web 和移动端为什么采用不同的信息组织方式？
- 抽到的某次 commit 改了什么、为什么改、怎么验证？
- 哪部分代码借助了 AI？你是怎样理解和验证它的？

---

## 7. 自主设计决策表（必须由你自己填写）

任务书要求每位同学在以下方向形成**自己的**设计决策，并能回答"为什么这样做，而不是只说我觉得这样好看"。建议把此表放进技术文档：

| 设计点 | 我的选择 | 为什么这样做 | 证据位置 |
|---|---|---|---|
| 重点节点怎样判断 | 例：连续次数×3 + 窗口异常次数×1 + 严重度×2 | 例：持续异常比偶发异常更需要处理；严重度避免"轻微但持续"的节点压过"严重突发"的节点 | Evidence/D2 |
| Dashboard 怎样组织多节点 | | | |
| 移动端保留哪些核心信息 | | | |
| 3D 怎样表达节点、重点与处理过程 | | | |
| ASR 指令怎样设计 | | | |
| Camera 快照怎样与事件关联 | | | |
| 事件状态怎样组织 | | | |
| 历史报告重点分析什么 | | | |
| 视频怎样讲完整故事 | | | |
| D1–D5 使用什么具体数据 | | | |

---

## 8. Open Enhancement（开放拓展）建议

**原则**：先完成共同完成线，再做拓展。每项拓展都要满足四条标准——**有问题来源、有实际增量、有运行证据、可解释可修改**；证据放在 `Evidence/Open/`，文档中与共同完成线明确区分。

| 投入 | 方向 | 解决 DormMate 的什么问题 |
|---|---|---|
| 低 | 消息确认（已发送 / 已接收 / 已执行） | 移动端操作后不知道是否生效 |
| 低 | 事件回放（按 events.json 在 3D 中重播） | 复盘时看不到过程 |
| 低 | 定时自动生成日报 | 报告需要手动运行 |
| 中 | FastAPI + SQLite 统一状态/历史服务 | 状态只在内存和文件中，历史查询不便 |
| 中 | 局域网真机访问 / PWA | 只能在电脑上演示 |
| 中 | glTF/GLB 宿舍模型 | 3D 只是几个方块 |
| 高 | LLM 语音助手（基于 state JSON 回答"现在哪个宿舍最该处理？"） | 固定指令的表达能力有限 |
| 高 | VLM 快照理解（窗户是否打开、风扇是否运转） | 快照只存图，不产生信息 |

> 评价原则："用了什么技术"不重要，"解决了什么问题、能否运行证明、能否现场解释和修改"才重要。

---

## 9. 参考时间安排（按 4 周示意，请按实际截止时间调整）

| 周 | 任务 | 阶段 |
|---|---|---|
| 第 1 周 | 环境、实时链路、状态中心、优先规则、事件闭环 | Phase 0–3 |
| 第 2 周 | Web/移动端协同、3D、多模态交互 | Phase 4–6 |
| 第 3 周 | 离线报告、Rule/ML、故障与修复、README 初稿 | Phase 7–10 |
| 第 4 周 | 交叉复现、PPT、技术文档、视频、模拟验收 | Phase 10–12 |

**边做边留证据**：每完成一个阶段就把截图/录屏放进 Evidence，比最后集中补做省事得多。

---

## 10. 最终自查清单（对照任务书第 10 章）

**功能**
- [ ] D1–D5 五个场景全部完成
- [ ] 离线分析链真实跑通（换 CSV 可重新生成 report）
- [ ] 实时系统链真实跑通（≥3 节点、不串线）
- [ ] E1 3D 数字空间增强完成（7 条最低线）
- [ ] E2 Camera/ASR/TTS 交互增强完成（6 条最低线）
- [ ] E3 Web—移动端实时同步与协同完成（含跨端联动）
- [ ] D3 事件能从发现、处理走到后续数据验证与恢复/未恢复
- [ ] Web/Dashboard、移动端、3D 围绕同一套实时状态和共享事件状态保持一致
- [ ] 已明确区分共同完成线与 Open Enhancement；拓展有运行与验证证据
- [ ] 至少保留 1 次真实故障与修复
- [ ] 至少保留 1 个 Rule/ML 对照案例

**红线复查**
- [ ] 点击"处理"不会直接变成"已恢复"
- [ ] 优先规则没有写死任何节点
- [ ] 同步不是靠两端手工输入
- [ ] report 没有手工改过结果
- [ ] 模拟数据、构造测试样本都有明确标注
- [ ] 没有手改 ML 输出，也没有为得到答案反复调参

**交付**
- [ ] GitHub 仓库、README、≥5 次有意义 Commit
- [ ] Evidence/ 完整（D1–D5、E1–E3、Debug、Reproduce）且有索引
- [ ] README 已完成一次同伴交叉复现，并保留"发现问题 → 修订 README → 再次复现"的证据
- [ ] PPT 完成（建议 10–15 页）
- [ ] 技术文档完成（建议 10–15 页正文）
- [ ] 演示视频完成（建议 5–8 分钟）
- [ ] 能通过 Run / Explain / Modify / Debug / Verify 现场核验

---

## 附录：常用命令速查

```bash
# 启动 Broker
mosquitto -c broker/mosquitto.conf -v

# 监听所有 DormMate 消息（排错利器）
mosquitto_sub -h localhost -t "dormmate/#" -v

# 手动发布一条数据（Linux/macOS 终端；Windows 下引号转义麻烦，建议用 publish_one.py）
mosquitto_pub -h localhost -t dormmate/v1/nodes/dorm-b/telemetry \
  -m '{"nodeId":"dorm-b","temperature":31.2,"humidity":58,"time":"2026-10-08T14:03:21+08:00","source":"simulated"}'

# 状态中心 / 模拟器 / 剧本回放 / 手动发一条
python core/core.py
python simulator/simulator.py
python simulator/simulator.py --scenario simulator/scenarios/d2_case1.json
python simulator/publish_one.py dorm-b 31.5 62

# 静态页面服务（在仓库根目录运行）
python -m http.server 8000
#   http://localhost:8000/web/    http://localhost:8000/mobile/    http://localhost:8000/three/

# 离线报告与模型训练
python analysis/make_report.py --csv data/history.csv --out report/report.html
python analysis/train_iforest.py

# 端口排查
netstat -ano | findstr 9001        # Windows
lsof -i :9001                      # macOS / Linux

# 查看提交历史
git log --oneline --graph
```

> 最后提醒：任务书允许借助 AI，但每一段代码你都要能讲清楚、能当场改、能当场修。用 AI 生成的代码，先读懂、加注释、自己跑通验证，再提交。
