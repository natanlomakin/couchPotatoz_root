import React, { useState } from "react";
import "../static/css/header.css";
import LinkButton from "./LinkButton";
import RegButton from "./RegButton";
import { removeCookie } from "../utils/cookieUtil";
import logo from "../assets/react.svg";
import { SERVER_URL } from "../utils/serverUtil";

const Header = () => {
  const [hamburgerCssClass, setHamburgerCssClass] = useState("hamburger");
  const [linkItemsCssClass, setLinkItemsCssClass] = useState("header-links");

  const navBarHamburgerActiveHandle = () => {
    setHamburgerCssClass("hamburger-active");
    setLinkItemsCssClass("header-links-active");
  };

  const navBarHamburgerHandle = () => {
    setHamburgerCssClass("hamburger");
    setLinkItemsCssClass("header-links");
  };

  return (
    <div className="header-container">
      <img className="logo" src={logo} alt="logo" />
      <nav>
        <div
          onClick={() => {
            hamburgerCssClass === "hamburger"
              ? navBarHamburgerActiveHandle()
              : navBarHamburgerHandle();
          }}
          className={hamburgerCssClass}
        >
          <span className="bar"></span>
          <span className="bar"></span>
          <span className="bar"></span>
        </div>
        <ul className={linkItemsCssClass}>
          <li
            onClick={() => {
              setHamburgerCssClass("hamburger");
              setLinkItemsCssClass("header-links");
            }}
            className="link-item"
          >
            {LinkButton("Home", "/")}
          </li>
          <li
            onClick={() => {
              setHamburgerCssClass("hamburger");
              setLinkItemsCssClass("header-links");
            }}
            className="link-item"
          >
            {LinkButton("Groups", "/groups")}
          </li>
          <li
            onClick={() => {
              setHamburgerCssClass("hamburger");
              setLinkItemsCssClass("header-links");
            }}
            className="link-item"
          >
            {LinkButton("Games", "/games")}
          </li>
          <li
            onClick={() => {
              setHamburgerCssClass("hamburger");
              setLinkItemsCssClass("header-links");
            }}
            className="link-item"
          >
            {LinkButton("Library", "/library")}
          </li>
        </ul>
      </nav>
      <nav>
        <ul className={linkItemsCssClass}>
          <li
            onClick={() => {
              setHamburgerCssClass("hamburger");
              setLinkItemsCssClass("header-links");
            }}
            className="link-item"
          >
            {LinkButton("Login", "/login")}
          </li>
          <li
            onClick={() => {
              setHamburgerCssClass("hamburger");
              setLinkItemsCssClass("header-links");
            }}
            className="link-item"
          >
            {LinkButton("Signup", "/signup")}
          </li>
          <li
            onClick={() => {
              setHamburgerCssClass("hamburger");
              setLinkItemsCssClass("header-links");
            }}
            className="link-item"
          >
            {RegButton("Sign out", "submit", () => {
              removeCookie("access_token");
              removeCookie("refresh_token");
              window.location.replace("http://localhost:5173/login");
            })}
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Header;
