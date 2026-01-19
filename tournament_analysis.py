"""
ARJUNA'S ANALYSIS MODULE: Detailed Results & Metrics
=====================================================

Generate comparison tables, graphs data, and deep analysis
of Dharma-Nīti strategy performance.
"""

import json
from typing import Dict, List
from datetime import datetime


class TournamentAnalyzer:
    """Analyze and visualize tournament results."""
    
    def __init__(self, tournament_summary: Dict):
        self.summary = tournament_summary
        self.results = tournament_summary["results"]
    
    def get_performance_metrics(self) -> Dict:
        """Extract key performance indicators."""
        return {
            "total_matches": self.summary["total_matches"],
            "total_score": self.summary["total_score"],
            "average_score": round(self.summary["average_score"], 2),
            "wins": self.summary["wins"],
            "losses": self.summary["losses"],
            "win_rate": round(self.summary["win_rate"], 3),
        }
    
    def get_opponent_breakdown(self) -> List[Dict]:
        """Detailed breakdown per opponent."""
        breakdown = []
        for result in self.results:
            breakdown.append({
                "opponent": result["opponent"],
                "our_score": result["our_score"],
                "opponent_score": result["opponent_score"],
                "score_difference": result["our_score"] - result["opponent_score"],
                "our_avg_per_round": round(result["our_avg"], 2),
                "cooperation_rate": round(result["our_coop"], 3),
                "outcome": "WIN" if result["won"] else "LOSS",
            })
        return breakdown
    
    def rank_opponents_by_difficulty(self) -> List[Dict]:
        """Rank opponents from hardest to easiest."""
        ranked = sorted(
            self.results,
            key=lambda x: x["score_difference"]
        )
        return [
            {
                "rank": i + 1,
                "opponent": r["opponent"],
                "difficulty": "Hard" if r["score_difference"] < 0 else "Medium" if r["score_difference"] < 100 else "Easy",
                "score_gap": r["score_difference"],
            }
            for i, r in enumerate(ranked)
        ]
    
    def get_strategy_classification(self) -> Dict:
        """Classify how our strategy behaves against different opponent types."""
        classifications = {
            "vs_cooperators": [],
            "vs_defectors": [],
            "vs_adapters": [],
        }
        
        for result in self.results:
            opp_name = result["opponent"]
            
            if "Cooperate" in opp_name:
                classifications["vs_cooperators"].append(result)
            elif "Defect" in opp_name or "Grudger" in opp_name:
                classifications["vs_defectors"].append(result)
            else:
                classifications["vs_adapters"].append(result)
        
        return {
            "vs_pure_cooperators": self._compute_category_stats(classifications["vs_cooperators"]),
            "vs_pure_defectors": self._compute_category_stats(classifications["vs_defectors"]),
            "vs_adaptive_strategies": self._compute_category_stats(classifications["vs_adapters"]),
        }
    
    def _compute_category_stats(self, results: List[Dict]) -> Dict:
        """Compute stats for a category of results."""
        if not results:
            return {"avg_score": 0, "win_rate": 0, "cooperation_rate": 0}
        
        total_score = sum(r["our_score"] for r in results)
        wins = sum(1 for r in results if r["won"])
        avg_coop = sum(r["our_coop"] for r in results) / len(results)
        
        return {
            "avg_score": round(total_score / len(results), 2),
            "win_rate": round(wins / len(results), 3),
            "cooperation_rate": round(avg_coop, 3),
            "matches_played": len(results),
        }
    
    def generate_report(self) -> str:
        """Generate human-readable tournament report."""
        metrics = self.get_performance_metrics()
        breakdown = self.get_opponent_breakdown()
        classification = self.get_strategy_classification()
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════╗
║           DHARMA-NĪTI STRATEGY: TOURNAMENT REPORT                   ║
║                    VALIDATION BY ARJUNA                             ║
╚══════════════════════════════════════════════════════════════════════╝

📊 OVERALL PERFORMANCE
─────────────────────────────────────────────────────────────────────
  Total Matches:         {metrics['total_matches']}
  Total Score:           {metrics['total_score']}
  Average Score/Match:   {metrics['average_score']}
  Wins:                  {metrics['wins']} / {metrics['total_matches']}
  Win Rate:              {metrics['win_rate']:.1%}

🎯 STRATEGY CLASSIFICATION
─────────────────────────────────────────────────────────────────────
vs Pure Cooperators:
  • Avg Score:           {classification['vs_pure_cooperators']['avg_score']}
  • Cooperation Rate:    {classification['vs_pure_cooperators']['cooperation_rate']:.1%}
  • Win Rate:            {classification['vs_pure_cooperators']['win_rate']:.1%}

vs Pure Defectors:
  • Avg Score:           {classification['vs_pure_defectors']['avg_score']}
  • Cooperation Rate:    {classification['vs_pure_defectors']['cooperation_rate']:.1%}
  • Win Rate:            {classification['vs_pure_defectors']['win_rate']:.1%}

vs Adaptive Strategies:
  • Avg Score:           {classification['vs_adaptive_strategies']['avg_score']}
  • Cooperation Rate:    {classification['vs_adaptive_strategies']['cooperation_rate']:.1%}
  • Win Rate:            {classification['vs_adaptive_strategies']['win_rate']:.1%}

📈 OPPONENT-BY-OPPONENT BREAKDOWN
─────────────────────────────────────────────────────────────────────
"""
        for opp in breakdown:
            report += f"""
{opp['opponent']}:
  Score: {opp['our_score']} vs {opp['opponent_score']} ({opp['outcome']})
  Cooperation: {opp['cooperation_rate']:.1%}
  Avg per Round: {opp['our_avg_per_round']}
"""
        
        report += "\n" + "="*70 + "\n"
        return report
    
    def export_json(self, filename: str = "tournament_results.json"):
        """Export results to JSON."""
        data = {
            "timestamp": datetime.now().isoformat(),
            "summary": self.summary,
            "metrics": self.get_performance_metrics(),
            "opponent_breakdown": self.get_opponent_breakdown(),
            "difficulty_ranking": self.rank_opponents_by_difficulty(),
            "strategy_classification": self.get_strategy_classification(),
        }
        
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Results exported to {filename}")
        return data


def create_chart_data(tournament_summary: Dict) -> Dict:
    """Prepare data for visualization/charting."""
    results = tournament_summary["results"]
    
    # Data for different chart types
    chart_data = {
        "bar_chart": {
            "labels": [r["opponent"] for r in results],
            "our_scores": [r["our_score"] for r in results],
            "opponent_scores": [r["opponent_score"] for r in results],
        },
        "cooperation_chart": {
            "labels": [r["opponent"] for r in results],
            "cooperation_rates": [r["our_coop"] for r in results],
        },
        "win_loss_chart": {
            "labels": [r["opponent"] for r in results],
            "outcomes": ["WIN" if r["won"] else "LOSS" for r in results],
        },
        "summary_metrics": {
            "total_score": tournament_summary["total_score"],
            "average_score": tournament_summary["average_score"],
            "win_rate": tournament_summary["win_rate"],
        }
    }
    
    return chart_data


if __name__ == "__main__":
    # Example usage - will be called from simulator
    pass
