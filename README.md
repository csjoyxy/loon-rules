# loon-rules

个人 Loon 分流规则仓库，每个目录一套规则，各自独立自动更新。

| 目录 | 规则文件 | 数据源 | 更新时间 |
|------|----------|--------|----------|
| `scamsniffer/` | `ScamSniffer.list` | ScamSniffer 开源钓鱼域名库（最新 30000 条） | 每天 04:17 CST |
| `ai/` | `ai.list` | v2fly `category-ai-!cn` + ACL4SSR AI | 每天 04:27 CST |
| `dustinwin/` | 16 个 `.list` | DustinWin ruleset_geodata（Mihomo 在用的分流规则 + Spotify，转 Loon 格式） | 每天 04:37 CST |

规则文件均为干净 Loon 格式（不带 policy），在 Loon 的 Remote Rule 里指定 policy 即可。

新增一套规则：新建目录 + `build.py`（输出 `.list` 到同目录）+ `.github/workflows/update-xxx.yml`，照抄现有结构。

