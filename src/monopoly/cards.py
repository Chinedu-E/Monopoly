from dataclasses import dataclass




@dataclass(frozen=True)
class Card:
    
    text: str
    id: int

    def get_text(self) -> str:
        return self.text

    def get_id(self) -> int:
        return self.id

    def to_action(self):
        ...

@dataclass(frozen=True)
class Action:

    tag: str
    amount: int

    def get_tag(self) -> str:
        return self.tag

    def get_amount(self) -> str:
        return self.amount