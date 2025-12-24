import argparse
import sys
from typing import Literal

from .ai import cpu_choice, cpu_demo_choice
from .engine import MatchState, ShotChoice, resolve_point, SHOT_PROFILE
from .narrative import describe_rally


def _prompt_user() -> ShotChoice:
    while True:
        choice = input("Choose your swing [safe/drive/power]: ").strip().lower()
        if choice in ("safe", "drive", "power"):
            return choice  # type: ignore[return-value]
        print("Please enter safe, drive, or power.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="FreeTennis - terminal tennis duel")
    parser.add_argument("--demo", action="store_true", help="Let the CPU control your player too.")
    parser.add_argument("--sets", type=int, default=3, choices=[1, 3], help="Play best of N sets.")
    args = parser.parse_args(argv)

    target_sets = (args.sets + 1) // 2
    state = MatchState(sets_to_win=target_sets)

    print("Welcome to FreeTennis! First to", target_sets, "sets wins.\n")
    while not state.is_match_over():
        print(state.score_summary())
        if state.in_tiebreak:
            print("Tie-break underway. First to 7, win by two.")

        player_choice: ShotChoice
        if args.demo:
            player_choice = cpu_demo_choice()
        else:
            player_choice = _prompt_user()
        cpu_shot = cpu_choice(
            gamescore=state.games,
            sets=state.sets_won,
            stamina=state.players["CPU"].stamina,
            opponent_stamina=state.players["You"].stamina,
            is_tiebreak=state.in_tiebreak,
        )

        winner, _, detail = resolve_point(state, player_choice, cpu_shot)
        report = state.register_point(winner)
        rally_story, swing_story = describe_rally(player_choice, cpu_shot, winner)

        print(rally_story)
        print(swing_story)
        print(report)
        print(detail)
        print()

    winner = "You" if state.sets_won["You"] > state.sets_won["CPU"] else "CPU"
    print(state.score_summary())
    print(f"Match over! {winner} takes it {state.set_history}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
