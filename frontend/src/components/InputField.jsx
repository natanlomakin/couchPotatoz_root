import React from "react";

const InputField = (
  inputLabel,
  inputLabelTarget,
  placeholder,
  inputType,
  onChangeFunction
) => {
  return (
    <div>
      <label htmlFor={inputLabelTarget} className="form-label">
        {inputLabel}
      </label>
      <input
        type={inputType}
        className="form-control"
        id={inputLabelTarget}
        placeholder={placeholder}
        onChange={onChangeFunction}
      ></input>
    </div>
  );
};

export default InputField;
