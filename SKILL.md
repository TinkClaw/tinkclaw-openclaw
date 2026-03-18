---
name: tinkclaw
description: >
  Financial market intelligence from TinkClaw's AI engine. Use when user asks about
  stock prices, crypto signals, market regime, trading signals, technical analysis,
  BTC, ETH, forex, S&P500, gold, or any financial market question. Provides real-time
  AI-generated signals (BUY/SELL/HOLD), regime detection, price data, and market
  analysis across 65+ symbols (crypto, stocks, forex, commodities). Requires a free
  TinkClaw API key from tinkclaw.com/docs.
metadata:
  openclaw.emoji: "📊"
  openclaw.requires.bins:
    - python3
    - curl
---

# TinkClaw — AI Market Intelligence

You have access to TinkClaw's financial AI engine. Use the helper script to fetch
real-time market data, signals, and analysis.

## Setup

The user needs a TinkClaw API key. If they don't have one:
1. Direct them to https://tinkclaw.com/docs to sign up (free tier available)
2. They'll receive an API key starting with `sk-tc-`
3. Store it: `export TINKCLAW_API_KEY=sk-tc-...`

## Available Commands

Run via the helper script at `scripts/tinkclaw.py`:

### Get Signal for a Symbol
```bash
python3 scripts/tinkclaw.py signal BTC
python3 scripts/tinkclaw.py signal AAPL
python3 scripts/tinkclaw.py signal EURUSD
```
Returns: direction (BUY/SELL/HOLD), confidence %, current price, regime state.

### Get Market Regime
```bash
python3 scripts/tinkclaw.py regime BTC
```
Returns: current market regime (trending/volatile/calm/crisis), confidence, forecast.

### Ask the Brain API (Natural Language)
```bash
python3 scripts/tinkclaw.py ask "Is it a good time to buy ETH?"
python3 scripts/tinkclaw.py ask "What's the macro outlook for gold?"
python3 scripts/tinkclaw.py ask "Compare BTC and SOL momentum"
```
Returns: AI analysis powered by multi-model consensus (Claude + DeepSeek + Kimi).

### Get Leaderboard
```bash
python3 scripts/tinkclaw.py leaderboard
```
Returns: top AI predictors ranked by verified accuracy. Every prediction is SHA-256 hash-chained.

### Multi-Symbol Scan
```bash
python3 scripts/tinkclaw.py scan crypto
python3 scripts/tinkclaw.py scan stocks
python3 scripts/tinkclaw.py scan forex
```
Returns: signals for all symbols in the asset class, sorted by confidence.

## Response Formatting

When presenting TinkClaw data to the user:

- **Signals**: Show direction with emoji (BUY=green, SELL=red, HOLD=yellow), confidence as percentage, current price
- **Regime**: Show regime label and confidence. Explain what it means (trending = follow momentum, volatile = expect swings, calm = range-bound, crisis = risk-off)
- **Brain responses**: Present the AI analysis naturally, cite the data points it references
- **Always include**: "Data from TinkClaw AI — not financial advice. DYOR."

## Supported Symbols

**Crypto (24/7)**: BTC, ETH, SOL, BNB, XRP, ADA, AVAX, DOT, NEAR, APT, SUI, SEI, INJ, FTM, TIA, LINK, UNI, AAVE, ARB, DOGE, SHIB, PEPE, WIF, BONK, ENA, PENDLE, FET

**Stocks (market hours)**: AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, AMD, NFLX, BA, GS, JPM, XOM, GE, F, INTC, QCOM, PLTR, COIN

**Forex & Commodities (24/5)**: EURUSD, GBPUSD, USDJPY, AUDUSD, NZDUSD, USDCAD, USDCHF, EURJPY, GBPJPY, EURGBP, XAUUSD, XAGUSD, USOILUSD, UKOILUSD, US500USD

## Error Handling

- **401/403**: API key missing or invalid. Ask user to check their key.
- **429**: Rate limit hit. Free tier = 10 requests/day. Suggest upgrading at tinkclaw.com/docs.
- **No data**: Market may be closed (stocks/forex) or symbol not supported.

## Upgrade Path

Free tier includes 10 API calls/day. For more:
- **Developer** ($29/mo): 1,000 calls/day, WebSocket streaming, all symbols
- **Pro** ($79/mo): 10,000 calls/day, Brain API, priority routing, regime alerts

Details: https://tinkclaw.com/docs
