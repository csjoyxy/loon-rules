#!/usr/bin/env python3
"""ScamSniffer 币圈钓鱼域名 -> Loon 规则（裁剪到最新 N 条）"""
import json, re, urllib.request, datetime, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ScamSniffer.list")
SRC = "https://raw.githubusercontent.com/scamsniffer/scam-database/main/blacklist/domains.json"
N = 30000  # 保留最新条数（源文件新的在前）
# 防误杀：这些公共平台本身绝不整域拦截
PROTECT = {"pages.dev","netlify.app","vercel.app","web.app","firebaseapp.com","github.io",
           "trycloudflare.com","workers.dev","gitbook.io","medium.com","google.com",
           "apple.com","icloud.com","binance.com","okx.com","x.com","twitter.com","t.me","telegram.org"}
HOST = re.compile(r"^(?=.{4,253}$)([a-z0-9-]{1,63}\.)+[a-z]{2,63}$")
data = json.load(urllib.request.urlopen(SRC, timeout=60))
out, seen = [], set()
for d in data:
    d = str(d).strip().lower().rstrip(".")
    if d.startswith("www."): d = d[4:]
    if not HOST.match(d) or d in PROTECT or d in seen: continue
    seen.add(d); out.append(d)
    if len(out) >= N: break
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
with open(OUT, "w") as f:
    f.write(f"# NAME: ScamSniffer crypto phishing (latest {len(out)})\n# SOURCE: {SRC}\n# UPDATED: {now}\n# TOTAL: {len(out)}\n")
    f.writelines(f"DOMAIN-SUFFIX,{d}\n" for d in out)
print("total", len(data), "kept", len(out))
