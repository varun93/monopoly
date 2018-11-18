import React, { Component } from "react";
import Space from "./Space";
import properties from "./properties";
import "./style.css";

export default class Board extends Component {
  state = {
    properties,
    game_history: [],
    playerOnePosition: 3,
    playerTwoPosition: 6,
    playerOneCash: 0,
    playerTwoCash: 0,
    turn: 0
  };

  componentWillReceiveProps(previousProps, nextProps) {
    //update the state with the incoming props for re-renders
    if (
      JSON.stringify(previousProps.gameState) !==
      JSON.stringify(nextProps.gameState)
    ) {
      const [
        turn,
        properties,
        playersPosition,
        playersCash,
        ...rest
      ] = nextProps;
      this.setState({
        playerOnePosition: playersPosition[0],
        playerTwoPosition: playersPosition[1],
        playerOneCash: playersCash[0],
        playerTwoCash: playersCash[1],
        turn
      });
    }
  }

  render() {
    const { properties, playerOnePosition, playerTwoPosition } = this.state;
    return (
      <div className="table">
        <div className="board">
          <div className="center" />
          {/* GO */}
          <Space
            playerOnePosition={playerOnePosition}
            playerTwoPosition={playerTwoPosition}
            index={0}
            key={0}
            space={properties[0]}
          />

          <div className="row horizontal-row bottom-row">
            {properties
              .slice(1, 10)
              .reverse()
              .map((property, index) => (
                <Space
                  playerOnePosition={playerOnePosition}
                  playerTwoPosition={playerTwoPosition}
                  space={property}
                  index={1 + index}
                  key={index + 1}
                />
              ))}
          </div>

          {/* Jail */}
          <Space
            playerOnePosition={playerOnePosition}
            playerTwoPosition={playerTwoPosition}
            space={properties[10]}
            index={10}
            key={10}
          />

          <div className="row vertical-row left-row">
            {properties
              .slice(11, 20)
              .reverse()
              .map((property, index) => (
                <Space
                  playerOnePosition={playerOnePosition}
                  playerTwoPosition={playerTwoPosition}
                  space={property}
                  index={11 + index}
                  key={11 + index}
                />
              ))}
          </div>

          {/* Free Parking */}
          <Space space={properties[20]} index={20} key={20} />

          <div className="row horizontal-row top-row">
            {properties.slice(21, 30).map((property, index) => (
              <Space
                playerOnePosition={playerOnePosition}
                playerTwoPosition={playerTwoPosition}
                space={property}
                index={21 + index}
                key={21 + index}
              />
            ))}
          </div>

          {/* Jail */}
          <Space
            playerOnePosition={playerOnePosition}
            playerTwoPosition={playerTwoPosition}
            space={properties[30]}
            index={30}
            key={30}
          />

          <div className="row vertical-row right-row">
            {properties.slice(31).map((property, index) => (
              <Space
                playerOnePosition={playerOnePosition}
                playerTwoPosition={playerTwoPosition}
                index={31 + index}
                key={31 + index}
                space={property}
              />
            ))}
          </div>
        </div>
      </div>
    );
  }
}
