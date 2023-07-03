import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../components/Header";
import axios from "axios";
import { SERVER_URL } from "../utils/serverUtil";
import LibraryGameContext from "../App";
import userLibrarys from "../App";
import { getCookie } from "../utils/cookieUtil";
import { parseJwt } from "../utils/tokenDecodeUtil";
import RegButton from "../components/RegButton";

const Library = () => {
  const [user, setUser] = useState("");
  const [userLibrarys, setuserLibrarys] = useState([]);
  const [userLibraryIds, setUserLibraryIds] = useState([]);
  const [userLibrarysGames, setuserLibrarysGames] = useState([]);
  const [isLibraryUpdated, setIsLibraryUpdated] = useState(false);
  const [userId, setUserId] = useState("");
  const [isUserLoggedIn, setIsUserLoggedIn] = useState(false);

  useEffect(() => {
    setIsLibraryUpdated(false);
    const server_data = async () => {
      const response = await axios(SERVER_URL + "/librarys/" + userId, {
        headers: {
          authorization: "Bearer " + getCookie("access_token"),
        },
        Accept: "application/json",
        "Content-Type": "application/json",
      });
      setuserLibrarys(response.data.data);
      setUserLibraryIds(response.data.library_ids);
    };
    if (getCookie("access_token")) {
      setUserId(parseJwt(getCookie("access_token")).sub);
      server_data();
      setIsUserLoggedIn(true);
    } else {
      setIsUserLoggedIn(false);
    }
  }, [isLibraryUpdated, isUserLoggedIn]);

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

  const removeGameFromLibrary = async (libraryId) => {
    setIsLibraryUpdated(true);
    const response = await axios.delete(SERVER_URL + "/librarys/" + libraryId, {
      headers: {
        authorization: "Bearer " + getCookie("access_token"),
      },
      Accept: "application/json",
      "Content-Type": "application/json",
    });
  };

  return (
    <div>
      {isUserLoggedIn ? (
        <div className="mainContainer">
          <h1>Library</h1>
          {userLibrarysGames.map((game, ind) => (
            <div className="test" key={ind}>
              <h2>{game.data.data.title}</h2>
              <img
                style={{ blockSize: "150px" }}
                src={game.data.data.thumbnail_url}
                alt=""
              />
              {RegButton("Remove", "submit", () =>
                removeGameFromLibrary(userLibraryIds[ind])
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="mainContainer">
          <h1>Library</h1>
          <p>Please log in first.</p>
        </div>
      )}
    </div>
  );
};

export default Library;
