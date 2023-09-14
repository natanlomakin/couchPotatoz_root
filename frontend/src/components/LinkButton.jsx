import React from "react";
import { NavLink } from "react-router-dom";
import "../static/css/linkButton.css";

const LinkButton = (displayText, address) => {
  return (
    <div className="linkButton-container">
      <NavLink className="link-button" to={address}>
        {displayText}
      </NavLink>
    </div>
  );
};

export default LinkButton;
