import React, { Component } from "react";
import socketIOClient from "socket.io-client";
import Board from "./Board";
import "./App.css";

class App extends Component {
  constructor() {
    super();
    this.state = {
      gameState: [],
      endpoint: "http://127.0.0.1:5000"
    };
  }

  componentDidMount() {
    const { endpoint } = this.state;
    this.socket = socketIOClient(endpoint);
    this.socket.on("connect", function() {
      console.log("Websocket connected!");
    });
    // message handler for the when state changes
    this.socket.on("game_state_updated", gameState => {
      this.setState({ gameState: gameState.state });
    });
  }

  startGame = () => {
    this.socket.emit("start_game");
  };

  render() {
    const { gameState } = this.state;
    const { startGame } = this;
    return (
      <div className="App">
        <button onClick={startGame}>Start Game</button>
        <Board gameState={gameState} />
      </div>
    );
  }
}

export default App;
