import React, { Component } from "react";
import Property from "./Property";
import "./style.css";

export default class Board extends Component {
  constructor(props, context) {
    super(props, context);

    const property1 = new Property("Go", "corner", null, [null], null);
    const property2 = new Property(
      "Old Kent Rd",
      "brown",
      60,
      [2, 4, 10, 30, 90, 160, 250],
      50
    );
    const property3 = new Property(
      "Community Chest",
      "bonus",
      null,
      [null],
      null
    );
    const property4 = new Property(
      "Whitechapel Road",
      "brown",
      60,
      [4, 8, 20, 60, 180, 320, 450],
      50
    );
    const property5 = new Property("Income Tax", "tax", null, [200], null);
    const property6 = new Property(
      "Kings Cross Station",
      "station",
      200,
      [25, 50, 100, 200],
      null
    );
    const property7 = new Property(
      "The Angel, Islington",
      "sky_blue",
      100,
      [6, 12, 30, 90, 270, 400, 550],
      50
    );
    const property8 = new Property("Chance", "bonus", null, [null], null);
    const property9 = new Property(
      "Euston Road",
      "sky_blue",
      100,
      [6, 12, 30, 90, 270, 400, 550],
      50
    );
    const property10 = new Property(
      "Pentonville Road",
      "sky_blue",
      120,
      [8, 16, 40, 100, 300, 450, 600],
      50
    );
    const property11 = new Property("Jail", "corner", null, [null], null);
    const property12 = new Property(
      "Pall Mall",
      "pink",
      140,
      [10, 20, 50, 150, 450, 625, 750],
      100
    );
    const property13 = new Property(
      "Electric Company",
      "utility",
      150,
      [0, 4, 10],
      null
    );
    const property14 = new Property(
      "Whitehall",
      "pink",
      140,
      [10, 20, 50, 150, 450, 625, 750],
      100
    );
    const property15 = new Property(
      "N'th'land Avenue",
      "pink",
      160,
      [12, 24, 60, 180, 500, 700, 900],
      100
    );
    const property16 = new Property(
      "Marylebone Station",
      "station",
      200,
      [25, 50, 100, 200],
      null
    );
    const property17 = new Property(
      "Bow Street",
      "orange",
      180,
      [14, 28, 70, 200, 550, 750, 950],
      100
    );
    const property18 = new Property(
      "Community Chest",
      "bonus",
      null,
      [null],
      null
    );
    const property19 = new Property(
      "M'b'r'gh Street",
      "orange",
      180,
      [14, 28, 70, 200, 550, 750, 950],
      100
    );
    const property20 = new Property(
      "Vine Street",
      "orange",
      200,
      [16, 32, 80, 220, 600, 800, 1000],
      100
    );
    const property21 = new Property(
      "Free Parking",
      "corner",
      null,
      [null],
      null
    );
    const property22 = new Property(
      "Strand",
      "red",
      220,
      [18, 36, 90, 250, 700, 875, 1050],
      150
    );
    const property23 = new Property("Chance", "bonus", null, [null], null);
    const property24 = new Property(
      "Fleet Street",
      "red",
      220,
      [18, 36, 90, 250, 700, 875, 1050],
      150
    );
    const property25 = new Property(
      "Trafalgar Square",
      "red",
      240,
      [20, 40, 100, 300, 750, 925, 1100],
      150
    );
    const property26 = new Property(
      "Fenchurch St Station",
      "station",
      200,
      [25, 50, 100, 200],
      null
    );
    const property27 = new Property(
      "Leicester Square",
      "yellow",
      260,
      [22, 44, 110, 330, 800, 975, 1150],
      150
    );
    const property28 = new Property(
      "Coventry Street",
      "yellow",
      260,
      [22, 44, 110, 330, 800, 975, 1150],
      150
    );
    const property29 = new Property(
      "Water Works",
      "utility",
      150,
      [0, 4, 10],
      null
    );
    const property30 = new Property(
      "Picadilly",
      "yellow",
      280,
      [22, 44, 120, 360, 850, 1025, 1200],
      150
    );
    const property31 = new Property("Go To Jail", "corner", null, [null], null);
    const property32 = new Property(
      "Regent Street",
      "green",
      300,
      [26, 52, 130, 390, 900, 1100, 1275],
      200
    );
    const property33 = new Property(
      "Oxford Street",
      "green",
      300,
      [26, 52, 130, 390, 900, 1100, 1275],
      200
    );
    const property34 = new Property(
      "Community Chest",
      "bonus",
      null,
      [null],
      null
    );
    const property35 = new Property(
      "Bond Street",
      "green",
      320,
      [28, 56, 150, 450, 1000, 1200, 1400],
      200
    );
    const property36 = new Property(
      "Liverpool St Station",
      "station",
      200,
      [25, 50, 100, 200],
      null
    );
    const property37 = new Property("Chance", "bonus", null, [null], null);
    const property38 = new Property(
      "Park Lane",
      "dark_blue",
      350,
      [35, 70, 175, 500, 1100, 1300, 1500],
      200
    );
    const property39 = new Property("Super Tax", "tax", null, [100], null);
    const property40 = new Property(
      "Mayfair",
      "dark_blue",
      400,
      [50, 100, 200, 600, 1400, 1700, 2000],
      200
    );

    this.properties = [
      property1,
      property2,
      property3,
      property4,
      property5,
      property6,
      property7,
      property8,
      property9,
      property10,
      property11,
      property12,
      property13,
      property14,
      property15,
      property16,
      property17,
      property18,
      property19,
      property20,
      property21,
      property22,
      property23,
      property24,
      property25,
      property26,
      property27,
      property28,
      property29,
      property30,
      property31,
      property32,
      property33,
      property34,
      property35,
      property36,
      property37,
      property38,
      property39,
      property40
    ];
  }

  render() {
    return (
      <div className="table">
        <div className="board">
          <div className="center">
            <div className="community-chest-deck">
              <h2 className="label">Community Chest</h2>
              <div className="deck" />
            </div>
            <h1 className="title">MONOPOLY</h1>
            <div className="chance-deck">
              <h2 className="label">Chance</h2>
              <div className="deck" />
            </div>
          </div>

          <div className="space corner go">
            <div className="container">
              <div className="instructions">
                Collect $200.00 salary as you pass
              </div>
              <div className="go-word">go</div>
            </div>
            <div className="arrow fa fa-long-arrow-left" />
          </div>

          <div className="row horizontal-row bottom-row">
            <div className="space property">
              <div className="container">
                <div className="color-bar light-blue" />
                <div className="name">Connecticut Avenue</div>
                <div className="price">PRICE $120</div>
              </div>
            </div>
            <div className="space property">
              <div className="container">
                <div className="color-bar light-blue" />
                <div className="name">Vermont Avenue</div>
                <div className="price">Price $100</div>
              </div>
            </div>
            <div className="space chance">
              <div className="container">
                <div className="name">Chance</div>
                <i className="drawing fa fa-question" />
              </div>
            </div>
            <div className="space property">
              <div className="container">
                <div className="color-bar light-blue" />
                <div className="name">Oriental Avenue</div>
                <div className="price">Price $100</div>
              </div>
            </div>
            <div className="space railroad">
              <div className="container">
                <div className="name">Reading Railroad</div>
                <i className="drawing fa fa-subway" />
                <div className="price">Price $200</div>
              </div>
            </div>
            <div className="space fee income-tax">
              <div className="container">
                <div className="name">Income Tax</div>
                <div className="diamond" />
                <div className="instructions">
                  Pay 10%
                  <br />
                  or
                  <br />
                  $200
                </div>
              </div>
            </div>
            <div className="space property">
              <div className="container">
                <div className="color-bar dark-purple" />
                <div className="name">Baltic Avenue</div>
                <div className="price">Price $50</div>
              </div>
            </div>
            <div className="space community-chest">
              <div className="container">
                <div className="name">Community Chest</div>
                <i className="drawing fa fa-cube" />
                <div className="instructions">
                  Follow instructions on top card
                </div>
              </div>
            </div>
            <div className="space property">
              <div className="container">
                <div className="color-bar dark-purple" />
                <div className="name three-line-name">
                  Mediter-
                  <br />
                  ranean
                  <br />
                  Avenue
                </div>
                <div className="price">Price $50</div>
              </div>
            </div>
          </div>

          <div className="space corner jail">
            <div className="just">Just</div>
            <div className="drawing">
              <div className="container">
                <div className="name">In</div>
                <div className="window">
                  <div className="bar" />
                  <div className="bar" />
                  <div className="bar" />
                  <i className="person fa fa-frown-o" />
                </div>
                <div className="name">Jail</div>
              </div>
            </div>
            <div className="visiting">Visiting</div>
          </div>

          <div className="row vertical-row left-row">
            <div className="space property">
              <div className="container">
                <div className="color-bar orange" />
                <div className="name">New York Avenue</div>
                <div className="price">Price $200</div>
              </div>
            </div>
            <div className="space property">
              <div className="container">
                <div className="color-bar orange" />
                <div className="name">Tennessee Avenue</div>
                <div className="price">Price $180</div>
              </div>
            </div>
            <div className="space community-chest">
              <div className="container">
                <div className="name">Community Chest</div>
                <i className="drawing fa fa-cube" />
                <div className="instructions">
                  Follow instructions on top card
                </div>
              </div>
            </div>
            <div className="space property">
              <div className="container">
                <div className="color-bar orange" />
                <div className="name">St. James Avenue</div>
                <div className="price">Price $180</div>
              </div>
            </div>
            <div className="space railroad">
              <div className="container">
                <div className="name long-name">Pennsylvania Railroad</div>
                <i className="drawing fa fa-subway" />
                <div className="price">Price $200</div>
              </div>
            </div>
            <div className="space property">
              <div className="container">
                <div className="color-bar purple" />
                <div className="name">Virginia Avenue</div>
                <div className="price">Price $160</div>
              </div>
            </div>
            <div className="space property">
              <div className="container">
                <div className="color-bar purple" />
                <div className="name">States Avenue</div>
                <div className="price">Price $140</div>
              </div>
            </div>
            <div className="space utility electric-company">
              <div className="container">
                <div className="name">Electric Company</div>
                <i className="drawing fa fa-lightbulb-o" />
                <div className="price">Price $150</div>
              </div>
            </div>
            <div className="space property">
              <div className="container">
                <div className="color-bar purple" />
                <div className="name">St. Charles Place</div>
                <div className="price">Price $140</div>
              </div>
            </div>
          </div>

          <div className="space corner free-parking">
            <div className="container">
              <div className="name">Free</div>
              <i className="drawing fa fa-car" />
              <div className="name">Parking</div>
            </div>
          </div>

          <div className="row horizontal-row top-row">
            <div className="space property">
              <div className="container">
                <div className="color-bar red" />
                <div className="name">Kentucky Avenue</div>
                <div className="price">Price $220</div>
              </div>
            </div>
            <div className="space chance">
              <div className="container">
                <div className="name">Chance</div>
                <i className="drawing fa fa-question blue" />
              </div>
            </div>
            <div className="space property">
              <div className="container">
                <div className="color-bar red" />
                <div className="name">Indiana Avenue</div>
                <div className="price">Price $220</div>
              </div>
            </div>
            <div className="space property">
              <div className="container">
                <div className="color-bar red" />
                <div className="name">Illinois Avenue</div>
                <div className="price">Price $200</div>
              </div>
            </div>
            <div className="space railroad">
              <div className="container">
                <div className="name">B & O Railroad</div>
                <i className="drawing fa fa-subway" />
                <div className="price">Price $200</div>
              </div>
            </div>
            <div className="space property">
              <div className="container">
                <div className="color-bar yellow" />
                <div className="name">Atlantic Avenue</div>
                <div className="price">Price $260</div>
              </div>
            </div>
            <div className="space property">
              <div className="container">
                <div className="color-bar yellow" />
                <div className="name">Ventnor Avenue</div>
                <div className="price">Price $260</div>
              </div>
            </div>
            <div className="space utility waterworks">
              <div className="container">
                <div className="name">Waterworks</div>
                <i className="drawing fa fa-tint" />
                <div className="price">Price $120</div>
              </div>
            </div>
            <div className="space property">
              <div className="container">
                <div className="color-bar yellow" />
                <div className="name">Marvin Gardens</div>
                <div className="price">Price $280</div>
              </div>
            </div>
          </div>

          <div className="space corner go-to-jail">
            <div className="container">
              <div className="name">Go To</div>
              <i className="drawing fa fa-gavel" />
              <div className="name">Jail</div>
            </div>
          </div>

          <div className="row vertical-row right-row">
            <div className="space property">
              <div className="container">
                <div className="color-bar green" />
                <div className="name">Pacific Avenue</div>
                <div className="price">Price $300</div>
              </div>
            </div>
            <div className="space property">
              <div className="container">
                <div className="color-bar green" />
                <div className="name three-line-name">
                  North Carolina Avenue
                </div>
                <div className="price">Price $300</div>
              </div>
            </div>
            <div className="space community-chest">
              <div className="container">
                <div className="name">Community Chest</div>
                <i className="drawing fa fa-cube" />
                <div className="instructions">
                  Follow instructions on top card
                </div>
              </div>
            </div>
            <div className="space property">
              <div className="container">
                <div className="color-bar green" />
                <div className="name long-name">Pennsylvania Avenue</div>
                <div className="price">Price $320</div>
              </div>
            </div>
            <div className="space railroad">
              <div className="container">
                <div className="name">Short Line</div>
                <i className="drawing fa fa-subway" />
                <div className="price">Price $200</div>
              </div>
            </div>
            <div className="space chance">
              <div className="container">
                <div className="name">Chance</div>
                <i className="drawing fa fa-question" />
              </div>
            </div>
            <div className="space property">
              <div className="container">
                <div className="color-bar dark-blue" />
                <div className="name">Park Place</div>
                <div className="price">Price $350</div>
              </div>
            </div>
            <div className="space fee luxury-tax">
              <div className="container">
                <div className="name">Luxury Tax</div>
                <div className="drawing fa fa-diamond" />
                <div className="instructions">Pay $75.00</div>
              </div>
            </div>
            {/*  */}
            <div className="space property">
              <div className="container">
                <div className="color-bar dark-blue" />
                <div className="name">Boardwalk</div>
                <div className="price">Price $400</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
