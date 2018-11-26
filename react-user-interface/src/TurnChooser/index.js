import React from "react";

const TurnChooser = ({ turnNumbers, turnNumberToJump, onChange }) => {
  turnNumbers = turnNumbers.length ? turnNumbers : ["Jump to Turn"];
  return (
    <select
      style={{ fontSize: "16px" }}
      className="custom-select"
      onChange={event => onChange(event.target.value)}
      value={turnNumberToJump}
    >
      {turnNumbers.map(turnNumber => {
        return (
          <option key={turnNumber} value={turnNumber}>
            {turnNumber}
          </option>
        );
      })}
    </select>
  );
};

export default TurnChooser;
