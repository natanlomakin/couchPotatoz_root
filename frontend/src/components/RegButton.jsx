import React from "react";
import "../static/css/regularButton.css";

const RegButton = (displayText, setType, onClickFunc) => {
  return (
    <div>
      <button type={setType} onClick={onClickFunc} className="regular-button">
        {displayText}
      </button>
    </div>
  );
};

export default RegButton;
