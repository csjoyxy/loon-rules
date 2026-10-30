#!/usr/bin/env python3
"""DustinWin ruleset -> Loon 规则（复刻 Mihomo 在用的 15 套分流规则）"""
import os, urllib.request, datetime

BASE = "https://github.com/DustinWin/ruleset_geodata/releases/download/mihomo-ruleset/"
# 与用户 mihomo.yaml 里 RULE-SET 引用的一致（fakeip-filter 为 Mihomo FakeIP 专用，Loon 不需要）
RULES = ["ads", "youtube", "applications", "private", "microsoft-cn", "apple-cn",
         "google-cn", "games-cn", "ai", "networktest", "proxy", "cn",
         "telegramip", "privateip", "cnip"]
OUTDIR = os.path.dirname(os.path.abspath(__file__))
LOON_TYPES = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "DOMAIN-WILDCARD",
              "IP-CIDR", "IP-CIDR6", "IP-ASN", "SRC-IP-CIDR", "SRC-IP-CIDR6"}

def convert(line):
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if "," in line:  # 已是标准规则格式
        return line if line.split(",", 1)[0].strip().upper() in LOON_TYPES else None
    if "/" in line:  # IP CIDR
        return f"IP-CIDR6,{line}" if ":" in line else f"IP-CIDR,{line}"
    if line.startswith("+."):  # DustinWin 的后缀标记
        line = line[2:]
    return f"DOMAIN-SUFFIX,{line}"

def main():
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    for name in RULES:
        url = BASE + name + ".list"
        req = urllib.request.Request(url, headers={"User-Agent": "loon-rules"})
        data = urllib.request.urlopen(req, timeout=180).read().decode("utf-8", errors="replace")
        out, seen = [], set()
        for raw in data.splitlines():
            r = convert(raw)
            if r and r not in seen:
                seen.add(r)
                out.append(r)
        with open(os.path.join(OUTDIR, name + ".list"), "w") as f:
            f.write(f"# NAME: DustinWin {name}\n# SOURCE: {url}\n# UPDATED: {now}\n# TOTAL: {len(out)}\n")
            f.writelines(l + "\n" for l in out)
        print(f"{name}: {len(out)}")

if __name__ == "__main__":
    main()
