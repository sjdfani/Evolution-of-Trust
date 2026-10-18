# Evolution of Trust

A terminal-based simulation of the iterated **Prisoner's Dilemma**, inspired by Nicky Case's interactive explainer [The Evolution of Trust](https://ncase.me/trust/).

Characters with different strategies play repeated rounds against each other, earn points according to a configurable payoff matrix, and — in the multiplayer tournament — the weakest players are replaced by copies of the strongest. Over time you can watch which strategies survive and how trust evolves in a population.

## Features

- **1 vs 1 match** — pick any two characters and watch them play round by round.
- **Multiplayer tournament** — a whole population plays a round-robin each round; the lowest scorers are eliminated and replaced by copies of the top scorers.
- **Manual or automatic population** — choose how many of each character to include, or split the population evenly.
- **Configurable payoffs and rules** — change the payoff matrix, number of rounds, population size and how many players are replaced each round, or reset them to the defaults.
- **Plots** — visualize score over time (1 vs 1), and population count and total score per character over rounds (multiplayer) with Matplotlib.

## Characters

| Character | Strategy |
| --- | --- |
| **Cooperator** | Always cooperates. |
| **Cheater** | Always cheats. |
| **Copycat** | Starts by cooperating, then copies whatever the opponent did in the previous round. |
| **Grudger** | Starts by cooperating and keeps cooperating until the opponent cheats even once; after that it always cheats. |
| **Detective** | Opens with Cooperate, Cheat, Cooperate, Cooperate. If the opponent ever cheated back, it plays like a Copycat; otherwise it plays like a Cheater. |
| **CopyKitten** \* | Starts by cooperating and only retaliates with a cheat after being cheated twice. |
| **Simpleton** \* | Starts by cooperating. If the opponent cooperated last round it repeats its last move; if the opponent cheated, it switches. |
| **Random** \* | Cooperates or cheats with a 50/50 chance. |

\* These characters are disabled by default. Set `IS_RANDOM_NESS = True` in [`src/constants.py`](src/constants.py) to include them.

## Default Settings

### Payoff matrix

Each cell shows `(player 1 score, player 2 score)`:

| | Opponent cooperates | Opponent cheats |
| --- | --- | --- |
| **You cooperate** | `(+2, +2)` | `(-1, +3)` |
| **You cheat** | `(+3, -1)` | `(0, 0)` |

### Rules

| Rule | Default |
| --- | --- |
| Rounds | `10` |
| Population size | `25` |
| Players replaced per round (remove tail players) | `5` |
| Starting score of each character | `20` |

All defaults live in [`src/constants.py`](src/constants.py). Payoffs and rules can also be changed at runtime from the menu.

## Requirements

- Python 3.9 or newer
- A macOS or Linux terminal (the menu uses the `clear` command)
- Dependencies listed in [`requirements.txt`](requirements.txt) (mainly `matplotlib`, `pandas` and `numpy`)

## Installation

```bash
git clone https://github.com/sjdfani/Evolution-of-Trust.git
cd Evolution-of-Trust

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Usage

```bash
python3 main.py
```

The main menu shows the current payoffs and rules, followed by these options:

| Option | Action |
| --- | --- |
| `1` | Set new payoff values |
| `2` | Reset payoffs to defaults |
| `3` | Set new rules (rounds, players replaced per round, population size) |
| `4` | Reset rules to defaults |
| `5` | Play a 1 vs 1 match |
| `6` | Play a multiplayer tournament |
| `9` | Exit |

After a match finishes, answer `y` or `yes` to the prompt to display the result plots.

### 1 vs 1

Select two characters from the list. They play for the configured number of rounds, and each move and running score is printed. The optional plot shows how each player's score changes over the rounds.

### Multiplayer

1. Choose **Manual** to enter how many of each character to include (the total must equal the population size), or **Automatic** to split the population evenly across all characters.
2. In every round, each player plays against every other player.
3. At the end of the round, players are sorted by score, the lowest `remove tail players` are removed, and the same number of copies of the top scorers are added.
4. After the final round, the population count and total score of each character per round are printed, and you can plot both.

To silence the per-move log, set `PRINT_LOG = False` in [`src/constants.py`](src/constants.py).

## Project Structure

```
Evolution-of-Trust/
├── main.py            # Entry point and interactive menu
├── requirements.txt   # Python dependencies
└── src/
    ├── constants.py   # Default payoffs, rules and feature flags
    ├── game.py        # Match logic, tournament, population handling and plots
    ├── individual.py  # Character strategies
    └── setting.py     # PayOffs and Rule classes
```

## Credits

Based on the ideas presented in [The Evolution of Trust](https://ncase.me/trust/) by Nicky Case.
