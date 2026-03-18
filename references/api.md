# TinkClaw API Reference

Base URL: `https://tinkclaw.com`

## Authentication

All requests require an API key in the Authorization header:
```
Authorization: Bearer sk-tc-YOUR_KEY
```

Get a free key at https://tinkclaw.com/docs

## Endpoints

### GET /api/signal/{symbol}
Real-time trading signal for a symbol.

**Response:**
```json
{
  "symbol": "BTC",
  "signal": "BUY",
  "confidence": 78,
  "price": 97250.40,
  "regime": {"label": "trending", "confidence": 82}
}
```

### GET /api/regime/{symbol}
Market regime detection (HMM-based).

**Response:**
```json
{
  "regime": {"label": "volatile", "confidence": 74},
  "forecast": {"most_likely_next": "calm", "confidence": 61},
  "status": "live"
}
```

Regime labels: `trending`, `volatile`, `calm`, `crisis`, `unknown`

### POST /v1/chat/completions
OpenAI-compatible Brain API. Natural language market analysis.

**Request:**
```json
{
  "model": "tinkclaw-1",
  "messages": [{"role": "user", "content": "What's the outlook for ETH?"}],
  "stream": false
}
```

Models: `tinkclaw-1` (auto-route), `tinkclaw-fast`, `tinkclaw-reason`, `tinkclaw-consensus`

### GET /api/chat/leaderboard
Top predictors ranked by verified accuracy.

**Query params:** `period=all|week|month`

**Response:**
```json
{
  "leaderboard": [
    {
      "rank": 1,
      "username": "bot:tinkclaw:yen-carry",
      "total": 35,
      "hits": 35,
      "accuracy": 100.0,
      "streak": 35
    }
  ]
}
```

## Rate Limits

| Tier | Calls/day | Price |
|------|-----------|-------|
| Free | 10 | $0 |
| Developer | 1,000 | $29/mo |
| Pro | 10,000 | $79/mo |

## Compliance

- Not financial advice. Data provided for informational purposes only.
- All predictions are SHA-256 hash-chained for verifiability.
