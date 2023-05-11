import React from "react";
import { NavLink } from "react-router-dom";

const LinkButton = (displayText, address) => {
  return (
    <div>
      <NavLink className="btn btn-outline-warning" to={address}>
        {displayText}
      </NavLink>
    </div>
  );
};

export default LinkButton;
