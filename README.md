#  Dharma-Nīti: The Righteous Strategy
### ⚖️ An Explainable Strategy for the Iterated Prisoner’s Dilemma

---

## 📜 Overview
**Dharma-Nīti** is a rule-based, fully explainable strategy for the **Iterated Prisoner’s Dilemma (IPD)**.  
It is designed to maximize **long-term payoff** by balancing **cooperation, proportional retaliation, noise tolerance, and conditional forgiveness**.

Instead of using black-box learning or reinforcement learning, the strategy leverages **ML-informed behavioral insights** to guide transparent decision rules.

> *"Strength without wisdom leads to ruin, and wisdom without strength invites exploitation."*

---

## ⚔️ Team: KODE KILLERS

**Members:**
- **Lavneesh** (Team Leader)
- **Deepanshu**
- **Malika**
- **Jatin**

---

## 💡 Core Idea
In repeated interactions, blind greed and blind forgiveness both fail.  
**Dharma-Nīti** follows the principle of *long-term rationality*:

- 🤝 **Start with Cooperation** to establish trust.
- ⚔️ **Retaliate Proportionally** against betrayal.
- 🛡️ **Tolerate Noise** (accidental defections).
- 🌱 **Forgive** only after sustained behavioral reform.
- 🛑 **Avoid Deadlocks** (permanent mutual defection loops).

This mirrors real-world strategic interactions where **stability** matters more than short-term gains.

---

## ✨ Strategy Characteristics

- **🔍 Explainable & Deterministic**  
  Every decision is driven by clear rules—no hidden learning or randomness.

- **🤖 ML-Informed, Not ML-Controlled**  
  Machine learning is used *offline* to analyze successful IPD strategies and derive thresholds (e.g., cooperation and betrayal rates). Final gameplay decisions remain rule-based.

- **🛡️ Robust to Noise**  
  Single or rare defections are treated as noise, preventing overreaction.

- **🛡️ Resistant to Exploitation**  
  Persistent betrayal triggers escalating but finite retaliation.

- **🌱 Forgiving, Not Forgetful**  
  Trust is rebuilt only after sustained cooperative behavior.

---

## 📊 Behavioral Features used in `feature_engineering.py`
The strategy computes interpretable features aligned with standard IPD datasets:

- **🔥 Provocability**: The probability of defecting when the opponent cooperates (Unprovoked aggression).
- **⚔️ Retaliation Rate**: The probability of defecting immediately after the opponent defects.
- **🌱 Forgiveness Rate**: The probability of returning to cooperation after a defecting state.
- **🤝 Cooperation Rate**: The overall frequency of cooperative moves.
- **🏁 First Move C**: The probability of cooperating on the very first move.

These features guide decision thresholds in an explainable manner.

---

## 🧠 Decision Logic (High Level) in `Krishna.py`

1.  **Trust**: Cooperate on the first move.
2.  **Justice**: Continue any active proportional retaliation.
3.  **Mercy**: Forgive after sustained reform.
4.  **Defense**: Respond to defection based on severity and history.
5.  **Reciprocity**: Reward cooperation and encourage stability.

---



## 💻 Implementation Details
- **Language**: Python 🐍
- **Dependencies**: Standard Library + Pandas/NumPy for analysis.
- **Core Class**: `DharmaNitiStrategy`
- **Key Methods**:
  - `decide_move()` – determines next action.
  - `update_history()` – updates internal state.

---

## 🏆 Evaluation Goals
The strategy is designed to excel in:
- Long tournaments (100–200 rounds).
- Matches against diverse opponents (Friendly, Hostile, Random).
- High-noise environments.

**Key Metrics:**
- Average payoff per match.
- Stability of cooperation.
- Resistance to exploitation.

---

## License
This project is intended for **academic, educational, and competitive use**.

---

## Authors
Developed as part of **Turing’s Playground / Weekend of Code (WOC)**  
by a team exploring explainable and ethical decision-making in strategic AI.
