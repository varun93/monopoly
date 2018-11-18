import React from "react";

const Space = ({ space, index, playerOnePosition, playerTwoPosition }) => {
  const { monopoly, class: category, name, price, instructions } = space;
  const playerOneClass = index === playerOnePosition ? "player-one" : "";
  const playerTwoClass = index === playerTwoPosition ? "player-two" : "";
  return (
    <div className={`space ${category}`}>
      <div className={`container ${playerOneClass} ${playerTwoClass}`}>
        {monopoly && <div className={`color-bar ${monopoly}`} />}
        {name && <div className="name">{name}</div>}
        {price && <div className="price">Price ${price}</div>}
        {instructions && <div className="instructions">{instructions}</div>}
      </div>
    </div>
  );
};

export default Space;
