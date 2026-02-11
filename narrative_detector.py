"""Narrative Detector - Advanced clustering and scoring of signals into emerging narratives"""

import re
from typing import List, Dict, Any, Tuple
from collections import defaultdict
from datetime import datetime

from signal_fetcher import Signal
from config import NARRATIVE_KEYWORDS


class Narrative:
    """Represents a detected narrative with associated signals, analysis, and explanation"""
    
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category
        self.signals: List[Signal] = []
        self.strength_score = 0.0
        self.momentum = "stable"  # rising, stable, declining
        self.confidence = 0.0  # 0-100 confidence in narrative
        self.evidence: List[str] = []
        self.why_emerging: str = ""  # Explanation of WHY this narrative is emerging
        self.build_ideas: List[Dict[str, str]] = []
        self.summary = ""
        self.key_metrics: Dict[str, Any] = {}  # On-chain metrics from Helius
    
    def add_signal(self, signal: Signal):
        self.signals.append(signal)
    
    def calculate_strength(self):
        """Calculate narrative strength with sophisticated multi-factor scoring"""
        if not self.signals:
            self.strength_score = 0.0
            self.confidence = 0.0
            return
        
        # === SIGNAL VOLUME SCORE (0-25 points) ===
        # More signals = stronger narrative
        signal_count = len(self.signals)
        volume_score = min(signal_count * 3, 25)
        
        # === SOURCE DIVERSITY SCORE (0-25 points) ===
        # Signals from multiple sources = more confidence
        source_counts = defaultdict(int)
        for s in self.signals:
            source_counts[s.source] += 1
        
        source_diversity = len(source_counts)
        diversity_score = min(source_diversity * 8, 25)
        
        # Bonus for having on-chain data (Helius)
        has_onchain = "helius_onchain" in source_counts
        if has_onchain:
            diversity_score = min(diversity_score + 10, 25)
        
        # === QUALITY SCORE (0-25 points) ===
        # Based on signal metadata quality indicators
        quality_score = 0
        
        # GitHub stars indicate project quality
        total_stars = sum(
            s.metadata.get("stars", 0) 
            for s in self.signals 
            if s.source == "github"
        )
        quality_score += min(total_stars / 500, 10)
        
        # Evidence items from research
        evidence_count = sum(
            len(s.metadata.get("evidence", []))
            for s in self.signals
        )
        quality_score += min(evidence_count * 1.5, 10)
        
        # On-chain metrics boost quality significantly
        for s in self.signals:
            if s.metadata.get("signal_strength") == "high":
                quality_score += 3
            elif s.metadata.get("signal_strength") == "medium":
                quality_score += 1
        
        quality_score = min(quality_score, 25)
        
        # === RECENCY SCORE (0-15 points) ===
        # More recent signals = more relevant
        now = datetime.now()
        recent_signals = 0
        for s in self.signals:
            try:
                # Handle timezone-aware vs naive datetimes
                ts = s.timestamp.replace(tzinfo=None) if s.timestamp.tzinfo else s.timestamp
                if (now - ts).days < 7:
                    recent_signals += 1
            except:
                recent_signals += 1  # Assume recent if can't parse
        recency_score = min(recent_signals * 2, 15)
        
        # === CATEGORY-SPECIFIC BOOSTS (0-10 points) ===
        category_boost = 0
        
        # AI Agents and RWA are particularly hot right now
        if self.category in ["ai_agents", "rwa_tokenization"]:
            category_boost = 5
        # Infrastructure is a long-term play with high conviction
        elif self.category == "infrastructure":
            category_boost = 3
        # Stablecoins have clear institutional signal
        elif self.category == "stablecoins_payfi":
            category_boost = 4
        
        # === FINAL CALCULATION ===
        raw_score = volume_score + diversity_score + quality_score + recency_score + category_boost
        self.strength_score = min(raw_score, 100)
        
        # Confidence is based on source diversity and evidence quality
        if source_diversity >= 3 and has_onchain:
            self.confidence = min(90, 60 + evidence_count * 3)
        elif source_diversity >= 2:
            self.confidence = min(75, 45 + evidence_count * 3)
        else:
            self.confidence = min(50, 30 + evidence_count * 3)
        
        # Determine momentum based on recent activity
        if recency_score > 10:
            self.momentum = "rising"
        elif recency_score > 5:
            self.momentum = "stable"
        else:
            self.momentum = "declining"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "category": self.category,
            "signal_count": len(self.signals),
            "strength_score": round(self.strength_score, 1),
            "confidence": round(self.confidence, 1),
            "momentum": self.momentum,
            "why_emerging": self.why_emerging,
            "evidence": self.evidence,
            "key_metrics": self.key_metrics,
            "build_ideas": self.build_ideas,
            "summary": self.summary,
            "signals": [s.to_dict() for s in self.signals]
        }


class NarrativeDetector:
    """Detects, clusters, and analyzes signals into narratives with explanations"""
    
    # Narrative definitions with display names and base explanations
    NARRATIVE_INFO = {
        "ai_agents": {
            "name": "AI Agents & Autonomous Trading",
            "base_why": "LLM capabilities reached threshold for autonomous decision-making. Solana's sub-second finality enables real-time agent execution. ai16z proved the model works at scale."
        },
        "infrastructure": {
            "name": "Infrastructure Upgrades (Firedancer/Alpenglow)",
            "base_why": "Previous cycle exposed congestion issues. Institutional adoption requires enterprise-grade performance. Firedancer and Alpenglow address core scaling challenges."
        },
        "stablecoins_payfi": {
            "name": "Stablecoin Revolution & PayFi",
            "base_why": "Solana's low fees make micropayments economically viable. Legacy payment giants (Visa, Western Union) validating blockchain rails. Regulatory clarity emerging."
        },
        "rwa_tokenization": {
            "name": "Real-World Asset Tokenization",
            "base_why": "SEC clarity on tokenized securities. TradFi demand for 24/7 markets. T+0 settlement superior to T+2 traditional. BlackRock and Fidelity entering space."
        },
        "mobile_consumer": {
            "name": "Mobile Web3 & Consumer Apps",
            "base_why": "Saga success proved demand for crypto phones. Hardware wallets solve UX. Token airdrops subsidize consumer adoption. Mobile-first generation entering crypto."
        },
        "depin": {
            "name": "DePIN (Decentralized Physical Infrastructure)",
            "base_why": "AI training demand outstripping centralized GPU supply. Decentralized compute 60% cheaper. Token incentives align hardware contributors. Helium proved model works."
        },
        "memecoins": {
            "name": "Meme Coins & Launchpads",
            "base_why": "Bonding curve innovation removed rug risk. Low friction = high velocity trading. Cultural moment for meme trading. Solana speed enables better trading UX."
        },
        "defi_evolution": {
            "name": "DeFi Protocol Evolution",
            "base_why": "Aggregation layer becoming essential infrastructure. Perp demand from CEX refugees. Liquid staking wars driving innovation and yield competition."
        },
        "zk_compression": {
            "name": "ZK Compression & State Management",
            "base_why": "State rent was blocking mass adoption experiments. Compressed NFTs proved concept. 1000x cost reduction unlocks new use cases. Now generalizing to all account types."
        }
    }
    
    def __init__(self):
        self.narratives: Dict[str, Narrative] = {}
        self._initialize_narratives()
    
    def _initialize_narratives(self):
        """Create narrative objects for each category"""
        for category, info in self.NARRATIVE_INFO.items():
            narrative = Narrative(name=info["name"], category=category)
            narrative.why_emerging = info["base_why"]
            self.narratives[category] = narrative
    
    def _match_keywords(self, text: str, keywords: List[str]) -> Tuple[bool, int, List[str]]:
        """Check if text matches keywords, return match count and matched keywords"""
        text_lower = text.lower()
        matched_keywords = [kw for kw in keywords if kw.lower() in text_lower]
        return len(matched_keywords) > 0, len(matched_keywords), matched_keywords
    
    def classify_signal(self, signal: Signal) -> List[str]:
        """Classify a signal into one or more narrative categories"""
        categories = []
        text = f"{signal.title} {signal.description}".lower()
        
        # Check metadata category if available (from research or Helius)
        if "category" in signal.metadata and signal.metadata["category"]:
            preset_cat = signal.metadata["category"]
            if preset_cat in self.narratives:
                categories.append(preset_cat)
        
        # Enhanced keyword matching
        for category, keywords in NARRATIVE_KEYWORDS.items():
            matched, count, matched_kws = self._match_keywords(text, keywords)
            if matched and count >= 1:
                if category not in categories:
                    categories.append(category)
                # Score based on match density
                signal.relevance_score = max(signal.relevance_score, min(count * 0.15, 1.0))
        
        # Check GitHub topics for additional signal
        if signal.source == "github":
            topics = signal.metadata.get("topics", [])
            for topic in topics:
                topic_text = topic.lower()
                for category, keywords in NARRATIVE_KEYWORDS.items():
                    if any(kw in topic_text for kw in keywords):
                        if category not in categories:
                            categories.append(category)
        
        return categories
    
    def process_signals(self, signals: List[Signal]):
        """Process all signals and assign them to narratives"""
        for signal in signals:
            categories = self.classify_signal(signal)
            signal.narrative_tags = categories
            
            for category in categories:
                if category in self.narratives:
                    self.narratives[category].add_signal(signal)
        
        # Calculate strengths and extract insights
        for narrative in self.narratives.values():
            narrative.calculate_strength()
            self._extract_evidence(narrative)
            self._extract_metrics(narrative)
            self._enhance_why_emerging(narrative)
    
    def _extract_evidence(self, narrative: Narrative):
        """Extract key evidence points from signals"""
        evidence = set()
        
        for signal in narrative.signals:
            # Add evidence from metadata
            if "evidence" in signal.metadata:
                for e in signal.metadata["evidence"]:
                    evidence.add(e)
            
            # Extract key metrics from description
            desc = signal.description
            
            # Dollar amounts (market signals)
            amounts = re.findall(r'\$[\d.,]+[BMK]?\+?', desc)
            for amt in amounts:
                evidence.add(f"Market signal: {amt}")
            
            # Percentages (growth metrics)
            pcts = re.findall(r'[\d.,]+%', desc)
            for pct in pcts:
                if float(pct.replace('%', '').replace(',', '')) > 20:
                    evidence.add(f"Growth: {pct}")
            
            # Large numbers (user/transaction counts)
            large_nums = re.findall(r'[\d.,]+[KM]\+?\s+(?:users|transactions|tokens|daily|active)', desc, re.I)
            for num in large_nums:
                evidence.add(f"Scale: {num}")
        
        narrative.evidence = list(evidence)[:12]  # Top 12 evidence points
    
    def _extract_metrics(self, narrative: Narrative):
        """Extract on-chain metrics from Helius signals"""
        metrics = {}
        
        for signal in narrative.signals:
            if signal.source == "helius_onchain" and "metrics" in signal.metadata:
                signal_metrics = signal.metadata["metrics"]
                
                # Merge metrics intelligently
                for key, value in signal_metrics.items():
                    if key not in metrics:
                        metrics[key] = value
                    elif isinstance(value, (int, float)) and isinstance(metrics[key], (int, float)):
                        # Sum numeric metrics
                        metrics[key] = value  # Use latest value
        
        narrative.key_metrics = metrics
    
    def _enhance_why_emerging(self, narrative: Narrative):
        """Enhance the WHY explanation with signal-specific insights"""
        # Collect why_emerging from individual signals
        signal_whys = []
        for signal in narrative.signals:
            if "why_emerging" in signal.metadata and signal.metadata["why_emerging"]:
                signal_whys.append(signal.metadata["why_emerging"])
        
        # If we have signal-specific explanations, enhance the base explanation
        if signal_whys:
            unique_whys = list(set(signal_whys))[:3]  # Top 3 unique explanations
            combined = f"{narrative.why_emerging}\n\n**Key Drivers:**\n"
            for why in unique_whys:
                combined += f"• {why}\n"
            narrative.why_emerging = combined.strip()
        
        # Add on-chain evidence if available
        if narrative.key_metrics:
            metrics_summary = []
            if "tps" in narrative.key_metrics:
                metrics_summary.append(f"{narrative.key_metrics['tps']:,} TPS network activity")
            if "total_supply_usd" in narrative.key_metrics:
                supply = narrative.key_metrics["total_supply_usd"]
                metrics_summary.append(f"${supply/1e9:.2f}B stablecoin supply")
            if "recent_tx_count" in narrative.key_metrics:
                metrics_summary.append(f"{narrative.key_metrics['recent_tx_count']} recent transactions")
            
            if metrics_summary:
                narrative.why_emerging += f"\n\n**On-Chain Validation:** {', '.join(metrics_summary)}"
    
    def get_top_narratives(self, limit: int = 7) -> List[Narrative]:
        """Get top narratives sorted by strength, filtering out weak ones"""
        sorted_narratives = sorted(
            self.narratives.values(),
            key=lambda n: (n.strength_score, len(n.signals), n.confidence),
            reverse=True
        )
        # Only return narratives with signals AND minimum strength
        return [n for n in sorted_narratives if n.signals and n.strength_score >= 20][:limit]
    
    def get_narrative_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of all narratives"""
        top = self.get_top_narratives()
        
        return {
            "detection_time": datetime.now().isoformat(),
            "total_signals": sum(len(n.signals) for n in self.narratives.values()),
            "active_narratives": len([n for n in self.narratives.values() if n.signals]),
            "top_narrative": top[0].name if top else None,
            "average_confidence": sum(n.confidence for n in top) / len(top) if top else 0,
            "narratives": [n.to_dict() for n in top]
        }


def detect_narratives(signals: List[Signal]) -> NarrativeDetector:
    """Main function to detect narratives from signals"""
    detector = NarrativeDetector()
    detector.process_signals(signals)
    return detector


if __name__ == "__main__":
    from signal_fetcher import fetch_all_signals
    
    signals = fetch_all_signals()
    detector = detect_narratives(signals)
    
    print("\n=== TOP NARRATIVES ===")
    for narrative in detector.get_top_narratives():
        print(f"\n{narrative.name}")
        print(f"  Strength: {narrative.strength_score:.1f}/100 (Confidence: {narrative.confidence:.0f}%)")
        print(f"  Momentum: {narrative.momentum}")
        print(f"  Signals: {len(narrative.signals)}")
        print(f"  Evidence: {', '.join(narrative.evidence[:3])}")
        print(f"  Why: {narrative.why_emerging[:150]}...")
