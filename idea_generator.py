"""Build Idea Generator - Creates concrete project ideas for each narrative"""

from typing import List, Dict, Any
from narrative_detector import Narrative


class BuildIdea:
    """Represents a concrete build idea"""
    
    def __init__(
        self,
        name: str,
        description: str,
        tech_stack: List[str],
        difficulty: str,
        potential_revenue: str,
        time_to_build: str,
        why_now: str
    ):
        self.name = name
        self.description = description
        self.tech_stack = tech_stack
        self.difficulty = difficulty  # beginner, intermediate, advanced
        self.potential_revenue = potential_revenue
        self.time_to_build = time_to_build
        self.why_now = why_now
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "tech_stack": self.tech_stack,
            "difficulty": self.difficulty,
            "potential_revenue": self.potential_revenue,
            "time_to_build": self.time_to_build,
            "why_now": self.why_now
        }


class IdeaGenerator:
    """Generates build ideas based on narrative context"""
    
    # Predefined ideas for each narrative category
    IDEA_TEMPLATES = {
        "ai_agents": [
            BuildIdea(
                name="AI Portfolio Rebalancer",
                description="An AI agent that monitors DeFi positions across Jupiter, Kamino, and Marinade, automatically rebalancing based on yield optimization and risk parameters. Uses Solana Agent Kit for transactions.",
                tech_stack=["Solana Agent Kit", "Python", "LangChain", "Jupiter API", "Helius RPC"],
                difficulty="intermediate",
                potential_revenue="0.1-0.5% management fee on AUM",
                time_to_build="3-4 weeks",
                why_now="ai16z proved autonomous trading is viable. Solana Agent Kit has 60+ pre-built actions. Market timing is perfect."
            ),
            BuildIdea(
                name="Social Signal Trading Bot",
                description="Agent that monitors KOL tweets (Mert, Toly, Akshay), analyzes sentiment, and executes trades on pump.fun tokens within seconds of mention. Risk management built-in.",
                tech_stack=["Eliza Framework", "Twitter API", "Pump.fun API", "Solana Web3.js"],
                difficulty="advanced",
                potential_revenue="Performance fees on profitable trades",
                time_to_build="4-6 weeks",
                why_now="KOL signals move markets instantly. ai16z's Marc AIndreessen processes thousands of signals/second. First-mover advantage critical."
            ),
            BuildIdea(
                name="AI-Powered NFT Valuation Agent",
                description="Agent that appraises NFTs by analyzing floor prices, traits, historical sales, and social sentiment. Provides instant quotes and can execute arbitrage on underpriced listings.",
                tech_stack=["Solana Agent Kit", "Magic Eden API", "Tensor API", "GPT-4 Vision"],
                difficulty="intermediate",
                potential_revenue="Arbitrage profits + valuation API fees",
                time_to_build="2-3 weeks",
                why_now="NFT market recovering. Automated valuation needed for DeFi collateralization. No dominant player yet."
            ),
            BuildIdea(
                name="Autonomous Grant Proposal Writer",
                description="AI that scans Superteam, Solana Foundation, and DAO treasuries for grants, then generates and submits tailored proposals based on your project. Learns from successful proposals.",
                tech_stack=["Claude API", "Notion API", "Solana Governance SDKs", "Python"],
                difficulty="beginner",
                potential_revenue="% of grants won or subscription model",
                time_to_build="2 weeks",
                why_now="$100M+ in ecosystem grants available. Manual applications are time-consuming. AI can 10x application output."
            ),
            BuildIdea(
                name="Multi-Agent Trading Swarm Orchestrator",
                description="Platform for deploying and managing multiple specialized AI agents (trend-follower, arbitrageur, market-maker) that coordinate strategies. Dashboard for performance tracking.",
                tech_stack=["Solana Agent Kit", "ElizaOS", "React", "PostgreSQL", "Jito MEV"],
                difficulty="advanced",
                potential_revenue="SaaS subscription + performance fees",
                time_to_build="6-8 weeks",
                why_now="Single agents are commoditized. Swarm intelligence is the next evolution. ai16z proves coordination is possible."
            ),
        ],
        "infrastructure": [
            BuildIdea(
                name="Firedancer Node Dashboard",
                description="Real-time monitoring dashboard for Firedancer validators showing TPS, latency, block production stats, and comparison with legacy validators. Alert system for anomalies.",
                tech_stack=["React", "Helius RPC", "WebSocket", "Grafana", "Prometheus"],
                difficulty="intermediate",
                potential_revenue="SaaS for validators ($50-200/mo)",
                time_to_build="3-4 weeks",
                why_now="Firedancer launching mid-2026. Validators need monitoring tools. First specialized dashboard wins market."
            ),
            BuildIdea(
                name="ZK Compression Migration Tool",
                description="One-click tool to migrate existing NFT collections and token accounts to compressed state. Calculates savings, handles migration, verifies integrity.",
                tech_stack=["Light Protocol SDK", "Metaplex", "TypeScript", "React"],
                difficulty="intermediate",
                potential_revenue="Per-migration fees or enterprise contracts",
                time_to_build="4-5 weeks",
                why_now="ZK Compression v2 is 1000x cheaper. Legacy collections need migration. Tooling gap is huge."
            ),
            BuildIdea(
                name="Latency Arbitrage Detector",
                description="Tool that identifies arbitrage opportunities created by Alpenglow's 150ms finality vs other chains. Alerts for cross-chain opportunities.",
                tech_stack=["Rust", "Jito", "Cross-chain bridges", "WebSocket feeds"],
                difficulty="advanced",
                potential_revenue="Arbitrage profits or API licensing",
                time_to_build="6-8 weeks",
                why_now="Alpenglow's 150ms finality creates new edge. CEX/DEX arb windows shrinking. Need specialized tools."
            ),
            BuildIdea(
                name="Developer Onboarding Accelerator",
                description="AI-powered tool that analyzes a dev's existing codebase and generates Solana program equivalents. Includes testing, deployment, and best practices.",
                tech_stack=["Claude API", "Anchor", "TypeScript", "VS Code Extension"],
                difficulty="intermediate",
                potential_revenue="SaaS subscription for agencies",
                time_to_build="4-6 weeks",
                why_now="17,700 developers and growing. 78% growth in builders. Onboarding is still painful. AI can accelerate."
            ),
        ],
        "stablecoins_payfi": [
            BuildIdea(
                name="AI Micropayment Orchestrator",
                description="SDK for AI agents to make and receive USDC micropayments. Handles batching, streaming payments, and cost optimization for agent-to-agent commerce.",
                tech_stack=["Solana Web3.js", "USDC SPL", "Helius", "TypeScript"],
                difficulty="intermediate",
                potential_revenue="0.01% transaction fee at scale",
                time_to_build="3-4 weeks",
                why_now="Standard Chartered says micropayments are Solana's killer app. AI agents need payment rails. No standard exists."
            ),
            BuildIdea(
                name="Cross-Border Remittance Tracker",
                description="Consumer app showing real-time USDC/USDPT remittance status, exchange rates, and fees vs Western Union traditional. Integrates with Solana Pay.",
                tech_stack=["React Native", "Solana Pay", "Circle API", "Maps API"],
                difficulty="beginner",
                potential_revenue="Affiliate fees from payment providers",
                time_to_build="2-3 weeks",
                why_now="Western Union launching USDPT. $700B/year remittance market. Users need comparison tools."
            ),
            BuildIdea(
                name="Stablecoin Yield Aggregator",
                description="Auto-routing tool that finds best USDC yields across Kamino, Marginfi, and Orca. One-click deposit and rebalancing with risk scores.",
                tech_stack=["Anchor", "Jupiter", "React", "Helius webhooks"],
                difficulty="intermediate",
                potential_revenue="0.1% performance fee",
                time_to_build="4-5 weeks",
                why_now="$4.25B USDC on Solana. Yields vary 5-15% across platforms. Users want simplicity."
            ),
            BuildIdea(
                name="Merchant Stablecoin Onramp",
                description="Shopify plugin that lets merchants accept USDC with instant conversion to local currency. Dashboard for reconciliation and tax reporting.",
                tech_stack=["Shopify SDK", "Solana Pay", "Circle API", "Node.js"],
                difficulty="intermediate",
                potential_revenue="0.5% payment processing fee",
                time_to_build="4-6 weeks",
                why_now="Visa settlement on Solana. Merchants want crypto without volatility. Plugin market is underserved."
            ),
        ],
        "rwa_tokenization": [
            BuildIdea(
                name="RWA Portfolio Tracker",
                description="Dashboard aggregating all tokenized stocks, bonds, and ETFs across Ondo, WisdomTree, xStocks. Shows P&L, dividends, and rebalancing suggestions.",
                tech_stack=["React", "Ondo API", "Solana RPC", "TradingView charts"],
                difficulty="beginner",
                potential_revenue="Premium features subscription",
                time_to_build="2-3 weeks",
                why_now="200+ Ondo assets on Solana. $1B+ RWA. No unified tracking tool. Users are fragmented."
            ),
            BuildIdea(
                name="Tokenized Stock Fractionalizer",
                description="Platform to buy fractional shares of tokenized stocks. Enable $1 minimum investments in Tesla, Apple via Ondo tokens.",
                tech_stack=["Anchor", "Ondo SDK", "React", "KYC integration"],
                difficulty="advanced",
                potential_revenue="0.25% trading fee",
                time_to_build="6-8 weeks",
                why_now="Tokenized equities up 2800%. Retail wants access. Fractionalization removes barriers."
            ),
            BuildIdea(
                name="RWA Collateral Oracle",
                description="Oracle providing real-time valuations of tokenized assets for DeFi lending protocols. Enables RWA-backed loans.",
                tech_stack=["Switchboard", "Pyth", "Rust", "Price feeds"],
                difficulty="advanced",
                potential_revenue="Oracle fees from protocols",
                time_to_build="5-7 weeks",
                why_now="DeFi needs RWA collateral. No reliable oracle for tokenized stocks. First mover captures protocol integrations."
            ),
            BuildIdea(
                name="RWA to DeFi Bridge UI",
                description="Simple interface to use tokenized bonds as collateral for USDC loans. Abstracts complexity of Ondo + lending protocol interaction.",
                tech_stack=["React", "Ondo SDK", "Kamino SDK", "TypeScript"],
                difficulty="intermediate",
                potential_revenue="Referral fees from protocols",
                time_to_build="3-4 weeks",
                why_now="Multiliquid just launched RWA redemption. Users want yield on idle assets. UX is currently terrible."
            ),
        ],
        "mobile_consumer": [
            BuildIdea(
                name="Seeker Rewards Aggregator",
                description="App that combines all Seeker-exclusive airdrops, quests, and rewards. Push notifications for new opportunities. Leaderboard for top earners.",
                tech_stack=["React Native", "Push notifications", "Solana Mobile SDK"],
                difficulty="beginner",
                potential_revenue="Promoted rewards from projects",
                time_to_build="2-3 weeks",
                why_now="150K Seeker preorders. Hardware-gated airdrops are new. Users need discovery tool."
            ),
            BuildIdea(
                name="Mobile-First DEX Experience",
                description="Tinder-style token discovery for mobile. Swipe right to buy, left to pass. Optimized for Seeker's dApp store.",
                tech_stack=["React Native", "Jupiter API", "Solana Mobile SDK", "Pump.fun API"],
                difficulty="intermediate",
                potential_revenue="Trading fees affiliate",
                time_to_build="3-4 weeks",
                why_now="Mobile trading is clunky. Seeker users want native experience. Gamification increases engagement."
            ),
            BuildIdea(
                name="Seed Vault Social Recovery",
                description="Add social recovery to Seeker's Seed Vault. Trusted friends can help recover wallet without compromising security.",
                tech_stack=["Solana Mobile SDK", "Shamir Secret Sharing", "React Native"],
                difficulty="advanced",
                potential_revenue="Premium feature subscription",
                time_to_build="4-6 weeks",
                why_now="Hardware wallets lack recovery options. Social recovery proven on Ethereum. Seeker needs this."
            ),
        ],
        "depin": [
            BuildIdea(
                name="DePIN Yield Optimizer",
                description="Dashboard comparing yields across Render, Helium, io.net, Nosana. Auto-allocates compute/bandwidth resources to highest paying network.",
                tech_stack=["Python", "DePIN protocol APIs", "React", "GPU detection"],
                difficulty="intermediate",
                potential_revenue="% of optimized yields",
                time_to_build="4-5 weeks",
                why_now="DePIN activity growing. Providers want max ROI on hardware. No unified optimization tool."
            ),
            BuildIdea(
                name="Dawn Network Coverage Mapper",
                description="Crowdsourced map showing Dawn Network bandwidth availability. Users can check coverage before contributing or buying.",
                tech_stack=["React", "Mapbox", "Dawn API", "WebSocket"],
                difficulty="beginner",
                potential_revenue="Ads or premium analytics",
                time_to_build="2-3 weeks",
                why_now="Dawn airdrop driving adoption. Coverage data is fragmented. Visual tool increases adoption."
            ),
            BuildIdea(
                name="GPU Marketplace for AI Training",
                description="Marketplace connecting GPU owners with AI developers needing compute. Escrow, SLA guarantees, performance benchmarking.",
                tech_stack=["Anchor", "Render/io.net APIs", "React", "Docker"],
                difficulty="advanced",
                potential_revenue="5-10% marketplace fee",
                time_to_build="6-8 weeks",
                why_now="AI training demand exploding. Centralized GPU is expensive. DePIN GPUs are underutilized."
            ),
        ],
        "memecoins": [
            BuildIdea(
                name="Pump.fun Analytics Pro",
                description="Real-time analytics for pump.fun launches. Bonding curve analysis, whale detection, rug pull probability score, social sentiment.",
                tech_stack=["React", "Pump.fun API", "Helius", "Twitter API"],
                difficulty="intermediate",
                potential_revenue="Premium subscription $20-50/mo",
                time_to_build="3-4 weeks",
                why_now="39K tokens/day on pump.fun. Most are scams. Traders need edge. First good analytics tool wins."
            ),
            BuildIdea(
                name="Meme Token Sniper Bot",
                description="Bot that detects new pump.fun launches, analyzes creator wallet history, and auto-buys promising tokens within first block.",
                tech_stack=["Rust", "Jito MEV", "Pump.fun SDK", "WebSocket"],
                difficulty="advanced",
                potential_revenue="Trading profits or bot rentals",
                time_to_build="4-6 weeks",
                why_now="First buyers get 10-100x. Manual trading too slow. Jito bundles enable priority."
            ),
            BuildIdea(
                name="Meme Launchpad Alternative",
                description="Pump.fun competitor with better tokenomics: anti-rug features, locked liquidity, creator vesting. Fair launch focused.",
                tech_stack=["Anchor", "React", "Metaplex", "Helius"],
                difficulty="advanced",
                potential_revenue="0.5-1% creation/trading fee",
                time_to_build="6-8 weeks",
                why_now="Pump.fun dominant but criticized. Market wants alternatives. $180M daily volume to capture."
            ),
        ],
        "defi_evolution": [
            BuildIdea(
                name="Intent-Based Trading Interface",
                description="Natural language trading: 'Swap $100 to SOL when price drops 5%'. AI interprets intent, executes via Jupiter.",
                tech_stack=["Claude API", "Jupiter SDK", "React", "WebSocket"],
                difficulty="intermediate",
                potential_revenue="Premium feature or affiliate",
                time_to_build="3-4 weeks",
                why_now="Intents are hot narrative. Trading UX still complex. AI + DeFi intersection underexplored."
            ),
            BuildIdea(
                name="Liquid Staking Comparator",
                description="Tool comparing mSOL, jitoSOL, bSOL yields, lock periods, and risks. One-click migration between LSTs.",
                tech_stack=["React", "Marinade/Jito/Blaze APIs", "TypeScript"],
                difficulty="beginner",
                potential_revenue="Referral fees from protocols",
                time_to_build="2-3 weeks",
                why_now="LST competition heating up. Users confused about differences. Migration is manual and complex."
            ),
        ],
        "zk_compression": [
            BuildIdea(
                name="cNFT Migration Service",
                description="Batch migration tool converting legacy NFT collections to compressed NFTs. Cost calculator, metadata preservation, verification.",
                tech_stack=["Light Protocol", "Metaplex", "TypeScript", "React"],
                difficulty="intermediate",
                potential_revenue="Per-NFT migration fee",
                time_to_build="3-4 weeks",
                why_now="1000x cost reduction with compression. Legacy collections paying high rent. Market needs migration path."
            ),
            BuildIdea(
                name="Compressed Token Factory",
                description="No-code platform to launch compressed tokens with minimal costs. Includes airdrop tools, holder snapshots, analytics.",
                tech_stack=["Light Protocol", "React", "Anchor", "Helius"],
                difficulty="intermediate",
                potential_revenue="Token creation fees",
                time_to_build="4-5 weeks",
                why_now="State rent is barrier to experimentation. Compression removes friction. First no-code tool wins."
            ),
        ],
    }
    
    def generate_ideas(self, narrative: Narrative) -> List[Dict[str, Any]]:
        """Generate build ideas for a narrative"""
        category = narrative.category
        
        if category not in self.IDEA_TEMPLATES:
            return self._generate_generic_ideas(narrative)
        
        ideas = self.IDEA_TEMPLATES[category]
        
        # Enhance ideas with narrative-specific context
        enhanced_ideas = []
        for idea in ideas[:5]:  # Top 5 ideas per narrative
            idea_dict = idea.to_dict()
            
            # Add narrative context
            idea_dict["narrative_context"] = {
                "narrative_name": narrative.name,
                "narrative_strength": narrative.strength_score,
                "supporting_evidence": narrative.evidence[:3]
            }
            
            enhanced_ideas.append(idea_dict)
        
        return enhanced_ideas
    
    def _generate_generic_ideas(self, narrative: Narrative) -> List[Dict[str, Any]]:
        """Generate generic ideas for unknown narratives"""
        return [
            {
                "name": f"{narrative.name} Analytics Dashboard",
                "description": f"Comprehensive analytics tool for tracking {narrative.name.lower()} trends and metrics.",
                "tech_stack": ["React", "Helius", "TypeScript"],
                "difficulty": "intermediate",
                "potential_revenue": "SaaS subscription",
                "time_to_build": "3-4 weeks",
                "why_now": f"Growing activity in {narrative.name.lower()} space. Analytics tools are needed."
            }
        ]


def generate_all_ideas(narratives: List[Narrative]) -> Dict[str, List[Dict[str, Any]]]:
    """Generate ideas for all narratives"""
    generator = IdeaGenerator()
    all_ideas = {}
    
    for narrative in narratives:
        ideas = generator.generate_ideas(narrative)
        narrative.build_ideas = ideas
        all_ideas[narrative.category] = ideas
    
    return all_ideas


if __name__ == "__main__":
    from signal_fetcher import fetch_all_signals
    from narrative_detector import detect_narratives
    
    signals = fetch_all_signals()
    detector = detect_narratives(signals)
    
    top_narratives = detector.get_top_narratives()
    all_ideas = generate_all_ideas(top_narratives)
    
    print("\n=== BUILD IDEAS ===")
    for category, ideas in all_ideas.items():
        print(f"\n{category.upper()}")
        for idea in ideas[:3]:
            print(f"  - {idea['name']}: {idea['description'][:80]}...")
