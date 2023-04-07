from collections import deque
import random
from typing import Union

from src.monopoly.cards import Card, Action
from src.monopoly.players import Participant




class Tile:

  def __init__(self, attributes: dict[str, Union[str, int]]):
    self.name: str = attributes["name"]
    self.price: int = attributes["price"]
    self.color = attributes["color"]
    self.monopoly_size: int = attributes["monopoly_size"] #NUMBER OF COLOURS IN GROUP
    self.board_position: int = attributes["position"] - 1
    self.price: int = attributes["price"]
    self.build_cost: int = attributes["build_cost"]
    self.rent: int = attributes["rent"]
    self.rent_1: int = attributes["rent_house_1"]
    self.rent_2: int = attributes["rent_house_2"]
    self.rent_3: int = attributes["rent_house_3"]
    self.rent_4: int = attributes["rent_house_4"]
    self.rent_hotel: int = attributes["rent_hotel"]
    self.tax: int = attributes["tax"]
    self.owner: Participant = None
    self.is_buildable = False

  def __eq__(self, other):
    return self.color == other.color

  def set_owner(self, player):
    self.owner = player

  def get_owner(self):
    return self.owner

  def on_landing(self):
    return Action(None, None)

  def copy(self):
    return self.__class__(self)
  
  
class Street(Tile):

  def __init__(self, attributes):
    super().__init__(attributes)
    self.is_buildable = True
    self.houses = 0
    self.hotels = 0

  def add_house(self, count) -> bool:
    if self.houses + count >4:
      print("Cannot add more houses max (4)")
      return False
    else:
      self.houses += count
      return True  

  def add_hotel(self) -> bool:
    if self.hotels != 0:
      print('Cannot add more properties ')
      return False
    else:
      self.hotels += 1
      return True

  def get_houses(self) -> int:
    return self.houses

  def get_hotels(self) -> int:
    return self.hotels

  def on_landing(self):
    owner = self.get_owner()
    if owner:
      props = [prop.color for prop in owner.properties if prop.color == self.color]
      if len(props) == self.monopoly_size: #If the owner owns all properties of that color
        if self.houses == 1:
          return Action("pay", self.rent_1)
        elif self.houses == 2:
          return Action("pay", self.rent_2)
        elif self.houses == 3:
          return Action("pay", self.rent_3)
        elif self.houses == 4:
          return Action("pay", self.rent_4)
        elif self.hotels == 1:
          return Action("pay", self.rent_hotel)
        else:
          return Action("pay", self.rent * 2)
      else:
        return Action("pay", self.rent)
    else:
      return Action("buy", self.price)
    

class RailRoad(Tile):
  def __init__(self, attributes):
    super().__init__(attributes)

  def on_landing(self):
    owner = self.get_owner()
    if owner:
      ...
    return super().on_landing()


class Utility(Tile):
  def __init__(self, attributes):
    super().__init__(attributes)

  def calculate_rent(self, rolls):
    pass

  def on_landing(self):
    return super().on_landing()
  
  
class JailV(Tile):
  '''Visiting Jail tile/ Jail cell '''

  def __init__(self, attributes):
    super().__init__(attributes)
    self.players = []
  
  def remove_player(self):
    ...

  def add_player(self):
    ...

  def __len__ (self):
    return len(self.players)


class Jail(Tile):
  '''Go to Jail tile '''
  def __init__(self, attributes):
    super().__init__(attributes)

  def on_landing(self):
    return Action("Jail", 0)


class Chance(Tile):
    
    def __init__(self, attributes):
      super().__init__(attributes)
      self.cards, self.ids = self.load_chance()

    def load_chance(self):
        with open(".data/chance.txt") as f:
            data = f.read()
        data = data.split('\n')
        ids = [i for i in range(len(data))]
        zipped = list(zip(data, ids))
        random.shuffle(zipped)
        data, ids = zip(*zipped)
        return deque(data), deque(ids)

    def get_chance(self) -> Card:
        card = self.cards.popleft()
        id = self.ids.popleft()
        self.ids.append(id)
        self.cards.append(card)
        return Card(card, id)

    def read_chance(self, card: str) -> tuple[str, Union(str, int)]:...

    def on_landing(self):
      return self.get_chance()


class Chest(Tile):
    
    def __init__(self, attributes):
      super().__init__(attributes)
      self.cards, self.ids = self.load_chest()

    def load_chest(self):
        with open(".data/community_chest.txt") as f:
            data = f.read()
        data = data.split('\n')
        ids = [i for i in range(len(data))]
        zipped = list(zip(data, ids))
        random.shuffle(zipped)
        data, ids = zip(*zipped)
        return deque(data), deque(ids)

    def get_community_chest(self) -> Card:
        card = self.cards.popleft()
        id = self.ids.popleft()
        self.ids.append(id)
        self.cards.append(card)
        return Card(card, id)

    def on_landing(self):
      return self.get_community_chest()
      
      
class Tax(Tile):
    
    def __init__(self, attributes):
      super().__init__(attributes)
      
    def on_landing(self):
        if self.name == "luxury":
            return 


class Go(Tile):
  def __init__(self, attributes):
      super().__init__(attributes)


class FreeParking(Tile): 
  def __init__(self, attributes):
    super().__init__(attributes)

        