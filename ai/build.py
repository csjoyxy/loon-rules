#!/usr/bin/env python3
"""AI 平台域名 -> Loon 规则（v2fly category-ai-!cn + ACL4SSR AI，全自动）"""
import urllib.request, datetime, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ai.list")

V2FLY = "https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/"
ACL4SSR = "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/AI.list"
# 用户手工补充（2026-10-25 起）
EXTRA_SUFFIX = ["hark.com"]

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "loon-ai-rules"})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8")

def parse_v2fly(name, seen_files, suffix, domain, keyword, stats):
    if name in seen_files:
        return
    seen_files.add(name)
    for raw in fetch(V2FLY + name).splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("include:"):
            parse_v2fly(line[8:].strip(), seen_files, suffix, domain, keyword, stats)
        elif line.startswith("full:"):
            domain.add(line[5:].strip().lower())
        elif line.startswith("domain:"):
            suffix.add(line[7:].strip().lower())
        elif line.startswith("keyword:"):
            keyword.add(line[8:].strip().lower())
        elif line.startswith("regexp:"):
            stats["regexp_skipped"] += 1
        else:
            suffix.add(line.lower())

def parse_acl4ssr(suffix, domain, keyword):
    for raw in fetch(ACL4SSR).splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 2:
            continue
        typ, val = parts[0].upper(), parts[1].lower()
        if typ == "DOMAIN-SUFFIX":
            suffix.add(val)
        elif typ == "DOMAIN":
            domain.add(val)
        elif typ == "DOMAIN-KEYWORD":
            keyword.add(val)

def covered_by_suffix(d, suffix_set):
    # d 是否被任一更广的 SUFFIX 覆盖（含自身相等）
    return any(d == s or d.endswith("." + s) for s in suffix_set)

def main():
    stats = {"regexp_skipped": 0}
    suffix, domain, keyword = set(), set(), set()
    parse_v2fly("category-ai-!cn", set(), suffix, domain, keyword, stats)
    parse_acl4ssr(suffix, domain, keyword)
    for s in EXTRA_SUFFIX:
        suffix.add(s.lower())

    # 去冗余：DOMAIN 被 SUFFIX 覆盖则删；SUFFIX 被更广 SUFFIX 覆盖则删
    domain = {d for d in domain if not covered_by_suffix(d, suffix)}
    suffix = {s for s in suffix if not any(s != o and s.endswith("." + o) for o in suffix)}

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    rules = ([f"DOMAIN-SUFFIX,{s}" for s in sorted(suffix)] +
             [f"DOMAIN,{d}" for d in sorted(domain)] +
             [f"DOMAIN-KEYWORD,{k}" for k in sorted(keyword)])
    rx_note = f" / regexp skipped {stats['regexp_skipped']}" if stats["regexp_skipped"] else ""
    with open(OUT, "w") as f:
        f.write("# NAME: AI platforms (v2fly category-ai-!cn + ACL4SSR AI)\n"
                f"# SOURCE: {V2FLY}category-ai-!cn , {ACL4SSR}\n"
                f"# UPDATED: {now}\n"
                f"# TOTAL: {len(rules)} (suffix {len(suffix)} / domain {len(domain)} / keyword {len(keyword)}{rx_note})\n")
        f.writelines(r + "\n" for r in rules)
    print(f"suffix {len(suffix)} domain {len(domain)} keyword {len(keyword)} "
          f"regexp_skipped {stats['regexp_skipped']} total {len(rules)}")

if __name__ == "__main__":
    main()
