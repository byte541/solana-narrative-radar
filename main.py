#!/usr/bin/env python3
"""
Solana Narrative Radar
======================
A tool that monitors the Solana ecosystem, detects emerging narratives,
and generates concrete build ideas for each narrative.

Usage:
    python main.py              # Run full analysis
    python main.py --json       # Output JSON only
    python main.py --html       # Output HTML only
"""

import sys
import os
import json
import argparse
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from signal_fetcher import fetch_all_signals, Signal
from narrative_detector import detect_narratives, NarrativeDetector
from idea_generator import generate_all_ideas
from report_generator import ReportGenerator
from config import OUTPUT_DIR


def print_banner():
    """Print the ASCII banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   🔮 SOLANA NARRATIVE RADAR                                   ║
    ║   ─────────────────────────                                   ║
    ║   Detecting emerging trends & build opportunities             ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_pipeline(output_format: str = "all") -> dict:
    """
    Run the full narrative detection pipeline.
    
    Args:
        output_format: "all", "json", "html", or "markdown"
    
    Returns:
        Dictionary with pipeline results and file paths
    """
    results = {
        "success": False,
        "timestamp": datetime.now().isoformat(),
        "signals_collected": 0,
        "narratives_detected": 0,
        "files_generated": []
    }
    
    try:
        # Step 1: Fetch signals
        print("\n📡 Phase 1: Fetching Signals...")
        print("   ├── Querying GitHub for trending Solana repos...")
        print("   └── Loading research-based signals...")
        
        signals = fetch_all_signals()
        results["signals_collected"] = len(signals)
        print(f"   ✓ Collected {len(signals)} signals\n")
        
        # Step 2: Detect narratives
        print("🔍 Phase 2: Detecting Narratives...")
        detector = detect_narratives(signals)
        top_narratives = detector.get_top_narratives()
        results["narratives_detected"] = len(top_narratives)
        
        for narrative in top_narratives:
            emoji = {
                "ai_agents": "🤖",
                "infrastructure": "🏗️",
                "stablecoins_payfi": "💵",
                "rwa_tokenization": "🏦",
                "mobile_consumer": "📱",
                "depin": "🌐",
                "memecoins": "🐸",
            }.get(narrative.category, "📊")
            
            strength_bar = "█" * int(narrative.strength_score / 10)
            print(f"   {emoji} {narrative.name}: {strength_bar} ({narrative.strength_score:.0f}/100)")
        
        print(f"\n   ✓ Detected {len(top_narratives)} active narratives\n")
        
        # Step 3: Generate build ideas
        print("💡 Phase 3: Generating Build Ideas...")
        all_ideas = generate_all_ideas(top_narratives)
        total_ideas = sum(len(ideas) for ideas in all_ideas.values())
        print(f"   ✓ Generated {total_ideas} build ideas\n")
        
        # Step 4: Generate reports
        print("📝 Phase 4: Generating Reports...")
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        generator = ReportGenerator(OUTPUT_DIR)
        
        paths = generator.save_reports(top_narratives)
        results["files_generated"] = list(paths.values())
        
        for format_type, path in paths.items():
            print(f"   ├── {format_type.upper()}: {path}")
        
        print("\n   ✓ Reports saved successfully\n")
        
        # Print summary
        print("═" * 60)
        print("📊 PIPELINE COMPLETE")
        print("═" * 60)
        print(f"   Signals Analyzed:     {results['signals_collected']}")
        print(f"   Narratives Detected:  {results['narratives_detected']}")
        print(f"   Build Ideas:          {total_ideas}")
        print(f"   Reports Generated:    {len(results['files_generated'])}")
        print("═" * 60)
        
        # Top recommendation
        if top_narratives:
            top = top_narratives[0]
            print(f"\n🎯 TOP RECOMMENDATION: Focus on {top.name}")
            if top.build_ideas:
                print(f"   → Start with: {top.build_ideas[0]['name']}")
        
        results["success"] = True
        results["top_narratives"] = [
            {
                "name": n.name,
                "strength": n.strength_score,
                "signals": len(n.signals),
                "ideas": len(n.build_ideas)
            }
            for n in top_narratives
        ]
        
    except Exception as e:
        print(f"\n❌ Error in pipeline: {e}")
        import traceback
        traceback.print_exc()
        results["error"] = str(e)
    
    return results


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Solana Narrative Radar - Detect emerging trends and build opportunities"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["all", "json", "html", "markdown"],
        default="all",
        help="Output format (default: all)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress banner and progress output"
    )
    parser.add_argument(
        "--output", "-o",
        default=OUTPUT_DIR,
        help=f"Output directory (default: {OUTPUT_DIR})"
    )
    
    args = parser.parse_args()
    
    if not args.quiet:
        print_banner()
    
    # Update output directory if specified
    if args.output != OUTPUT_DIR:
        from config import OUTPUT_DIR as cfg_dir
        os.makedirs(args.output, exist_ok=True)
    
    results = run_pipeline(args.format)
    
    if not args.quiet:
        print("\n✨ Done! Check the output directory for reports.")
    
    return 0 if results["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
