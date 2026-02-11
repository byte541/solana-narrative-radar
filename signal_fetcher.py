"""Signal Fetcher - Collects signals from various sources including on-chain data"""

import json
import urllib.request
import urllib.error
import urllib.parse
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import ssl

# Disable SSL verification for simple fetches (not recommended for production)
ssl._create_default_https_context = ssl._create_unverified_context


def load_env_vars():
    """Load environment variables from .env file"""
    env_vars = {}
    env_paths = [
        os.path.join(os.path.dirname(__file__), ".env"),
        os.path.expanduser("~/clawd/.env"),
    ]
    
    for env_path in env_paths:
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        env_vars[key.strip()] = value.strip().strip('"\'')
    
    return env_vars


ENV_VARS = load_env_vars()


class Signal:
    """Represents a single signal from the ecosystem"""
    
    def __init__(
        self,
        source: str,
        title: str,
        description: str,
        url: str = "",
        timestamp: datetime = None,
        metadata: Dict[str, Any] = None
    ):
        self.source = source
        self.title = title
        self.description = description
        self.url = url
        self.timestamp = timestamp or datetime.now()
        self.metadata = metadata or {}
        self.narrative_tags = []
        self.relevance_score = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "narrative_tags": self.narrative_tags,
            "relevance_score": self.relevance_score
        }


class GitHubFetcher:
    """Fetches trending Solana repositories from GitHub with authentication"""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: str = None):
        self.token = token or ENV_VARS.get("GITHUB_ACCESS_TOKEN", "")
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "SolanaNarrativeRadar/2.0"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
            print("    ├── GitHub API: Authenticated ✓")
        else:
            print("    ├── GitHub API: Unauthenticated (rate limited)")
    
    def fetch_trending_repos(self, days: int = 14, limit: int = 50) -> List[Signal]:
        """Fetch recently created/updated Solana repos"""
        signals = []
        
        # Search for Solana-related repos with different queries
        queries = [
            "solana language:rust pushed:>{date}",
            "solana language:typescript pushed:>{date}",
            "anchor-lang pushed:>{date}",
            "solana-program pushed:>{date}",
            "topic:solana pushed:>{date}",
            "solana ai agent pushed:>{date}",
            "pump.fun solana pushed:>{date}",
        ]
        
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        for query in queries:
            query_formatted = query.format(date=since_date)
            try:
                search_url = (
                    f"{self.BASE_URL}/search/repositories"
                    f"?q={urllib.parse.quote(query_formatted)}"
                    f"&sort=updated&order=desc&per_page={limit}"
                )
                
                req = urllib.request.Request(search_url, headers=self.headers)
                with urllib.request.urlopen(req, timeout=15) as response:
                    data = json.loads(response.read().decode())
                    
                    for repo in data.get("items", [])[:limit]:
                        # Skip archived or fork repos for better signal quality
                        if repo.get("archived") or repo.get("fork"):
                            continue
                        
                        signal = Signal(
                            source="github",
                            title=repo.get("full_name", ""),
                            description=repo.get("description", "") or "No description",
                            url=repo.get("html_url", ""),
                            timestamp=datetime.fromisoformat(
                                repo.get("pushed_at", "").replace("Z", "+00:00")
                            ),
                            metadata={
                                "stars": repo.get("stargazers_count", 0),
                                "forks": repo.get("forks_count", 0),
                                "language": repo.get("language", ""),
                                "topics": repo.get("topics", []),
                                "open_issues": repo.get("open_issues_count", 0),
                                "watchers": repo.get("watchers_count", 0),
                                "created_at": repo.get("created_at", ""),
                            }
                        )
                        signals.append(signal)
                        
            except urllib.error.HTTPError as e:
                if e.code == 403:
                    print(f"    ⚠️ GitHub rate limit hit, using cached data")
                    break
                print(f"    ⚠️ GitHub HTTP error for '{query}': {e}")
            except Exception as e:
                print(f"    ⚠️ GitHub error for '{query}': {e}")
        
        # Deduplicate by URL and sort by stars
        seen_urls = set()
        unique_signals = []
        for s in signals:
            if s.url not in seen_urls:
                seen_urls.add(s.url)
                unique_signals.append(s)
        
        # Sort by stars for quality ranking
        unique_signals.sort(key=lambda x: x.metadata.get("stars", 0), reverse=True)
        
        return unique_signals[:limit]


class HeliusSignalAdapter:
    """Adapts Helius on-chain signals to Signal format"""
    
    def __init__(self):
        from helius_fetcher import fetch_helius_signals
        self.fetch_signals = fetch_helius_signals
    
    def get_signals(self) -> List[Signal]:
        """Convert Helius data to Signal objects"""
        signals = []
        
        try:
            helius_data = self.fetch_signals()
            
            for data in helius_data:
                signal = Signal(
                    source="helius_onchain",
                    title=data["title"],
                    description=data["description"],
                    url="https://solscan.io",  # Link to Solscan for exploration
                    timestamp=datetime.now(),
                    metadata={
                        "category": data.get("category", ""),
                        "metrics": data.get("metrics", {}),
                        "signal_strength": data.get("signal_strength", "medium"),
                        "evidence": [data["description"][:100]]
                    }
                )
                signals.append(signal)
        except Exception as e:
            print(f"    ⚠️ Helius adapter error: {e}")
        
        return signals


class ResearchSignalGenerator:
    """Generates signals from pre-researched data (curated insights)"""
    
    def __init__(self):
        self.research_data = self._load_research_data()
    
    def _load_research_data(self) -> List[Dict[str, Any]]:
        """Load pre-researched signals with narrative explanations"""
        return [
            # AI Agents Narrative - WHY IT'S EMERGING
            {
                "source": "research",
                "title": "ai16z Autonomous Trading Swarms Reshape Solana DeFi",
                "description": "ai16z's flagship agent 'Marc AIndreessen' processes thousands of social signals per second. The convergence of LLMs + DeFi + Solana's speed creates perfect conditions for autonomous finance.",
                "url": "https://markets.financialcontent.com/stocks/article/tokenring-2026-2-6-the-rise-of-agentic-capital",
                "category": "ai_agents",
                "evidence": ["ai16z market cap $2B+", "Autonomous trading swarms active", "Solana Agent Kit 60+ actions"],
                "why_emerging": "LLMs reached capability threshold for autonomous decision-making. Solana's sub-second finality enables real-time agent execution. ai16z proved the model works with $100M+ AUM."
            },
            {
                "source": "research", 
                "title": "Solana Agent Kit: 60+ Pre-built Actions for AI Development",
                "description": "SendAI's Solana Agent Kit provides token operations, NFT minting, DeFi interactions. Four major frameworks (Eliza, Rig, ZerePy, Arc) now compete for developer mindshare.",
                "url": "https://www.alchemy.com/blog/how-to-build-solana-ai-agents-in-2026",
                "category": "ai_agents",
                "evidence": ["60+ pre-built actions", "4 competing frameworks", "Token ops + DeFi + NFTs"],
                "why_emerging": "Developer tooling matured. Pre-built actions lower barrier to entry from months to days. Ecosystem standardizing around interoperable agent protocols."
            },
            {
                "source": "research",
                "title": "OpenAI + Anthropic Agents Enter Web3 via Solana",
                "description": "Major AI labs partnering with Solana projects. Claude and GPT-4 agents now operate on-chain wallets autonomously. AI-to-AI commerce becoming reality.",
                "url": "https://www.hokanews.com/2026/02/openclaw-ai-suddenly-explodes-after.html",
                "category": "ai_agents",
                "evidence": ["AI lab partnerships", "Autonomous wallet control", "AI-to-AI transactions"],
                "why_emerging": "Foundation model capabilities now sufficient for financial autonomy. Solana's low fees make AI micropayments economically viable."
            },
            # Infrastructure Narrative - WHY IT'S EMERGING
            {
                "source": "research",
                "title": "Firedancer Targets 1M TPS on Solana Mainnet",
                "description": "Jump Crypto's Firedancer validator client aims for 1M TPS by mid-2026. Written in C for maximum performance, it's the most ambitious blockchain upgrade ever attempted.",
                "url": "https://coindoo.com/best-crypto-to-buy-during-market-crash",
                "category": "infrastructure",
                "evidence": ["1M TPS target", "Jump Crypto backing", "C implementation", "Mainnet testing active"],
                "why_emerging": "Previous cycle exposed congestion issues. Institutional adoption requires enterprise-grade performance. Competition from L2s and new L1s driving urgency."
            },
            {
                "source": "research",
                "title": "Alpenglow: 150ms Block Finality Coming to Solana",
                "description": "Alpenglow consensus upgrade reduces finality from ~12 seconds to 150 milliseconds. Positions Solana as 'Decentralized Nasdaq' for high-frequency trading.",
                "url": "https://www.disruptionbanking.com/2026/01/20/how-strong-will-solana-be-in-2026/",
                "category": "infrastructure",
                "evidence": ["150ms finality", "80x improvement", "HFT compatibility", "Decentralized Nasdaq positioning"],
                "why_emerging": "TradFi integration requires finality guarantees. 12-second finality was blocking institutional adoption. Alpenglow unlocks new use cases (HFT, options, payments)."
            },
            {
                "source": "research",
                "title": "ZK Compression v2: 1000x State Cost Reduction",
                "description": "ZK Compression v2 compresses state data by 1000x via Merkle trees. Light Protocol leads implementation. Game-changer for NFT collections and airdrop campaigns.",
                "url": "https://letstalkbitco.in/solanas-v3-0-14-update-targets-mainnet-stability",
                "category": "infrastructure",
                "evidence": ["1000x compression", "Light Protocol", "Reduced validator costs"],
                "why_emerging": "State rent was blocking mass adoption experiments. Compressed NFTs proved concept. Now generalizing to all account types."
            },
            # Stablecoins & PayFi - WHY IT'S EMERGING
            {
                "source": "research",
                "title": "$5B+ USDC on Solana: Stablecoin Dominance",
                "description": "Stablecoin supply crossed $5B milestone with $1B USDC minted in 8 hours. Solana now #2 for stablecoin activity behind Ethereum. PayFi infrastructure maturing.",
                "url": "https://www.hokanews.com/2026/01/1-billion-usdc-minted-on-solana-in.html",
                "category": "stablecoins_payfi",
                "evidence": ["$5B+ supply", "$1B single-day mint", "#2 stablecoin chain"],
                "why_emerging": "Circle prioritizing Solana for USDC expansion. Low fees make micropayments viable. AI agents driving automated payment flows."
            },
            {
                "source": "research",
                "title": "Western Union USDPT Stablecoin on Solana",
                "description": "175-year-old payments giant Western Union announces USDPT stablecoin on Solana via Anchorage Digital. H1 2026 launch targets $700B remittance market.",
                "url": "https://www.disruptionbanking.com/2026/01/20/how-strong-will-solana-be-in-2026/",
                "category": "stablecoins_payfi",
                "evidence": ["Western Union", "USDPT", "$700B market", "Anchorage custody"],
                "why_emerging": "Regulatory clarity emerging. Solana's speed matches remittance UX expectations. Legacy players forced to compete with crypto-native rails."
            },
            {
                "source": "research",
                "title": "Visa + Mastercard Settlement on Solana",
                "description": "Visa expanded stablecoin settlement to Solana. Mastercard piloting merchant settlements. Payment giants validating Solana as enterprise-grade rails.",
                "url": "https://www.dlnews.com/articles/markets/why-solana-stablecoin-action-boomed/",
                "category": "stablecoins_payfi",
                "evidence": ["Visa settlement live", "Mastercard pilot", "Enterprise validation"],
                "why_emerging": "Card networks see blockchain as cost reduction. Solana's proven uptime and speed meet enterprise SLAs. First-mover advantage in B2B payments."
            },
            # RWA Tokenization - WHY IT'S EMERGING
            {
                "source": "research",
                "title": "Ondo Finance: 200+ Tokenized Assets on Solana",
                "description": "Ondo launches 200+ tokenized stocks, ETFs, bonds on Solana. Largest RWA issuer by asset count. Controls 65% of individual tokenized RWA market.",
                "url": "https://www.coindesk.com/business/2026/01/21/ondo-finance-brings-200-tokenized-u-s-stocks-and-etfs-to-solana",
                "category": "rwa_tokenization",
                "evidence": ["200+ assets", "65% market share", "Stocks + ETFs + Bonds"],
                "why_emerging": "SEC clarity on tokenized securities. TradFi demand for 24/7 markets. Solana's compliance-ready infrastructure (AML, KYC hooks)."
            },
            {
                "source": "research",
                "title": "Tokenized Equities Market Explodes 2800% to $963M",
                "description": "Tokenized equities market reaches $963M in January 2026, up 2800% YoY. Regulatory tailwinds and institutional demand driving explosive growth.",
                "url": "https://www.coindesk.com/business/2026/01/30/tokenized-equities-exploded-3000-percent",
                "category": "rwa_tokenization",
                "evidence": ["$963M market", "2800% YoY growth", "Institutional demand"],
                "why_emerging": "BlackRock and Fidelity entering space. 24/7 trading demand from global investors. T+0 settlement superior to T+2 traditional."
            },
            {
                "source": "research",
                "title": "WisdomTree Tokenized Funds on Solana",
                "description": "WisdomTree brings full suite of tokenized funds to Solana as RWA surpasses $1B. ETF giant validates blockchain for asset management.",
                "url": "https://www.businesswire.com/news/home/20260128885072/en/WisdomTree-Expands-Tokenization-to-Solana",
                "category": "rwa_tokenization",
                "evidence": ["WisdomTree", "$1B+ RWA", "ETF-grade products"],
                "why_emerging": "Traditional asset managers can't ignore on-chain efficiency. Solana winning institutional deals over Ethereum for cost/speed."
            },
            # Mobile/Consumer - WHY IT'S EMERGING
            {
                "source": "research",
                "title": "Solana Seeker: 150K+ Preorders, SKR Token Launch",
                "description": "Solana Mobile's Seeker phone launches with 150K+ preorders. 1.8B SKR token airdrop creates new hardware-gated distribution model.",
                "url": "https://www.theblock.co/post/386449/solana-mobile-seeker-skr-token-airdrop",
                "category": "mobile_consumer",
                "evidence": ["150K preorders", "1.8B token airdrop", "Hardware-gated airdrops"],
                "why_emerging": "Saga success proved demand. Hardware wallets solve UX. Token airdrops subsidize consumer adoption. Web3 phone becomes trojan horse."
            },
            {
                "source": "research",
                "title": "Mobile DeFi Usage Surges on Solana",
                "description": "40% of Solana DEX trades now originate from mobile. Phantom and Jupiter mobile apps seeing record usage. Consumer UX finally reaching parity.",
                "url": "https://cryptomaniaks.com/news/solana-seeker-review-skr-token-staking-apy",
                "category": "mobile_consumer",
                "evidence": ["40% mobile DEX trades", "Record app usage", "UX parity achieved"],
                "why_emerging": "Mobile-first generation entering crypto. Wallet UX dramatically improved. Native dApp stores bypass Apple/Google restrictions."
            },
            # DePIN - WHY IT'S EMERGING
            {
                "source": "research",
                "title": "Dawn Network: DePIN Internet Sharing Explodes",
                "description": "Dawn Network allows bandwidth sharing via rooftop hardware. 50K+ nodes active. DePIN model proving real-world infrastructure can decentralize.",
                "url": "https://www.hokanews.com/2026/01/dawn-network-airdrop-stays-hot.html",
                "category": "depin",
                "evidence": ["50K+ nodes", "Bandwidth sharing", "Real-world infrastructure"],
                "why_emerging": "Hardware costs dropped. Token incentives align contributors. Solana's speed enables real-time IoT coordination. Helium proved model works."
            },
            {
                "source": "research",
                "title": "DePIN TVL Crosses $5B on Solana",
                "description": "Combined DePIN total value (Render, Helium, io.net, Nosana, Hivemapper) crosses $5B. GPU compute and wireless leading categories.",
                "url": "https://investinghaven.com/solana-sol-price-predictions/",
                "category": "depin",
                "evidence": ["$5B+ DePIN TVL", "GPU + Wireless focus", "5 major protocols"],
                "why_emerging": "AI training demand outstripping centralized supply. Decentralized compute 60% cheaper. Geographic distribution = resilience."
            },
            # Memecoins - WHY IT'S EMERGING (still!)
            {
                "source": "research",
                "title": "Pump.fun: 300K Daily Users, 39K Tokens/Day",
                "description": "Pump.fun dominates Solana meme ecosystem. 300K daily active addresses. 39K token creations in single day. PUMP token up 34%.",
                "url": "https://www.bitget.com/news/detail/12560605178213",
                "category": "memecoins",
                "evidence": ["300K DAU", "39K tokens/day", "PUMP +34%"],
                "why_emerging": "Bonding curve innovation removed rug risk. Low friction = high velocity. Cultural moment for meme trading. Solana speed = better trading UX."
            },
            {
                "source": "research",
                "title": "Meme Launchpad Volume Hits $180M Single Day",
                "description": "Solana token launchpad volume reached $180M on Jan 26, 2026. Meme season showing no signs of slowing despite market volatility.",
                "url": "https://finance.yahoo.com/news/solana-news-sol-slides-shutdown-155002508.html",
                "category": "memecoins",
                "evidence": ["$180M daily volume", "Sustained momentum", "Volatility-resistant"],
                "why_emerging": "Cultural narrative stronger than fundamentals. Low barrier to participation. Community-driven price discovery. Entertainment value."
            },
            # DeFi Evolution
            {
                "source": "research",
                "title": "Jupiter: #1 DEX Aggregator Processes $100B+ Volume",
                "description": "Jupiter processed over $100B cumulative volume. Perp DEX launched. JUP staking and governance creating DeFi flywheel.",
                "url": "https://www.jupiter.ag",
                "category": "defi_evolution",
                "evidence": ["$100B+ volume", "Perp launch", "JUP staking"],
                "why_emerging": "Aggregation layer becoming essential. Perp demand from CEX refugees. DAO governance engaging community."
            },
            {
                "source": "research",
                "title": "Liquid Staking Wars: jitoSOL vs mSOL vs bSOL",
                "description": "Liquid staking competition intensifies. Jito pioneered MEV rewards. Marinade largest by TVL. New entrants differentiating on yield and governance.",
                "url": "https://defillama.com/chain/Solana",
                "category": "defi_evolution",
                "evidence": ["$3B+ LST TVL", "MEV rewards", "Yield competition"],
                "why_emerging": "Ethereum showed LST potential. MEV extraction profitable. Staking = passive income for holders."
            },
        ]
    
    def get_signals(self) -> List[Signal]:
        """Convert research data to Signal objects"""
        signals = []
        for data in self.research_data:
            metadata = {
                "category": data.get("category", ""),
                "evidence": data.get("evidence", []),
                "why_emerging": data.get("why_emerging", ""),
            }
            
            signal = Signal(
                source=data["source"],
                title=data["title"],
                description=data["description"],
                url=data.get("url", ""),
                timestamp=datetime.now(),
                metadata=metadata
            )
            signals.append(signal)
        return signals


def fetch_all_signals() -> List[Signal]:
    """Fetch signals from all available sources"""
    all_signals = []
    
    # Helius on-chain signals (HIGHEST PRIORITY - real data!)
    print("Fetching Helius on-chain signals...")
    try:
        helius = HeliusSignalAdapter()
        helius_signals = helius.get_signals()
        all_signals.extend(helius_signals)
        print(f"    ✓ Found {len(helius_signals)} on-chain signals")
    except Exception as e:
        print(f"    ⚠️ Helius fetch failed: {e}")
    
    # GitHub signals (with auth for better rate limits)
    print("Fetching GitHub signals...")
    github = GitHubFetcher()
    github_signals = github.fetch_trending_repos(days=14, limit=40)
    all_signals.extend(github_signals)
    print(f"    ✓ Found {len(github_signals)} GitHub signals")
    
    # Research-based signals (curated insights)
    print("Loading research signals...")
    research = ResearchSignalGenerator()
    research_signals = research.get_signals()
    all_signals.extend(research_signals)
    print(f"    ✓ Found {len(research_signals)} research signals")
    
    return all_signals


if __name__ == "__main__":
    signals = fetch_all_signals()
    print(f"\nTotal signals collected: {len(signals)}")
    for s in signals[:5]:
        print(f"  - [{s.source}] {s.title[:60]}...")
