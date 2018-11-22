import React from "react";

const PlayerInfo = ({ cash, debt }) => {
  return (
    <div className="center">
      <div className="player-one-info">
        <h2 className="label">Player One Info</h2>
        <div>Cash : $30</div>
        <div>Debt : $0</div>
      </div>
      <div className="player-two-info">
        <h2 className="label">Player Two Info</h2>
        <div>Cash : $50</div>
        <div>Debt : $0</div>
      </div>
    </div>
  );
};

export default PlayerInfo;
