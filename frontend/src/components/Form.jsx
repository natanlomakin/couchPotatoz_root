import React from "react";
import InputField from "./InputField";
import RegButton from "./RegButton";

const Form = (formTarget, onSubmitFunction) => {
  const [email, setEmail] = useState("");
  return (
    <div>
      {formTarget == "signup" ? (
        <form onSubmit={onSubmitFunction} className="row g-3">
          <div className="col-md-6">
            {InputField(
              "Email",
              "inputEmail4",
              "email@gmail.com",
              "email",
              (e) => setEmail(e.target.value)
            )}
          </div>
          <div className="col-md-6">
            {InputField("Password", "inputPassword4", "", "password")}
          </div>
          <div className="col-md-6">
            {InputField("First name", "inputFirstName", "john", "text")}
          </div>
          <div className="col-md-6">
            {InputField("Last name", "inputLastName", "doe", "text")}
          </div>
          <div className="col-md-6">
            {InputField("User name", "inputUserName", "jd", "text")}
          </div>
          <div className="col-12">
            {InputField(
              "Profile photo",
              "inputProfileImage",
              "No file chosen",
              "file"
            )}
          </div>
          <div className="col-12">{RegButton("Sign up", "submit", null)}</div>
        </form>
      ) : (
        <form className="row g-3">
          <div className="col-md-6">
            {InputField("Email", "inputEmail4", "email@gmail.com", "email")}
          </div>
          <div className="col-md-6">
            {InputField("Password", "inputPassword4", "", "password")}
          </div>
          <div className="col-12">{RegButton("Sign up", "submit", null)}</div>
        </form>
      )}
    </div>
  );
};

export default Form;
