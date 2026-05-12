from app.evaluators.base_evaluator import BaseEvaluator

class GoalStreakEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__("Any Team Goal Streak 3+ (NO)", 0.94)

    async def get_historical_probability(self, match_id: int) -> float:
        return self.default_base_prob

class CornerDensityEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__("Corner Density (Under 13.5)", 0.88)

    async def get_historical_probability(self, match_id: int) -> float:
        return self.default_base_prob

class FirstHalfBookingsEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__("1st Half Bookings (Under 1.5)", 0.75)

    async def get_historical_probability(self, match_id: int) -> float:
        return self.default_base_prob

class TenMinuteDrawEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__("Ten Minute Draw (00:00 - 09:59)", 0.82)

    async def get_historical_probability(self, match_id: int) -> float:
        return self.default_base_prob

class PenaltyAwardedEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__("Penalty Awarded (NO)", 0.78)

    async def get_historical_probability(self, match_id: int) -> float:
        return self.default_base_prob

class FirstGoalIntervalEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__("First Goal Interval (1-15 Mins - NONE)", 0.70)

    async def get_historical_probability(self, match_id: int) -> float:
        return self.default_base_prob

class HomeMultiGoalsEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__("Home Multi Goals (1-3)", 0.85)

    async def get_historical_probability(self, match_id: int) -> float:
        return self.default_base_prob

class AwayMultiGoalsEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__("Away Multi Goals (0-3)", 0.91)

    async def get_historical_probability(self, match_id: int) -> float:
        return self.default_base_prob

class BothHalvesScoreEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__("Either Team to Score in Both Halves (NO)", 0.65)

    async def get_historical_probability(self, match_id: int) -> float:
        return self.default_base_prob

class FirstHalfGoalStreakEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__("1st Half Goal Streak 2+ (NO)", 0.89)

    async def get_historical_probability(self, match_id: int) -> float:
        return self.default_base_prob

# Registry to easily load all evaluators
ALL_EVALUATORS = [
    GoalStreakEvaluator(),
    CornerDensityEvaluator(),
    FirstHalfBookingsEvaluator(),
    TenMinuteDrawEvaluator(),
    PenaltyAwardedEvaluator(),
    FirstGoalIntervalEvaluator(),
    HomeMultiGoalsEvaluator(),
    AwayMultiGoalsEvaluator(),
    BothHalvesScoreEvaluator(),
    FirstHalfGoalStreakEvaluator()
]
