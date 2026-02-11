"""Signal Fetcher - Collects signals from various sources"""

import json
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timedelta
from typing import List, Dict, Any
import ssl

# Disable SSL verification for simple fetches (not recommended for production)
ssl._create_default_https_context = ssl._create_unverified_context


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
    """Fetches trending Solana repositories from GitHub"""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: str = None):
        self.token = token
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "SolanaNarrativeRadar/1.0"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    def fetch_trending_repos(self, days: int = 7, limit: int = 30) -> List[Signal]:
        """Fetch recently created/updated Solana repos"""
        signals = []
        
        # Search for Solana-related repos
        queries = [
            "solana language:rust",
            "solana language:typescript",
            "anchor-lang",
            "solana-program",
            "topic:solana"
        ]
        
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        for query in queries[:2]:  # Limit queries to avoid rate limits
            try:
                search_url = (
                    f"{self.BASE_URL}/search/repositories"
                    f"?q={urllib.parse.quote(query)}+pushed:>{since_date}"
                    f"&sort=stars&order=desc&per_page={limit}"
                )
                
                req = urllib.request.Request(search_url, headers=self.headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    data = json.loads(response.read().decode())
                    
                    for repo in data.get("items", [])[:limit]:
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
                                "open_issues": repo.get("open_issues_count", 0)
                            }
                        )
                        signals.append(signal)
                        
            except Exception as e:
                print(f"Error fetching GitHub data for '{query}': {e}")
        
        # Deduplicate by URL
        seen_urls = set()
        unique_signals = []
        for s in signals:
            if s.url not in seen_urls:
                seen_urls.add(s.url)
                unique_signals.append(s)
        
        return unique_signals[:limit]


class ResearchSignalGenerator:
    """Generates signals from pre-researched data (for when APIs are limited)"""
    
    def __init__(self):
        self.research_data = self._load_research_data()
    
    def _load_research_data(self) -> List[Dict[str, Any]]:
        """Load pre-researched signals based on web search results"""
        # This is populated from our Phase 1 research
        return [
            # AI Agents Narrative
            {
                "source": "research",
                "title": "ai16z Autonomous Trading Swarms Reshape Solana DeFi",
                "description": "ai16z's flagship agent 'Marc AIndreessen' processes thousands of social signals per second, turning Solana into a laboratory for autonomous finance. Trading swarms now blur the line between software and hedge fund managers.",
                "url": "https://markets.financialcontent.com/stocks/article/tokenring-2026-2-6-the-rise-of-agentic-capital",
                "category": "ai_agents",
                "evidence": ["ai16z trending", "autonomous trading", "Solana Agent Kit 60+ actions"]
            },
            {
                "source": "research", 
                "title": "Solana Agent Kit: 60+ Pre-built Actions for AI Development",
                "description": "SendAI's Solana Agent Kit provides token operations, NFT minting, DeFi interactions. Four major frameworks now dominate Solana AI agent development in 2026.",
                "url": "https://www.alchemy.com/blog/how-to-build-solana-ai-agents-in-2026",
                "category": "ai_agents",
                "evidence": ["60+ pre-built actions", "token operations", "DeFi interactions"]
            },
            {
                "source": "research",
                "title": "OpenClaw AI Gains Momentum Across Solana and Base",
                "description": "OpenClaw AI agents gain momentum across Solana and Base. New USDC hackathon highlights growing role of AI in Web3 automation.",
                "url": "https://www.hokanews.com/2026/02/openclaw-ai-suddenly-explodes-after.html",
                "category": "ai_agents",
                "evidence": ["Security fix drives adoption", "USDC hackathon", "Web3 automation"]
            },
            # Infrastructure Narrative
            {
                "source": "research",
                "title": "Firedancer Targets 1M TPS on Solana Mainnet",
                "description": "Jump Crypto's Firedancer validator client aims for 1 million TPS by mid-2026, fixing congestion from past cycles. Currently testing on mainnet.",
                "url": "https://coindoo.com/best-crypto-to-buy-during-market-crash-blockdag-sol-ondo-finance-render-stand-out/",
                "category": "infrastructure",
                "evidence": ["1M TPS target", "Jump Crypto", "mainnet testing"]
            },
            {
                "source": "research",
                "title": "Alpenglow Brings 150ms Block Finality to Solana",
                "description": "Alpenglow consensus upgrade expected early 2026 reduces finality from ~12 seconds to 150 milliseconds. Positions Solana as 'Decentralized Nasdaq'.",
                "url": "https://www.disruptionbanking.com/2026/01/20/how-strong-will-solana-be-in-2026/",
                "category": "infrastructure",
                "evidence": ["150ms finality", "early 2026 launch", "Decentralized Nasdaq narrative"]
            },
            {
                "source": "research",
                "title": "ZK Compression v2: 1000x State Data Reduction",
                "description": "ZK Compression v2 compresses state data by up to 1,000x, slashing storage costs for validators and making project launches cheaper.",
                "url": "https://letstalkbitco.in/solanas-v3-0-14-update-targets-mainnet-stability-amid-scalability-race-to-1m-tps/",
                "category": "infrastructure",
                "evidence": ["1000x compression", "reduced validator costs", "cheaper launches"]
            },
            # Stablecoins & PayFi Narrative
            {
                "source": "research",
                "title": "$1 Billion USDC Minted on Solana in 8 Hours",
                "description": "Stablecoin activity surges with $1B USDC minted in 8 hours, pushing total to $4.25B in 2026. Signals shift toward payments and DeFi liquidity.",
                "url": "https://www.hokanews.com/2026/01/1-billion-usdc-minted-on-solana-in.html",
                "category": "stablecoins_payfi",
                "evidence": ["$4.25B USDC", "rapid minting", "payments adoption"]
            },
            {
                "source": "research",
                "title": "Western Union to Launch USDPT Stablecoin on Solana",
                "description": "175-year-old payments giant Western Union announces USDPT stablecoin on Solana via Anchorage Digital for H1 2026 launch.",
                "url": "https://www.disruptionbanking.com/2026/01/20/how-strong-will-solana-be-in-2026/",
                "category": "stablecoins_payfi",
                "evidence": ["Western Union", "USDPT", "institutional adoption"]
            },
            {
                "source": "research",
                "title": "Visa Expands Stablecoin Settlement to Solana",
                "description": "Visa debuted stablecoin settlement for partners on Solana in December. AI-driven micropayments demonstrate Solana's cost advantages.",
                "url": "https://www.dlnews.com/articles/markets/why-solana-stablecoin-action-boomed-over-2025/",
                "category": "stablecoins_payfi",
                "evidence": ["Visa settlement", "micropayments", "institutional rails"]
            },
            # RWA Tokenization Narrative
            {
                "source": "research",
                "title": "Ondo Finance Brings 200+ Tokenized Assets to Solana",
                "description": "Ondo launches 200+ tokenized stocks, ETFs, bonds on Solana, becoming largest RWA issuer by asset count. Controls 65% of individual tokenized RWA.",
                "url": "https://www.coindesk.com/business/2026/01/21/ondo-finance-brings-200-tokenized-u-s-stocks-and-etfs-to-solana",
                "category": "rwa_tokenization",
                "evidence": ["200+ assets", "largest RWA issuer", "65% market share"]
            },
            {
                "source": "research",
                "title": "WisdomTree Expands Tokenized Funds to Solana",
                "description": "WisdomTree brings full suite of tokenized funds to Solana as RWA on Solana surpasses $1B. Regulated financial products now on-chain.",
                "url": "https://www.businesswire.com/news/home/20260128885072/en/WisdomTree-Expands-Tokenization-Ecosystem-to-Solana",
                "category": "rwa_tokenization",
                "evidence": ["WisdomTree", "$1B+ RWA", "regulated products"]
            },
            {
                "source": "research",
                "title": "Tokenized Equities Explode 2800% YoY to $963M",
                "description": "Tokenized equities market reaches $963M in January 2026, up 2900% YoY. Ondo and xStocks dominate issuance.",
                "url": "https://www.coindesk.com/business/2026/01/30/the-market-for-tokenized-equities-has-exploded-by-almost-3-000-in-a-single-year",
                "category": "rwa_tokenization",
                "evidence": ["$963M market", "2800% growth", "regulatory developments"]
            },
            # Mobile/Consumer Narrative
            {
                "source": "research",
                "title": "Solana Seeker Launches with 1.8B SKR Token Airdrop",
                "description": "Solana Mobile's Seeker phone launches with 150K+ preorders. SKR token airdrop for users and developers marks new hardware-gated distribution model.",
                "url": "https://www.theblock.co/post/386449/solana-mobile-seeker-skr-token-airdrop",
                "category": "mobile_consumer",
                "evidence": ["150K preorders", "1.8B token airdrop", "hardware-gated airdrops"]
            },
            {
                "source": "research",
                "title": "Seeker Phone Enables 24% APY Staking",
                "description": "Solana Seeker integrates wallet and dApps directly, allowing native staking with reported 24% APY. Consumer-grade Web3 experience.",
                "url": "https://cryptomaniaks.com/news/solana-seeker-review-skr-token-staking-apy",
                "category": "mobile_consumer",
                "evidence": ["24% APY staking", "native dApp integration", "consumer focus"]
            },
            # DePIN Narrative
            {
                "source": "research",
                "title": "Dawn Network: DePIN Internet Sharing on Solana",
                "description": "Dawn Network allows users to share unused internet bandwidth through rooftop radio hardware. Built on Solana, developed by Andrena.",
                "url": "https://www.hokanews.com/2026/01/dawn-network-airdrop-stays-hot.html",
                "category": "depin",
                "evidence": ["bandwidth sharing", "rooftop hardware", "real-world infrastructure"]
            },
            {
                "source": "research",
                "title": "DePIN Activity Grows Alongside Tokenization",
                "description": "Growing DePIN activity on Solana with Render, Helium, Hivemapper. High TPS enables real-time IoT and infrastructure coordination.",
                "url": "https://investinghaven.com/solana-sol-price-predictions/",
                "category": "depin",
                "evidence": ["Render", "Helium", "infrastructure growth"]
            },
            # Memecoins Narrative
            {
                "source": "research",
                "title": "Pump.fun Hits 300K Daily Active Addresses",
                "description": "Pump.fun dominates Solana meme ecosystem with 300K daily active addresses and 39K token creations in single day. PUMP token up 34%.",
                "url": "https://www.bitget.com/news/detail/12560605178213",
                "category": "memecoins",
                "evidence": ["300K DAU", "39K tokens/day", "PUMP +34%"]
            },
            {
                "source": "research",
                "title": "Meme Coin Launchpad Volume Hits $180M 2026 High",
                "description": "Solana token launchpad volume reached nearly $180M on Jan 26, reflecting strong on-chain trading momentum.",
                "url": "https://finance.yahoo.com/news/solana-news-sol-slides-shutdown-155002508.html",
                "category": "memecoins",
                "evidence": ["$180M volume", "launchpad activity", "trading momentum"]
            },
            # Developer Ecosystem
            {
                "source": "research",
                "title": "Solana Developer Base Reaches 17,708 Active Contributors",
                "description": "Electric Capital data shows 17,708 total active developers on Solana by November 2025. Builder interest up 78% over two years.",
                "url": "https://www.disruptionbanking.com/2026/01/20/how-strong-will-solana-be-in-2026/",
                "category": "infrastructure",
                "evidence": ["17,708 developers", "78% growth", "strong ecosystem"]
            },
        ]
    
    def get_signals(self) -> List[Signal]:
        """Convert research data to Signal objects"""
        signals = []
        for data in self.research_data:
            signal = Signal(
                source=data["source"],
                title=data["title"],
                description=data["description"],
                url=data.get("url", ""),
                timestamp=datetime.now(),
                metadata={
                    "category": data.get("category", ""),
                    "evidence": data.get("evidence", [])
                }
            )
            signals.append(signal)
        return signals


def fetch_all_signals() -> List[Signal]:
    """Fetch signals from all available sources"""
    all_signals = []
    
    # GitHub signals
    print("Fetching GitHub signals...")
    github = GitHubFetcher()
    github_signals = github.fetch_trending_repos(days=14, limit=20)
    all_signals.extend(github_signals)
    print(f"  Found {len(github_signals)} GitHub signals")
    
    # Research-based signals
    print("Loading research signals...")
    research = ResearchSignalGenerator()
    research_signals = research.get_signals()
    all_signals.extend(research_signals)
    print(f"  Found {len(research_signals)} research signals")
    
    return all_signals


if __name__ == "__main__":
    signals = fetch_all_signals()
    print(f"\nTotal signals collected: {len(signals)}")
    for s in signals[:5]:
        print(f"  - [{s.source}] {s.title[:60]}...")
