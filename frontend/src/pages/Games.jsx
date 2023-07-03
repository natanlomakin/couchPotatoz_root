import React, { useEffect, useState } from "react";
import axios from "axios";
import { SERVER_URL } from "../utils/serverUtil";
import { getCookie } from "../utils/cookieUtil";
import { parseJwt } from "../utils/tokenDecodeUtil";
import RegButton from "../components/RegButton";

const Games = () => {
  const [userId, setUserId] = useState("");
  const [gamesData, setGamesData] = useState([]);
  const [isUserLoggedIn, setIsUserLoggedIn] = useState(false);
  const [gameIds, setGameIds] = useState([]);
  const [userGamesData, setUserGamesData] = useState([]);
  const [gamePlatformId, setGamePlatformId] = useState("");

  useEffect(() => {
    if (getCookie("access_token")) {
      setUserId(parseJwt(getCookie("access_token")).sub);
      setIsUserLoggedIn(true);
    }
    const server_data = async () => {
      const response = await axios(SERVER_URL + "/games/", {
        headers: {
          authorization: "Bearer " + getCookie("access_token"),
        },
        Accept: "application/json",
        "Content-Type": "application/json",
      }).then((res) => {
        setGamesData(res.data.data);
        setGameIds(res.data.gameIds);
      });
    };
    server_data();
  }, []);

  const isGameInLibrary = async (gameId, platformId) => {
    if (isUserLoggedIn) {
      const response = await axios(SERVER_URL + "/librarys/" + userId, {
        headers: {
          authorization: "Bearer " + getCookie("access_token"),
        },
        Accept: "application/json",
        "Content-Type": "application/json",
      });
      setUserGamesData(response.data.data);
      for (let i = 0; i < response.data.data.length; i++) {
        if (response.data.data[i].game_id == gameId) {
          console.log("alredy in library");
          return false;
        }
      }
      addGameToLibrary(gameId, platformId);
      console.log("added");
    } else {
      console.log("log in");
    }
  };

  const addGameToLibrary = async (gameId, platformId) => {
    const response = await axios.post(
      SERVER_URL + "/librarys/",
      { user_id: userId, game_id: gameId, platform_id: platformId },
      {
        headers: {
          authorization: "Bearer " + getCookie("access_token"),
        },
        Accept: "application/json",
        "Content-Type": "application/json",
      }
    );
  };

  return (
    <div>
      {gamesData.map((game, ind) => (
        <div key={ind}>
          <h2>{game.title}</h2>
          <img
            style={{ blockSize: "250px" }}
            src={game.thumbnail_url}
            alt="none"
          ></img>
          <h4>{game.genre}</h4>
          {RegButton("Add", "submit", () =>
            isGameInLibrary(gameIds[ind], game.platform_id)
          )}
        </div>
      ))}
      <h1></h1>
    </div>
  );
};

export default Games;
