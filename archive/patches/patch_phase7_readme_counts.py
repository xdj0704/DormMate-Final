# -*- coding: utf-8 -*-
"""修 README 里的测试条数：106 -> 109、1130 -> 1133（**临时脚本，不进仓库**）。

起因：打开报告给用户看的时候发现标题印的是写死的「core → history.csv → 本报告」，
而第二、第三份报告读的根本不是 history.csv —— 给 PHASE7_TITLE 加了一格文件名，
顺带补了 3 条测试。改完测试是 1133 条，README 里那句 1130 当场就过期了。

和上一个补丁同一个规矩：README 是 CRLF，读和写都 newline=""，按**整行 / 唯一子串**
替换，命中数不是 1 就当场停下，落地前断言 bare LF == 0。
"""
import io
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
README = os.path.join(ROOT, "nova-dormmate-final-2026", "README.md")

# (旧子串, 新子串) —— 每一处在全文里必须**只出现一次**
EDITS = [
    ("# ①②③⑪⑫⑬⑭⑮⑯⑰⑱⑲㉓㉔，共 1130 条",
     "# ①②③⑪⑫⑬⑭⑮⑯⑰⑱⑲㉓㉔，共 1133 条"),

    ("186 + 35 + 106 = 1130 条",
     "186 + 35 + 109 = 1133 条"),

    ("（106 条，需要 pandas / matplotlib）",
     "（109 条，需要 pandas / matplotlib）"),

    ("| ㉔ 106 条 |",
     "| ㉔ 109 条 |"),

    # ㉔ 那条的说明末尾补上这次新加的三条测试，别让描述和条数对不上
    ("两个方向的不一致都高亮而一致的不高亮 |",
     "两个方向的不一致都高亮而一致的不高亮；**标题**——印的是**真正读的那个 CSV**"
     "（换成 --csv 就跟着换，不写死 history.csv）、summary 里没有文件名时说「未指定」、"
     "文件名里的 & 要转义 |"),

    ("`py -3.14 -m unittest tests.test_history tests.test_make_report` 全绿（35 + 106 条）",
     "`py -3.14 -m unittest tests.test_history tests.test_make_report` 全绿（35 + 109 条）"),
]


def main():
    with io.open(README, "r", encoding="utf-8", newline="") as fh:
        text = fh.read()

    if text.count("\r\n") != text.count("\n"):
        raise SystemExit("读进来的 README 里已经有 bare LF，先查清楚再改")

    for old, new in EDITS:
        hits = text.count(old)
        if hits != 1:
            raise SystemExit("【%s】命中 %d 次（预期 1 次）" % (old[:40], hits))
        text = text.replace(old, new)
        print("  改掉 %-46s" % old[:46])

    bare = text.count("\n") - text.count("\r\n")
    if bare != 0:
        raise SystemExit("结果里有 %d 处 bare LF，不落盘" % bare)

    with io.open(README, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)

    print("写出 %s" % README)
    print("  剩余 1130 处：%d，1133 处：%d，bare LF 0 处"
          % (text.count("1130"), text.count("1133")))


main()
