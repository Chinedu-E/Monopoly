import random
from typing import Any, Callable
from .money import Money



    
class BrokeBoyError(Exception):
    
    def __init__(self, message: str):
        self.message = message
        
    def __str__(self):
        return self.message
    
    
class Balance:
    
    def __init__(self, money: Money = None):
        if money:
            self.money = money
        else:
            self.money = Money()
            
    def add_money(self, money: Money):
        if sum(list(self.money.denominations.values())) == 0: #If it is an empty account
            self.money = money
        else:
            self.money += money
    

    def total(self):
        return self.money.total()
    
    def remove_money(self, money: Money):
        if sum(list(self.money.denominations.values())) == 0:
            raise BrokeBoyError("You're broke my guy!")
        else:
            self.money -= money

class Dice:

  def __init__(self):
    self.die1 = 1
    self.die2 = 1

  def roll(self) -> tuple:
    self.die1 = random.randint(1, 6)
    self.die2 = random.randint(1, 6)
    return self.die1, self.die2

  def get_total(self) -> int:
    return self.die1 + self.die2

  def __str__(self):
    return f"{self.die1}  {self.die2}"
    
def generate_sequence(): ...



class StatsTracker:
    transactions_num: int = 0
    
    def __init__(self, func) -> None:
        self.func: Callable[[Any], Any] = func
        self.money_in: int = 0
        self.money_out: int = 0
        self.transactions_num: int = 0
        self.net_profit: int = 0

    def __post_init__(self):...

    def __call__(self, *args, **kwds) -> Any:
        print(args)
        money: Money = self.func(*args, **kwds)
        self.transactions_num += 1
        self.money_out += money.total()

    @staticmethod
    def track(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            StatsTracker.transactions_num += 1
        return wrapper
        
def buy_assets(banker, player):
    pos = player.get_position()
    



if __name__ == "__main__":
    money = Money()
    money.add_money("10", 2)
    money.add_money("100", 5)
    money.add_money("500", 5)
    bal = Balance(money)
    bal.add_money(money)
    t = money - money
    print(t)
    print(t.total())