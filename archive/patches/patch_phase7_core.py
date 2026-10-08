# -*- coding: utf-8 -*-
"""Phase7 第 1 步：config.py 加 HISTORY_PATH、core.py 挂上历史 CSV（**临时脚本，不进仓库**）。

为什么用脚本而不是手改：config.py 和 core.py 都是 **CRLF**（web/ 和 README 也是），
手改时插进去的换行是裸 LF —— 一个文件里混两种换行，diff 会把整段显示成"改过"，
而且下一次 git 规范化的时候又整份翻一遍。

手法：所有锚点和替换文本都写成 "\n" 的普通字符串，过一遍 crlf() 再匹配/落盘，
落盘前断言「裸 LF 仍然是 0」。锚点都带 count == 1 的断言 —— 匹配不到就当场停，
不会写出一个半改的文件。
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(ROOT, "nova-dormmate-final-2026")


def crlf(text):
    """写成 "\n" 的字面量 -> CRLF。已经是 CRLF 的不会被改成 \r\r\n。"""
    return text.replace("\r\n", "\n").replace("\n", "\r\n")


def patch(rel_path, edits):
    """edits 是 [(锚点, 替换, 标签)]，逐个替换，最后一次性落盘。"""
    path = os.path.join(REPO, rel_path)
    with io.open(path, encoding="utf-8", newline="") as fh:
        src = fh.read()

    out = src
    for old, new, label in edits:
        old, new = crlf(old), crlf(new)
        count = out.count(old)
        if count != 1:
            sys.exit("!! %s：锚点「%s」匹配到 %d 处（要正好 1 处）" % (rel_path, label, count))
        out = out.replace(old, new)
        print("   %-28s ok" % label)

    if out.count("\n") != out.count("\r\n"):
        sys.exit("!! %s：落盘前发现裸 LF %d 个"
                 % (rel_path, out.count("\n") - out.count("\r\n")))

    with io.open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(out)
    print("%s：%d 行 -> %d 行" % (rel_path, len(src.splitlines()), len(out.splitlines())))


# ---------------------------------------------------------------- config.py

CONFIG_EDITS = [
    (
        '''EVENTS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "events.json"
)
''',
        '''EVENTS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "events.json"
)


# ---- 历史行（Phase7）----
# core 每收到一条**合法**遥测就往这儿 append 一行，九列见 history.py 的 HEADER。
# 它是**离线分析的输入**：
#
#     py -3.14 analysis/make_report.py --csv data/history.csv
#
# 和 events.json 一样，这份也是运行期产生的数据、不是源码，所以同样进 .gitignore：
# 它一秒一行、每次跑都在变，入库的话每回演示完都多一个「改动」，真正要提交的
# 输入（data/ 下那几份 *_sim.csv）反而被淹掉。要看内容就自己跑一遍 core。
HISTORY_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "history.csv"
)
''',
        "config.py HISTORY_PATH",
    ),
]

# ---------------------------------------------------------------- core.py

CORE_EDITS = [
    (
        "import events  # noqa: E402\nimport rules  # noqa: E402\n",
        "import events  # noqa: E402\n"
        "import history  # noqa: E402\n"
        "import rules  # noqa: E402\n",
        "core.py import history",
    ),
    (
        """        events_path: str | Path | None = None,
    ) -> None:
""",
        """        events_path: str | Path | None = None,
        history_path: str | Path | None = None,
    ) -> None:
""",
        "core.py __init__ 签名",
    ),
    (
        """        self.events_load_message = self.event_book.load()
""",
        """        self.events_load_message = self.event_book.load()

        # ---- 历史行（Phase7）----
        # 默认同样是 None = 不碰磁盘，理由和上面一模一样：造一个 Core 不等于
        # 「现在该往 data/ 里写文件了」，跑测试的时候更不该。run() 显式递路径。
        #
        # 名字叫 history_writer 而不是 history：NodeState 上已经有一个 history
        # （内存里最近 N 条，给趋势图用的），两个都叫 history 的话，
        # 「self.history」在哪个类里是什么意思，读的人得先数一层。
        self.history_path = None if history_path is None else Path(history_path)
        self.history_writer = history.HistoryWriter(self.history_path)
""",
        "core.py 建 writer",
    ),
    (
        """        reason = self._reason_for(record["nodeId"], now_wall)
        for line in self.event_book.observe(node, record, reason=reason):
            log("事件", line)
""",
        """        # 这一条读数落在哪条案卷里？两头都要看一眼：案卷可能被这条报文
        # **开出来**（异常段的第一条），也可能被它**收掉**（凑够 N 条正常的那一条）。
        # 所以先记下「进来时开着的那条」，写完再看一眼「出去时开着的那条」——
        # 后者管开案那一种（第一条异常读数自己就该带着刚开出来的案号），
        # 前者管收案那一种（那条正常读数还是验证数据，属于那条案卷）。
        # 不去拿 last_for() 攀一条早就结掉的案子：那是编。
        case_before = self.event_book.open_event(record["nodeId"])

        reason = self._reason_for(record["nodeId"], now_wall)
        for line in self.event_book.observe(node, record, reason=reason):
            log("事件", line)
""",
        "core.py 记下案卷（前）",
    ),
    (
        """                reason=top.reason,
            )

        # 每收一条就重算并（内容变了才）重发快照。""",
        """                reason=top.reason,
            )

        # 历史行落盘（Phase7）。放在这儿而不是 handle_message 一进来就写：
        # event_id 要的是「这条读数落在哪条案卷里」，而那得等 observe 跑完才知道。
        # 换句话说，这一行写下去的时候，这条报文引起的变化**都已经落定了**。
        self._write_history(record, case_before)

        # 每收一条就重算并（内容变了才）重发快照。""",
        "core.py 写历史行",
    ),
    (
        """        for entry in self.ranked(now_wall):
            if entry.node_id == node_id:
                return entry.reason
        return None
""",
        """        for entry in self.ranked(now_wall):
            if entry.node_id == node_id:
                return entry.reason
        return None

    def _write_history(self, record: dict[str, Any], case_before: Any = None) -> None:
        \"\"\"把一条**已经校验通过**的报文追加进历史 CSV（Phase7）。

        写的是「读数」不是「状态」：一行下去就不改了，所以这里不重写整个文件、
        也不用关心上一次写到哪儿了（不像 events.json 那本要随状态机改）。

        `case_before` 是进这个方法之前那个节点开着的事件（可能没有）。挑案卷的
        规矩见调用点 —— 一句话：**能把这条读数归到某条案卷上就归，归不上就留空**，
        不为了「这一列不留空」去编一个案号。
        \"\"\"
        case = self.event_book.open_event(record["nodeId"]) or case_before
        self.history_writer.append(
            record,
            event_id="" if case is None else case.event_id,
            event_state="" if case is None else case.state,
        )
        # 写不进去（磁盘满 / 被 Excel 占着 / 目录没了）**不许拖垮 core**：
        # 那件事和「宿舍是不是偏热」没有关系，而这台 core 还得接着判状态。
        # 所以只在出错那一刻打一行，之后静默跳过 —— 每条都打的话日志会被刷满。
        message = self.history_writer.take_error()
        if message is not None:
            log("历史", f"{message} —— 以后不再写 CSV，core 照常跑")
""",
        "core.py _write_history",
    ),
    (
        """    core = Core(cfg, quiet=quiet, events_path=config.EVENTS_PATH)
""",
        """    core = Core(cfg, quiet=quiet, events_path=config.EVENTS_PATH,
                history_path=config.HISTORY_PATH)
""",
        "run() 递路径",
    ),
    (
        """    log("事件", f"{core.events_path.name}：{core.events_load_message}")
""",
        """    log("事件", f"{core.events_path.name}：{core.events_load_message}")
    # 历史 CSV 是**追加**的，所以「这一次接着哪一份往下写」也要让人看见：
    # 是新起一份，还是接在昨天那份后面继续加，验收时这两件事完全不一样。
    log("历史", f"{core.history_path.name}："
                f"{'接在已有文件后面写' if core.history_path.exists() else '新起一份，先写表头'}"
                f"　（{config.HISTORY_PATH}）")
""",
        "run() 打一行历史",
    ),
    (
        """        client.disconnect()
        client.loop(timeout=0.5)   # 把 disconnect 真正送出去
""",
        """        # 历史 CSV 收尾。每条都 flush 过，所以这里关不关都不会丢数据 ——
        # 关是因为 Windows 上一个进程攥着的文件，Excel 是打不开的，
        # 而「一边跑 core 一边翻那份 CSV」正是验收时会做的事。
        core.history_writer.close()

        client.disconnect()
        client.loop(timeout=0.5)   # 把 disconnect 真正送出去
""",
        "run() 收尾关文件",
    ),
    (
        """        print(f"  事件文件      {config.EVENTS_PATH}")
""",
        """        print(f"  事件文件      {config.EVENTS_PATH}")
        print(f"  历史文件      {config.HISTORY_PATH}（每收一条合法遥测追加一行）")
""",
        "启动核对打印",
    ),
]

patch("config.py", CONFIG_EDITS)
patch("core.py", CORE_EDITS)
print("完了")
