import React, { Component } from "react";
import socketIOClient from "socket.io-client";
import Board from "./Board";
import TurnChooser from "./TurnChooser";
import "./App.css";

class App extends Component {
  constructor() {
    super();
    this.state = {
      gameState: [],
      gameHistory: [],
      endpoint: "http://127.0.0.1:5000",
      currentStepNumber: 0,
      turn: 0,
      turnNumbers: [],
      turnNumberToJump: 0
    };
  }

  didGameEnd = () => {};

  componentDidMount() {
    const { endpoint } = this.state;
    this.socket = socketIOClient(endpoint);
    this.socket.on("connect", function() {
      console.log("Websocket connected!");
    });
    // message handler for the when state changes
    this.socket.on("game_state_updated", gameHistory => {
      gameHistory = gameHistory.state;
      this.setState({ gameHistory }, () => {
        const lastTurnNumber = gameHistory[gameHistory.length - 1][1][0];
        this.setState({ turnNumbers: [...Array(lastTurnNumber + 1).keys()] });
      });
    });
  }

  getFirstInstanceOfTurn = turn => {
    const { gameHistory } = this.state;
    for (let index = 0; index < gameHistory.length; index++) {
      const gameState = gameHistory[index];
      if (gameState[1][0] === parseInt(turn)) {
        return [index, gameState[1]];
      }
    }
    return false;
  };

  startGame = () => {
    this.socket.emit("start_game");
  };

  setGameState = (currentStepNumber, gameHistory) => {
    const gameState = gameHistory[currentStepNumber][1];
    this.setState({ currentStepNumber, gameState });
  };

  previousMove = () => {
    let { currentStepNumber, gameHistory } = this.state;
    currentStepNumber -= 1;
    this.setGameState(currentStepNumber, gameHistory);
  };

  nextMove = () => {
    let { currentStepNumber, gameHistory } = this.state;
    currentStepNumber += 1;
    this.setGameState(currentStepNumber, gameHistory);
  };

  jumpToTurn = turnNumberToJump => {
    const [currentStepNumber, gameState] = this.getFirstInstanceOfTurn(
      turnNumberToJump
    );
    this.setState({ gameState, currentStepNumber, turnNumberToJump });
  };

  render() {
    const { gameState, turnNumberToJump, turnNumbers } = this.state;
    const { startGame, previousMove, nextMove, jumpToTurn } = this;
    return (
      <div className="App">
        <button
          type="button"
          className="center-block start-game btn btn-primary"
          onClick={startGame}
        >
          Start Game
        </button>
        <button
          type="button"
          className="previous-move btn btn-danger"
          onClick={previousMove}
        >
          Previous Move
        </button>
        <button
          type="button"
          className="next-move btn btn-success"
          onClick={nextMove}
        >
          Next Move
        </button>
        <TurnChooser
          onChange={jumpToTurn}
          turnNumbers={turnNumbers}
          turnNumberToJump={turnNumberToJump}
        />
        <Board gameState={gameState} />
      </div>
    );
  }
}

export default App;
