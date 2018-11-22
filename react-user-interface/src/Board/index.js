import React, { Component } from "react";
import * as constants from "./constants";
import Space from "./Space";
import properties from "./properties";
import "./style.css";
import PlayerInfo from "./PlayerInfo";

export default class Board extends Component {
  state = {
    properties,
    game_history: [],
    playerOnePosition: 3,
    playerTwoPosition: 6,
    playerOneCash: 0,
    playerTwoCash: 0,
    constructions: {
      1: { owner: 2, numberOfConstructions: 6 }
    },
    turn: 0
  };

  parsePhaseText = (phaseNumber, payload) => {
    const phaseNameMapping = {
      [constants.BSTM]: "BSTM Phase",
      [constants.TRADE_OFFER]: "Trade",
      [constants.DICE_ROLL]: "Dice Rolled", // dice number
      [constants.BUYING]: "Buying Properties",
      [constants.AUCTION]: "Auctioning Properties", // two tuple; (property_id,winner)
      [constants.PAYMENT]: "Payment", //
      [constants.JAIL]: "In/Out Jail", //yes out of jail
      [constants.CHANCE_CARD]: "Chance Card", //id
      [constants.COMMUNITY_CHEST_CARD]: "Community Card" //id
      // dice)
    };
    const phaseName = phaseNameMapping[phaseNumber];
    console.log(phaseName);

    switch (phaseNumber) {
      case constants.BSTM:
        break;
      case constants.TRADE_OFFER:
        break;
      case constants.DICE_ROLL:
        break;
      case constants.BUYING:
        break;
      case constants.AUCTION:
        break;
      case constants.PAYMENT:
        break;
      case constants.JAIL:
        break;
      case constants.CHANCE_CARD:
        break;
      case constants.COMMUNITY_CHEST_CARD:
        break;
      case constants.JUST_VISTING:
        break;
      default:
        break;
    }
  };

  componentWillReceiveProps(nextProps) {
    //update the state with the incoming props for re-renders
    if (
      nextProps.gameState &&
      JSON.stringify(nextProps.gameState) !==
        JSON.stringify(this.props.gameState)
    ) {
      const [
        turn,
        properties,
        playersPosition,
        playersCash
      ] = nextProps.gameState;

      const constructions = {};

      properties.forEach((element, index) => {
        const propertyValue = Math.abs(element);
        //
        let numberOfConstructions = 0;
        let owner = null;
        if (propertyValue > 0) {
          numberOfConstructions = propertyValue - 1;
          owner = element > 0 ? 1 : 2;
        }
        constructions[index] = { numberOfConstructions, owner };
      });

      this.setState({
        playerOnePosition: playersPosition[0],
        playerTwoPosition: playersPosition[1],
        playerOneCash: playersCash[0],
        playerTwoCash: playersCash[1],
        constructions,
        turn
      });
    }
  }

  render() {
    const {
      properties,
      playerOnePosition,
      playerTwoPosition,
      constructions,
      playerOneCash,
      playerTwoCash
    } = this.state;

    return (
      <div className="table">
        <div className="board">
          <PlayerInfo
            playerOneCash={playerOneCash}
            playerTwoCash={playerTwoCash}
          />
          {/* GO */}
          <Space
            playerOnePosition={playerOnePosition}
            playerTwoPosition={playerTwoPosition}
            index={0}
            key={0}
            constructions={constructions[0]}
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
                  constructions={constructions[1 + index]}
                  key={index + 1}
                />
              ))}
          </div>

          {/* Jail */}
          <Space
            playerOnePosition={playerOnePosition}
            playerTwoPosition={playerTwoPosition}
            space={properties[10]}
            constructions={constructions[10]}
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
                  constructions={constructions[11 + index]}
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
                constructions={constructions[21 + index]}
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
            constructions={constructions[30]}
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
                constructions={constructions[31 + index]}
                space={property}
              />
            ))}
          </div>
        </div>
      </div>
    );
  }
}
