import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import "./index.css";
import App from "./App";
import Home from "./pages/Home.jsx";
import Groups from "./pages/Groups";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}>
          <Route path="/" element={<Home />}></Route>
          <Route path="/groups" element={<Groups />}></Route>
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
