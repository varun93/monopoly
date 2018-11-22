import React from "react";

const Space = ({
  space,
  index,
  constructions = {},
  playerOnePosition,
  playerTwoPosition
}) => {
  const { monopoly, class: category, name, price, instructions } = space;
  const playerOneClass = index === playerOnePosition ? "player-one" : "";
  const playerTwoClass = index === playerTwoPosition ? "player-two" : "";
  const { numberOfConstructions, owner } = constructions;
  return (
    <div className={`space ${category}`}>
      <div className={`container ${playerOneClass} ${playerTwoClass}`}>
        {monopoly && <div className={`color-bar ${monopoly}`} />}
        {name && <div className="name">{name}</div>}
        {numberOfConstructions && (
          <div className="construction-count">{numberOfConstructions}</div>
        )}
        {price && <div className="price">Price ${price}</div>}
        {instructions && <div className="instructions">{instructions}</div>}
        {owner && <div className={`owner-${owner}`} />}
      </div>
    </div>
  );
};

export default Space;
