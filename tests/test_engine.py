import random
import unittest

from freetennis.engine import MatchState, resolve_point


class ScoringTest(unittest.TestCase):
    def test_regular_game_no_deuce(self) -> None:
        state = MatchState()
        for _ in range(4):
            state.register_point("You")
        self.assertEqual(state.games["You"], 1)
        self.assertEqual(state.games["CPU"], 0)
        self.assertFalse(state.in_tiebreak)
        self.assertEqual(state.points, {"You": 0, "CPU": 0})

    def test_deuce_and_advantage(self) -> None:
        state = MatchState()
        for _ in range(3):
            state.register_point("You")
            state.register_point("CPU")
        state.register_point("You")  # Advantage You
        self.assertEqual(state.point_label("You"), "Ad")
        state.register_point("CPU")  # Back to deuce
        self.assertEqual(state.point_label("You"), "40")
        state.register_point("CPU")
        state.register_point("CPU")  # CPU closes game
        self.assertEqual(state.games["CPU"], 1)

    def test_tiebreak_reaches_set(self) -> None:
        state = MatchState()
        state.games = {"You": 6, "CPU": 6}
        state.in_tiebreak = True
        for _ in range(7):
            state.register_point("You")
        self.assertEqual(state.sets_won["You"], 1)
        self.assertEqual(state.games, {"You": 0, "CPU": 0})
        self.assertFalse(state.in_tiebreak)


class SimulationTest(unittest.TestCase):
    def test_resolve_point_uses_random_seed(self) -> None:
        random.seed(42)
        state = MatchState()
        winner1, _, _ = resolve_point(state, "safe", "safe")
        random.seed(42)
        state2 = MatchState()
        winner2, _, _ = resolve_point(state2, "safe", "safe")
        self.assertEqual(winner1, winner2)


if __name__ == "__main__":
    unittest.main()
