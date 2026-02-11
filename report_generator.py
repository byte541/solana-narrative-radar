"""Report Generator - Creates stunning HTML dashboard and comprehensive reports"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any

from narrative_detector import Narrative


class ReportGenerator:
    """Generates beautiful, data-rich reports in HTML and Markdown formats"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_markdown(self, narratives: List[Narrative], timestamp: datetime = None) -> str:
        """Generate a comprehensive markdown report"""
        timestamp = timestamp or datetime.now()
        
        md = []
        md.append("# 🔮 Solana Narrative Radar Report")
        md.append(f"\n**Generated:** {timestamp.strftime('%Y-%m-%d %H:%M UTC')}")
        md.append(f"\n**Analysis Period:** Past 14 days")
        md.append(f"\n**Total Signals Analyzed:** {sum(len(n.signals) for n in narratives)}")
        md.append(f"\n**Data Sources:** GitHub API, Helius On-Chain Data, Ecosystem Research")
        md.append("\n---\n")
        
        # Executive Summary
        md.append("## 📊 Executive Summary\n")
        md.append("The following narratives are emerging in the Solana ecosystem, ranked by signal strength, source diversity, and on-chain validation:\n")
        
        for i, narrative in enumerate(narratives, 1):
            strength_bar = "█" * int(narrative.strength_score / 10) + "░" * (10 - int(narrative.strength_score / 10))
            momentum_icon = "📈" if narrative.momentum == "rising" else "➡️" if narrative.momentum == "stable" else "📉"
            md.append(f"{i}. **{narrative.name}** [{strength_bar}] {narrative.strength_score:.0f}/100 {momentum_icon}")
            md.append(f"   - Confidence: {narrative.confidence:.0f}% | Signals: {len(narrative.signals)}")
        
        md.append("\n---\n")
        
        # Detailed Narratives
        for narrative in narratives:
            md.append(f"## {self._get_emoji(narrative.category)} {narrative.name}")
            md.append(f"\n**Strength Score:** {narrative.strength_score:.0f}/100 | **Confidence:** {narrative.confidence:.0f}% | **Momentum:** {narrative.momentum.title()} | **Signals:** {len(narrative.signals)}\n")
            
            # Why This Narrative is Emerging
            md.append("### 🎯 Why This Narrative is Emerging")
            md.append(f"\n{narrative.why_emerging}\n")
            
            # Evidence
            if narrative.evidence:
                md.append("\n### 🔍 Key Evidence")
                for ev in narrative.evidence[:6]:
                    md.append(f"- {ev}")
            
            # On-Chain Metrics
            if narrative.key_metrics:
                md.append("\n### 📡 On-Chain Metrics (via Helius)")
                for key, value in narrative.key_metrics.items():
                    if isinstance(value, (int, float)) and value > 0:
                        formatted = f"{value:,.0f}" if isinstance(value, int) else f"{value:,.2f}"
                        md.append(f"- **{key.replace('_', ' ').title()}:** {formatted}")
            
            # Build Ideas
            if narrative.build_ideas:
                md.append("\n### 💡 Build Ideas")
                for idea in narrative.build_ideas[:3]:
                    md.append(f"\n#### {idea['name']}")
                    md.append(f"\n{idea['description']}")
                    md.append(f"\n- **Tech Stack:** {', '.join(idea['tech_stack'])}")
                    md.append(f"- **Difficulty:** {idea['difficulty'].title()}")
                    md.append(f"- **Time to Build:** {idea['time_to_build']}")
                    md.append(f"- **Revenue Model:** {idea['potential_revenue']}")
                    md.append(f"- **Why Now:** {idea['why_now']}")
            
            # Top Signals
            md.append("\n### 📡 Top Signals")
            for signal in narrative.signals[:5]:
                source_icon = {"github": "🐙", "helius_onchain": "⛓️", "research": "📰"}.get(signal.source, "📊")
                md.append(f"- {source_icon} [{signal.title}]({signal.url})")
            
            md.append("\n---\n")
        
        # Action Plan
        md.append("## 🚀 Recommended Action Plan\n")
        md.append("Based on narrative strength, confidence levels, and on-chain validation:\n")
        
        if narratives:
            top = narratives[0]
            md.append(f"1. **Highest Priority:** {top.name}")
            md.append(f"   - Strength {top.strength_score:.0f}/100 with {top.confidence:.0f}% confidence")
            if top.build_ideas:
                md.append(f"   - Start with: **{top.build_ideas[0]['name']}**")
        
        if len(narratives) > 1:
            second = narratives[1]
            md.append(f"\n2. **Secondary Focus:** {second.name}")
            md.append(f"   - {second.momentum.title()} momentum, good market timing")
        
        if len(narratives) > 2:
            third = narratives[2]
            md.append(f"\n3. **Emerging Opportunity:** {third.name}")
        
        md.append("\n---\n")
        md.append("*Report generated by Solana Narrative Radar v2.0*")
        md.append(f"\n*Data sources: GitHub API (authenticated), Helius On-Chain API, Curated Research*")
        
        return "\n".join(md)
    
    def generate_html(self, narratives: List[Narrative], timestamp: datetime = None) -> str:
        """Generate a stunning HTML dashboard report"""
        timestamp = timestamp or datetime.now()
        total_signals = sum(len(n.signals) for n in narratives)
        
        # Get on-chain data summary for header
        onchain_stats = self._get_onchain_summary(narratives)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solana Narrative Radar | Live Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --sol-purple: #9945FF;
            --sol-green: #14F195;
            --sol-blue: #00D1FF;
            --sol-pink: #FF6B6B;
            --sol-orange: #FFA726;
            --bg-dark: #0a0a0f;
            --bg-card: #12121a;
            --bg-card-hover: #1a1a25;
            --text-primary: #ffffff;
            --text-secondary: #8888a0;
            --border-color: #2a2a3a;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        /* Hero Header */
        .hero {{
            background: linear-gradient(135deg, rgba(153, 69, 255, 0.15) 0%, rgba(0, 209, 255, 0.15) 50%, rgba(20, 241, 149, 0.1) 100%);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            padding: 40px;
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
        }}
        
        .hero::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at 30% 30%, rgba(153, 69, 255, 0.1) 0%, transparent 50%);
            animation: pulse 8s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 0.5; }}
            50% {{ transform: scale(1.1); opacity: 0.8; }}
        }}
        
        .hero-content {{
            position: relative;
            z-index: 1;
        }}
        
        .hero h1 {{
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--sol-green) 0%, var(--sol-blue) 50%, var(--sol-purple) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 12px;
        }}
        
        .hero .tagline {{
            font-size: 1.1rem;
            color: var(--text-secondary);
            margin-bottom: 24px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            margin-top: 20px;
        }}
        
        .stat-card {{
            background: rgba(255,255,255,0.05);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px 20px;
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--sol-green);
        }}
        
        .stat-label {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-top: 4px;
        }}
        
        /* Live Badge */
        .live-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(20, 241, 149, 0.15);
            border: 1px solid var(--sol-green);
            color: var(--sol-green);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-bottom: 16px;
        }}
        
        .live-dot {{
            width: 8px;
            height: 8px;
            background: var(--sol-green);
            border-radius: 50%;
            animation: blink 1.5s infinite;
        }}
        
        @keyframes blink {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.3; }}
        }}
        
        /* Narrative Cards */
        .section-title {{
            font-size: 1.4rem;
            font-weight: 700;
            margin: 30px 0 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .narratives-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
            gap: 24px;
        }}
        
        .narrative-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .narrative-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--sol-purple), var(--sol-green));
            opacity: 0;
            transition: opacity 0.3s;
        }}
        
        .narrative-card:hover {{
            transform: translateY(-4px);
            border-color: var(--sol-purple);
            box-shadow: 0 20px 40px rgba(153, 69, 255, 0.15);
        }}
        
        .narrative-card:hover::before {{
            opacity: 1;
        }}
        
        .narrative-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
        }}
        
        .narrative-emoji {{
            font-size: 2rem;
            margin-bottom: 8px;
        }}
        
        .narrative-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1.3;
        }}
        
        .score-badge {{
            background: linear-gradient(135deg, var(--sol-purple), var(--sol-blue));
            padding: 8px 14px;
            border-radius: 10px;
            font-weight: 700;
            font-size: 1.1rem;
            white-space: nowrap;
        }}
        
        .metrics-row {{
            display: flex;
            gap: 16px;
            margin: 16px 0;
            flex-wrap: wrap;
        }}
        
        .metric {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}
        
        .metric-value {{
            color: var(--sol-green);
            font-weight: 600;
        }}
        
        .momentum-badge {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        
        .momentum-rising {{
            background: rgba(20, 241, 149, 0.15);
            color: var(--sol-green);
        }}
        
        .momentum-stable {{
            background: rgba(0, 209, 255, 0.15);
            color: var(--sol-blue);
        }}
        
        .momentum-declining {{
            background: rgba(255, 107, 107, 0.15);
            color: var(--sol-pink);
        }}
        
        /* Strength Bar */
        .strength-bar-container {{
            margin: 16px 0;
        }}
        
        .strength-bar {{
            height: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .strength-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--sol-green), var(--sol-blue), var(--sol-purple));
            border-radius: 4px;
            transition: width 1s ease-out;
        }}
        
        .strength-labels {{
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin-top: 6px;
        }}
        
        /* Why Section */
        .why-section {{
            background: rgba(153, 69, 255, 0.08);
            border-left: 3px solid var(--sol-purple);
            padding: 14px;
            border-radius: 0 8px 8px 0;
            margin: 16px 0;
        }}
        
        .why-title {{
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--sol-purple);
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .why-text {{
            font-size: 0.9rem;
            color: var(--text-secondary);
            line-height: 1.6;
            white-space: pre-line;
        }}
        
        .why-text-content {{
            display: block;
        }}
        
        .why-text-content.collapsed {{
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .why-toggle {{
            background: none;
            border: none;
            color: var(--sol-purple);
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            padding: 8px 0 0 0;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            transition: color 0.2s;
        }}
        
        .why-toggle:hover {{
            color: var(--sol-green);
        }}
        
        .why-toggle-icon {{
            transition: transform 0.3s ease;
        }}
        
        .why-toggle.expanded .why-toggle-icon {{
            transform: rotate(180deg);
        }}
        
        /* Evidence Pills */
        .evidence-section {{
            margin: 16px 0;
        }}
        
        .evidence-title {{
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 10px;
        }}
        
        .evidence-pills {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        
        .evidence-pill {{
            background: rgba(20, 241, 149, 0.1);
            border: 1px solid rgba(20, 241, 149, 0.3);
            color: var(--sol-green);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }}
        
        /* Build Ideas */
        .ideas-section {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid var(--border-color);
        }}
        
        .ideas-title {{
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--sol-blue);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        
        .idea-card {{
            background: rgba(0, 209, 255, 0.05);
            border: 1px solid rgba(0, 209, 255, 0.2);
            border-radius: 10px;
            padding: 14px;
            margin: 10px 0;
        }}
        
        .idea-name {{
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 6px;
        }}
        
        .idea-desc {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-bottom: 10px;
        }}
        
        .idea-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        
        .idea-tag {{
            background: rgba(153, 69, 255, 0.15);
            color: var(--sol-purple);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 500;
        }}
        
        /* Signals */
        .signals-section {{
            margin-top: 16px;
        }}
        
        .signals-title {{
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-bottom: 10px;
        }}
        
        .signal {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 0;
            border-bottom: 1px solid var(--border-color);
            text-decoration: none;
            color: var(--text-secondary);
            font-size: 0.85rem;
            transition: color 0.2s;
        }}
        
        .signal:last-child {{
            border-bottom: none;
        }}
        
        .signal:hover {{
            color: var(--sol-green);
        }}
        
        .signal-icon {{
            font-size: 1rem;
            flex-shrink: 0;
        }}
        
        /* Action Plan */
        .action-plan {{
            background: linear-gradient(135deg, rgba(20, 241, 149, 0.1), rgba(0, 209, 255, 0.1));
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 30px;
            margin: 40px 0;
        }}
        
        .action-plan h2 {{
            font-size: 1.4rem;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .action-item {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 18px;
            margin: 12px 0;
            display: flex;
            gap: 16px;
            align-items: flex-start;
        }}
        
        .action-number {{
            background: linear-gradient(135deg, var(--sol-purple), var(--sol-green));
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            flex-shrink: 0;
        }}
        
        .action-content {{
            flex: 1;
        }}
        
        .action-title {{
            font-weight: 600;
            margin-bottom: 4px;
        }}
        
        .action-desc {{
            font-size: 0.9rem;
            color: var(--text-secondary);
        }}
        
        /* Footer */
        footer {{
            text-align: center;
            padding: 40px 20px;
            color: var(--text-secondary);
            font-size: 0.85rem;
            border-top: 1px solid var(--border-color);
            margin-top: 40px;
        }}
        
        footer a {{
            color: var(--sol-purple);
            text-decoration: none;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 2rem;
            }}
            
            .narratives-grid {{
                grid-template-columns: 1fr;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Hero Section -->
        <header class="hero">
            <div class="hero-content">
                <div class="live-badge">
                    <span class="live-dot"></span>
                    <span>LIVE DATA</span>
                </div>
                <h1>🔮 Solana Narrative Radar</h1>
                <p class="tagline">Real-time narrative detection with on-chain data validation via Helius API</p>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{len(narratives)}</div>
                        <div class="stat-label">Active Narratives</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{total_signals}</div>
                        <div class="stat-label">Signals Analyzed</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{onchain_stats.get('tps', 'N/A')}</div>
                        <div class="stat-label">Network TPS</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{onchain_stats.get('stablecoins', 'N/A')}</div>
                        <div class="stat-label">Stablecoin TVL</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{timestamp.strftime('%H:%M')}</div>
                        <div class="stat-label">Last Updated (UTC)</div>
                    </div>
                </div>
            </div>
        </header>
        
        <!-- Narratives Section -->
        <h2 class="section-title">📊 Emerging Narratives</h2>
        <div class="narratives-grid">
"""
        
        # Generate narrative cards
        for narrative in narratives:
            emoji = self._get_emoji(narrative.category)
            momentum_class = f"momentum-{narrative.momentum}"
            momentum_icon = "📈" if narrative.momentum == "rising" else "➡️" if narrative.momentum == "stable" else "📉"
            
            html += f"""
            <div class="narrative-card">
                <div class="narrative-header">
                    <div>
                        <div class="narrative-emoji">{emoji}</div>
                        <div class="narrative-title">{narrative.name}</div>
                    </div>
                    <div class="score-badge">{narrative.strength_score:.0f}</div>
                </div>
                
                <div class="metrics-row">
                    <div class="metric">
                        <span>Confidence:</span>
                        <span class="metric-value">{narrative.confidence:.0f}%</span>
                    </div>
                    <div class="metric">
                        <span>Signals:</span>
                        <span class="metric-value">{len(narrative.signals)}</span>
                    </div>
                    <span class="momentum-badge {momentum_class}">{momentum_icon} {narrative.momentum.title()}</span>
                </div>
                
                <div class="strength-bar-container">
                    <div class="strength-bar">
                        <div class="strength-fill" style="width: {narrative.strength_score}%"></div>
                    </div>
                    <div class="strength-labels">
                        <span>Signal Strength</span>
                        <span>{narrative.strength_score:.0f}/100</span>
                    </div>
                </div>
                
                <div class="why-section">
                    <div class="why-title">🎯 Why This Narrative is Emerging</div>
                    <div class="why-text">
                        <span class="why-text-content{' collapsed' if len(narrative.why_emerging) > 200 else ''}">{narrative.why_emerging}</span>
                        {f'<button class="why-toggle" onclick="toggleWhy(this)"><span>Read more</span><span class="why-toggle-icon">▼</span></button>' if len(narrative.why_emerging) > 200 else ''}
                    </div>
                </div>
"""
            
            # Evidence pills
            if narrative.evidence:
                html += """
                <div class="evidence-section">
                    <div class="evidence-title">Key Evidence:</div>
                    <div class="evidence-pills">
"""
                for ev in narrative.evidence[:4]:
                    html += f'                        <span class="evidence-pill">{ev[:40]}{"..." if len(ev) > 40 else ""}</span>\n'
                html += """                    </div>
                </div>
"""
            
            # Build ideas
            if narrative.build_ideas:
                html += """
                <div class="ideas-section">
                    <div class="ideas-title">💡 Top Build Ideas</div>
"""
                for idea in narrative.build_ideas[:2]:
                    html += f"""
                    <div class="idea-card">
                        <div class="idea-name">{idea['name']}</div>
                        <div class="idea-desc">{idea['description'][:120]}...</div>
                        <div class="idea-meta">
                            <span class="idea-tag">{idea['difficulty'].title()}</span>
                            <span class="idea-tag">{idea['time_to_build']}</span>
                            <span class="idea-tag">{idea['potential_revenue'][:30]}</span>
                        </div>
                    </div>
"""
                html += """                </div>
"""
            
            # Top signals
            html += """
                <div class="signals-section">
                    <div class="signals-title">📡 Recent Signals:</div>
"""
            for signal in narrative.signals[:3]:
                icon = {"github": "🐙", "helius_onchain": "⛓️", "research": "📰"}.get(signal.source, "📊")
                title = signal.title[:45] + "..." if len(signal.title) > 45 else signal.title
                html += f'                    <a href="{signal.url}" class="signal" target="_blank"><span class="signal-icon">{icon}</span> {title}</a>\n'
            
            html += """                </div>
            </div>
"""
        
        # Action Plan
        html += """
        </div>
        
        <div class="action-plan">
            <h2>🚀 Recommended Action Plan</h2>
"""
        
        if narratives:
            top = narratives[0]
            html += f"""
            <div class="action-item">
                <div class="action-number">1</div>
                <div class="action-content">
                    <div class="action-title">Highest Priority: {top.name}</div>
                    <div class="action-desc">Strength {top.strength_score:.0f}/100 with {top.confidence:.0f}% confidence. {f"Start with: {top.build_ideas[0]['name']}" if top.build_ideas else "Strong momentum in this space."}</div>
                </div>
            </div>
"""
            
            if len(narratives) > 1:
                second = narratives[1]
                html += f"""
            <div class="action-item">
                <div class="action-number">2</div>
                <div class="action-content">
                    <div class="action-title">Secondary Focus: {second.name}</div>
                    <div class="action-desc">{second.momentum.title()} momentum with solid on-chain validation. Good timing for builders.</div>
                </div>
            </div>
"""
            
            if len(narratives) > 2:
                third = narratives[2]
                html += f"""
            <div class="action-item">
                <div class="action-number">3</div>
                <div class="action-content">
                    <div class="action-title">Watch: {third.name}</div>
                    <div class="action-desc">Emerging opportunity with growing signal strength. Monitor for timing.</div>
                </div>
            </div>
"""
        
        html += f"""
        </div>
        
        <footer>
            <p>Generated by <strong>Solana Narrative Radar v2.0</strong></p>
            <p>Data sources: <a href="https://helius.xyz" target="_blank">Helius API</a> (on-chain), GitHub API, Ecosystem Research</p>
            <p>Report generated: {timestamp.strftime('%Y-%m-%d %H:%M UTC')}</p>
        </footer>
    </div>
    
    <script>
        function toggleWhy(btn) {{
            const content = btn.previousElementSibling;
            const isCollapsed = content.classList.contains('collapsed');
            
            if (isCollapsed) {{
                content.classList.remove('collapsed');
                btn.classList.add('expanded');
                btn.querySelector('span:first-child').textContent = 'Show less';
            }} else {{
                content.classList.add('collapsed');
                btn.classList.remove('expanded');
                btn.querySelector('span:first-child').textContent = 'Read more';
            }}
        }}
    </script>
</body>
</html>
"""
        return html
    
    def _get_emoji(self, category: str) -> str:
        """Get emoji for narrative category"""
        emojis = {
            "ai_agents": "🤖",
            "infrastructure": "🏗️",
            "stablecoins_payfi": "💵",
            "rwa_tokenization": "🏦",
            "mobile_consumer": "📱",
            "depin": "🌐",
            "memecoins": "🐸",
            "defi_evolution": "💱",
            "zk_compression": "🔐"
        }
        return emojis.get(category, "📊")
    
    def _get_onchain_summary(self, narratives: List[Narrative]) -> Dict[str, str]:
        """Extract on-chain stats summary from narratives"""
        stats = {"tps": "N/A", "stablecoins": "N/A"}
        
        for narrative in narratives:
            metrics = narrative.key_metrics
            if "tps" in metrics and metrics["tps"]:
                stats["tps"] = f"{metrics['tps']:,}"
            if "total_supply_usd" in metrics and metrics["total_supply_usd"]:
                stats["stablecoins"] = f"${metrics['total_supply_usd']/1e9:.1f}B"
        
        return stats
    
    def save_reports(self, narratives: List[Narrative]) -> Dict[str, str]:
        """Save HTML, Markdown, and JSON reports"""
        timestamp = datetime.now()
        
        # Generate reports
        md_content = self.generate_markdown(narratives, timestamp)
        html_content = self.generate_html(narratives, timestamp)
        
        # Save files
        md_path = os.path.join(self.output_dir, "narrative_report.md")
        html_path = os.path.join(self.output_dir, "narrative_report.html")
        
        with open(md_path, "w") as f:
            f.write(md_content)
        
        with open(html_path, "w") as f:
            f.write(html_content)
        
        # Also save JSON data
        json_path = os.path.join(self.output_dir, "narrative_data.json")
        with open(json_path, "w") as f:
            json.dump({
                "version": "2.0",
                "timestamp": timestamp.isoformat(),
                "total_signals": sum(len(n.signals) for n in narratives),
                "narratives": [n.to_dict() for n in narratives]
            }, f, indent=2)
        
        return {
            "markdown": md_path,
            "html": html_path,
            "json": json_path
        }


if __name__ == "__main__":
    from signal_fetcher import fetch_all_signals
    from narrative_detector import detect_narratives
    from idea_generator import generate_all_ideas
    
    # Full pipeline
    signals = fetch_all_signals()
    detector = detect_narratives(signals)
    top_narratives = detector.get_top_narratives()
    generate_all_ideas(top_narratives)
    
    # Generate reports
    generator = ReportGenerator()
    paths = generator.save_reports(top_narratives)
    
    print("\n=== REPORTS GENERATED ===")
    for format_type, path in paths.items():
        print(f"  {format_type}: {path}")
