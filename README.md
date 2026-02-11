# 🔮 Solana Narrative Radar

**Detect emerging narratives in the Solana ecosystem — backed by real on-chain data — and get concrete build ideas for each one.**

Built for the [Superteam Earn Narrative Detection Tool Bounty](https://earn.superteam.fun/).

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Signals](https://img.shields.io/badge/signals-68+-orange.svg)
![On--chain](https://img.shields.io/badge/on--chain-Helius%20API-9945FF.svg)

## 🌐 Live Demo

**[View the latest narrative report →](https://byte541.github.io/solana-narrative-radar/)**

---

## 🎯 What It Does

Solana Narrative Radar monitors the Solana ecosystem across **three signal layers** and surfaces what's starting to matter before it's obvious:

1. **Fetches Signals** — GitHub trending repos, live on-chain data via Helius API, and curated research signals
2. **Scores Narratives** — Multi-factor algorithm: signal volume, source diversity, on-chain validation, recency, and category-specific boosts
3. **Explains WHY** — Each narrative includes a structured explanation of why it's emerging, with on-chain evidence
4. **Generates Build Ideas** — 3-5 concrete project ideas per narrative, each with tech stack, timeline, and revenue model
5. **Outputs Reports** — Interactive HTML dashboard, Markdown report, and raw JSON

---

## 📊 Current Narratives Detected

| Narrative | Strength | Confidence | Key Signal |
|-----------|----------|------------|------------|
| 💱 DeFi Protocol Evolution | 89/100 | High | Jito, Jupiter, intents-based trading |
| 🏗️ Infrastructure (Firedancer/Alpenglow) | 85/100 | High | 1M TPS, 150ms finality |
| 🤖 AI Agents & Autonomous Trading | 78/100 | High | ai16z, Solana Agent Kit (60+ actions) |
| 💵 Stablecoin Revolution & PayFi | 74/100 | Medium | $4.25B USDC, Western Union USDPT |
| 🏦 RWA Tokenization | 70/100 | Medium | Ondo 200+ assets, WisdomTree |
| 🐸 Meme Coins & Launchpads | 66/100 | Medium | Pump.fun 300K DAU, $180M volume |
| 🌐 DePIN | 60/100 | Medium | Helium, Render, Dawn Network |

---

## 🔍 Signal Sources

### 1. On-Chain Data (Helius API)
Real-time Solana network data — this is what most tools miss:
- **Network TPS** and active validator counts
- **Program activity** — transaction counts for Jupiter, Raydium, Pump.fun, Kamino, Jito, and more
- **Stablecoin supply** — USDC, USDT, USDS mint addresses tracked live
- **NFT marketplace activity** — Magic Eden, Tensor

### 2. GitHub Activity (Authenticated)
Higher rate limits with GitHub token:
- Trending Solana repos (Rust, TypeScript, Anchor) pushed in last 14 days
- Star counts, fork activity, topic tags
- Deduplication across search queries

### 3. Research Signals
Pre-analyzed signals from authoritative sources:
- **Helius** ecosystem reports
- **Messari** research
- **Electric Capital** developer reports
- **KOL tracking**: Mert (Helius), Toly (Solana Labs), Akshay (Superteam)
- Institutional signals: Visa, Western Union, Ondo, WisdomTree

---

## 📐 How Signals Are Detected & Ranked

### Signal Collection
Each source produces `Signal` objects with source, title, description, URL, timestamp, and metadata.

### Narrative Classification
Signals are classified into narrative categories using:
1. **Keyword matching** — each category has a curated keyword list (`config.py`)
2. **Metadata tags** — research signals carry pre-labeled categories
3. **GitHub topics** — repo topics mapped to narrative categories

### Narrative Scoring (0–100)
Multi-factor algorithm across 4 dimensions:

| Factor | Max Points | Description |
|--------|-----------|-------------|
| Signal volume | 25 | More signals = stronger narrative |
| Source diversity + on-chain bonus | 25 | GitHub + research + on-chain = full score |
| Quality (GitHub stars + evidence items) | 25 | Weighted by real engagement |
| Recency | 15 | Recent signals weighted higher |
| Category boost | 10 | Hot categories (AI, infra) get extra weight |

Narratives also get:
- **Confidence %** — based on source diversity and signal count
- **Momentum** — rising / stable / declining (based on recent vs older signals)
- **WHY explanation** — key drivers extracted from evidence

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/byte541/solana-narrative-radar.git
cd solana-narrative-radar

# Optional: set your Helius API key for live on-chain data
export HELIUS_API_KEY=your_key_here  # free tier at helius.dev

# No other dependencies needed — Python stdlib only
python3 main.py
```

Output files in `./output/`:
- `narrative_report.html` — Interactive HTML dashboard
- `narrative_report.md` — Markdown report
- `narrative_data.json` — Raw data for further processing

### CLI Options

```bash
python3 main.py --format html      # HTML only
python3 main.py --format markdown  # Markdown only
python3 main.py --format json      # JSON only
python3 main.py --quiet            # No progress output
```

---

## 📁 Project Structure

```
solana-narrative-radar/
├── main.py               # Entry point + CLI
├── config.py             # Narrative keywords, KOLs, settings
├── signal_fetcher.py     # GitHub + research signal collection
├── helius_fetcher.py     # On-chain data via Helius API
├── narrative_detector.py # Multi-factor scoring + classification
├── idea_generator.py     # Build idea generation engine
├── report_generator.py   # HTML/Markdown/JSON output
├── docs/                 # GitHub Pages (live demo)
│   └── index.html
├── output/               # Generated reports (gitignored)
└── README.md
```

---

## 💡 Sample Build Ideas

### For DeFi Protocol Evolution:
- **Intent-Based Trading Interface** — "Swap when SOL drops 5%" with Jito integration · 4-6 weeks · 0.1% fee
- **Liquid Staking Comparator** — One-click migration between mSOL/jitoSOL/bSOL · 2-3 weeks · referral fees

### For AI Agents Narrative:
- **AI Portfolio Rebalancer** — Auto-rebalance DeFi positions using Solana Agent Kit · 4-6 weeks · 0.1-0.5% AUM fee
- **Social Signal Trading Bot** — Trade pump.fun tokens on KOL mentions · 2-3 weeks · performance fees
- **Multi-Agent Trading Swarm** — Orchestrate specialized sub-agents · 8-12 weeks · SaaS + performance fees

### For Stablecoin/PayFi:
- **AI Micropayment SDK** — Agent-to-agent payment rails · 3-4 weeks · per-transaction fee
- **Cross-Border Remittance Tracker** — $700B/year market · 4-6 weeks · spread fee

---

## 🛠️ Extending the Tool

### Add a new signal source

```python
# In signal_fetcher.py
class MyFetcher:
    def fetch_signals(self) -> List[Signal]:
        return [Signal(source="my_source", title="...", description="...")]

# In fetch_all_signals():
my = MyFetcher()
all_signals.extend(my.fetch_signals())
```

### Add a new narrative category

```python
# In config.py
NARRATIVE_KEYWORDS = {
    "my_narrative": ["keyword1", "keyword2", ...]
}

# In narrative_detector.py — NARRATIVE_NAMES dict
"my_narrative": "My Narrative Display Name"
```

---

## 📈 Future Improvements

- [ ] **Real-time X/Twitter monitoring** — KOL tweet feeds via API
- [ ] **Webhook mode** — Helius webhooks for instant on-chain alerts
- [ ] **Scheduled reports** — Daily cron with Telegram/Discord delivery
- [ ] **LLM-powered summaries** — Claude API for deeper narrative analysis
- [ ] **Web interface** — React frontend for interactive exploration

---

## 🏆 Bounty Submission

Submitted for the **Narrative Detection Tool** bounty on Superteam Earn:

- **Prize Pool**: $3,500 (1st: $2K · 2nd: $1K · 3rd: $500)
- **Deadline**: February 15, 2026
- **Winners announced**: March 1, 2026

### Requirements Met
- ✅ Monitors Solana ecosystem signals (GitHub, on-chain, research, KOLs)
- ✅ Detects emerging narratives with strength scores + confidence
- ✅ Explains WHY each narrative is emerging
- ✅ Outputs 3-5 build ideas per narrative (with tech stack, timeline, revenue)
- ✅ README with data sources and detection methodology
- ✅ Hosted live demo (GitHub Pages)
- ✅ Instructions to reproduce

---

## 📜 License

MIT License — feel free to fork and build on this!

---

*Built with 💜 for the Solana ecosystem*
