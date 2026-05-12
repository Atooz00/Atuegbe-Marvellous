from abc import ABC, abstractmethod
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)

class BaseEvaluator(ABC):
    """
    Abstract base class for all TrenchOps market evaluators.
    """

    def __init__(self, market_name: str, default_base_prob: float):
        self.market_name = market_name
        self.default_base_prob = default_base_prob

    @abstractmethod
    async def get_historical_probability(self, match_id: int) -> float:
        """
        Fetch/calculate the historical base probability $P$ for this market.
        """
        pass

    async def calculate_trench_multiplier(self, match_id: int) -> float:
        """
        Calculate the 'Trench Multiplier' based on recent team forms.
        For v1.0 mock, we return a flat multiplier or small random boost.
        """
        # Mock logic: if teams are low scoring, add 2-3%
        return 0.025

    async def evaluate_signal(self, match_id: int, bookmaker_odds: float) -> Tuple[bool, Dict[str, Any]]:
        """
        Main evaluation flow:
        1. Calculate final probability P
        2. Calculate EV
        3. Determine Kelly Stake
        4. Return Signal Decision
        """
        try:
            base_p = await self.get_historical_probability(match_id)
            multiplier = await self.calculate_trench_multiplier(match_id)
            final_p = min(0.99, base_p + multiplier) # Cap at 99%

            implied_prob = 1 / bookmaker_odds

            # Value Signal: if Bookmaker Implied Prob is lower than our P by > 5%
            has_value = implied_prob < (final_p - 0.05)

            # EV Calculation: (P * G) - L
            # G = Net odds (Decimal Odds - 1)
            # L = Probability of loss (1 - P)
            gain = bookmaker_odds - 1
            loss_prob = 1 - final_p
            ev = (final_p * gain) - loss_prob

            # Quarter-Kelly Criterion
            # f* = (bp - q) / b (where b is net odds gain, p is win prob, q is loss prob)
            # We use 0.25 multiplier for safety
            if gain > 0:
                full_kelly = ((gain * final_p) - loss_prob) / gain
            else:
                full_kelly = 0

            quarter_kelly = max(0, full_kelly * 0.25)

            # Final Signal Decision
            # Only trigger if EV is positive and it has value based on our 5% discrepancy rule
            is_signal = has_value and ev > 0.01 and quarter_kelly > 0

            signal_data = {
                "market": self.market_name,
                "calculated_prob": round(final_p, 4),
                "implied_prob": round(implied_prob, 4),
                "odds": bookmaker_odds,
                "ev": round(ev, 4),
                "suggested_kelly_pct": round(quarter_kelly, 4),
                "is_signal": is_signal
            }

            return is_signal, signal_data

        except Exception as e:
            logger.error(f"Error evaluating signal for {self.market_name}: {e}")
            return False, {}
