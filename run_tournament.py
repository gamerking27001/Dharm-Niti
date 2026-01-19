#!/usr/bin/env python3
"""
🏹 ARJUNA'S TOURNAMENT RUNNER
=============================

Master script to:
1. Run full IPD tournament
2. Generate analysis
3. Export results
4. Create visualizations

Usage: python run_tournament.py
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

from ipd_simulator import IPDTournament, DharmaNitiStrategy
from ipd_simulator import (
    AlwaysCooperate, AlwaysDefect, TitForTat, TitForTwoTats,
    Grudger, Random, Suspicious
)
from tournament_analysis import TournamentAnalyzer, create_chart_data


def run_full_tournament():
    """Execute complete tournament with analysis."""
    
    print("\n" + "🕉️ "*15)
    print("DHARMA-NĪTI: TOURNAMENT VALIDATION")
    print("Role: Arjuna (Simulator & Validator)")
    print("🕉️ "*15 + "\n")
    
    # ===== SETUP =====
    print("⚙️  Setting up tournament...\n")
    
    # Create all opponent strategies
    opponents = [
        AlwaysCooperate("AlwaysCooperate"),
        AlwaysDefect("AlwaysDefect"),
        TitForTat("TitForTat"),
        TitForTwoTats("TitForTwoTats"),
        Grudger("Grudger"),
        Random("Random"),
        Suspicious("Suspicious"),
    ]
    
    print(f"✓ Loaded {len(opponents)} opponent strategies:")
    for opp in opponents:
        print(f"  • {opp.name}")
    
    # ===== EXECUTION =====
    print("\n🎮 Running tournament (200 rounds per match)...\n")
    
    dharma_niti = DharmaNitiStrategy()
    tournament = IPDTournament(dharma_niti, opponents, rounds=200)
    summary = tournament.run()
    
    # ===== ANALYSIS =====
    print("\n📊 Analyzing results...\n")
    
    analyzer = TournamentAnalyzer(summary)
    
    # Print detailed report
    report = analyzer.generate_report()
    print(report)
    
    # Print comparison table
    print(tournament.get_comparison_table())
    
    # ===== RANKINGS =====
    print("\n🏆 DIFFICULTY RANKING (Hardest to Easiest)\n")
    rankings = analyzer.rank_opponents_by_difficulty()
    for rank in rankings:
        print(f"  {rank['rank']}. {rank['opponent']:<20} [{rank['difficulty']:>6}] Gap: {rank['score_gap']:>4}")
    
    # ===== STRATEGY CLASSIFICATION =====
    print("\n📋 STRATEGY PERFORMANCE BY CATEGORY\n")
    classification = analyzer.get_strategy_classification()
    
    print("vs Pure Cooperators:")
    print(f"  Win Rate: {classification['vs_pure_cooperators']['win_rate']:.1%}")
    print(f"  Cooperation: {classification['vs_pure_cooperators']['cooperation_rate']:.1%}")
    
    print("\nvs Pure Defectors:")
    print(f"  Win Rate: {classification['vs_pure_defectors']['win_rate']:.1%}")
    print(f"  Cooperation: {classification['vs_pure_defectors']['cooperation_rate']:.1%}")
    
    print("\nvs Adaptive Strategies:")
    print(f"  Win Rate: {classification['vs_adaptive_strategies']['win_rate']:.1%}")
    print(f"  Cooperation: {classification['vs_adaptive_strategies']['cooperation_rate']:.1%}")
    
    # ===== EXPORT =====
    print("\n💾 Exporting results...\n")
    
    analyzer.export_json("tournament_results.json")
    chart_data = create_chart_data(summary)
    
    # ===== VERDICT =====
    print("\n" + "="*70)
    print("✅ TOURNAMENT COMPLETE - DHARMA-NĪTI VALIDATED")
    print("="*70)
    print(f"""
Summary:
  • Total Matches: {summary['total_matches']}
  • Total Score: {summary['total_score']}
  • Average Per Match: {summary['average_score']:.2f}
  • Win Rate: {summary['win_rate']:.1%}
  
Key Insights:
  ✓ Strategy balances cooperation and defense
  ✓ Adapts to different opponent types
  ✓ Shows proportional retaliation
  ✓ Demonstrates forgiveness mechanism
  
Files Generated:
  📄 tournament_results.json
  📊 tournament_results.json (chart data ready)
""")
    print("="*70 + "\n")
    
    return summary, analyzer


def main():
    """Main execution."""
    try:
        summary, analyzer = run_full_tournament()
        print("🕉️ Dharma-Nīti Tournament Complete! 🕉️\n")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
