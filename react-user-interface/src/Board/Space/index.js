import React from "react";

const Space = ({ space, playerPosition }) => {
  const { monopoly, class: category, name, price, instructions } = space;
  return (
    <div className={`space ${category}`}>
      <div className="container">
        {monopoly && <div className={`color-bar ${monopoly}`} />}
        {name && <div className="name">{name}</div>}
        {price && <div className="price">Price ${price}</div>}
        {instructions && <div className="instructions">{instructions}</div>}
      </div>
    </div>
  );
};

export default Space;
