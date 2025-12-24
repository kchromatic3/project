import random
from typing import Literal, Tuple

ShotChoice = Literal["safe", "drive", "power"]

_OPENINGS = [
    "A sharp serve opens the point.",
    "Rally begins with a deep return.",
    "They trade quick backhands cross-court.",
    "Serve clipped the tape but lands in.",
]

_EXCHANGES = [
    "A looping topspin pushes back the defender.",
    "They grind through a long backhand exchange.",
    "A sudden drop shot pulls the opponent forward.",
    "Footwork gets choppy as they reset with a moonball.",
    "Crowd hushes as both players wait for a short ball.",
]

_FINISHERS = [
    "A bold forehand down the line ends it.",
    "The reply floats long under pressure.",
    "Volley winner tucked away.",
    "A forced error as the ball sails wide.",
    "A net cord dribbles over for the point.",
]


def describe_rally(
    player_shot: ShotChoice, cpu_shot: ShotChoice, winner: str
) -> Tuple[str, str]:
    opening = random.choice(_OPENINGS)
    middle = random.choice(_EXCHANGES)
    finisher = random.choice(_FINISHERS)

    tone = {
        "safe": "disciplined",
        "drive": "assertive",
        "power": "huge-risk",
    }
    swing_note = f"You play a {tone[player_shot]} ball; CPU answers with {tone[cpu_shot]} pace."
    winner_note = f"{winner} takes the point."
    return " ".join([opening, middle, finisher]), f"{swing_note} {winner_note}"
