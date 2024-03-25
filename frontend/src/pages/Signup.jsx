import Form from "../components/Form";
import axios from "axios";
import { SERVER_URL } from "../utils/serverUtil";
import React, { useEffect, useState } from "react";
import InputField from "../components/InputField";
import RegButton from "../components/RegButton";

const Signup = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [userName, setUserName] = useState("");
  const [profileImage, setProfileImage] = useState("");

  const signupHandle = async (e) => {
    e.preventDefault();
    const response = await axios
      .post(SERVER_URL + "/users/signup", {
        email: email,
        password: password,
        firstName: firstName,
        lastName: lastName,
        userName: userName,
        profile_image_url: profileImage,
      })
      .then(window.location.replace("http://localhost:5173/login"));
  };
  return (
    <div>
      <form onSubmit={signupHandle} className="row g-3">
        <div className="col-md-6">
          {InputField("Email", "inputEmail4", "email@gmail.com", "email", (e) =>
            setEmail(e.target.value)
          )}
        </div>
        <div className="col-md-6">
          {InputField("Password", "inputPassword4", "", "password", (e) =>
            setPassword(e.target.value)
          )}
        </div>
        <div className="col-md-6">
          {InputField("First name", "inputFirstName", "john", "text", (e) =>
            setFirstName(e.target.value)
          )}
        </div>
        <div className="col-md-6">
          {InputField("Last name", "inputLastName", "doe", "text", (e) =>
            setLastName(e.target.value)
          )}
        </div>
        <div className="col-md-6">
          {InputField("User name", "inputUserName", "jd", "text", (e) =>
            setUserName(e.target.value)
          )}
        </div>
        <div className="col-12">
          {InputField(
            "Profile photo",
            "inputProfileImage",
            "No file chosen",
            "file",
            (e) => setProfileImage(e.target.value)
          )}
        </div>
        <div className="col-12">{RegButton("Sign up", "submit", null)}</div>
      </form>
    </div>
  );
};

export default Signup;
