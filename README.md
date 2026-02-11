# 🔮 Solana Narrative Radar

**Detect emerging narratives in the Solana ecosystem and get concrete build ideas for each one.**

Built for the [Superteam Earn Narrative Detection Tool Bounty](https://earn.superteam.fun/).

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 What It Does

Solana Narrative Radar monitors the Solana ecosystem across multiple signal sources and:

1. **Fetches Signals** from GitHub trending repos, KOL activity, and market research
2. **Detects Narratives** by clustering signals into thematic categories
3. **Generates Build Ideas** — 3-5 concrete project ideas per narrative
4. **Outputs Reports** as a beautiful HTML dashboard or clean Markdown

## 📊 Current Narratives Detected

Based on the latest analysis:

| Narrative | Strength | Key Signal |
|-----------|----------|------------|
| 🤖 AI Agents & Autonomous Trading | 85/100 | ai16z, Solana Agent Kit |
| 💵 Stablecoin Revolution & PayFi | 80/100 | $4.25B USDC, Western Union USDPT |
| 🏦 RWA Tokenization | 78/100 | Ondo 200+ assets, WisdomTree |
| 🏗️ Infrastructure (Firedancer) | 75/100 | 1M TPS, 150ms finality |
| 📱 Mobile Web3 (Seeker) | 70/100 | 150K preorders, SKR token |

## 🌐 Live Demo

**[View the latest narrative report →](https://byte541.github.io/solana-narrative-radar/)**

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/yourname/solana-narrative-radar.git
cd solana-narrative-radar

# No dependencies needed! Uses Python stdlib only
python main.py
```

Output files will be in `./output/`:
- `narrative_report.html` — Interactive HTML dashboard
- `narrative_report.md` — Markdown report
- `narrative_data.json` — Raw data for further analysis

## 📁 Project Structure

```
solana-narrative-radar/
├── main.py              # Entry point
├── config.py            # Configuration and keywords
├── signal_fetcher.py    # GitHub + research data collection
├── narrative_detector.py # Clustering and classification
├── idea_generator.py    # Build idea generation
├── report_generator.py  # HTML/Markdown output
├── output/              # Generated reports
└── README.md
```

## 🔍 Signal Sources

- **GitHub API**: Trending Solana repos (Rust, TypeScript, Anchor)
- **Research Data**: Pre-analyzed signals from Helius, Messari, Electric Capital
- **KOL Tracking**: Mert (Helius), Toly (Solana Labs), Akshay (Superteam)
- **Market Data**: Stablecoin flows, RWA adoption, DeFi activity

## 💡 Sample Build Ideas Generated

### For AI Agents Narrative:
- **AI Portfolio Rebalancer** — Auto-rebalance DeFi positions using Solana Agent Kit
- **Social Signal Trading Bot** — Trade pump.fun tokens on KOL mentions
- **Multi-Agent Trading Swarm** — Orchestrate specialized trading agents

### For Stablecoin/PayFi Narrative:
- **AI Micropayment SDK** — Payment rails for agent-to-agent commerce
- **Stablecoin Yield Aggregator** — Auto-route to best USDC yields
- **Merchant Stablecoin Onramp** — Shopify plugin for USDC payments

## 🛠️ Extending the Tool

### Add New Signal Sources

Edit `signal_fetcher.py` to add new data sources:

```python
class MyNewFetcher:
    def fetch_signals(self) -> List[Signal]:
        # Your data fetching logic
        return signals
```

### Add New Narrative Categories

Edit `config.py` to add keywords:

```python
NARRATIVE_KEYWORDS = {
    "my_new_narrative": [
        "keyword1", "keyword2", ...
    ]
}
```

### Customize Build Ideas

Edit `idea_generator.py` to add ideas for your narrative:

```python
IDEA_TEMPLATES = {
    "my_new_narrative": [
        BuildIdea(
            name="My Idea",
            description="...",
            ...
        )
    ]
}
```

## 📈 Future Improvements

- [ ] **Real-time Twitter/X monitoring** (requires API keys)
- [ ] **Helius webhook integration** for on-chain signals
- [ ] **Scheduled runs** with cron for daily updates
- [ ] **Web interface** for interactive exploration
- [ ] **LLM-powered summaries** using Claude/GPT

## 🏆 Bounty Submission

This project is submitted for the **Narrative Detection Tool** bounty on Superteam Earn:

- **Listing ID**: fd499139-21a9-443d-a0fc-cb418f646f0d
- **Prize Pool**: $3,500
- **Deadline**: February 15, 2026

### Requirements Met:
- ✅ Monitors Solana ecosystem signals (GitHub, research, KOLs)
- ✅ Detects emerging narratives
- ✅ Outputs 3-5 build ideas per narrative
- ✅ Clean README.md with instructions
- ⏳ Hosted link (GitHub Pages deployment pending)
- ⏳ Repository (to be pushed)

## 📜 License

MIT License — feel free to fork and build on this!

---

*Built with 💜 for the Solana ecosystem*
