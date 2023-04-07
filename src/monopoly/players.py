from typing import Generator, Literal, Union
from .money import Money, BankMoney
from .properties import Street, Tile
from .cards import Card
from .utilities import Balance, Dice, StatsTracker
from .rules import jail_rule


class Participant:
  
  def recieve_money(self, money): ...
  ...

class Player(Participant):

  def __init__(self, name: str):
    self.name = name
    self.balance = Balance()
    self.jail_fine = Money({"50": 1})
    self.old_position: int = 0
    self.new_position: int = 0
    self.cards = []
    self.properties: list[Tile] = []


  def add_property(self, unit):
    self.properties.append(unit)

  def recieve_money(self, money: Money):
    self.balance.add_money(money)
    

  def pay_money(self, money: Money, player: Participant):
    self.balance.remove_money(money)
    player.recieve_money(money)
    
  def get_total_balance(self) -> int:
    return self.balance.total()

  @jail_rule
  def roll(self, dice: Dice) -> Generator[tuple[int, int], Dice, str]:
    """returns a generator of player's rolls and also would return "jail" on a triple roll """
    return dice.roll()

  def set_position(self, new_position: int):
    self.old_position = self.new_position
    self.new_position = new_position
    if self.new_position >= 40:
      self.new_position = self.new_position - 40

  def get_position(self) -> int:
    return self.new_position

  def reset(self):
    return Player(self.name)

  def get_past_positions(self) -> tuple[int, int]:
    return self.old_position, self.new_position

  def get_name(self) -> str:
    return self.name
  
  def get_property(self, tile: Tile) -> Tile:
    for prop in self.properties:
      if prop.name == tile.name:
        return prop
    return None
    
  def recieve_buildings(self, building_type: Literal["hotels", "houses"],
                     count: int,  street: Street):
    s = self.get_property(street)
    if building_type == "hotels":
      s.add_hotel()
    else:
      s.add_house(count)

  
class Banker(Participant):

  def __init__(self):
    self.money = BankMoney()
    self.player_starting_amount = Money({"500": 2, "100": 4, "50": 1, "20": 1, "10": 2, "5": 1, "1": 5})
    self.go_money: Money = Money({"100": 2})
    self.assets_count: int = 40
    self.assets = {'hotels': 12,
                   'houses': 32,
                   }

  def distribute_money(self, players: list[Player]) -> None:
    for player in players:
      player.recieve_money(self.player_starting_amount)

  def bank_total(self) -> int:
    return self.money.total()

  def give_money(self, money: Money, player: Player):
    player.recieve_money(money)

  def recieve_money(self, money: Money):
    self.money += money
    
  def give_go_money(self, player: Player):
    player.recieve_money(self.go_money)
    self.money -= self.player_starting_amount

  def give_property(self, player: Player, property: Tile):
    player.add_property(property)
  
  def give_buildings(self, player: Player,  building_type: Literal["hotels", "houses"],
                     count: int, street: Street):
    self.assets[building_type] -= count
    player.recieve_buildings(building_type, count, street)
    
  def oversee_trade(self, players: list[Player],
                    properties: list[Union(Tile, Card)],
                    mapping: dict[str, str]):
    ...


