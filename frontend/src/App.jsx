import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import { Outlet } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Friends from "./components/Friends";

function App() {
  return (
    <div className="App">
      <Header />
      <Outlet />
      <hr />
      <Friends />
      <Footer />
    </div>
  );
}

export default App;
