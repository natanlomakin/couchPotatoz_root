import React, { useEffect, useState } from "react";
import axios from "axios";
import { SERVER_URL } from "../utils/serverUtil";
import { getCookie } from "../utils/cookieUtil";
import { parseJwt } from "../utils/tokenDecodeUtil";

const Friends = () => {
  const [userFriendsList, setUserFriendsList] = useState([]);
  const [isUserLoggedIn, setIsUserLoggedIn] = useState(false);
  const [isUserFriendsUpdated, setIsUserFriendsUpdated] = useState(false);
  const [userId, setUserId] = useState("");
  const [userFriendsData, setUserFriendsData] = useState([]);

  useEffect(() => {
    setIsUserFriendsUpdated(false);
    const server_data = async () => {
      const response = await axios.get(SERVER_URL + "/friends/" + userId, {
        headers: {
          authorization: "Bearer " + getCookie("access_token"),
        },
        Accept: "application/json",
        "Content-Type": "application/json",
      });
      setUserFriendsList(response.data.data);
    };
    if (getCookie("access_token")) {
      setUserId(parseJwt(getCookie("access_token")).sub);
      server_data();
      setIsUserLoggedIn(true);
    } else {
      setUserFriendsList([]);
      setIsUserLoggedIn(false);
    }
  }, [userFriendsList, isUserFriendsUpdated, isUserLoggedIn]);

  useEffect(() => {
    setIsUserFriendsUpdated(false);
    const result = [];
    const userFriendsServerData = async () => {
      for (let i = 0; i < userFriendsList.length; i++) {
        result.push(
          await axios(
            SERVER_URL + "/users/friend/" + userFriendsList[i].target_id
          )
        );
      }
      setUserFriendsData(result);
    };
    userFriendsServerData();
  }, [userFriendsList]);
  return (
    <div>
      <button
        className="btn btn-primary"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#collapseExample"
        aria-expanded="false"
        aria-controls="collapseExample"
      >
        Friends
      </button>
      <div className="collapse" id="collapseExample">
        {userFriendsData.map((friend, ind) => (
          <div className="card card-body" key={ind}>
            <h4>{friend.data.data.userName}</h4>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Friends;
