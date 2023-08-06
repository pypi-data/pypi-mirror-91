from typing import List, DefaultDict
from ..engines import PitchEngine
from ..domain import StockPrice, Strategy, Portfolio, Position, Pitch, Side
from ..indicators import AbstractIndicator
from collections import defaultdict


class PortfolioWrapper(object):
    def __init__(self, seed_prices: List[StockPrice], indicators: List[AbstractIndicator], strategies: List[Strategy], portfolio: Portfolio = Portfolio(), paper_money: bool = True):
        self.engine = PitchEngine(
            seed_prices=seed_prices,
            indicators=indicators,
            strategies=strategies
        )

        self.portfolio = portfolio
        self.paper_money = paper_money

        ## history
        self.strategy_operations: DefaultDict[str, DefaultDict[str, List[Position]]] = defaultdict(lambda: defaultdict(list))

    def run(self, pitch: Pitch) -> List[Position]:
        self.portfolio.reload()

        positions = self.engine.run(pitch, self.portfolio)

        if self.paper_money:
            ## execuate fake trades
            self.portfolio.add_positions([ position for position in positions if position.action == Side.Buy ])
            self.portfolio.remove_positions([ position for position in positions if position.action == Side.Sell ])

            ## cache portfolio moves
            self.portfolio.cache()

        for position in positions:
            self.strategy_operations[position.strategy_id][position.symbol].append(position)

        return positions
