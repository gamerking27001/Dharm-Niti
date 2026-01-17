"""
Dharma-Nīti Strategy for Iterated Prisoner's Dilemma

This strategy follows long-term rational cooperation principles.
It begins with cooperation, retaliates proportionally against betrayal,
and gradually forgives when the opponent reforms.

Machine Learning is used only offline to justify thresholds and rules.
The final strategy is fully rule-based, deterministic, and explainable.
"""


class DharmaNitiStrategy:
    """
    A rule-based Iterated Prisoner's Dilemma strategy that balances:
    - Cooperation
    - Proportional retaliation
    - Controlled forgiveness

    The strategy is robust to noise and avoids permanent defection cycles.
    """

    def __init__(self):
        # === MOVE HISTORY ===
        self.opponent_history = []
        self.own_history = []

        # === BEHAVIOR TRACKING ===
        self.opponent_defections = 0
        self.betrayals = 0
        self.consecutive_defections = 0

        # === RETALIATION CONTROL ===
        self.retaliation_remaining = 0
        self.rounds_since_betrayal = 0

        # === ML-DERIVED THRESHOLDS (OFFLINE ANALYSIS) ===
        self.COOPERATIVE_THRESHOLD = 0.70     # Strong cooperation indicator
        self.BETRAYAL_THRESHOLD = 0.30        # Exploitative behavior indicator
        self.RECENT_WINDOW = 15               # Trend stability window
        self.NOISE_TOLERANCE = 2               # Allowed accidental defections
        self.FORGIVENESS_WINDOW = 5            # Required reform length


    def decide_move(self) -> str:
        """
        Decide the next move based on opponent behavior.
        Returns: "C" (Cooperate) or "D" (Defect)
        """

        # Rule 1: Start with cooperation
        if not self.opponent_history:
            return "C"

        features = self._compute_features()

        # Rule 2: Execute proportional retaliation if active
        if self.retaliation_remaining > 0:
            self.retaliation_remaining -= 1
            return "D"

        # Rule 3: Grant forgiveness if opponent reforms
        if self._should_forgive(features):
            self._reset_retaliation()
            return "C"

        # Rule 4: Respond to opponent defection
        if self.opponent_history[-1] == "D":
            return self._handle_defection(features)

        # Rule 5: Reward cooperation
        return self._handle_cooperation(features)


    def update_history(self, own_move: str, opponent_move: str):
        """Update internal state after each round."""

        self.own_history.append(own_move)
        self.opponent_history.append(opponent_move)

        if opponent_move == "D":
            self.opponent_defections += 1
            self.consecutive_defections += 1
            if own_move == "C":
                self.betrayals += 1
                self.rounds_since_betrayal = 0
        else:
            self.consecutive_defections = 0
            self.rounds_since_betrayal += 1


    def _compute_features(self) -> dict:
        """Compute interpretable opponent behavior metrics."""

        total = len(self.opponent_history)
        coop_count = self.opponent_history.count("C")

        overall_coop = coop_count / total
        recent = self.opponent_history[-min(self.RECENT_WINDOW, total):]
        recent_coop = recent.count("C") / len(recent)

        our_coop = self.own_history.count("C")
        betrayal_rate = self.betrayals / our_coop if our_coop else 0

        return {
            "overall_coop": overall_coop,
            "recent_coop": recent_coop,
            "betrayal_rate": betrayal_rate,
            "aggressive_streak": self.consecutive_defections >= 3,
            "total_rounds": total
        }


    def _handle_defection(self, features: dict) -> str:
        """
        Respond to opponent defection using proportional retaliation.
        """

        # Noise tolerance: ignore isolated mistakes by cooperative opponents
        if (
            features["overall_coop"] > self.COOPERATIVE_THRESHOLD
            and self.consecutive_defections == 1
            and self.opponent_defections <= self.NOISE_TOLERANCE
        ):
            return "C"

        # Single betrayal → Tit-for-Tat response
        if self.consecutive_defections == 1:
            self.retaliation_remaining = 1
            return "D"

        # Sustained aggression → escalated but limited retaliation
        if features["aggressive_streak"]:
            self.retaliation_remaining = min(3, self.consecutive_defections)
            return "D"

        # High betrayal frequency → defensive stance
        if features["betrayal_rate"] > self.BETRAYAL_THRESHOLD:
            self.retaliation_remaining = 2
            return "D"

        return "D"


    def _handle_cooperation(self, features: dict) -> str:
        """
        Respond to opponent cooperation.
        """

        # Reward strong cooperation
        if features["overall_coop"] > self.COOPERATIVE_THRESHOLD:
            return "C"

        # Reward improving behavior
        if features["recent_coop"] > 0.60:
            return "C"

        # Cautious testing against exploiters
        if features["betrayal_rate"] > self.BETRAYAL_THRESHOLD:
            return "C" if features["total_rounds"] % 3 == 0 else "D"

        return "C"


    def _should_forgive(self, features: dict) -> bool:
        """
        Check whether opponent has demonstrated sustained reform.
        """

        if features["total_rounds"] < self.FORGIVENESS_WINDOW:
            return False

        recent = self.opponent_history[-self.FORGIVENESS_WINDOW:]
        return (
            all(move == "C" for move in recent)
            and self.rounds_since_betrayal >= self.FORGIVENESS_WINDOW
            and features["recent_coop"] > 0.80
        )


    def _reset_retaliation(self):
        """Clear retaliation state after forgiveness."""
        self.retaliation_remaining = 0
        self.consecutive_defections = 0
