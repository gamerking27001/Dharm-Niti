"""
ARJUNA'S CODE: IPD Simulator & Tournament Framework
====================================================

Responsibility: Tournament & Validation (Arjuna role)

Tasks:
- Implement IPD simulator
- Simulate 200-round matches
- Your strategy vs known strategies
- Track average payoff, total reward, win rate

Deliverables:
- Tournament results
- Comparison tables
- Graphs
"""

import random
from typing import Tuple, Dict, List
from Krishna import DharmaNitiStrategy


# ============================================================
# PAYOFF MATRIX (Prisoner's Dilemma)
# ============================================================

PAYOFF_MATRIX = {
    ("C", "C"): (3, 3),      # Both cooperate → mutual reward
    ("C", "D"): (0, 5),      # I cooperate, opponent defects → I lose, they gain
    ("D", "C"): (5, 0),      # I defect, opponent cooperates → I gain, they lose
    ("D", "D"): (1, 1),      # Both defect → mutual punishment
}


# ============================================================
# OPPONENT STRATEGIES
# ============================================================

class OpponentStrategy:
    """Base class for opponent strategies."""
    
    def __init__(self, name: str):
        self.name = name
        self.opponent_history = []
        self.own_history = []
    
    def decide_move(self) -> str:
        """Return 'C' or 'D'."""
        raise NotImplementedError
    
    def update_history(self, own_move: str, opponent_move: str):
        """Track moves for history-based decisions."""
        self.own_history.append(own_move)
        self.opponent_history.append(opponent_move)
    
    def reset(self):
        """Reset for new tournament."""
        self.opponent_history = []
        self.own_history = []


class AlwaysCooperate(OpponentStrategy):
    """Naive cooperator - always cooperates."""
    def decide_move(self) -> str:
        return "C"


class AlwaysDefect(OpponentStrategy):
    """Pure defector - always defects."""
    def decide_move(self) -> str:
        return "D"


class TitForTat(OpponentStrategy):
    """Classic Tit-for-Tat: copy opponent's last move."""
    def decide_move(self) -> str:
        if not self.opponent_history:
            return "C"  # Start with cooperation
        return self.opponent_history[-1]


class TitForTwoTats(OpponentStrategy):
    """Forgiving variant: defect only if opponent defects twice in a row."""
    def decide_move(self) -> str:
        if len(self.opponent_history) < 2:
            return "C"
        # Defect only if opponent defected last 2 rounds
        if self.opponent_history[-1] == "D" and self.opponent_history[-2] == "D":
            return "D"
        return "C"


class Grudger(OpponentStrategy):
    """Never forgets: cooperate until first defection, then always defect."""
    def decide_move(self) -> str:
        if "D" in self.opponent_history:
            return "D"  # Permanent defection after any betrayal
        return "C"


class Random(OpponentStrategy):
    """Random 50/50 strategy."""
    def decide_move(self) -> str:
        return "C" if random.random() < 0.5 else "D"


class Suspicious(OpponentStrategy):
    """Starts with defection, then mirrors opponent."""
    def decide_move(self) -> str:
        if not self.opponent_history:
            return "D"  # Start with suspicion
        return self.opponent_history[-1]


# ============================================================
# IPD MATCH ENGINE
# ============================================================

class IPDMatch:
    """Single match between two strategies."""
    
    def __init__(self, strategy1, strategy2, rounds: int = 200):
        self.strategy1 = strategy1
        self.strategy2 = strategy2
        self.rounds = rounds
        self.score1 = 0
        self.score2 = 0
        self.history = []
    
    def play(self) -> Tuple[int, int]:
        """
        Play the match for specified rounds.
        Returns: (strategy1_score, strategy2_score)
        """
        for _ in range(self.rounds):
            move1 = self.strategy1.decide_move()
            move2 = self.strategy2.decide_move()
            
            payoff1, payoff2 = PAYOFF_MATRIX[(move1, move2)]
            self.score1 += payoff1
            self.score2 += payoff2
            
            self.history.append((move1, move2))
            
            self.strategy1.update_history(move1, move2)
            self.strategy2.update_history(move2, move1)
        
        return self.score1, self.score2
    
    def get_stats(self) -> Dict:
        """Return match statistics."""
        coop1 = sum(1 for m1, m2 in self.history if m1 == "C")
        coop2 = sum(1 for m1, m2 in self.history if m2 == "C")
        
        return {
            "score1": self.score1,
            "score2": self.score2,
            "avg_score1": self.score1 / self.rounds,
            "avg_score2": self.score2 / self.rounds,
            "cooperation_rate1": coop1 / self.rounds,
            "cooperation_rate2": coop2 / self.rounds,
            "rounds": self.rounds,
        }


# ============================================================
# TOURNAMENT ENGINE
# ============================================================

class IPDTournament:
    """Multi-match tournament framework."""
    
    def __init__(self, our_strategy, opponents: List[OpponentStrategy], rounds: int = 200):
        self.our_strategy = our_strategy
        self.opponents = opponents
        self.rounds = rounds
        self.results = []
    
    def run(self) -> Dict:
        """Run full tournament against all opponents."""
        print(f"\n{'='*70}")
        print(f"TOURNAMENT: {self.our_strategy.name if hasattr(self.our_strategy, 'name') else 'Dharma-Nīti'}")
        print(f"{'='*70}")
        print(f"Rounds per match: {self.rounds}")
        print(f"Number of opponents: {len(self.opponents)}\n")
        
        total_score = 0
        wins = 0
        
        for opponent in self.opponents:
            # Reset both strategies
            self.our_strategy = DharmaNitiStrategy()
            opponent.reset()
            
            # Play match
            match = IPDMatch(self.our_strategy, opponent, self.rounds)
            our_score, opp_score = match.play()
            stats = match.get_stats()
            
            # Record result
            result = {
                "opponent": opponent.name,
                "our_score": our_score,
                "opponent_score": opp_score,
                "our_avg": stats["avg_score1"],
                "opponent_avg": stats["avg_score2"],
                "our_coop": stats["cooperation_rate1"],
                "opponent_coop": stats["cooperation_rate2"],
                "won": our_score > opp_score,
            }
            self.results.append(result)
            
            total_score += our_score
            if result["won"]:
                wins += 1
            
            # Print match result
            status = "✓ WIN" if result["won"] else "✗ LOSS" if result["won"] == False else "= TIE"
            print(f"{opponent.name:20} | Score: {our_score:3} vs {opp_score:3} ({status})")
            print(f"  → Our cooperation: {stats['cooperation_rate1']:.1%} | Opponent: {stats['cooperation_rate2']:.1%}")
        
        # Tournament summary
        return self._generate_summary(total_score, wins)
    
    def _generate_summary(self, total_score: int, wins: int) -> Dict:
        """Generate tournament summary statistics."""
        avg_score = total_score / len(self.opponents)
        win_rate = wins / len(self.opponents)
        
        summary = {
            "total_matches": len(self.opponents),
            "total_score": total_score,
            "average_score": avg_score,
            "wins": wins,
            "losses": len(self.opponents) - wins,
            "win_rate": win_rate,
            "results": self.results,
        }
        
        print(f"\n{'-'*70}")
        print(f"TOURNAMENT SUMMARY")
        print(f"{'-'*70}")
        print(f"Total Score: {total_score}")
        print(f"Average Score per Match: {avg_score:.2f}")
        print(f"Wins: {wins}/{len(self.opponents)} ({win_rate:.1%})")
        print(f"{'='*70}\n")
        
        return summary
    
    def get_comparison_table(self) -> str:
        """Generate formatted comparison table."""
        table = "\n" + "="*90 + "\n"
        table += f"{'Opponent':<20} | {'Our Score':>8} | {'Their Score':>8} | {'Our Coop':>10} | {'Result':>8}\n"
        table += "-"*90 + "\n"
        
        for result in self.results:
            status = "WIN ✓" if result["won"] else "LOSS ✗"
            table += f"{result['opponent']:<20} | {result['our_score']:>8} | {result['opponent_score']:>8} | {result['our_coop']:>9.1%} | {status:>8}\n"
        
        table += "="*90 + "\n"
        return table


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    """Run the complete tournament."""
    
    # Create opponents
    opponents = [
        AlwaysCooperate("AlwaysCooperate"),
        AlwaysDefect("AlwaysDefect"),
        TitForTat("TitForTat"),
        TitForTwoTats("TitForTwoTats"),
        Grudger("Grudger"),
        Random("Random"),
        Suspicious("Suspicious"),
    ]
    
    # Create Dharma-Nīti strategy
    dharma_niti = DharmaNitiStrategy()
    
    # Run tournament
    tournament = IPDTournament(dharma_niti, opponents, rounds=200)
    summary = tournament.run()
    
    # Print comparison table
    print(tournament.get_comparison_table())
    
    # Return results for visualization
    return summary


if __name__ == "__main__":
    main()
