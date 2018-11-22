import React from "react";

const PlayerInfo = ({
  playerOneCash,
  playerTwoCash,
  playerOneDebt,
  playerTwoDebt
}) => {
  return (
    <div className="center">
      <div className="player-one-info">
        <h2 className="label">Player One Info</h2>
        <div>Cash : {playerOneCash}</div>
        <div>Debt : {playerOneDebt}</div>
      </div>
      <div className="player-two-info">
        <h2 className="label">Player Two Info</h2>
        <div>Cash : {playerTwoCash}</div>
        <div>Debt : {playerTwoDebt}</div>
      </div>
    </div>
  );
};

export default PlayerInfo;
