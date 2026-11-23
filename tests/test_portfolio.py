"""Known-answer and failure tests for portfolio.py.   Run:  python -m unittest -v"""
import io
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import portfolio as P  # noqa: E402


class KnownAnswers(unittest.TestCase):
    def test_two_asset_volatility_by_hand(self):
        # 50/50, vols 10% and 20%, corr 0.5: var = .25*.01 + .25*.04 + 2*.25*.5*.1*.2 = .0175
        cov = P.covariance_matrix([[1, 0.5], [0.5, 1]], [0.10, 0.20])
        self.assertAlmostEqual(P.portfolio_volatility([0.5, 0.5], cov), math.sqrt(0.0175), places=12)

    def test_grid_count_matches_combinatorics(self):
        # 5 assets in 5% steps: C(20 + 4, 4) = 10,626 mixes; every one sums to 1
        mixes = list(P.long_only_mixes(5))
        self.assertEqual(len(mixes), math.comb(24, 4))
        self.assertTrue(all(abs(sum(m) - 1) < 1e-9 for m in mixes))

    def test_cap_is_enforced_inside_the_search(self):
        self.assertTrue(all(max(m) <= 0.40 + 1e-9 for m in P.long_only_mixes(5, max_weight=0.40)))
        # 40% cap with 2 assets is impossible (needs 100%); 3 assets: only 40/40/20 patterns
        self.assertEqual(list(P.long_only_mixes(2, max_weight=0.40)), [])

    def test_lowest_risk_matches_closed_form(self):
        # Two uncorrelated assets, vols 10% and 20%: min variance weight = .04/(.01+.04) = 80%
        cov = P.covariance_matrix([[1, 0], [0, 1]], [0.10, 0.20])
        best = P.lowest_risk_mix([0.05, 0.05], cov, objective=0.0, max_weight=1.0)
        self.assertEqual([round(w, 2) for w in best["weights"]], [0.80, 0.20])

    def test_objective_infeasible_returns_none(self):
        cov = P.covariance_matrix([[1, 0], [0, 1]], [0.1, 0.2])
        self.assertIsNone(P.lowest_risk_mix([0.05, 0.06], cov, objective=0.07, max_weight=1.0))

    def test_max_feasible_return_under_cap(self):
        # 40% x 10% + 40% x 8% + 20% x 6% = 8.4%
        self.assertAlmostEqual(P.max_feasible_return([0.06, 0.10, 0.08], 0.40), 0.084)

    def test_estimate_known_answer(self):
        # A alternates +2%, 0%: mean 1%/month -> 12%/yr; sample sd = 1% x sqrt(12/11);
        # B is the mirror image, so the correlation is exactly -1.
        rows = [[0.02, 0.0], [0.0, 0.02]] * 6
        est = P.estimate(rows)
        self.assertAlmostEqual(est["returns"][0], 0.12, places=12)
        self.assertAlmostEqual(est["volatilities"][0], 0.01 * math.sqrt(12 / 11) * math.sqrt(12), places=12)
        self.assertAlmostEqual(est["correlation"][0][1], -1.0, places=12)

    def test_zero_volatility_refused(self):
        with self.assertRaises(ValueError):
            P.estimate([[0.01, 0.02 * (i % 2)] for i in range(12)])

    def test_backtest_no_cost_single_asset_matches_compounding(self):
        bt = P.backtest([1.0, 0.0], [[0.10, 0.0], [-0.05, 0.0]], cost_bps=0)
        self.assertAlmostEqual(bt["path"][-1], 1.10 * 0.95, places=12)

    def test_backtest_costs_reduce_value(self):
        rows = [[0.05, -0.05]] * 24
        free = P.backtest([0.5, 0.5], rows, cost_bps=0)["path"][-1]
        paid = P.backtest([0.5, 0.5], rows, cost_bps=25)["path"][-1]
        self.assertLess(paid, free)

    def test_drawdown_known_answer(self):
        perf = P.performance([1.0, 1.2, 0.9, 1.0], [0.2, -0.25, 1 / 9])
        self.assertAlmostEqual(perf["max_drawdown"], 0.9 / 1.2 - 1)


class NewProject2Pieces(unittest.TestCase):
    def test_inverse_volatility_known_answer(self):
        # vols 10% and 20% -> inverse 10 and 5 -> weights 2/3 and 1/3
        w = P.inverse_volatility_weights([0.10, 0.20])
        self.assertAlmostEqual(w[0], 2 / 3, places=12)
        self.assertAlmostEqual(sum(w), 1.0, places=12)

    def test_mandate_check_names_the_failed_rule(self):
        out = P.mandate_check([0.7, 0.3], [0.10, 0.10])
        self.assertFalse(out["passes"])
        self.assertEqual(out["failed_rules"], ["no fund above 40%"])

    def test_signal_is_point_in_time(self):
        # Changing every price AFTER the as-of month must not change the signal as of that month
        names, dates, prices = P.read_prices(str(ROOT / "data" / "prices.csv"))
        w = [0.15, 0.0, 0.40, 0.25, 0.20]
        before = P.risk_signal(dates, prices, w, "2023-09")
        altered = [row if d <= "2023-09" else [x * 3 for x in row] for d, row in zip(dates, prices)]
        after = P.risk_signal(dates, altered, w, "2023-09")
        self.assertEqual(before, after)

    def test_signal_needs_full_window(self):
        names, dates, prices = P.read_prices(str(ROOT / "data" / "prices.csv"))
        self.assertIsNone(P.risk_signal(dates, prices, [0.2] * 5, dates[11]))   # only 11 returns
        self.assertIsNotNone(P.risk_signal(dates, prices, [0.2] * 5, dates[12]))


class Refusals(unittest.TestCase):
    def test_bad_correlation_refused(self):
        with self.assertRaises(ValueError):
            P.validate_correlation([[1, 1.2], [1.2, 1]], 2)
        with self.assertRaises(ValueError):
            P.validate_correlation([[1, 0.3], [0.2, 1]], 2)

    def test_bad_prices_refused(self):
        for bad in ["Date,A\n2020-02,1\n2020-01,1\n2020-03,1\n",          # out of order
                    "Date,A\n2020-01,1\n2020-02,0\n2020-03,1\n",          # zero price
                    "Date,A\n2020-01,1\n2020-02,1,2\n2020-03,1\n"]:      # ragged row
            with self.assertRaises(ValueError):
                P.read_prices(io.StringIO(bad))


class ProjectData(unittest.TestCase):
    def setUp(self):
        self.names, _, prices = P.read_prices(str(ROOT / "data" / "prices.csv"))
        self.returns = P.monthly_returns(prices)

    def test_data_shape(self):
        self.assertEqual(self.names, ["XLE", "XOP", "AMLP", "ICLN", "NLR"])
        self.assertEqual(len(self.returns), 60)

    def test_recommended_mix_reproduces_lab15(self):
        est = P.estimate(self.returns)
        cov = P.covariance_matrix(est["correlation"], est["volatilities"])
        mix = P.lowest_risk_mix(est["returns"], cov)
        self.assertEqual([round(w, 2) for w in mix["weights"]], [0.15, 0.0, 0.40, 0.25, 0.20])
        self.assertAlmostEqual(mix["volatility"], 0.17138330, places=6)   # Lab 15 / Lab 20 value
        uncapped = P.lowest_risk_mix(est["returns"], cov, max_weight=1.0)
        self.assertEqual([round(w, 2) for w in uncapped["weights"]], [0.0, 0.0, 0.70, 0.20, 0.10])

    def test_holdout_choice_ignores_test_months(self):
        # Scrambling the 36 test months must not change the mix chosen on the first 24
        train = self.returns[:24]
        est = P.estimate(train)
        cov = P.covariance_matrix(est["correlation"], est["volatilities"])
        chosen = P.lowest_risk_mix(est["returns"], cov)["weights"]
        scrambled = train + [[-r for r in row] for row in self.returns[24:]]
        est2 = P.estimate(scrambled[:24])
        cov2 = P.covariance_matrix(est2["correlation"], est2["volatilities"])
        self.assertEqual(chosen, P.lowest_risk_mix(est2["returns"], cov2)["weights"])


if __name__ == "__main__":
    unittest.main()
