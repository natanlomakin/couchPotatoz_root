import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import "./index.css";
import App from "./App";
import Home from "./pages/Home.jsx";
import Groups from "./pages/Groups";
import Library from "./pages/Library";
import SingleGroup from "./pages/SingleGroup";
import Signup from "./pages/Signup";
import Login from "./pages/Login";
import Games from "./pages/Games";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}>
          <Route path="/" element={<Home />}></Route>
          <Route path="/groups" element={<Groups />}></Route>
          <Route path="/games" element={<Games />}></Route>
          <Route path="/groups/:libraryId" element={<SingleGroup />}></Route>
          <Route path="/library" element={<Library />}></Route>
          <Route path="/signup" element={<Signup />}></Route>
          <Route path="/login" element={<Login />}></Route>
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
