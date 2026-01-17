# Dharma-Nīti  
### An Explainable Strategy for the Iterated Prisoner’s Dilemma

## Overview
**Dharma-Nīti** is a rule-based, fully explainable strategy for the **Iterated Prisoner’s Dilemma (IPD)**.  
It is designed to maximize **long-term payoff** by balancing **cooperation, proportional retaliation, noise tolerance, and conditional forgiveness**.

Instead of using black-box learning or reinforcement learning, the strategy leverages **ML-informed behavioral insights** to guide transparent decision rules.

---

## Core Idea
In repeated interactions, blind greed and blind forgiveness both fail.  
Dharma-Nīti follows the principle of *long-term rationality*:

- Start with cooperation to establish trust  
- Retaliate proportionally against betrayal  
- Tolerate occasional noise or accidental defections  
- Forgive only after sustained behavioral reform  
- Avoid permanent mutual defection loops  

This mirrors real-world strategic interactions where stability matters more than short-term gains.

---

## Strategy Characteristics

- **Explainable & Deterministic**  
  Every decision is driven by clear rules—no hidden learning or randomness.

- **ML-Informed, Not ML-Controlled**  
  Machine learning is used *offline* to analyze successful IPD strategies and derive thresholds (e.g., cooperation and betrayal rates).  
  Final gameplay decisions remain rule-based.

- **Robust to Noise**  
  Single or rare defections are treated as noise, preventing overreaction.

- **Resistant to Exploitation**  
  Persistent betrayal triggers escalating but finite retaliation.

- **Forgiving, Not Forgetful**  
  Trust is rebuilt only after sustained cooperative behavior.

---

## Behavioral Features Used
The strategy computes interpretable features aligned with standard IPD datasets:

- Overall opponent cooperation rate  
- Recent cooperation trend (rolling window)  
- Betrayal frequency (defection after cooperation)  
- Aggression persistence (defection streaks)  

These features guide decision thresholds in an explainable manner.

---

## Decision Logic (High Level)

1. Cooperate on the first move  
2. Continue any active proportional retaliation  
3. Forgive after sustained reform  
4. Respond to defection based on severity and history  
5. Reward cooperation and encourage stability  

---

## Implementation
- Language: **Python**
- Dependencies: **Python Standard Library only**
- Core class: `DharmaNitiStrategy`
- Key methods:
  - `decide_move()` – determines next action
  - `update_history()` – updates internal state
  - Feature computation & helper functions

---

## Evaluation
The strategy is designed to perform well in:
- Long tournaments (100–200 rounds)
- Matches against:
  - Always Cooperate
  - Always Defect
  - Tit-for-Tat–like strategies
  - Exploitative or noisy opponents

Performance is evaluated using:
- Average payoff per match  
- Stability of cooperation  
- Resistance to exploitation  

---

## Philosophy
Inspired by the concept of **Dharma-Nīti (righteous strategy)**:
> Strength without wisdom leads to ruin,  
> and wisdom without strength invites exploitation.

This strategy seeks the balance.

---

## License
This project is intended for academic, educational, and competitive use.

---

## Authors
Developed as part of **Turing’s Playground / Weekend of Code (WOC)**  
by a team exploring explainable and ethical decision-making in strategic AI.
