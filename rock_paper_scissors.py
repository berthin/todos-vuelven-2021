import click
from typing import List
from random import choice
from enum import Enum, auto
from dataclasses import dataclass, field


class GameMoves(Enum):
    pass


class GameRules:
    def determine_winner(self, game_round: List[GameMoves]) -> int:
        pass


@dataclass
class Player:
    name: str

    def move(self) -> GameMoves:
        pass


@dataclass
class Game:
    rules: GameRules
    players: List[Player] = field(default_factory=list)

    def addPlayer(self, player: Player):
        self.players.append(player)

    def play(self) -> Player:
        game_round = [player.move() for player in self.players]
        winner = self.rules.determine_winner(game_round)
        return self.players[winner]


class DrawException(Exception):
    pass


class GameMode(Enum):
    SOLO = 'solo'
    MULTIJUGADOR = 'multijugador'

    def __str__(self):
        return self.value


class GameDifficulty(Enum):
    FACIL = 'facil'
    DIFICIL = 'dificil'

    def __str__(self):
        return self.value


class Result(Enum):
    DRAW = auto()
    LOSE = auto()
    WIN = auto()


class RockPaperSissorsMoves(GameMoves):
    ROCK='piedra'
    PAPER='papel'
    SCISSORS='tijeras'


class RockPaperSissorsRules(GameRules):
    def __init__(self):
        #       ROCK PAPER SCISSORS
        # ROCK    D    L     W
        # PAPER   W    D     L
        # SCISSOR L    W     D
        # 0,1,2,  index=3  (3+3-1)%3
        # 2,0,1,  index=2
        # 1,2,0   index=1

        self.round_combinations = dict()
        results = [Result.DRAW, Result.LOSE, Result.WIN]
        index = 0
        for move1 in RockPaperSissorsMoves:
            for move2 in RockPaperSissorsMoves:
                self.round_combinations[(move1, move2)] = results[index % len(results)]
                index += 1
            index += len(results) - 1

    def determine_winner(self, game_round) -> int:
        try:
            return {
                Result.WIN: 0,   # player1
                Result.LOSE: 1,  # player2
            }[self.round_combinations[tuple(game_round)]]
        except KeyError as error:
            raise DrawException


@dataclass
class HumanPlayer(Player):
    def move(self):
        return RockPaperSissorsMoves(input(f'{self.name}: '))


@dataclass
class Strategy:
    def move(self):
        pass


class FacilStrategy(Strategy):
    def move(self):
        return RockPaperSissorsMoves.ROCK


class DificilStrategy(Strategy):
    def move(self):
        return choice(list(RockPaperSissorsMoves))


def factory_strategy(difficulty: GameDifficulty) -> Strategy:
    if difficulty == GameDifficulty.FACIL:
        return FacilStrategy()
    elif difficulty == GameDifficulty.DIFICIL:
        return DificilStrategy()


@dataclass
class ComputerPlayer(Player):
    difficulty: GameDifficulty = None

    def move(self):
        computer_move = factory_strategy(self.difficulty).move()
        print(f'{self.name}: {computer_move.value}')
        return computer_move


@click.command()
@click.option('--modo', type=click.Choice(map(str, GameMode)), required = True, help='Modo de juego')
@click.option('--dificultad', type=click.Choice(map(str, GameDifficulty)), required = False, help='Nivel de dificultad')
def init(modo, dificultad):
    game = Game(rules=RockPaperSissorsRules())

    game.addPlayer(HumanPlayer(name='Jugador1'))
    if GameMode(modo) == GameMode.SOLO:
        game.addPlayer(ComputerPlayer(name='Computador', difficulty=GameDifficulty(dificultad)))
    else:
        game.addPlayer(HumanPlayer(name='Jugador2'))

    try:
        winner = game.play()
        print(f'Vencedor: {winner.name}')
    except DrawException:
        print(f'Empate!')


if __name__ == '__main__':
    init()
