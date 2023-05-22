import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../components/Header";
import axios from "axios";
import { SERVER_URL } from "../utils/serverUtil";
import LibraryGameContext from "../App";
import userLibrarys from "../App";

const Library = () => {
  const [user, setUser] = useState("");
  const [userLibrarys, setuserLibrarys] = useState([]);
  const [userLibrarysGames, setuserLibrarysGames] = useState([]);
  const [isLibraryUpdated, setIsLibraryUpdated] = useState(false);
  const { userId } = useParams();

  useEffect(() => {
    setIsLibraryUpdated(false);
    const server_data = async () => {
      const response = await axios(SERVER_URL + "/librarys/" + userId, {
        Accept: "application/json",
        "Content-Type": "application/json",
      });
      setuserLibrarys(response.data.data);
    };
    server_data();
  }, [isLibraryUpdated]);

  useEffect(() => {
    setIsLibraryUpdated(false);
    const result = [];
    const libraryGameData = async () => {
      for (let i = 0; i < userLibrarys.length; i++) {
        result.push(
          await axios(SERVER_URL + "/games/" + userLibrarys[i].game_id)
        );
      }
      setuserLibrarysGames(result);
    };
    libraryGameData();
  }, [userLibrarys]);

  return (
    <div>
      <div className="mainContainer">
        <h1>Library</h1>
        {userLibrarysGames.map((game, ind) => (
          <div className="test" key={ind}>
            <h2>{game.data.data.title}</h2>
            <img src={game.data.data.thumbnail_url} alt="" />
          </div>
        ))}
        <h3>test</h3>
      </div>
    </div>
  );
};

export default Library;
