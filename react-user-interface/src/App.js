import React, { Component } from "react";
import socketIOClient from "socket.io-client";
import Board from "./Board";
import "./App.css";

class App extends Component {
  constructor() {
    super();
    this.state = {
      gameState: [],
      gameHistory: [],
      endpoint: "http://127.0.0.1:5000",
      currentStepNumber: 0
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
      this.setState({ gameHistory: gameHistory.state });
    });
  }

  startGame = () => {
    this.socket.emit("start_game");
  };

  previousMove = () => {
    let { currentStepNumber, gameHistory } = this.state;
    currentStepNumber -= 1;
    const gameState = gameHistory[currentStepNumber];
    console.log(gameState);
    this.setState({ currentStepNumber, gameState: gameState[1] });
  };

  nextMove = () => {
    let { currentStepNumber, gameHistory } = this.state;
    currentStepNumber += 1;
    const gameState = gameHistory[currentStepNumber];
    console.log(gameState, gameHistory);
    this.setState({ currentStepNumber, gameState: gameState[1] });
  };

  render() {
    const { gameState } = this.state;
    const { startGame, previousMove, nextMove } = this;
    return (
      <div className="App">
        <button onClick={startGame}>Start Game</button>
        <button onClick={previousMove}>Previous Move</button>
        <button onClick={nextMove}>Next Move</button>
        <Board gameState={gameState} />
      </div>
    );
  }
}

export default App;
