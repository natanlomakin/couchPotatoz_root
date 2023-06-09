import React from "react";
import "../static/css/header.css";
import LinkButton from "./LinkButton";
import RegButton from "./RegButton";
import { removeCookie } from "../utils/cookieUtil";

const Header = () => {
  return (
    <nav className="navbar navbar-expand-lg bg-body-tertiary">
      <div className="container-fluid">
        {LinkButton("HOME", "/")}
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarTogglerDemo02"
          aria-controls="navbarTogglerDemo02"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarTogglerDemo02">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item">{LinkButton("Groups", "/groups")}</li>
            <li className="nav-item">{LinkButton("Games", "/games")}</li>
            <li className="nav-item">{LinkButton("Library", "/library")}</li>
          </ul>
          <div>
            <ul className="navbar-nav">
              <li className="nav-item">{LinkButton("Login", "/login")}</li>
              <li className="nav-item">{LinkButton("Signup", "/signup")}</li>
              <li className="nav-item">
                {RegButton("Sign out", "submit", () => {
                  removeCookie("access_token");
                  removeCookie("refresh_token");
                  window.location.reload();
                })}
              </li>
            </ul>
          </div>
          <form className="d-flex" role="search">
            <input
              className="form-control me-2"
              type="search"
              placeholder="Search"
              aria-label="Search"
            />
            {RegButton("Search", "submit", null)}
          </form>
        </div>
      </div>
    </nav>
  );
};

export default Header;
