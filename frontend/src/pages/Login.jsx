import React, { useState } from "react";
import Form from "../components/Form";
import axios from "axios";
import { SERVER_URL } from "../utils/serverUtil";
import InputField from "../components/InputField";
import RegButton from "../components/RegButton";
import { setCookie } from "../utils/cookieUtil";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const loginHandle = async (e) => {
    e.preventDefault();
    let result = await axios
      .post(
        SERVER_URL + "/users/login",
        {
          email: email,
          password: password,
        },
        { "Content-Type": "application/json" }
      )
      .then((response) => {
        console.log(response);
        setCookie("access_token", response.data.data.access_token);
        setCookie("refresh_token", response.data.data.refresh_token);
        window.location.reload();
      });
  };

  return (
    <div>
      <form onSubmit={loginHandle} className="row g-3">
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
        <div className="col-12">{RegButton("Login", "submit", null)}</div>
      </form>
    </div>
  );
};

export default Login;
