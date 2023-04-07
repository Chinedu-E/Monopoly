from collections import Counter



class Money:
    default_denominations = {"500": 0, "100": 0, "50": 0, "20": 0, "10": 0, "5": 0, "1": 0}
    
    def __init__(self, denominations: dict[str, int] = None):
        if denominations:
            self.denominations = self.default_denominations | denominations
        else:
            self.denominations = self.default_denominations
        
    def __add__ (self, other):
        m1 = self.denominations.copy()
        m2 = other.denominations.copy()
        denominations = Counter(m1) + Counter(m2)
        return Money(denominations)
    
    def __sub__ (self, other):
        m1 = Counter(self.denominations.copy())
        m2 = Counter(other.denominations.copy())
        m1.subtract(m2)
        return Money(m1)
    
    def __mul__(self, other):
        if isinstance(other, Money):
            pass
        elif isinstance(other, int):
            tot = self.total()
            return tot * other
        else:
            raise TypeError("Money can only be compared with Money and Integer")
    
    def __repr__(self):
        return f"Money({self.denominations})"
    
    def __del__(self): ...
    
    def __lt__(self, other):
        if isinstance(other, Money):
            tot1 = self.total()
            tot2 = other.total()
            return tot1 < tot2
        elif isinstance(other, int):
            tot1 = self.total()
            return tot1 < other
        else:
            raise TypeError("Money can only be compared with Money and Integer")
    
    def __le__(self, other):
        if isinstance(other, Money):
            tot1 = self.total()
            tot2 = other.total()
            return tot1 <= tot2
        elif isinstance(other, int):
            tot1 = self.total()
            return tot1 <= other
        else:
            raise TypeError("Money can only be compared with Money and Integer")
    
    def __gt__(self, other):
        if isinstance(other, Money):
            tot1 = self.total()
            tot2 = other.total()
            return tot1 > tot2
        elif isinstance(other, int):
            tot1 = self.total()
            return tot1 > other
        else:
            raise TypeError("Money can only be compared with Money and Integer")
    
    def __ge__(self, other):
        if isinstance(other, Money):
            tot1 = self.total()
            tot2 = other.total()
            return tot1 >= tot2
        elif isinstance(other, int):
            tot1 = self.total()
            return tot1 >= other
        else:
            raise TypeError("Money can only be compared with Money and Integer")
    
    def __eq__(self, other):
        if isinstance(other, Money):
            tot1 = self.total()
            tot2 = other.total()
            return tot1 == tot2
        elif isinstance(other, int):
            tot1 = self.total()
            return tot1 == other
        else:
            raise TypeError("Money can only be compared with Money and Integer")
    
    def __ne__(self, other):
        if isinstance(other, Money):
            tot1 = self.total()
            tot2 = other.total()
            return tot1 != tot2
        elif isinstance(other, int):
            tot1 = self.total()
            return tot1 != other
        else:
            raise TypeError("Money can only be compared with Money and Integer")
    
    def add_money(self, denomination: str, amount: int) -> None:
        val = self.denominations.get(denomination, 0)
        self.denominations[denomination] = val + amount

    def total(self) -> int:
        denums = list(self.denominations.keys())
        amounts = list(self.denominations.values())
        total = sum([int(denum) * amount for denum, amount in zip(denums, amounts)])
        return total
    
    def copy(self):
        return self.__class__(self)
    
    
class OutOfDenominationError(Exception):
    
    def __init__(self, denomination: str):
        self.denomination = denomination
        self.message = "Bank has run out of specified denomination"
        
    def __str__(self):
        return f"{self.denomination} -> {self.denomination}"    
    
    
class BankMoney(Money):
    default_denominations = {"500": 20, "100": 20, "50": 30, "20": 50, "10": 40, "5": 40, "1": 40}

    def __init__(self):
      super().__init__()
          
          
    def give_money(self, denomination: str, amount: int) -> Money:
      value = self.denominations.get(denomination, 0)
      to_give = {denomination: amount}
      if value != 0:
        self.denominations[denomination] -= amount
        return Money(to_give)
      else:
          raise OutOfDenominationError(denomination)
    
    def collect_money(self, denomination: str, amount: int):
        val = self.denominations.get(denomination, 0)
        self.denominations[denomination] = val + amount
        
        
        
        
if __name__ == '__main__':
    bank = BankMoney()
    money = Money({"100": 2})
    print(money)