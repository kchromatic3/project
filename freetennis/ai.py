import random
from typing import Dict, Literal

ShotChoice = Literal["safe", "drive", "power"]


def cpu_choice(
    gamescore: Dict[str, int],
    sets: Dict[str, int],
    stamina: float,
    opponent_stamina: float,
    is_tiebreak: bool,
) -> ShotChoice:
    """
    Decide how aggressive the CPU should be.

    The CPU ramps up risk when behind late in sets and cools off when ahead.
    Stamina also tempers the selection.
    """
    me_games = gamescore["CPU"]
    opp_games = gamescore["You"]
    me_sets = sets["CPU"]
    opp_sets = sets["You"]

    pressure = 0
    pressure += (opp_games - me_games) * 0.6
    pressure += (opp_sets - me_sets) * 1.2
    pressure += -0.5 if is_tiebreak and me_games >= 6 else 0
    pressure += (1 - stamina) * 1.0
    pressure += (opponent_stamina - stamina) * 0.5

    # Normalize to a 0-1 range via sigmoid-like squashing.
    aggressiveness = 1 / (1 + pow(2.7, -pressure))

    if aggressiveness < 0.32:
        return "safe"
    if aggressiveness < 0.62:
        return "drive"
    return "power"


def cpu_demo_choice() -> ShotChoice:
    """Random swing for demo vs demo matches."""
    return random.choice(["safe", "drive", "power"])
