import React from "react";

const Space = ({ card }) => {
  const { group, name, price } = card;
  return (
    <div className="space property">
      <div className="container">
        <div className={`color-bar ${group}`} />
        <div className="name">${name}</div>
        <div className="price">Price ${price}</div>
      </div>
    </div>
  );
};

export default Space;
