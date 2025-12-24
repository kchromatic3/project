## FreeTennis

FreeTennis is a compact, terminal-friendly tennis game. Rally against an adaptive AI, decide how risky your swings should be, and work through a best-of-three set match with authentic tennis scoring (love, deuce, advantage, tie-breaks).

### Playing

```bash
python -m freetennis
```

You will be prompted each point to choose your swing:

- **safe** – high consistency, fewer winners.
- **drive** – balanced risk and pressure.
- **power** – go for broke at the cost of errors and stamina.

The CPU adjusts its aggression based on the score and both players fatigue over time. Points include short rally narratives so you can picture the exchanges.

### Options

- `--demo` will let the CPU play itself while still printing the match story.
- `--sets 1` (or 3) changes how many sets are required to win the match.

### Running tests

```bash
python -m unittest
```

### Project layout

- `freetennis/` – core game engine and CLI entrypoint.
- `tests/` – unit tests for scoring and simulation helpers.

