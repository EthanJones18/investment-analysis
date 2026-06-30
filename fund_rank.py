#!/usr/bin/env python3
"""国内公募基金行情 - 昨日收益排行查询工具

数据源: 天天基金网(东方财富)开放式基金排行接口
  http://fund.eastmoney.com/data/rankhandler.aspx

用法:
  python3 fund_rank.py              # 全部公募基金, 昨日日增长率前十
  python3 fund_rank.py --top 20     # 前 20 名
  python3 fund_rank.py --type gp    # 仅股票型 (gp/hh/zq/zs/qdii/fof/all)
  python3 fund_rank.py --asc        # 改为升序(看跌幅榜)

说明:
  "昨日收益" = 最近一个净值日期的日增长率(日涨跌幅)。基金净值通常在
  交易日收盘后(约 19:00-21:00)更新, 所以 T 日盘后查询到的即 T 日净值,
  非交易日查询到的是上一个交易日的净值。脚本会打印实际净值日期供核对。
"""
import argparse
import json
import re
import sys
from datetime import datetime

import requests

RANK_URL = "http://fund.eastmoney.com/data/rankhandler.aspx"

# rankhandler 返回的每条记录为逗号分隔字符串, 字段含义(常用部分):
#  0 基金代码  1 拼音缩写  2 基金简称  3 净值日期  4 单位净值  5 累计净值
#  6 日增长率  7 近1周  8 近1月  9 近3月  10 近6月  11 近1年  12 近2年
#  13 近3年   14 今年来  15 成立来
FIELDS = ["代码", "_py", "名称", "净值日期", "单位净值", "累计净值",
          "日增长率", "近1周", "近1月", "近3月", "近6月", "近1年",
          "近2年", "近3年", "今年来", "成立来"]

# 基金类型: 接口 ft 参数
FUND_TYPES = {
    "all": "全部", "gp": "股票型", "hh": "混合型", "zq": "债券型",
    "zs": "指数型", "qdii": "QDII", "fof": "FOF",
}


def fetch_rank(ftype="all", top=10, asc=False):
    """拉取开放式基金排行(按日增长率排序)。"""
    params = {
        "op": "ph",          # 排行
        "dt": "kf",          # 开放式基金
        "ft": ftype,         # 基金类型
        "rs": "",
        "gs": "0",
        "sc": "rzdf",        # sort column = 日增长率(yesterday's daily return)
        "st": "asc" if asc else "desc",
        "qdii": "",
        "tabSubtype": ",,,,,",
        "pi": "1",
        "pn": str(max(top, 10)),
        "dx": "1",
    }
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0 Safari/537.36"),
        "Referer": "http://fund.eastmoney.com/data/fundranking.html",
        "Accept": "*/*",
    }
    r = requests.get(RANK_URL, params=params, headers=headers, timeout=15)
    r.raise_for_status()
    return parse_rank(r.text)


def parse_rank(text):
    """解析 rankhandler 返回的 JS 文本: var rankData = {datas:[...], ...}。"""
    m = re.search(r"datas:\s*(\[.*?\])\s*,\s*allRecords", text, re.S)
    if not m:
        raise ValueError("未能解析接口返回内容, 接口格式可能已变更")
    rows = json.loads(m.group(1))
    funds = []
    for row in rows:
        parts = row.split(",")
        rec = {FIELDS[i]: parts[i] for i in range(min(len(FIELDS), len(parts)))}
        rec.pop("_py", None)
        funds.append(rec)
    return funds


def print_table(funds, top, nav_date, ftype):
    title = f"昨日公募基金({FUND_TYPES.get(ftype, ftype)})收益排行 前{top}"
    print(f"\n{'='*68}")
    print(f"📊 {title}")
    print(f"{'='*68}")
    print(f"⏰ 查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📅 净值日期: {nav_date}  (即'昨日'收益对应的交易日)")
    print(f"💡 数据源: 天天基金网(东方财富) 开放式基金排行")
    print(f"{'-'*68}")
    print(f"{'排名':<4}{'代码':<9}{'名称':<20}{'日增长率':>9}{'单位净值':>10}")
    print(f"{'-'*68}")
    for i, f in enumerate(funds[:top], 1):
        name = f.get("名称", "")
        # 中文按 2 列宽对齐: 截断到 ~18 显示宽度
        disp = name if _w(name) <= 19 else _truncate(name, 18) + "…"
        pad = " " * max(0, 20 - _w(disp))
        rzdf = f.get("日增长率", "")
        rzdf_s = f"{rzdf}%" if rzdf not in ("", "---") else "--"
        print(f"{i:<4}{f.get('代码',''):<9}{disp}{pad}{rzdf_s:>9}"
              f"{f.get('单位净值',''):>10}")
    print(f"{'='*68}\n")


def _w(s):
    """估算显示宽度: 中文算 2, 其余算 1。"""
    return sum(2 if ord(c) > 0x2E7F else 1 for c in s)


def _truncate(s, width):
    out, w = "", 0
    for c in s:
        cw = 2 if ord(c) > 0x2E7F else 1
        if w + cw > width:
            break
        out += c
        w += cw
    return out


def main():
    ap = argparse.ArgumentParser(description="国内公募基金 昨日收益排行查询")
    ap.add_argument("--top", type=int, default=10, help="显示前 N 名(默认 10)")
    ap.add_argument("--type", default="all", choices=list(FUND_TYPES),
                    help="基金类型(默认 all 全部)")
    ap.add_argument("--asc", action="store_true", help="升序(查看跌幅榜)")
    ap.add_argument("--save", action="store_true", help="保存 JSON 到 output/")
    args = ap.parse_args()

    print("🚀 正在查询国内公募基金昨日收益排行...")
    try:
        funds = fetch_rank(args.type, args.top, args.asc)
    except (requests.exceptions.ProxyError,
            requests.exceptions.HTTPError) as e:
        # 出口代理对未放行域名以 403 拒绝 CONNECT, requests 会抛 HTTPError/ProxyError
        status = getattr(getattr(e, "response", None), "status_code", None)
        if isinstance(e, requests.exceptions.ProxyError) or status in (403, 407):
            print("❌ 网络受限: 当前环境的出口策略禁止访问 fund.eastmoney.com。")
            print("   请在可访问该域名的环境(允许 *.eastmoney.com)中运行本脚本。")
            print(f"   详情: {e}")
            sys.exit(2)
        print(f"❌ 查询失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        sys.exit(1)

    if not funds:
        print("❌ 未获取到任何基金数据")
        sys.exit(1)

    nav_date = funds[0].get("净值日期", "N/A")
    print_table(funds, args.top, nav_date, args.type)

    if args.save:
        ts = datetime.now().strftime("%Y%m%d_%H%M")
        path = f"output/fund_rank_top{args.top}_{args.type}_{ts}.json"
        payload = {
            "查询时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "净值日期": nav_date,
            "基金类型": FUND_TYPES.get(args.type, args.type),
            "排序": "日增长率" + ("升序" if args.asc else "降序"),
            "数据": funds[:args.top],
        }
        with open(path, "w", encoding="utf-8") as fp:
            json.dump(payload, fp, ensure_ascii=False, indent=2)
        print(f"💾 已保存: {path}")

    print("✅ 查询完成！")


if __name__ == "__main__":
    main()
