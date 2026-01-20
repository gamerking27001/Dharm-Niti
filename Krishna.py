#Dharma-Nīti Strategy for Iterated Prisoners Dilemma

#A fully rule-based, deterministic, and explainable strategy.
#Machine Learning is used only offline to justify thresholds.

#Core principles:Trust first,Punish betrayal proportionally,Forgive genuine reform,Avoid endless retaliation
class DharmaNitiStrategy:
    def __init__(self):
        #History
        self.own_history = []
        self.opponent_history = []
        #State Tracking
        self.total_rounds = 0
        self.consecutive_opponent_defections = 0
        self.betrayals = 0
        self.rounds_since_last_betrayal = 0
         #Retaliation  Control
        self.retaliation_remaining = 0
        self.in_retaliation_phase = False
        #Ml justified (offline)
        self.COOPERATIVE_THRESHOLD = 0.70
        self.BETRAYAL_RATE_THRESHOLD = 0.30
        self.RECENT_WINDOW = 15
        self.NOISE_TOLERANCE = 1
        self.FORGIVENESS_WINDOW = 5
        self.MIN_ROUNDS_FOR_JUDGMENT = 10
 #Main decision function
    def decide_move(self) -> str:
        #Rule 1:Start with cooperation
        if self.total_rounds == 0:
            return "C"
        features = self._compute_features()
        #Rule 2: Execute retaliation if active
        if self.retaliation_remaining > 0:
            self.retaliation_remaining -= 1
            #Auto-exit retaliation phase cleanly
            if self.retaliation_remaining == 0:
                self.in_retaliation_phase = False
            return "D"
        #Rule 3: Forgive if opponent has genuinely reformed
        if self._should_forgive(features):
            self._reset_retaliation_state()
            return "C"
        #Rule 4: Respond to opponent's last move
        if self.opponent_history[-1] == "D":
            return self._handle_defection(features)
        #Rule 5: Reward cooperation
        return self._handle_cooperation(features)
    #Update state after each round
    def update_history(self, own_move: str, opponent_move: str):
        self.own_history.append(own_move)
        self.opponent_history.append(opponent_move)
        self.total_rounds += 1
        if opponent_move == "D":
            self.consecutive_opponent_defections += 1
            #Betrayal = opponent defects while we cooperate
            if own_move == "C":
                self.betrayals += 1
                self.rounds_since_last_betrayal = 0
        else:
            self.consecutive_opponent_defections = 0
            self.rounds_since_last_betrayal += 1
    #Feature computation
    def _compute_features(self) -> dict:
        total = self.total_rounds
        coop_count = self.opponent_history.count("C")
        overall_coop = coop_count / total
        recent_slice = self.opponent_history[-min(self.RECENT_WINDOW, total):]
        recent_coop = recent_slice.count("C") / len(recent_slice)
        own_coop = self.own_history.count("C")
        betrayal_rate = (
            self.betrayals / own_coop
            if own_coop >= self.MIN_ROUNDS_FOR_JUDGMENT
            else 0.0
        )
        return {
            "overall_coop": overall_coop,
            "recent_coop": recent_coop,
            "betrayal_rate": betrayal_rate,
            "aggressive_streak": self.consecutive_opponent_defections >= 2,
            "total_rounds": total
        }
    #Deflection handling
    def _handle_defection(self, features: dict) -> str:
        #Noise tolerance: forgive one accidental defection
        if (
            features["overall_coop"] > self.COOPERATIVE_THRESHOLD
            and self.consecutive_opponent_defections <= self.NOISE_TOLERANCE
        ):
            return "C"
        #First clear betrayal → single retaliation
        if self.consecutive_opponent_defections == 1:
            self._start_retaliation(1)
            return "D"
        #Sustained aggression → bounded retaliation
        if features["aggressive_streak"]:
            self._start_retaliation(min(2, self.consecutive_opponent_defections))
            return "D"
        #High betrayal frequency → defensive posture
        if features["betrayal_rate"] > self.BETRAYAL_RATE_THRESHOLD:
            self._start_retaliation(2)
            return "D"

        return "D"
    #Cooperation handling
    def _handle_cooperation(self, features: dict) -> str:
        # Strong cooperative opponent
        if features["overall_coop"] > self.COOPERATIVE_THRESHOLD:
            return "C"
        # Improving behavior
        if features["recent_coop"] > 0.60:
            return "C"
        # Cautious probing against exploiters
        if features["betrayal_rate"] > self.BETRAYAL_RATE_THRESHOLD:
            return "C" if self.total_rounds % 4 == 0 else "D"
        return "C"
    #Forgiveness logic
    def _should_forgive(self, features: dict) -> bool:
        if features["total_rounds"] < self.MIN_ROUNDS_FOR_JUDGMENT:
            return False
        recent_moves = self.opponent_history[-self.FORGIVENESS_WINDOW:]
        return (
            all(move == "C" for move in recent_moves)
            and self.rounds_since_last_betrayal >= self.FORGIVENESS_WINDOW
            and features["recent_coop"] > 0.80
        )
    #Retailation Control
    def _start_retaliation(self, length: int):
        if not self.in_retaliation_phase:
            self.retaliation_remaining = length
            self.in_retaliation_phase = True
    def _reset_retaliation_state(self):
        self.retaliation_remaining = 0
        self.in_retaliation_phase = False
        self.consecutive_opponent_defections = 0
