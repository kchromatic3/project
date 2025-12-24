from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Literal, Optional, Tuple

ShotChoice = Literal["safe", "drive", "power"]

POINT_LABELS = ["0", "15", "30", "40", "Ad"]

SHOT_PROFILE: Dict[ShotChoice, Dict[str, float]] = {
    "safe": {"attack": 0.2, "error": 0.04, "stamina_cost": 0.01},
    "drive": {"attack": 0.4, "error": 0.08, "stamina_cost": 0.02},
    "power": {"attack": 0.65, "error": 0.14, "stamina_cost": 0.04},
}


@dataclass
class PlayerState:
    name: str
    stamina: float = 1.0

    def apply_stamina_cost(self, choice: ShotChoice) -> None:
        cost = SHOT_PROFILE[choice]["stamina_cost"]
        self.stamina = max(0.4, self.stamina - cost)


@dataclass
class MatchState:
    sets_to_win: int = 2
    players: Dict[str, PlayerState] = field(
        default_factory=lambda: {"You": PlayerState("You"), "CPU": PlayerState("CPU")}
    )
    games: Dict[str, int] = field(default_factory=lambda: {"You": 0, "CPU": 0})
    points: Dict[str, int] = field(default_factory=lambda: {"You": 0, "CPU": 0})
    tiebreak_points: Dict[str, int] = field(default_factory=lambda: {"You": 0, "CPU": 0})
    sets_won: Dict[str, int] = field(default_factory=lambda: {"You": 0, "CPU": 0})
    in_tiebreak: bool = False
    set_history: list[Tuple[int, int]] = field(default_factory=list)

    def reset_game(self) -> None:
        self.points = {"You": 0, "CPU": 0}
        self.in_tiebreak = False
        self.tiebreak_points = {"You": 0, "CPU": 0}

    def point_label(self, player: str) -> str:
        if self.in_tiebreak:
            return str(self.tiebreak_points[player])
        opp = "CPU" if player == "You" else "You"
        if self.points[player] >= 3 and self.points[opp] >= 3:
            if self.points[player] == self.points[opp]:
                return "40"
            return "Ad" if self.points[player] > self.points[opp] else "40"
        return POINT_LABELS[min(self.points[player], 4)]

    def _game_winner(self) -> Optional[str]:
        if self.in_tiebreak:
            for player in ("You", "CPU"):
                opp = "CPU" if player == "You" else "You"
                if self.tiebreak_points[player] >= 7 and self.tiebreak_points[player] - self.tiebreak_points[opp] >= 2:
                    return player
            return None

        for player in ("You", "CPU"):
            opp = "CPU" if player == "You" else "You"
            if self.points[player] >= 4 and self.points[player] - self.points[opp] >= 2:
                return player
        return None

    def _set_winner(self) -> Optional[str]:
        for player in ("You", "CPU"):
            opp = "CPU" if player == "You" else "You"
            if self.games[player] >= 6 and self.games[player] - self.games[opp] >= 2:
                return player
            if self.games[player] == 7 and self.games[opp] == 6:
                return player
        return None

    def is_match_over(self) -> bool:
        return any(sets >= self.sets_to_win for sets in self.sets_won.values())

    def score_summary(self) -> str:
        sets = f"Sets: You {self.sets_won['You']} - CPU {self.sets_won['CPU']}"
        games = f"Games: You {self.games['You']} - CPU {self.games['CPU']}"
        if self.in_tiebreak:
            points = f"Tie-break: You {self.tiebreak_points['You']} - CPU {self.tiebreak_points['CPU']}"
        else:
            points = f"Points: You {self.point_label('You')} - CPU {self.point_label('CPU')}"
        return " | ".join([sets, games, points])

    def register_point(self, winner: str) -> Optional[str]:
        loser = "CPU" if winner == "You" else "You"
        if self.in_tiebreak:
            self.tiebreak_points[winner] += 1
        else:
            self.points[winner] += 1

        game_winner = self._game_winner()
        if game_winner:
            self.games[game_winner] += 1
            self.reset_game()

            # initiate tie-break at 6-6
            if self.games["You"] == 6 and self.games["CPU"] == 6:
                self.in_tiebreak = True

            set_winner = self._set_winner()
            if set_winner:
                self.sets_won[set_winner] += 1
                self.set_history.append((self.games["You"], self.games["CPU"]))
                self.games = {"You": 0, "CPU": 0}
                self.reset_game()
                return f"{set_winner} wins the set."
            return f"{game_winner} holds the game."

        return f"{winner} wins the point."


def resolve_point(
    state: MatchState, player_choice: ShotChoice, cpu_choice: ShotChoice
) -> Tuple[str, str, str]:
    """
    Simulate a rally and return (winner, narrative, detail).
    """
    player = state.players["You"]
    cpu = state.players["CPU"]

    player.apply_stamina_cost(player_choice)
    cpu.apply_stamina_cost(cpu_choice)

    player_attack = SHOT_PROFILE[player_choice]["attack"]
    cpu_attack = SHOT_PROFILE[cpu_choice]["attack"]

    player_error = SHOT_PROFILE[player_choice]["error"] * (1 + (1 - player.stamina) * 1.5)
    cpu_error = SHOT_PROFILE[cpu_choice]["error"] * (1 + (1 - cpu.stamina) * 1.5)

    base_chance = 0.5
    base_chance += (player_attack - cpu_attack) * 0.25
    base_chance += (cpu_error - player_error) * 0.55
    base_chance += (player.stamina - cpu.stamina) * 0.1
    base_chance = max(0.05, min(0.95, base_chance))

    import random

    roll = random.random()
    winner = "You" if roll < base_chance else "CPU"
    detail = (
        f"Model: P(win)={base_chance:.2f} (roll {roll:.2f}) "
        f"| stamina You {player.stamina:.2f}, CPU {cpu.stamina:.2f}"
    )
    return winner, "rally", detail
