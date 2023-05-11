import React from "react";

const RegButton = (displayText, setType, onClickFunc) => {
  return (
    <div>
      <button type={setType} onClick={onClickFunc} className="btn btn-secondary">
        {displayText}
      </button>
    </div>
  );
};

export default RegButton;
