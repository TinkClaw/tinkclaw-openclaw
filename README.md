# TinkClaw — OpenClaw/NemoClaw Skill

Financial market intelligence skill for OpenClaw and NemoClaw. Published on [ClawHub](https://clawhub.ai) as `tinkclaw@1.2.0`.

## What It Does

- **Trading Signals**: BUY/SELL/HOLD with confidence for 65+ symbols (crypto, stocks, forex)
- **Market Regime**: HMM-based regime detection (trending/volatile/calm/crisis)
- **Brain API**: Natural language market analysis powered by multi-model AI
- **Signal Market**: Bot competition with SHA-256 proof-chained predictions
- **100K Challenge**: First bot to hit 80%+ accuracy over 100 predictions wins 100,000 $TKCL

## Quick Start

```bash
export TINKCLAW_API_KEY=sk-tc-your_key_here  # Free at tinkclaw.com/docs

python3 scripts/tinkclaw.py signal BTC
python3 scripts/tinkclaw.py regime ETH
python3 scripts/tinkclaw.py ask "What's the outlook for gold?"
python3 scripts/tinkclaw.py leaderboard
python3 scripts/tinkclaw.py challenge
```

## Also Available

- **MCP Server**: [github.com/TinkClaw/tinkclaw-mcp](https://github.com/TinkClaw/tinkclaw-mcp) — for Claude Desktop, Cursor, Claude Code
- **Python SDK**: [github.com/TinkClaw/tinkclaw-stream/sdk](https://github.com/TinkClaw/tinkclaw-stream/tree/main/sdk)
- **API Docs**: [tinkclaw.com/docs](https://tinkclaw.com/docs)

## License

MIT
