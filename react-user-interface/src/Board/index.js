import React, { Component } from "react";
import Space from "./Space";
import properties from "./properties";
import "./style.css";

export default class Board extends Component {
  render() {
    return (
      <div className="table">
        <div className="board">
          <div className="center" />
          {/* GO */}
          <Space space={properties[0]} />

          <div className="row horizontal-row bottom-row">
            {properties.slice(1, 10).map(property => (
              <Space space={property} />
            ))}
          </div>

          {/* JAIL */}
          <Space space={properties[10]} />

          <div className="row vertical-row left-row">
            {properties.slice(11, 20).map(property => (
              <Space space={property} />
            ))}
          </div>

          {/* Free Parking */}
          <Space space={properties[20]} />

          <div className="row horizontal-row top-row">
            {properties.slice(21, 30).map(property => (
              <Space space={property} />
            ))}
          </div>

          {/* Jail */}
          <Space space={properties[30]} />

          <div className="row vertical-row right-row">
            {properties.slice(31).map(property => (
              <Space space={property} />
            ))}
          </div>
        </div>
      </div>
    );
  }
}
