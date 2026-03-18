#!/usr/bin/env python3
"""
TinkClaw OpenClaw Helper — Fetches market intelligence from TinkClaw API.

Usage:
    python3 tinkclaw.py signal BTC
    python3 tinkclaw.py regime ETH
    python3 tinkclaw.py ask "What's the outlook for gold?"
    python3 tinkclaw.py leaderboard
    python3 tinkclaw.py scan crypto|stocks|forex
"""

import json
import os
import sys
import urllib.request
import urllib.error

API_BASE = os.getenv("TINKCLAW_API_URL", "https://tinkclaw.com")
API_KEY = os.getenv("TINKCLAW_API_KEY", "")

CRYPTO = [
    "BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "AVAX", "DOT", "NEAR", "APT",
    "SUI", "SEI", "INJ", "FTM", "TIA", "LINK", "UNI", "AAVE", "ARB",
    "DOGE", "SHIB", "PEPE", "WIF", "BONK", "ENA", "PENDLE", "FET",
]
STOCKS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "AMD", "NFLX",
    "BA", "GS", "JPM", "XOM", "GE", "F", "INTC", "QCOM", "PLTR", "COIN",
]
FOREX = [
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "NZDUSD", "USDCAD", "USDCHF",
    "EURJPY", "GBPJPY", "EURGBP", "XAUUSD", "XAGUSD", "USOILUSD",
    "UKOILUSD", "US500USD",
]


def _request(path: str, method: str = "GET", body: dict | None = None) -> dict:
    """Make an authenticated request to TinkClaw API."""
    url = f"{API_BASE}{path}"
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"

    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        try:
            err = json.loads(error_body)
        except Exception:
            err = {"error": error_body or e.reason}
        if e.code == 401:
            print("ERROR: Invalid or missing API key. Get one at https://tinkclaw.com/docs")
        elif e.code == 429:
            print("ERROR: Rate limit reached. Free tier = 10/day. Upgrade at https://tinkclaw.com/docs")
        else:
            print(f"ERROR ({e.code}): {err.get('error', e.reason)}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"ERROR: Cannot reach TinkClaw API — {e.reason}")
        sys.exit(1)


def cmd_signal(symbol: str):
    """Fetch trading signal for a symbol."""
    symbol = symbol.upper().replace("-USD", "")
    data = _request(f"/api/signal/{symbol}")

    signal = data.get("signal", "HOLD")
    conf = data.get("confidence", 0)
    price = data.get("price", 0)
    regime = data.get("regime", {})

    emoji = {"BUY": "\u2705", "SELL": "\u274c", "HOLD": "\u26a0\ufe0f"}.get(signal, "")

    print(json.dumps({
        "symbol": symbol,
        "signal": signal,
        "signal_display": f"{emoji} {signal}",
        "confidence": f"{conf}%",
        "price": price,
        "regime": regime.get("label", "unknown"),
        "regime_confidence": regime.get("confidence", 0),
    }, indent=2))


def cmd_regime(symbol: str):
    """Fetch market regime for a symbol."""
    symbol = symbol.upper().replace("-USD", "")
    data = _request(f"/api/regime/{symbol}")

    print(json.dumps({
        "symbol": symbol,
        "regime": data.get("regime", {}).get("label", "unknown"),
        "confidence": data.get("regime", {}).get("confidence", 0),
        "forecast": data.get("forecast", {}),
        "status": data.get("status", "unknown"),
    }, indent=2))


def cmd_ask(question: str):
    """Ask the Brain API a natural language question."""
    if not API_KEY:
        print("ERROR: Brain API requires an API key. Get one at https://tinkclaw.com/docs")
        sys.exit(1)

    data = _request("/v1/chat/completions", method="POST", body={
        "model": "tinkclaw-1",
        "messages": [{"role": "user", "content": question}],
        "stream": False,
    })

    choices = data.get("choices", [])
    if choices:
        content = choices[0].get("message", {}).get("content", "No response.")
        print(content)
    else:
        print("No response from Brain API.")

    usage = data.get("usage", {})
    if usage:
        print(f"\n[Tokens: {usage.get('total_tokens', 0)} | Model: {data.get('model', 'tinkclaw-1')}]")


def cmd_leaderboard():
    """Fetch the prediction leaderboard."""
    data = _request("/api/chat/leaderboard?period=all")
    lb = data.get("leaderboard", [])

    results = []
    for e in lb[:10]:
        results.append({
            "rank": e.get("rank", 0),
            "name": e.get("username", ""),
            "record": f"{e.get('hits', 0)}W / {e.get('misses', 0)}L",
            "accuracy": f"{e.get('accuracy', 0)}%",
            "predictions": e.get("total", 0),
            "streak": e.get("streak", 0),
        })

    print(json.dumps({"leaderboard": results, "note": "All predictions SHA-256 hash-chained. Verify at tinkclaw.com"}, indent=2))


def cmd_scan(asset_class: str):
    """Scan all symbols in an asset class for signals."""
    asset_class = asset_class.lower()
    symbols = {"crypto": CRYPTO, "stocks": STOCKS, "forex": FOREX}.get(asset_class)
    if not symbols:
        print(f"ERROR: Unknown asset class '{asset_class}'. Use: crypto, stocks, forex")
        sys.exit(1)

    results = []
    for sym in symbols:
        try:
            data = _request(f"/api/signal/{sym}")
            signal = data.get("signal", "HOLD")
            conf = data.get("confidence", 0)
            if signal != "HOLD":
                results.append({
                    "symbol": sym,
                    "signal": signal,
                    "confidence": conf,
                    "price": data.get("price", 0),
                })
        except SystemExit:
            continue

    results.sort(key=lambda x: x["confidence"], reverse=True)
    print(json.dumps({"scan": asset_class, "signals": results, "count": len(results)}, indent=2))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "signal" and len(sys.argv) >= 3:
        cmd_signal(sys.argv[2])
    elif cmd == "regime" and len(sys.argv) >= 3:
        cmd_regime(sys.argv[2])
    elif cmd == "ask" and len(sys.argv) >= 3:
        cmd_ask(" ".join(sys.argv[2:]))
    elif cmd == "leaderboard":
        cmd_leaderboard()
    elif cmd == "scan" and len(sys.argv) >= 3:
        cmd_scan(sys.argv[2])
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
