const readline = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout
})


class Player {
  constructor(name) {
    this.name = name;
    this.move = null;
  }
}

class ComputerPlayer extends Player {
  static get EASY_DIFFICULTY() { return 'facil';}
  static get NORMAL_DIFFICULTY() { return 'normal';}

  constructor(name, difficulty) {
    super(name);
    this.difficulty = difficulty;
  }


  async nextMove() {
    if (this.difficulty === ComputerPlayer.EASY_DIFFICULTY) {
      this.move = new Move(Move.ROCK);
    } else if (this.difficulty === ComputerPlayer.NORMAL_DIFFICULTY) {
      this.move = new Move();
    }
    console.log(`${this.name}: ${this.move.name}`);
  }
}

class HumanPlayer extends Player {
  async nextMove() {
    this.move = await Move.readMove(this.name);
  }
}

class Move {
  static get PAPER() { return 'papel'; }
  static get ROCK() { return 'piedra'; }  
  static get SCISSORS () { return 'tijera'; }
  
  constructor(name) {
    this.options = [Move.ROCK, Move.PAPER, Move.SCISSORS];
    this.name = name ? name : this.random();
  }

  win() {
    switch (this.name) {
      case Move.ROCK:
        return Move.SCISSORS;
      case Move.PAPER:
        return Move.ROCK;
      case Move.SCISSORS:
        return Move.PAPER;
    }
  }

  random() {
    return this.options[Math.floor(Math.random() * this.options.length)];
  }

  static async readMove(PlayerName) {
    return new Promise((resolve, reject) => {
      readline.question(PlayerName+': ', answer => {
        resolve(new Move(answer));
      })
    });
  }
}

class Rule {
  static get TIE () { return null; }

  constructor(players) {
    this.players = players;
  }

  getWinner() {
    const moves = this.players.map(player => player.move);
    if (moves[0].name === moves[1].name) return Rule.TIE;
    return moves[0].win() === moves[1].name ? this.players[0] : this.players[1];
  }
}

class Game {
  constructor(players, mode, rule) {
    this.players = players;
    this.mode = mode;
    this.rule = rule;
  }

  async play() {
    for (const player of this.players) {
      await player.nextMove();
    }
    
    return this.rule.getWinner();
  }
}

class RockPaperScissorsGame extends Game {
  static get MULTIPLAYER() { return 'multijugador'; }
  static get SINGLEPLAYER() { return 'solo'; }
  constructor(mode, difficulty) {
    const players = RockPaperScissorsGame.definePlayers(mode, difficulty);
    const rule = new Rule(players);
    super(players, mode, rule);
  }

  static definePlayers(mode, difficulty) {
    let players = [];
    if (mode === RockPaperScissorsGame.MULTIPLAYER) {
      players[0] = new HumanPlayer('Jugador1');
      players[1] = new HumanPlayer('Jugador2');
    }
    else if (mode === RockPaperScissorsGame.SINGLEPLAYER) {
      players[0] = new HumanPlayer('Jugador1');
      players[1] = new ComputerPlayer('Computador', difficulty);
    }

    return players;
  }
} 

async function main() {
  /*node index.js --modo=solo --dificultad=norma */

  let mode = '';
  let difficulty = '';
  process.argv.forEach(arg => {
    if (arg.includes('--modo')) {
      mode = arg.split('=')[1];
    } else if (arg.includes('--dificultad')) {
      difficulty = arg.split('=')[1];
    }
  });
  const rockPaperScissors = new RockPaperScissorsGame(mode, difficulty);
  const winner = await rockPaperScissors.play();
  console.log(winner === Rule.TIE ? `Empate` : `Ganador: ${winner.name}`);
  readline.close();
}

main();
