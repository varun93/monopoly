import React from "react";

const Space = ({
  space,
  index,
  constructions = {},
  playerOnePosition,
  playerTwoPosition
}) => {
  const { monopoly, class: category, name, price, instructions } = space;
  const playerOnePresent = index === playerOnePosition ? true : "";
  const playerTwoPresent = index === playerTwoPosition ? true : "";
  const { numberOfConstructions, owner } = constructions;
  return (
    <div className={`space ${category}`}>
      <div className={`container`}>
        {monopoly && <div className={`color-bar ${monopoly}`} />}
        {name && <div className="name">{name}</div>}
        {numberOfConstructions && (
          <div className="construction-count">{numberOfConstructions}</div>
        )}
        {playerOnePresent && <div className="center-block player-one" />}
        {playerTwoPresent && <div className="center-block player-two" />}
        {price && <div className="price">Price ${price}</div>}
        {instructions && <div className="instructions">{instructions}</div>}
        {owner && <div className={`owner-${owner}`} />}
      </div>
    </div>
  );
};

export default Space;
