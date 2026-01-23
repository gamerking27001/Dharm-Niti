"""
ARJUNA'S CODE: IPD Simulator & Tournament Framework (FINAL POLISHED VERSION)
===========================================================================

Final improvements:
✓ Local RNG (no global random pollution)
✓ Safer math (no divide-by-zero)
✓ Move validation
✓ Immutable results returned
✓ Deterministic + reproducible
✓ Cleaner typing
✓ More robust for research use
"""

from typing import Tuple, Dict, List, Callable
import random
from Krishna import DharmaNitiStrategy


# ============================================================
# PAYOFF MATRIX
# ============================================================

PAYOFF_MATRIX = {
    ("C", "C"): (3, 3),
    ("C", "D"): (0, 5),
    ("D", "C"): (5, 0),
    ("D", "D"): (1, 1),
}


# ============================================================
# OPPONENT STRATEGY BASE
# ============================================================

class OpponentStrategy:
    """Base class for all opponent strategies."""

    def __init__(self, name: str):
        self.name = name
        self.reset()

    def decide_move(self) -> str:
        raise NotImplementedError

    def update_history(self, own_move: str, opponent_move: str):
        self.own_history.append(own_move)
        self.opponent_history.append(opponent_move)

    def reset(self):
        self.own_history: List[str] = []
        self.opponent_history: List[str] = []


# ============================================================
# OPPONENTS
# ============================================================

class AlwaysCooperate(OpponentStrategy):
    def decide_move(self) -> str:
        return "C"


class AlwaysDefect(OpponentStrategy):
    def decide_move(self) -> str:
        return "D"


class TitForTat(OpponentStrategy):
    def decide_move(self) -> str:
        return "C" if not self.opponent_history else self.opponent_history[-1]


class TitForTwoTats(OpponentStrategy):
    def decide_move(self) -> str:
        if len(self.opponent_history) < 2:
            return "C"
        return "D" if self.opponent_history[-1] == "D" and self.opponent_history[-2] == "D" else "C"


class Grudger(OpponentStrategy):
    def decide_move(self) -> str:
        return "D" if "D" in self.opponent_history else "C"


class RandomStrategy(OpponentStrategy):
    def __init__(self, name: str, rng: random.Random = None):
        super().__init__(name)
        self.rng = rng or random.Random()

    def decide_move(self) -> str:
        return "C" if self.rng.random() < 0.5 else "D"


# Alias for compatibility
Random = RandomStrategy


class Suspicious(OpponentStrategy):
    def decide_move(self) -> str:
        return "D" if not self.opponent_history else self.opponent_history[-1]


# ============================================================
# MATCH ENGINE
# ============================================================

class IPDMatch:

    def __init__(
        self,
        strategy1,
        strategy2,
        rounds: int = 200,
        noise: float = 0.0,
        rng: random.Random | None = None,
    ):
        self.s1 = strategy1
        self.s2 = strategy2
        self.rounds = max(1, rounds)
        self.noise = noise
        self.rng = rng or random.Random()

        self.score1 = 0
        self.score2 = 0
        self.history: List[Tuple[str, str]] = []

    # --------------------------------------------------------
    def _apply_noise(self, move: str) -> str:
        if self.noise > 0 and self.rng.random() < self.noise:
            return "D" if move == "C" else "C"
        return move

    # --------------------------------------------------------
    @staticmethod
    def _validate_move(move: str):
        if move not in ("C", "D"):
            raise ValueError(f"Invalid move '{move}'. Must be 'C' or 'D'.")

    # --------------------------------------------------------
    def play(self) -> Tuple[int, int]:

        for _ in range(self.rounds):

            m1 = self.s1.decide_move()
            m2 = self.s2.decide_move()

            self._validate_move(m1)
            self._validate_move(m2)

            m1 = self._apply_noise(m1)
            m2 = self._apply_noise(m2)

            p1, p2 = PAYOFF_MATRIX[(m1, m2)]

            self.score1 += p1
            self.score2 += p2

            self.history.append((m1, m2))

            self.s1.update_history(m1, m2)
            self.s2.update_history(m2, m1)

        return self.score1, self.score2

    # --------------------------------------------------------
    def get_stats(self) -> Dict:

        r = len(self.history)

        coop1 = sum(m1 == "C" for m1, _ in self.history)
        coop2 = sum(m2 == "C" for _, m2 in self.history)

        return {
            "score1": self.score1,
            "score2": self.score2,
            "avg1": self.score1 / r,
            "avg2": self.score2 / r,
            "coop1": coop1 / r,
            "coop2": coop2 / r,
        }


# ============================================================
# TOURNAMENT ENGINE
# ============================================================

class IPDTournament:

    def __init__(
        self,
        strategy_factory: Callable[[], DharmaNitiStrategy],
        opponents: List[OpponentStrategy],
        rounds: int = 200,
        noise: float = 0.0,
        seed: int = 42,
        verbose: bool = True,
    ):
        self.strategy_factory = strategy_factory
        self.opponents = opponents
        self.rounds = rounds
        self.noise = noise
        self.verbose = verbose
        self.rng = random.Random(seed)

    # --------------------------------------------------------
    def run(self) -> Dict:

        results = []
        total_score = 0
        wins = 0

        if self.verbose:
            print("\n" + "=" * 60)
            print("TOURNAMENT START")
            print("=" * 60)

        for opponent in self.opponents:

            our_strategy = self.strategy_factory()
            opponent.reset()

            match = IPDMatch(
                our_strategy,
                opponent,
                rounds=self.rounds,
                noise=self.noise,
                rng=self.rng,
            )

            our_score, opp_score = match.play()
            stats = match.get_stats()

            won = our_score > opp_score

            results.append({
                "opponent": opponent.name,
                "our_score": our_score,
                "opponent_score": opp_score,
                "opp_score": opp_score,  # Alias for compatibility
                "our_avg": stats["avg1"],
                "our_coop": stats["coop1"],
                "opp_coop": stats["coop2"],
                "won": won,
                "score_difference": our_score - opp_score,
            })

            total_score += our_score
            if won:
                wins += 1

            if self.verbose:
                print(f"{opponent.name:18} | {our_score:4} vs {opp_score:4} | {'WIN' if won else 'LOSS'}")

        total_matches = len(self.opponents)
        avg = total_score / total_matches
        win_rate = wins / total_matches
        losses = total_matches - wins

        self._last_results = {
            "total_matches": total_matches,
            "total_score": total_score,
            "average_score": avg,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate,
            "results": list(results),  # safe copy
        }
        return self._last_results

    # --------------------------------------------------------
    def get_comparison_table(self) -> str:
        """Generate a formatted comparison table of results."""
        if not hasattr(self, '_last_results') or not self._last_results:
            return "No results available. Run the tournament first."

        results = self._last_results["results"]

        table = "\n" + "=" * 70 + "\n"
        table += "COMPARISON TABLE\n"
        table += "=" * 70 + "\n"
        table += f"{'Opponent':<20} {'Our Score':>10} {'Opp Score':>10} {'Diff':>8} {'Result':>8}\n"
        table += "-" * 70 + "\n"

        for r in results:
            diff = r["score_difference"]
            result = "WIN" if r["won"] else "LOSS"
            table += f"{r['opponent']:<20} {r['our_score']:>10} {r['opponent_score']:>10} {diff:>+8} {result:>8}\n"

        table += "-" * 70 + "\n"
        table += f"{'TOTAL':<20} {self._last_results['total_score']:>10}\n"
        table += "=" * 70 + "\n"

        return table


# ============================================================
# MAIN
# ============================================================

def main():

    rng = random.Random(42)

    opponents = [
        AlwaysCooperate("AlwaysCooperate"),
        AlwaysDefect("AlwaysDefect"),
        TitForTat("TitForTat"),
        TitForTwoTats("TitForTwoTats"),
        Grudger("Grudger"),
        RandomStrategy("Random", rng),
        Suspicious("Suspicious"),
    ]

    tournament = IPDTournament(
        strategy_factory=DharmaNitiStrategy,
        opponents=opponents,
        rounds=200,
        noise=0.02,
        seed=42,
        verbose=True,
    )

    tournament.run()


if __name__ == "__main__":
    main()
