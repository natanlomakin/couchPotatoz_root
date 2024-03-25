import React, { useEffect, useState } from "react";
import axios from "axios";
import { SERVER_URL } from "../utils/serverUtil";
import { getCookie } from "../utils/cookieUtil";
import { parseJwt } from "../utils/tokenDecodeUtil";
import RegButton from "../components/RegButton";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "../static/css/games.css";

const Games = () => {
  const [userId, setUserId] = useState("");
  const [gamesData, setGamesData] = useState([]);
  const [isUserLoggedIn, setIsUserLoggedIn] = useState(false);
  const [gameIds, setGameIds] = useState([]);
  const [userGamesData, setUserGamesData] = useState([]);
  const [gamePlatformId, setGamePlatformId] = useState("");
  const [gameSearchValue, setgameSearchValue] = useState("");
  const [gameGenres, setGameGenres] = useState([]);
  const [filterGamesByGenre, setFilterGamesByGenre] = useState("");

  const addedGameToastify = () =>
    toast.success("Added to library", { position: "top-center" });
  const failedToAddGameToastify = (text) =>
    toast.error(text, { position: "top-center" });

  useEffect(() => {
    if (getCookie("access_token")) {
      setUserId(parseJwt(getCookie("access_token")).sub);
      setIsUserLoggedIn(true);
    }
  }, []);

  useEffect(() => {
    const server_data = async () => {
      const response = gameSearchValue
        ? await axios(SERVER_URL + "/games/search/" + gameSearchValue, {
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
            },
          })
        : await axios(SERVER_URL + "/games/", {
            headers: {
              authorization: "Bearer " + getCookie("access_token"),
            },
            Accept: "application/json",
            "Content-Type": "application/json",
          });
      setGamesData(response.data.data);
      setGameIds(response.data.gameIds);
    };
    server_data();
  }, [gameSearchValue]);

  for (let i = 0; i < gamesData.length; i++) {
    if (!gameGenres.includes(gamesData[i].genre)) {
      gameGenres.push(gamesData[i].genre);
    }
  }

  const handleFilterGames = (e) => {
    setFilterGamesByGenre(e.target.value);
  };

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
          failedToAddGameToastify("Game already in library");
          return false;
        }
      }
      addedGameToastify();
      addGameToLibrary(gameId, platformId);
    } else {
      failedToAddGameToastify("Please login first");
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
    <div className="main-container">
      <div className="game-search">
        <input
          id="game-search"
          className="game-search-input"
          type="text"
          placeholder="Game title"
          autoComplete={"false"}
          onChange={(e) => {
            setgameSearchValue(e.target.value);
          }}
        ></input>
        <label className="input-label" htmlFor="game-search">
          Search{" "}
        </label>
      </div>
      <div className="game-genre-filter">
        <select onChange={handleFilterGames}>
          <option value={""}>None</option>
          {gameGenres.map((genre) => (
            <option
              value={genre}
              //onClick={(e) => handleFilterGames(e.eventPhase.value)}
            >
              {genre}
            </option>
          ))}
        </select>
      </div>
      <div className="games-view">
        {filterGamesByGenre
          ? gamesData
              .filter((game) => {
                let countGenres = 0;
                if (game.genre === filterGamesByGenre) {
                  countGenres++;
                  if (countGenres > 0) {
                    return true;
                  } else {
                    return false;
                  }
                }
              })
              .map((game, ind) => (
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
              ))
          : gamesData.map((game, ind) => (
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
      </div>
      <ToastContainer autoClose={2000} />
    </div>
  );
};

export default Games;
