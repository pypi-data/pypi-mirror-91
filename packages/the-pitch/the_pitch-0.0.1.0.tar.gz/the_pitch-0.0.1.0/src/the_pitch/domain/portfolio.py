from collections import defaultdict
from typing import Dict, List
from . import Position
import json


class Portfolio(object):
    def __init__(self, cache_path: str = None):
        self.active_positions: Dict[str, List[Position]] = defaultdict(list)
        self.cache_path = cache_path

    def add_positions(self, new_positions: List[Position]) -> None:
        for position in new_positions:
            self.active_positions[position.strategy_id].append(position)

    def remove_positions(self, old_positions: List[Position]) -> None:
        for position in old_positions:
            self.remove_position(position.strategy_id, position.symbol)

    def remove_position(self, strategy_id: str, symbol: str) -> None:
        if strategy_id in self.active_positions:
            self.active_positions[strategy_id] = list(filter(
              lambda p: p.symbol != symbol,
              self.active_positions[strategy_id],
            ))

    def get_positions_by_strategy(self, strategy_id: str) -> List[Position]:
        return self.active_positions[strategy_id]

    def get_positions(self, strategy_id: str, symbol: str) -> List[Position]:
        return list(filter(
          lambda p: p.symbol == symbol,
          self.get_positions_by_strategy(strategy_id)
        ))

    def cache(self):
        if self.cache_path is None:
            return

        obj = {}
        for strategy_id, items in self.active_positions.items():
            obj[strategy_id] = [ item.to_obj() for item in items ]

        contents = json.dumps(obj)
        with open(self.cache_path, 'w') as output:
            output.write(contents)

    def reload(self):
        if self.cache_path is None:
            return

        with open(self.cache_path, 'r') as input:
            contents = input.read()

        self.active_positions = defaultdict(list)
        for strategy_id, items in json.loads(contents).items():
            self.active_positions[strategy_id] = [ Position.create(item) for item in items ]
