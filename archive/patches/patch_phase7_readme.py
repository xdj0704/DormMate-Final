# -*- coding: utf-8 -*-
"""把 Phase7 那一节写进 README.md（**临时脚本，不进仓库**）。

README 是 **CRLF + 无 BOM**，而 Python 默认会把读进来的 \\r\\n 全部翻译成 \\n ——
存回去就是一份全 LF 的 README，git diff 会显示「整个文件都改了」。所以：

  * 读和写都用 newline=""（一个字符都不让它翻译）；
  * 拆成行的列表，每一处替换按**整行**匹配，不在行中间动手；
  * 写完断言一次 bare LF == 0，对不上就不落盘。

每一处替换都断言「正好命中一次」：命中 0 次说明 README 已经变了，命中 2 次说明
锚点选得太宽 —— 两种都必须当场停下，绝不能让它悄悄改错地方。

（改这里的字之前先想清楚：README 里的条文是拿来看的，不是拿来「跑」的，
所以宁可少写一句，也不要写一句没验过的。）
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
README = os.path.join(ROOT, "nova-dormmate-final-2026", "README.md")


# ----------------------------------------------------------------------
# 一、主要功能表：加一行
# ----------------------------------------------------------------------

PY_ANALYSIS_ROW = (
    "| Python 分析 | ✅ 已完成（Step 2-2~2-5） | 读 CSV → 规则复核 → 状态统计 → 出 "
    "`report/trend.png` 趋势图 → 出 `report/report.html`；支线还能渲染一份 Markdown 报告 |"
)
SNAPSHOT_ROW = (
    "| 现场快照 | ✅ 已完成（Step 3-1） | 摄像头预览 + 一键拍照，快照显示在页面右侧，标明拍摄时间与分辨率 |"
)
PHASE7_FEATURE_ROW = (
    "| **离线分析链 + 单文件报告** | ✅ 已完成（Phase7） | 两段：①`core.py` 每收到一条"
    "**合法**遥测就往 `data/history.csv` 追加一行（九列，`ml_label` 一列一律空着，理由见下），"
    "只追加、从不改；②`analysis/make_report.py` 读那份 CSV 加 `data/events.json`，出**一份单文件 "
    "HTML**（每个宿舍的温湿度极值与均值、趋势图 base64 内嵌、事件时间线、今日摘要、预留的 "
    "Rule-ML 对照区、数据来源是模拟还是构造）。换一份 `--csv` 报告整篇跟着变 —— 报告是数据的纯函数 |"
)


# ----------------------------------------------------------------------
# 二、目录结构
# ----------------------------------------------------------------------

DIR_EVENTS = [
    "├── events.py                # Step D3 事件状态机：OPEN→HANDLING→RECOVERED/UNRESOLVED，读写 data/events.json",
    "│                            #   恢复与否只看 core 后来收到的报文，处理指令只把事件推到 HANDLING",
    "├── core/",
]
DIR_EVENTS_NEW = [
    "├── events.py                # Step D3 事件状态机：OPEN→HANDLING→RECOVERED/UNRESOLVED，读写 data/events.json",
    "│                            #   恢复与否只看 core 后来收到的报文，处理指令只把事件推到 HANDLING",
    "├── history.py               # Phase7 历史行落盘：每收到一条合法遥测，往 data/history.csv 追加一行",
    "│                            #   九列见文件头的 HEADER；只追加、从不改；写不进去也不抛异常（不拖垮 core）",
    "├── core/",
]

DIR_ANALYSIS = [
    "│   ├── ml.py                # Step 9-2：Isolation Forest 与固定规则的对照（只用历史 fit）",
    "│   └── report.py            # 把同一个 summary 渲染成 Markdown 报告",
]
DIR_ANALYSIS_NEW = [
    "│   ├── ml.py                # Step 9-2：Isolation Forest 与固定规则的对照（只用历史 fit）",
    "│   ├── make_report.py       # Phase7：读历史 CSV + 事件 JSON，出一份**单文件** HTML（图 base64 内嵌）",
    "│   └── report.py            # 把同一个 summary 渲染成 Markdown 报告",
]

DIR_DATA = [
    "│   ├── dorm-a_history_sim.csv  # Step 9-1：dorm-a 的 40 条「平时」历史（全正常，固定种子生成）",
    "│   └── new_samples.csv      # Step 9-1：6 条待判断的新数据（25/60、26/62、29/72、31/60、25/80、17/60）",
    "│                            # （events.json 是 core 自己写的事件记录，运行时产物，不入库 —— 见 .gitignore）",
]
DIR_DATA_NEW = [
    "│   ├── dorm-a_history_sim.csv  # Step 9-1：dorm-a 的 40 条「平时」历史（全正常，固定种子生成）",
    "│   ├── new_samples.csv      # Step 9-1：6 条待判断的新数据（25/60、26/62、29/72、31/60、25/80、17/60）",
    "│   └── constructed_samples.csv  # Phase7：17 行手写的「构造样本」，九列和 history.csv 一字不差；",
    "│                            #   source 写「构造样本」，最后三行的 ml_label 有值 —— 全项目唯一一份",
    "│                            #   能把报告里「Rule-ML 对比」跑成真表格的输入",
    "│                            # （events.json / history.csv 是 core 自己写的运行期产物，不入库）",
]

DIR_REPORT = [
    "│   └── ml_result.json       # Step 9-3：ML 那一段的结论，给看板 fetch（只留文件名，不含本机路径）",
    "├── reports/",
]
DIR_REPORT_NEW = [
    "│   ├── ml_result.json       # Step 9-3：ML 那一段的结论，给看板 fetch（只留文件名，不含本机路径）",
    "│   ├── history-report.html      # Phase7 的产物，**不入库**（.gitignore 里那三行）：一个命令",
    "│   ├── day-sim-report.html      #   就能再生成，换一份 --csv 就整篇不一样，入库只会让每次改",
    "│   └── constructed-report.html  #   代码都多出几百 KB 的 diff。默认 --out 是 history-report.html",
    "│                                #   （刻意不叫 report.html —— 那个名字是 analysis.py 那份的）",
    "├── reports/",
]

DIR_TEST_CORE = [
    "│   ├── test_core.py         # Phase2：core 的 topic 解析 / 报文校验 / 拒收 / 清 retained 的空报文 / 状态机 / 优先排序 / 快照 / 遗嘱 / 配置核对（115 条）",
    "│   │                        #   Step E3-1 补了 26 条：focus 指令 + 快照的 events / rejects / history 三块",
]
DIR_TEST_CORE_NEW = [
    "│   ├── test_core.py         # Phase2：core 的 topic 解析 / 报文校验 / 拒收 / 清 retained 的空报文 / 状态机 / 优先排序 / 快照 / 遗嘱 / 配置核对（138 条）",
    "│   │                        #   Step E3-1 补了 26 条：focus 指令 + 快照的 events / rejects / history 三块",
    "│   │                        #   Phase7 补了 23 条：on_message 那条路上多写一行 history.csv",
]

DIR_TEST_EVENTS = [
    "│   ├── test_events.py       # Step D3：事件状态机 / 落盘读取 / 指令校验 / D3 剧本重放 / 四条红线的静态检查（164 条，不连 broker）",
    "│   │                        #   Step E3-1 补了 19 条：Event.view() 的列 + mark_priority()",
    "│   ├── fixtures/",
]
DIR_TEST_EVENTS_NEW = [
    "│   ├── test_events.py       # Step D3：事件状态机 / 落盘读取 / 指令校验 / D3 剧本重放 / 四条红线的静态检查（186 条，不连 broker）",
    "│   │                        #   Step E3-1 补了 19 条：Event.view() 的列 + mark_priority()",
    "│   │                        #   Phase7 补了 22 条：event_id / event_state 两个字段怎么落进 history.csv",
    "│   ├── test_history.py      # Phase7：history.csv 的九列表头 / 一格怎么写文本 / 追加写与表头只写一次 / 写不进去不抛异常 / core 接线（35 条）",
    "│   ├── test_make_report.py  # Phase7：make_report.py —— 每节点统计 / 长空档断线 / 内嵌图 / source 归类 / 事件时间线 / ML 对照表（106 条，需要 pandas / matplotlib）",
    "│   ├── fixtures/",
]


# ----------------------------------------------------------------------
# 三、跑测试：944 -> 1130
# ----------------------------------------------------------------------

TESTS_CMD = [
    "py -3.14 -m unittest discover -s tests -t . -v   # ①②③⑪⑫⑬⑭⑮⑯⑰⑱⑲，共 944 条",
]
TESTS_CMD_NEW = [
    "py -3.14 -m unittest discover -s tests -t . -v   # ①②③⑪⑫⑬⑭⑮⑯⑰⑱⑲㉓㉔，共 1130 条",
]

TESTS_SUM = [
    "`unittest discover` 会把 `tests/` 下十二个 `test_*.py` 一起收进来",
    "（23 + 206 + 54 + 30 + 123 + 124 + 22 + 115 + 29 + 15 + 39 + 164 = 944 条），所以 `py -3.14` 那条要装 pandas 和 matplotlib，",
]
TESTS_SUM_NEW = [
    "`unittest discover` 会把 `tests/` 下十四个 `test_*.py` 一起收进来",
    "（23 + 206 + 54 + 30 + 123 + 124 + 22 + 138 + 29 + 15 + 39 + 186 + 35 + 106 = 1130 条），所以 `py -3.14` 那条要装 pandas 和 matplotlib，",
]

TESTS_TABLE_TAIL = [
    "",
    "⑤ 的做法是把**真实的** `script.js` 加载进一个最小 DOM 桩里直接调函数，",
]
TESTS_TABLE_TAIL_NEW = [
    "",
    "| ㉓ 35 条 | Phase7 的 `history.py`。**表头**——九列且顺序一字不差、写出来的首行和常量是同一串、"
    "BOM 只写一次、重启再开会话不许在文件中间再冒一行表头、每一行都是 CRLF；**一格怎么写**——"
    "`None` 是空串不是 `\"None\"`、`25.0` 打成 `25`（和手写 CSV 一个写法）、`bool` 不算数字、"
    "`ml_label` 永远是空串且只从 `ML_LABEL_EMPTY` 来；**生命周期**——没给路径就不碰磁盘、"
    "父目录自己建、`close()` 调两次没事、**写不进去只记一笔不抛异常**且出错原因只报一次；"
    "**接线**——走真的 `on_message`：合法报文写一行、被拒的不写、第五格是 `rules.judge_status` 算的"
    "（不是抄报文里的 `status`）、四组回归数据落进 CSV 后逐行对得上；**两个事件列**——开案那条"
    "自己带着刚开出来的案号、案子中间共享同一个、收案那条也还带着、案子之外的读数是空的 |",
    "| ㉔ 106 条 | Phase7 的 `analysis/make_report.py`。**每节点统计**——条数 / 异常条数 / 缺读数"
    "（缺读数**不算**异常）各算各的、极值与均值来自数据本身；**长空档**——隔夜那段必须断开线、"
    "一段里几个空档全断、中位数要忽略掉那个巨大的间隔、只有两个间隔时退回用小的那个（用中位数的话"
    "永远触发不了）；**颜色**——跟着节点名走而不是跟着行的下标走（去掉 dorm-b 不许把 dorm-c 重上色）、"
    "登记表以外的节点拿剩下的槽、槽用完了复用最后一色；**内嵌图**——报告里不许有外部 `src` / `href` / "
    "`<script>` / `<link>`，同一份输入两次跑出**同样的字节**；**source 归类**——`sim` 归模拟数据、"
    "「构造样本」不归模拟数据、混着来就分开列、认不出来的记成「未归类」而**不猜**、"
    "没有这一列时如实说没有；**事件时间线**——五类节点都出得来、按时间排、"
    "只有 `kind == \"camera\"` 才算照片、时间优先用 core 那个 `time` 并把快门时刻附上、"
    "被拒的指令标成被拒、字段坏掉不崩、太长时封顶并写明；**ML 那一段**——"
    "「没有这一列」和「整列是空的」是**两句不同的话**（一条测试盯着它们不许混）、"
    "有值才出表、只列有标签的行、两个方向的不一致都高亮而一致的不高亮 |",
    "",
    "⑤ 的做法是把**真实的** `script.js` 加载进一个最小 DOM 桩里直接调函数，",
]


# ----------------------------------------------------------------------
# 四、Phase7 正文（插在 ## 已知限制 之前）
# ----------------------------------------------------------------------

PHASE7_SECTION = r"""
## Phase7：core 落盘 → 单文件离线报告

Phase7 把「采集 → 展示」这条线接到了「归档 → 离线分析」上。两个进程、两份文件，
中间不经过网络：

```
core.py ──每收到一条合法遥测──→ data/history.csv   （一行一条读数，只追加）
core.py ──事件状态机每次变动──→ data/events.json   （Step D3 就有了）

data/history.csv + data/events.json
  └─→ py -3.14 analysis/make_report.py
        └─→ report/history-report.html   ← 一个文件，双击就能打开
```

两头的共同点是**都是读文件**：`analysis/make_report.py` 不认识 broker、不 import
core、不碰 1883 —— 给它两份文件它就出报告。所以「换一份 CSV、报告整篇跟着变」
这句话是可以当场验的，见下面「复现操作」。

### 九列，其中一列永远是空的

`history.py` 的 `HEADER` 就是这九列，列名和顺序都不许动
（`tests/test_history.py` 里有一条逐字比对）：

| 列 | 谁填的 | 说明 |
|---|---|---|
| `time` | 报文 | 报文里那个时刻，**不是**收到时刻 —— 和 core 别处一个口径 |
| `nodeId` | 报文 | |
| `temperature` / `humidity` | 报文 | 数字走 `%g`：`25.0` 打成 `25`、`57.60` 打成 `57.6`，和 `data/` 下那几份手写 CSV 一个写法 |
| `status` | **core 算的** | `rules.judge_status` 的结论。报文里那个 `status` 只用来对账，落盘的是重算的（有一条测试专门钉这件事） |
| `ml_label` | **不填** | 见下 |
| `event_id` / `event_state` | 事件状态机 | 这条读数落在哪条案卷里；案卷之外留空 |
| `source` | 报文 | 发的人是谁：模拟器 `sim` / 剧本 `script` / 页面 `web` / 手写文件 `模拟`、`构造样本` |

**`ml_label` 一列 core 一律写空串，这是刻意的。** core 里没有 ML —— 为了填满
这一列去猜一个标签写进去，就是在报告里伪造一个「模型判断」。真正的 ML 结论在
另一条链上（`analysis/ml.py` 跑完写 `report/ml_result.json`），它是**离线**的，
不回填这份 CSV。留着一列空着，离线那边才分得出「这一行根本没跑 ML」和
「跑了、判成 normal」—— 整列不存在的话，这两种情况在报告里长得一模一样。

### 追加写，而且写不进去不许拖垮 core

这份文件是**档案**不是状态：一行写下去就不再动它。所以没有「重写整个文件」这一步
（`events.json` 有，它得跟着状态机改），也就没有「跑到一半崩了、文件是半截的」
那种事 —— 最坏情况是最后一行没写全，删掉重来即可。

表头只看**文件本身**空不空，不看「这个进程写过没有」：core 重启一次就再写一份表头
的话，文件中间会冒出一行表头，读的人只会以为后面那些是另一张表。

磁盘满了、文件被 Excel 独占打开着、目录被删了 —— 这些都发生过，而它们和「宿舍
是不是偏热」没有关系。所以 `HistoryWriter` 出错时**不抛异常**：记下那句话、把自己
关掉、之后每条静默跳过，让 core 接着跑；那句话由 `take_error()` 取一次，core 拿它
打一行日志 —— 只在出错当时打一次，不然现场每秒一条遥测会把日志刷满。

### 报告是数据的纯函数

报告里的数字没有一个是写死的，也没有一处是「上一次跑剩下的状态」。最直接的证据
是同一个脚本喂三份不同的 CSV：

| `--csv` | 条数 | source 归类 | ML 那一段 |
|---|---|---|---|
| `data/history.csv`（默认） | 跑多久写多久 | 全部 `sim` → 模拟数据 | 占位（这一列是空的） |
| `data/day_sim.csv` | 864 | 全部 `模拟` → 模拟数据 | 占位（**压根没有这一列**） |
| `data/constructed_samples.csv` | 17 | 「构造样本」 | **真出对照表**（唯一一份 `ml_label` 有值的输入） |

`history.csv` 那一格故意不写条数：它是 core 的运行期产物，core 在跑就一直在长。

### 图为什么 base64 内嵌

要求是「单文件、直接打开、不需要额外静态资源」。`analysis/analysis.py` 出的
`report/report.html` 用的是 `<img src="trend.png">` —— 那份报告和 `trend.png` 必须
待在一起，拷走一个就只剩个裂图。Phase7 这份把 PNG 编成 `data:` URL 写在 HTML 里，
代价是文件大（三百来 KB，一大半是那张图），换来的是**拷到哪里都不坏**。
`tests/test_make_report.py` 里有一条断言报告里没有任何外部 `src` / `href` /
`<script>` / `<link>`。

图本身是两张上下堆叠的子图（温度一张、湿度一张），**不是双 Y 轴** —— 温湿度量纲
不同，画在一个轴上要么一条被压平、要么得给两条轴，读的人会拿两条轴的交点当结论。
阈值线画成虚线，数值取 `rules.py` 里的常量（不在画图的地方再抄一遍）。三个节点的
颜色按固定顺序取，而且**跟着节点名走**：去掉 dorm-b 再跑，dorm-a 和 dorm-c 的颜色
不会跟着往前挪一格。

### 长空档把线断开，不连一条假的直线

这是画完图**看了**才发现的一条：`data/history.csv` 里有一段隔夜的空档（那天跑完
停了十几个小时又接着跑），默认的折线会在两个点之间拉一条笔直的长线，看起来像
「这两个时刻之间一直稳定在某个值」。这和缺读数是同一类错 —— 都是**编出一段没
发生过的连续性**，只是这次没有空值可抓，更难发现。

所以两点之间的间隔超过采样中位数的 6 倍时，中间插一个 `NaN` 把线断开，并在图下面
那行说明里写清楚断了几处、为什么断。判「采样间隔」用的是**正间隔的中位数**；只有
两三行数据时中位数取不到，就退回用最小的那个正间隔 —— 只有两个间隔时中位数总会
取到大的那个，而它永远不可能超过自己的 6 倍，空档检测就一次都不会触发。

### Rule-ML 对照表：预留区域，三种写法

报告里有一段「Rule-ML 对比」。它有三种样子，取决于输入：

1. **CSV 里压根没有 `ml_label` 这一列** —— 说「这份数据里没有这一列」；
2. **有这一列，但全是空的** —— 说「这一列是空的」，并解释为什么空（core 不跑 ML）；
3. **有值** —— 出对照表：宿舍 / 时间 / 温湿度 / 固定规则的说法 / CSV 里那个
   `ml_label` / 一致不一致，**两个方向的不一致都高亮**（规则说正常而 ML 说异常、
   反过来也算）。

前两种是**两句不同的话**，不是同一句的两种说法 —— 有一条测试盯着它们不许混。
`data/constructed_samples.csv` 是第三种的样板：那三行 `ml_label` 是**手写**的，验的是
报告的对照表和高亮，不是模型准不准（真跑模型是 `analysis/ml.py` 那条链）。

### 事件时间线

读 `data/events.json`，把每条案卷的五个节点摆成一条时间线：**开案 / 定为重点 /
收到处理指令 / 现场快照 / 结案**。现场快照只数 `kind == "camera"` 的那种记录 ——
同一个 `add_snapshot` 也被状态流转用着，那些记录没有 `kind`，混进来会把「拍了几张
照片」数错。每条的时间优先用 core 那个 `time`，和前端快门时刻（`stamp`）不一样时
把 `stamp` 附在后面：两台机器的钟差多少，一眼看得出。

CSV 和 `events.json` 的时间范围**不重叠**时会多出一句提醒 —— 那多半是拿了一份别的
时刻的 CSV 配了一份现在的事件，报告里那些对不上号的地方是先说清楚，而不是让人
自己去发现。

### 复现操作：换两份 CSV，看报告整篇变

```bash
# ① 先让 core 跑一会儿，攒出一份 history.csv（Phase7 之前没有这个文件）
py -3.14 core.py                                  # 另开一个终端
py -3.14 simulator/simulator.py --all-nodes       # 再开一个终端

# ② 默认参数：读 history.csv，出 report/history-report.html
py -3.14 analysis/make_report.py

# ③ 换一份完全不同的 CSV，出第二份报告（864 行、一天的数据）
py -3.14 analysis/make_report.py --csv data/day_sim.csv --out report/day-sim-report.html

# ④ 再换一份：这份的 ml_label 有值，「Rule-ML 对比」从占位变成真表格
py -3.14 analysis/make_report.py --csv data/constructed_samples.csv --out report/constructed-report.html
```

然后把三份 HTML 各双击打开一遍。`--csv` / `--events` / `--out` 的相对路径都按
**项目根**展开（和 `analysis.py` 一个规则），在哪个目录下敲都一样。

**不要手工改 `report/*.html` 里的任何数字。** 要改就改输入再跑一遍 —— 那三份报告
本来就不入库（`.gitignore` 里三行），理由正是「它们必须能重新生成」。

### 自测清单

- [ ] `py -3.14 -m unittest tests.test_history tests.test_make_report` 全绿（35 + 106 条）
- [ ] `data/history.csv` 不在时先起 core：日志里有 `[历史] history.csv：新起一份，先写表头`，文件头就是那九列，之后每条合法遥测多一行
- [ ] 拿 MQTTX 发一条**非法**报文（比如缺 `humidity`）：reject 上有它，**history.csv 不多行**
- [ ] 依次发 `25/60`、`16/60`、`31/60`、`25/80` 四条：CSV 里 `status` 那列是 `正常 / 偏冷 / 偏热 / 偏湿`（重算的，不是抄报文里那个）
- [ ] 制造一段异常 → 处理 → 恢复：那条案卷的 `event_id` 从开案那条读数一直跟到收案那条；案卷之外的读数是空的
- [ ] `ml_label` 那一列**从头到尾都是空的**（这是对的，不是没做完）
- [ ] 默认参数跑一遍 `make_report.py`：命令行打出每个宿舍的温湿度极值与均值、数据来源那句、事件条数、报告路径与大小
- [ ] 打开 `report/history-report.html`：把 `report/` 里除 HTML 外的东西挪走照样显示（图是内嵌的，没有任何外部资源）
- [ ] 换 `--csv data/day_sim.csv` 再出一份：条数、极值、趋势图、事件时间线**全都变了**，两份的数字一个都对不上
- [ ] 换 `--csv data/constructed_samples.csv`：「Rule-ML 对比」从占位变成一张表，两个方向的不一致各至少高亮一行
- [ ] 故意把 CSV 里一格改坏（比如温度写成 `不热`）：报告**不炸**，那一行按「缺读数」算
- [ ] 故意填一个不存在的 `--csv`：报错说的是「这一份要先跑 core / 模拟器攒出来」，不是一串 traceback

### Evidence 证据建议

1. core 终端那两行：`[历史] history.csv：新起一份，先写表头`，以及启动参数表里的
   `历史文件 …（每收一条合法遥测追加一行）`
2. `data/history.csv` 用 Excel / WPS 打开的样子（中文不乱码 = BOM 生效；列就是那九列）
3. **同一份脚本、三份不同 CSV** 的三次命令行输出截图（条数 / 极值 / 来源那句各不相同）
4. 三份报告并排打开：`history-report.html`、`day-sim-report.html`、
   `constructed-report.html`（第三份那张 Rule-ML 对照表要看得清高亮）
5. 趋势图那张：三个节点各自的颜色、阈值虚线、**断开的隔夜空档**（说明里写着断了几处）
6. 把 `report/` 里除 HTML 外的文件挪走之后报告照样显示 —— 证明单文件
7. `git check-ignore -v report/history-report.html` 的输出（报告不入库是有意的）

### 变异测试

把下面这几处**故意改坏**，对应的测试必须红：

| 改哪儿 | 谁该红 |
|---|---|
| `history.py` 的 `HEADER` 里删掉 `ml_label` | ㉓ 的表头那三条 |
| `row_of()` 第五格改成 `record.get("status")`（不重算） | ㉓ `test_status_column_is_computed_not_copied` |
| `_cell()` 里把 `None` 打成 `"None"` | ㉓ `test_missing_is_empty_not_none` |
| `append()` 出错时改成 `raise` 而不是 `_fail()` | ㉓ `test_write_failure_does_not_raise_and_stops` |
| `_open()` 里改成「每次都写表头」 | ㉓ `test_header_only_once_across_reopen` |
| `assign_colors()` 改成按下标取色（`NODE_COLORS[len(out)]`） | ㉔ `test_colours_follow_the_node_not_the_row_count` |
| `break_long_gaps()` 直接 `return 0` | ㉔ `test_a_night_long_gap_gets_a_break` 那几条 |
| `sampling_basis()` 去掉「少于 3 个正间隔就取最小的」那条回退 | ㉔ `test_only_two_intervals_uses_the_smaller_one` |
| `ml_section()` 把「没有这一列」和「整列是空的」合成一句话 | ㉔ `test_the_placeholder_does_not_claim_there_is_a_column_when_there_is_none` |
| `timeline_entries()` 里不再过滤 `kind == "camera"` | ㉔ `test_only_camera_snapshots_count_as_photos` |
| `plot_trend_base64()` 改成写一份 `trend.png` 再用 `<img src="trend.png">` | ㉔ `test_section_inlines_the_image_and_never_an_external_file` |
""".strip("\n").split("\n")


# ----------------------------------------------------------------------
# 五、已知限制：设计如此 / 环境依赖 各加几行
# ----------------------------------------------------------------------

LIMITS_DESIGN_TAIL = [
    "",
    "### 还没做",
]
LIMITS_DESIGN_TAIL_NEW = [
    "| `data/history.csv` 会一直长，没有轮转、没有上限 | 它是**档案**，一条读数一行，只追加 —— 一条都不许丢，所以没有「超过 N 条就删老的」这种事（那是 core 内存里 `historyMax` 管的另一码事）。`--all-nodes` 默认 5 秒一轮 = 每小时 2160 行，跑一整天约 5 万行、两三 MB。要归档就在演示前把文件挪走：core 下次启动发现文件是空的，会重新写一行表头（**不会**在中间补表头） |",
    "| `make_report.py` 出的报告**不是** `report/report.html` | 两个脚本、两份报告，**有意不合并**：`analysis/analysis.py` 那份是 Step 2-5 的交付物，图是外部 `trend.png`（拷走就裂）；Phase7 这份要的是「单文件、换一份 CSV 就整篇重来」，连数据源都不一样（前者读导出的 CSV + 那两份 C 部分数据，后者读 core 落盘的 `history.csv`）。所以默认输出是 `report/history-report.html` —— 不叫 `report.html` 就是为了不至于让人以为哪个覆盖了哪个 |",
    "| Phase7 那三份生成的报告**不入库** | `.gitignore` 里点名了三行（`report/history-report.html` / `day-sim-report.html` / `constructed-report.html`），理由是三条：①一个替换一份 CSV 就是一次全量重排，几百 KB 的 HTML 进仓库只会把真正要提交的东西淹在 diff 里；②「报告结果禁止手工修改」的前提就是「报告是跑出来的」，一旦入库，看到的人第一反应是去改文件而不是改输入再跑；③`history-report.html` 的输入 `data/history.csv` 本来就忽略，这份报告离开那台机器就再也复现不出来，单独入库是孤儿。**`report/report.html` 不在这个列表里**，它是早就入库的交付物 |",
    "| 报告里那张趋势图是**死图**，没有悬停/放大 | HTML 图表那套交互（十字准星、tooltip）在单文件报告里没做 —— 这是一张内嵌的 PNG，不是 canvas。要数字就看图下面那张「每个宿舍的温湿度」表：极值和均值都在上面。真要能悬停就把这一块改成 SVG 或 canvas 自绘，那是另一件事，不在 Phase7 的范围里 |",
    "| 事件时间线最多列 160 条 | `TIMELINE_MAX` 封顶，超了会**写明**「共 N 条，这里列了前 160 条」而不是悄悄截断。这是给「一屏能读完」让的路；完整的那一份永远在 `data/events.json` 里（报告是「一帧」，不是档案，和快照只留最近 20 条那个限制同一个道理） |",
    "",
    "### 还没做",
]

LIMITS_ENV_TAIL = [
    "",
    "## 排查",
]
LIMITS_ENV_TAIL_NEW = [
    "| `analysis/make_report.py` 需要 pandas / matplotlib | 和 `analysis.py` 是同两个依赖，没装时**报错方式不一样**：读不进来就直接退出（不会写出一份半截报告）；pandas 在、matplotlib 不在时**报告照出**，只是「趋势图」那一块换成一句「这一段没跑 + 原因」，其余各段一个不少。画图那几只测试同样在 `skipUnless(HAS_MPL)` 里，跳过不是失败 |",
    "| `make_report.py` 对 `history.csv` 的**列**有要求，对**行**没有 | 九列缺了哪一列会当场说清楚缺哪一列（`analysis.load()` 那道把关）；多出来的列不管。行数、节点数、时间跨度都不限 —— 一份 17 行的构造样本和一份 864 行的日数据走的是同一条路。**没有 `source` 列**时说「看不出这份数据是模拟的还是现采的」，**没有 `ml_label` 列**时 Rule-ML 那一段出占位 —— 都不算错 |",
    "",
    "## 排查",
]


EDITS = [
    ("主要功能表", [PY_ANALYSIS_ROW, SNAPSHOT_ROW],
     [PY_ANALYSIS_ROW, PHASE7_FEATURE_ROW, SNAPSHOT_ROW]),
    ("目录结构 · history.py", DIR_EVENTS, DIR_EVENTS_NEW),
    ("目录结构 · make_report.py", DIR_ANALYSIS, DIR_ANALYSIS_NEW),
    ("目录结构 · constructed_samples.csv", DIR_DATA, DIR_DATA_NEW),
    ("目录结构 · report/", DIR_REPORT, DIR_REPORT_NEW),
    ("目录结构 · test_core.py 条数", DIR_TEST_CORE, DIR_TEST_CORE_NEW),
    ("目录结构 · 两个新测试文件", DIR_TEST_EVENTS, DIR_TEST_EVENTS_NEW),
    ("跑测试 · 命令行", TESTS_CMD, TESTS_CMD_NEW),
    ("跑测试 · 合计", TESTS_SUM, TESTS_SUM_NEW),
    ("跑测试 · 表格", TESTS_TABLE_TAIL, TESTS_TABLE_TAIL_NEW),
    ("正文 · Phase7", ["", "", "## 已知限制"],
     ["", ""] + PHASE7_SECTION + ["", "", "## 已知限制"]),
    ("已知限制 · 设计如此", LIMITS_DESIGN_TAIL, LIMITS_DESIGN_TAIL_NEW),
    ("已知限制 · 环境依赖", LIMITS_ENV_TAIL, LIMITS_ENV_TAIL_NEW),
]


def apply(lines, label, old, new):
    """整行匹配，命中数必须是 1。"""
    width = len(old)
    hits = [
        i for i in range(len(lines) - width + 1)
        if lines[i:i + width] == old
    ]
    if len(hits) != 1:
        raise SystemExit("【%s】锚点命中 %d 次（预期 1 次）" % (label, len(hits)))
    at = hits[0]
    # 锚点里不含空行的（比如「主要功能表」那两行），确认它没被更大的块套住
    out = lines[:at] + list(new) + lines[at + width:]
    print("  %-34s 第 %5d 行　%d 行 -> %d 行" % (label, at + 1, width, len(new)))
    return out


def main():
    with io.open(README, "r", encoding="utf-8", newline="") as fh:
        text = fh.read()

    if text.count("\r\n") != text.count("\n"):
        raise SystemExit("读进来的 README 里已经有 bare LF，先查清楚再改")

    lines = text.split("\r\n")
    print("原样读入：%d 行，CRLF %d 处，bare LF 0 处" % (len(lines), text.count("\r\n")))

    for label, old, new in EDITS:
        lines = apply(lines, label, old, new)

    out = "\r\n".join(lines)

    bare = out.count("\n") - out.count("\r\n")
    if bare != 0:
        raise SystemExit("结果里有 %d 处 bare LF，不落盘" % bare)
    if out.count("\r\n") != out.count("\n"):
        raise SystemExit("换行数对不上，不落盘")
    # 全文里不许出现我脚本自己的痕迹
    for bad in ("PY_ANALYSIS_ROW", "LIMITS_ENV_TAIL", "PHASE7_SECTION"):
        if bad in out:
            raise SystemExit("正文里混进了脚本变量名 %s，不落盘" % bad)

    with io.open(README, "w", encoding="utf-8", newline="") as fh:
        fh.write(out)

    print("写出 %s" % README)
    print("  %d 行、%d 字节、CRLF %d 处、bare LF 0 处、没有 BOM（首字符 %r）"
          % (len(lines), len(out.encode("utf-8")), out.count("\r\n"), out[0]))


main()
