"""Check the short-horizon experiment against the author's manuscript and main runs."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_tts_figures import summarize

DATA = json.loads((ROOT / "data/tts_runs.json").read_text())


class TTSData(unittest.TestCase):
    def test_manuscript_results(self):
        result = summarize(DATA)
        self.assertEqual(result["n_runs"], 84)
        self.assertEqual(result["long_wins"], 9)
        self.assertEqual(result["system_long_wins"], 4)
        self.assertEqual(result["model_long_wins"], {"gpt-6-astra": 6, "claude-opus-5-5": 3})
        claude_short_wins = {r["task"] for r in result["comparisons"]
                             if r["model"] == "claude-opus-5-5" and max(r["ratios"].values()) > 1}
        self.assertEqual(claude_short_wins, {"flux", "lmcache", "orpo"})
        for level, expected in (("Operator", 102.6), ("Module", 96.9), ("System", 77.3)):
            self.assertAlmostEqual(result["geometric_means_pct"][level]["4"], expected, delta=.05)
        for level, expected in (("Operator", 101.3), ("Module", 96.5), ("System", 79.4)):
            self.assertAlmostEqual(result["geometric_means_pct"][level]["2"], expected, delta=.05)

    def test_long_runs_match_main_experiment(self):
        raw = json.loads((ROOT / "data/raw/runs.json").read_text())
        keys = {"flux": "flux-moe", "orpo": "orpo", "sd35m": "sd35", "lmcache": "lmcache", "kvzip": "kvzip", "llada": "llada"}
        models = {"gpt-6-astra": "astra", "claude-opus-5-5": "claude"}
        for panel in DATA["panels"]:
            curve = next(c for c in panel["curves"] if c["allocation"] == 1)
            original = raw["tasks"][keys[panel["task"]]]["runs"][models[panel["model"]]]
            best = max(p[1] for p in original["points"] if p[1] is not None and p[2] == "valid" and p[0] <= panel["budget"])
            self.assertAlmostEqual(curve["plotted_best_scores"][-1], best, places=8, msg=panel["id"])

    def test_rejects_invalid_budgets_and_group_scores(self):
        for mutation in ("budget", "group"):
            data = copy.deepcopy(DATA)
            if mutation == "budget":
                data["panels"][0]["curves"][1]["budget_hours"] = 12
            else:
                data["panels"][0]["groups"][0]["plotted_best_scores"][-1] += 10
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                summarize(data)


if __name__ == "__main__":
    unittest.main()
