# -*- coding: utf-8 -*-
"""E2-3 的端到端对账（**临时脚本，不进仓库**）。

验的是「浏览器那边拼出来的那条 snapshot 指令，正在跑的 core 收不收」——
unit test 用的是 tests/ 里的假 broker，这里走的是真 Mosquitto + 真 core。

做的事：
  1) 订 dormmate/v1/state，等一帧，把 focus 和每间开着的案子打出来
  2) 照 web/multimodal.js 拼出来的样子发一条 snapshot 指令（水印用 ASCII，
     免得命令行过 GBK）
  3) 等下一帧，看 cameraCount 有没有涨
"""
import json
import sys
import time

import paho.mqtt.client as mqtt

HOST, PORT = "127.0.0.1", 1883
STATE, CMD = "dormmate/v1/state", "dormmate/v1/cmd"

frames = []


def on_connect(c, u, f, rc, props=None):
    c.subscribe(STATE, qos=1)


def on_message(c, u, msg):
    try:
        frames.append(json.loads(msg.payload.decode("utf-8")))
    except Exception as e:  # noqa: BLE001
        print("读不懂的一帧：", e)


def wait_frame(after_count, timeout=12.0):
    end = time.time() + timeout
    while time.time() < end:
        if len(frames) > after_count:
            return frames[-1]
        time.sleep(0.2)
    return None


def open_case(snap, node_id):
    for e in snap.get("events", {}).get("events", []):
        if e.get("nodeId") == node_id and e.get("state") in ("OPEN", "HANDLING"):
            return e
    return None


def camera_count(snap, node_id):
    e = open_case(snap, node_id)
    return None if e is None else (e.get("event_id"), e.get("cameraCount"))


cli = mqtt.Client(client_id="dormmate-e2-link-%d" % (int(time.time()) % 100000))
cli.on_connect, cli.on_message = on_connect, on_message
cli.connect(HOST, PORT, 20)
cli.loop_start()

snap = wait_frame(0)
if snap is None:
    print("!! 一帧快照都没收到：core 在跑吗？")
    sys.exit(1)

print("== 现状 ==")
print("快照版本", snap.get("v"), "时间", snap.get("time"))
print("焦点", (snap.get("focus") or {}).get("nodeId"))
print("重点", (snap.get("priority") or {}).get("nodeId"))
for n in snap.get("nodes", []):
    print("  %-8s %s  %s" % (n.get("nodeId"), n.get("status"), camera_count(snap, n.get("nodeId"))))

# 挑一间开着的案子。一期案子是「正常 -> 异常」那一刻开的，所以现成的通常没有 ——
# core 那边刚把前一期判成 UNRESOLVED / RECOVERED，下一期要等这间**再一次**转异常。
# 模拟器 5 秒一条、随机游走，等一会儿一般就有了。
target = None
deadline = time.time() + 150
while time.time() < deadline:
    for n in snap.get("nodes", []):
        if open_case(snap, n.get("nodeId")):
            target = n.get("nodeId")
            break
    if target:
        break
    got = wait_frame(len(frames) - 1, timeout=8.0)
    if got is not None:
        snap = got
        print("  等开案… 焦点=%s 重点=%s  %s" % (
            (snap.get("focus") or {}).get("nodeId"),
            (snap.get("priority") or {}).get("nodeId"),
            " ".join("%s:%s" % (n.get("nodeId"), n.get("status"))
                     for n in snap.get("nodes", []))))

if target is None:
    print("\n!! 等了 150 秒还是没有未结案的事件 —— snapshot 会被 core 拒收。")
    print("   这一段本身就是证据：core 只往开着的事件上挂，前端说了不算。")
    cli.loop_stop()
    sys.exit(2)
print("\n开着的案子在", target)

ev = open_case(snap, target)
before = ev.get("cameraCount")
stamp = time.strftime("%Y-%m-%d %H:%M:%S")

body = {
    "nodeId": target,
    "action": "snapshot",
    "source": "web",
    "stamp": stamp,
    "width": 640,
    "height": 480,
    "bytes": 48213,
    "file": "%s-%s-%s.png" % (target, ev["event_id"], stamp.replace("-", "").replace(":", "").replace(" ", "")),
    "eventId": ev["event_id"],
    "watermark": "%s / event %s / %s" % (target, ev["event_id"], stamp),
}

print("\n== 发一条 web 形状的 snapshot 指令 ==")
print(json.dumps(body, ensure_ascii=False))
print("（拍之前 cameraCount =", before, "，event_id =", ev["event_id"], "）")

n = len(frames)
cli.publish(CMD, json.dumps(body, ensure_ascii=False), qos=1, retain=False)

after = wait_frame(n)
if after is None:
    print("!! 发完之后没等到新快照")
    cli.loop_stop()
    sys.exit(1)

got = camera_count(after, target)
print("\n== 拍之后 ==")
print("cameraCount ->", got)
if got and got[1] == before + 1:
    print("\nOK：core 收下了，而且只动了那个计数 —— 这正是页面要等的回执。")
else:
    print("\n注意：计数没涨。core 的拒绝理由只在它的日志里（[指令] ... 没接受）。")

cli.loop_stop()
