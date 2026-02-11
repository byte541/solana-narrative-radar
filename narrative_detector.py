"""Narrative Detector - Clusters signals into emerging narratives"""

import re
from typing import List, Dict, Any, Tuple
from collections import defaultdict
from datetime import datetime

from signal_fetcher import Signal
from config import NARRATIVE_KEYWORDS


class Narrative:
    """Represents a detected narrative with associated signals and analysis"""
    
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category
        self.signals: List[Signal] = []
        self.strength_score = 0.0
        self.momentum = "stable"  # rising, stable, declining
        self.evidence: List[str] = []
        self.build_ideas: List[Dict[str, str]] = []
        self.summary = ""
    
    def add_signal(self, signal: Signal):
        self.signals.append(signal)
    
    def calculate_strength(self):
        """Calculate narrative strength based on signals"""
        if not self.signals:
            self.strength_score = 0.0
            return
        
        # Base score from signal count
        base_score = min(len(self.signals) * 10, 50)
        
        # Bonus for diverse sources
        sources = set(s.source for s in self.signals)
        source_bonus = len(sources) * 10
        
        # Bonus for GitHub stars (if available)
        github_stars = sum(
            s.metadata.get("stars", 0) 
            for s in self.signals 
            if s.source == "github"
        )
        star_bonus = min(github_stars / 100, 20)
        
        # Bonus for evidence items
        evidence_bonus = len(self.evidence) * 5
        
        self.strength_score = min(
            base_score + source_bonus + star_bonus + evidence_bonus, 
            100
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "category": self.category,
            "signal_count": len(self.signals),
            "strength_score": round(self.strength_score, 1),
            "momentum": self.momentum,
            "evidence": self.evidence,
            "build_ideas": self.build_ideas,
            "summary": self.summary,
            "signals": [s.to_dict() for s in self.signals]
        }


class NarrativeDetector:
    """Detects and clusters signals into narratives"""
    
    # Narrative definitions with display names
    NARRATIVE_NAMES = {
        "ai_agents": "AI Agents & Autonomous Trading",
        "infrastructure": "Infrastructure Upgrades (Firedancer/Alpenglow)",
        "stablecoins_payfi": "Stablecoin Revolution & PayFi",
        "rwa_tokenization": "Real-World Asset Tokenization",
        "mobile_consumer": "Mobile Web3 & Consumer Apps",
        "depin": "DePIN (Decentralized Physical Infrastructure)",
        "memecoins": "Meme Coins & Launchpads",
        "defi_evolution": "DeFi Protocol Evolution",
        "zk_compression": "ZK Compression & State Management"
    }
    
    def __init__(self):
        self.narratives: Dict[str, Narrative] = {}
        self._initialize_narratives()
    
    def _initialize_narratives(self):
        """Create narrative objects for each category"""
        for category, name in self.NARRATIVE_NAMES.items():
            self.narratives[category] = Narrative(name=name, category=category)
    
    def _match_keywords(self, text: str, keywords: List[str]) -> Tuple[bool, int]:
        """Check if text matches any keywords, return match count"""
        text_lower = text.lower()
        matches = sum(1 for kw in keywords if kw.lower() in text_lower)
        return matches > 0, matches
    
    def classify_signal(self, signal: Signal) -> List[str]:
        """Classify a signal into one or more narrative categories"""
        categories = []
        text = f"{signal.title} {signal.description}".lower()
        
        # Check metadata category if available
        if "category" in signal.metadata:
            preset_cat = signal.metadata["category"]
            if preset_cat in self.narratives:
                categories.append(preset_cat)
        
        # Keyword matching
        for category, keywords in NARRATIVE_KEYWORDS.items():
            matched, count = self._match_keywords(text, keywords)
            if matched and count >= 1:
                if category not in categories:
                    categories.append(category)
                signal.relevance_score = max(signal.relevance_score, count * 0.2)
        
        # Check GitHub topics
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
        
        # Calculate strengths
        for narrative in self.narratives.values():
            narrative.calculate_strength()
            self._extract_evidence(narrative)
    
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
            if "$" in desc:
                # Find dollar amounts
                amounts = re.findall(r'\$[\d.,]+[BMK]?', desc)
                for amt in amounts:
                    evidence.add(f"Market signal: {amt}")
            
            if "%" in desc:
                # Find percentages
                pcts = re.findall(r'[\d.,]+%', desc)
                for pct in pcts:
                    evidence.add(f"Growth metric: {pct}")
        
        narrative.evidence = list(evidence)[:10]  # Top 10 evidence points
    
    def get_top_narratives(self, limit: int = 5) -> List[Narrative]:
        """Get top narratives sorted by strength"""
        sorted_narratives = sorted(
            self.narratives.values(),
            key=lambda n: (n.strength_score, len(n.signals)),
            reverse=True
        )
        return [n for n in sorted_narratives if n.signals][:limit]
    
    def get_narrative_summary(self) -> Dict[str, Any]:
        """Get summary of all narratives"""
        return {
            "detection_time": datetime.now().isoformat(),
            "total_signals": sum(len(n.signals) for n in self.narratives.values()),
            "active_narratives": len([n for n in self.narratives.values() if n.signals]),
            "narratives": [n.to_dict() for n in self.get_top_narratives()]
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
        print(f"  Strength: {narrative.strength_score:.1f}/100")
        print(f"  Signals: {len(narrative.signals)}")
        print(f"  Evidence: {', '.join(narrative.evidence[:3])}")
