import React from "react";

const TurnChooser = ({ turnNumbers, turnNumberToJump, onChange }) => {
  return (
    <select
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
