# -*- coding: utf-8 -*-
"""造一份「构造样本」CSV（**临时脚本，不进仓库**）。

为什么不在 shell 里 echo：这份文件要 CRLF + UTF-8 BOM（和 data/ 下别的 CSV 一个
口径，.gitattributes 也是这么给它定的），而且列值里有中文。顺着 shell 走一遍，
换行和编码都得靠管道自己猜。

内容的设计意图（写清楚是因为这份文件要提交，读的人得知道它是干什么的）：

  * 九列，和 history.py 的 HEADER **一字不差**——它是「core 那份 CSV 长什么样」
    的样板，列不对就跑不到一起。
  * source 一律写「构造样本」：这份是手写的，不是模拟器跑的，报告里必须归到
    「构造样本」而不是「模拟数据」。
  * **ml_label 这一列有值**（最后三行）。别的 CSV 里这列全空，报告那一段就只出
    一句占位；这份用来把「Rule-ML 对比」那一块真正跑起来 —— 预留的区域是不是
    真能用，得有一份能把两条分支都走到的输入。
    ml_label 的值是**手写的**，不是真跑模型算的：这里要验的是报告的对照表和
    高亮，不是模型准不准。真跑模型是 analysis/ml.py 那条链。
  * 里面刻意留了两行「两种口径说法不一致」的（规则说正常、ml_label 说 abnormal），
    这样报告里那个高亮至少有一条是亮的 —— 全是「一致」的话，等于没验。
  * dorm-a 有一段偏热（31/60 连续三条），好让事件链那边有东西可对：
    31/60 按统一规则算「偏热」。
  * 25/60 正常、16/60 偏冷、25/80 偏湿 —— 四组回归数据都出现一遍。
"""
import io
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(ROOT, "nova-dormmate-final-2026")
OUT = os.path.join(REPO, "data", "constructed_samples.csv")

HEADER = ["time", "nodeId", "temperature", "humidity", "status",
          "ml_label", "event_id", "event_state", "source"]

# (time, nodeId, temperature, humidity, ml_label, event_id, event_state)
# status 一列**不在这里写**，下面按统一规则算出来 —— 手写 status 正是这份
# 数据最该避免的错：报告里那条「规则复核」横幅就是专门抓这个的。
ROWS = [
    ("2026-09-23 14:00:00", "dorm-a", 25, 60, "", "", ""),
    ("2026-09-23 14:05:00", "dorm-a", 31, 60, "", "dorm-a-20260923-140500", "OPEN"),
    ("2026-09-23 14:10:00", "dorm-a", 33, 58, "", "dorm-a-20260923-140500", "OPEN"),
    ("2026-09-23 14:15:00", "dorm-a", 32, 61, "", "dorm-a-20260923-140500", "HANDLING"),
    ("2026-09-23 14:20:00", "dorm-a", 26, 60, "", "dorm-a-20260923-140500", "HANDLING"),
    ("2026-09-23 14:25:00", "dorm-a", 25, 59, "", "dorm-a-20260923-140500", "RECOVERED"),
    ("2026-09-23 14:00:00", "dorm-b", 25, 80, "", "", ""),
    ("2026-09-23 14:05:00", "dorm-b", 26, 82, "", "dorm-b-20260923-140500", "OPEN"),
    ("2026-09-23 14:10:00", "dorm-b", 24, 79, "", "dorm-b-20260923-140500", "OPEN"),
    ("2026-09-23 14:15:00", "dorm-b", 25, 77, "", "dorm-b-20260923-140500", "HANDLING"),
    ("2026-09-23 14:20:00", "dorm-b", 25, 74, "", "dorm-b-20260923-140500", "RECOVERED"),
    ("2026-09-23 14:05:00", "dorm-c", 16, 60, "", "", ""),
    ("2026-09-23 14:10:00", "dorm-c", 17, 62, "", "dorm-c-20260923-140500", "OPEN"),
    ("2026-09-23 14:15:00", "dorm-c", 19, 60, "", "dorm-c-20260923-140500", "RECOVERED"),
    ("2026-09-24 09:00:00", "dorm-a", 25, 60, "normal", "", ""),
    ("2026-09-24 09:05:00", "dorm-a", 25, 61, "abnormal", "", ""),
    ("2026-09-24 09:10:00", "dorm-b", 25, 80, "normal", "", ""),
]


def status_of(temperature, humidity):
    """统一规则。四行，和 status_rules.compute_status 一模一样 ——
    这里抄一遍是为了让这份**数据文件**不依赖项目的代码（它要能单独拷走），
    抄错的话报告开头那条「规则复核」横幅会当场炸出来。"""
    if temperature < 18:
        return "偏冷"
    if temperature >= 30:
        return "偏热"
    if humidity >= 75:
        return "偏湿"
    return "正常"


def main():
    lines = [",".join(HEADER)]
    for time, node_id, temperature, humidity, ml, event_id, state in ROWS:
        lines.append(",".join([
            time, node_id, str(temperature), str(humidity),
            status_of(temperature, humidity), ml, event_id, state, "构造样本",
        ]))

    # CRLF + UTF-8 BOM：和 data/ 下别的 CSV、和 history.py 写出来的那份同一个口径。
    text = chr(0xFEFF) + "\r\n".join(lines) + "\r\n"
    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)

    print("写出 %s" % OUT)
    print("  %d 行数据（不含表头）、%d 列、CRLF + BOM" % (len(ROWS), len(HEADER)))
    print("  source 全是「构造样本」；ml_label 有值的 %d 行"
          % sum(1 for row in ROWS if row[4]))


main()
