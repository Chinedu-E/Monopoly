import numpy as np
import pandas as pd
from .money import Money
from typing import Union


class Board:
    ''' Represents the monopoly game board'''

    def __init__(self, players):
        self.players = players
        self.reset()

    def __getitem__(self, item: int):
        return self.board[item]

    def __fill_board(self):
        '''Fills the board with tile objects '''
        module = __import__("properties") #import properties.py
        for pos, tile_attributes in self.table.iterrows():
            class_ = getattr(module, tile_attributes["class"]) #importing the appropriate class for tile
            self.board[pos] = class_(tile_attributes) #instantiating class

    def push_player(self, player, position: Union(int, str, tuple[int, int])):
        '''Moves player from the current position to specified position
            Args:
                player: 
                    An instance of the Player class.
                position: 
                    Move destination. it could be a tuple indicating a dice roll,
                    it could be a string indicating the name of the move destination,
                    and it could be an integer indicating the dice roll total.
            
            Returns:
                None
                
            Raises:
                NotImplementedError: raised when position entered can be used to move player'''
        if isinstance(position, tuple) and len(position) == 2:
            total = position[0] + position[1]
            player.set_position(player.new_position + total)
        elif isinstance(position, str):
            total = self.get_tile_position(position)
            if position == "Jail":
                player.set_position(total)
            else:
                player.set_position(player.new_position + total)
        elif isinstance(position, int):
            player.set_position(position)
        else:
            raise NotImplementedError

    def get_tile_position(self, tile_name: str) -> int:
        df = self.table[self.table["name"] == tile_name]
        position = df.index.values[0]
        return position

    def show_position(self, players: list) -> np.ndarray:
        board = np.zeros(40, dtype=object)
        for player in players:
            curr_position = player.get_position()
            board[curr_position] = player.get_name()
        return board

    def is_monopoly(self, color: str) -> bool:
        df = self.table[self.table["color"] == color]
        positions = df.index.values
        owners = np.array([],dtype= str)
        for pos in positions:
            owner = self[pos].get_owner()
            if owner:
                owners = np.append(owners, owner)
            else:
                return False
        return np.all(owners == owners[0])

    def rank_players(self, players: list, metrics: str = "cash"):
        if metrics == "cash":
            cash: list[tuple[int, int]] = []
            for i, player in enumerate(players):
                cash.append((i, player.balance.total()))
            cash.sort(key= lambda x: x[1], reverse=True)
            leader: list[tuple[int, int]] = [(players[i[0]].get_name(), players[i[0]].balance.total()) for i in cash]
            return leader
        else:
            raise NotImplementedError
        

    def buy_assets(self, player, banker):
        pos = player.get_position()
        tile = self[pos]
        tile.set_owner(player)
        banker.give_property(player, tile.copy())

    def trade_assets(self, player1, player2):
        ...

    def check_passed_go(self, player) -> bool:
        old_position, new_position = player.get_positions()
        if old_position > new_position:
            return True
        return False

    def eject_player(self, player):
        try:
            self.players.remove(player)
            return True

        except ValueError:
            print(f"player {player.get_name()} is not in the game")
            return False

    def read_action(self, action, player, banker):
        player_pos = player.get_position()
        tile_name = self[player_pos].name
        tag = action.tag
        amount = action.amount

        if amount:
            money = Money.int_to_denominations(amount, wrap = True)
        
        ACTION_MAP = {"Advance": self.push_player(player, tile_name),
                    "pay": player.pay_money(money),
                    "collect": banker.give_money(money, player)}

        return  ACTION_MAP[tag]

    def is_game_over(self, claim_draw: bool = False):
        if claim_draw:
            if self.total_turns == 700:
                return True
            else:
                return False
        else:
            if len(self.players) == 1:
                return True
            else:
                return False

    def __reset_players(self):
        for i, player in enumerate(self.players):
            self.players[i] = player.reset()

    def reset(self):
        self.board = np.zeros(40, dtype=object)
        self.total_turns = 0
        self.table = pd.read_csv("./board.csv") #csv file containing all information on board tiles
        self.__fill_board()
        self.__reset_players()

    
    