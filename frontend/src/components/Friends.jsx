import React, { useEffect, useState, useCallback } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";
import onClose from "react-use-websocket";
import axios from "axios";
import { SERVER_URL, WS_SERVER_URL } from "../utils/serverUtil";
import { getCookie } from "../utils/cookieUtil";
import { parseJwt } from "../utils/tokenDecodeUtil";

const Friends = () => {
  const [userFriendsList, setUserFriendsList] = useState([]);
  const [isUserLoggedIn, setIsUserLoggedIn] = useState(false);
  const [isUserFriendsUpdated, setIsUserFriendsUpdated] = useState(false);
  const [userId, setUserId] = useState("");
  const [userFriendsData, setUserFriendsData] = useState([]);
  const [messageHistory, setMessageHistory] = useState([]);
  const [message, setMessage] = useState("");
  const [targetName, setTargetName] = useState("");
  const [targetId, setTargetId] = useState("");
  const [isMessageSent, setIsMessageSent] = useState(false);
  const [lastSentMessage, setLastSentMessage] = useState([]);
  const [privateChatId, setPrivateChatId] = useState("");

  const { sendMessage, lastMessage } = useWebSocket(
    WS_SERVER_URL + "/messages/ws/" + privateChatId
  );

  useEffect(() => {
    if (lastMessage !== null) {
      setLastSentMessage((prev) => prev.concat(lastMessage));
    }
  }, [lastMessage, setLastSentMessage]);

  const handleSendMessage = () => {
    console.log("message");
    if (message.trim() !== "") {
      console.log(lastSentMessage);
      sendMessage(message, false);
      setMessage("");
    }
  };

  const handleSendHttpMessage = async () => {
    const response = await axios.post(
      SERVER_URL + "/messages/",
      {
        source_id: userId,
        target_id: targetId,
        massage_content: message,
      },
      {
        headers: {
          authorization: "Bearer " + getCookie("access_token"),
        },
        Accept: "application/json",
        "Content-Type": "application/json",
      }
    );
  };

  const handleCreatePrivateCHat = async (user2Id) => {
    const response = await axios.post(
      SERVER_URL + "/chat/private/",
      {
        user1: userId,
        user2: user2Id,
      },
      {
        headers: {
          authorization: "Bearer " + getCookie("access_token"),
        },
        Accept: "application/json",
        "Content-Type": "application/json",
      }
    );
    setPrivateChatId(response.data.data.chatId);
  };

  const handleDeletePrivateCHat = async () => {
    const response = await axios.delete(
      SERVER_URL + "/chat/private/" + userId + "/" + targetId,

      {
        headers: {
          authorization: "Bearer " + getCookie("access_token"),
        },
        Accept: "application/json",
        "Content-Type": "application/json",
      }
    );
  };

  const handleGetPrivateChatId = async (user2Id) => {
    const response = await axios(
      SERVER_URL + "/chat/private/" + userId + "/" + user2Id,
      {
        headers: {
          authorization: "Bearer " + getCookie("access_token"),
        },
        Accept: "application/json",
        "Content-Type": "application/json",
      }
    );
    if (response.data.data.chatId) {
      setPrivateChatId(response.data.data.chatId);
    } else {
      handleCreatePrivateCHat(user2Id);
    }
  };

  useEffect(() => {
    setLastSentMessage([]);
    setIsMessageSent(false);
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
  }, [isUserFriendsUpdated, isUserLoggedIn]);

  useEffect(() => {
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

  const userMessageHistory = async (source_id, target_id) => {
    const response = await axios(
      SERVER_URL + "/messages/" + source_id + "/" + target_id,
      {
        headers: {
          authorization: "Bearer " + getCookie("access_token"),
        },
        Accept: "application/json",
        "Content-Type": "application/json",
      }
    );
    setMessageHistory(response.data.data);
  };

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
            {friend.data.data.id}
            <div>
              <button
                className="btn btn-primary"
                type="button"
                data-bs-toggle="offcanvas"
                data-bs-target="#offcanvasBottom"
                aria-controls="offcanvasBottom"
                onClick={() => {
                  setTargetId("");
                  setTargetName(friend.data.data.userName);
                  setTargetId(friend.data.data.id);
                  setLastSentMessage([]);
                  userMessageHistory(userId, friend.data.data.id);
                  handleGetPrivateChatId(friend.data.data.id);
                  /* handleCreatePrivateCHat(); */
                }}
              >
                Send message
              </button>
            </div>
          </div>
        ))}
      </div>
      <div
        className="offcanvas offcanvas-bottom"
        tabindex="-1"
        id="offcanvasBottom"
        data-bs-backdrop="static"
        aria-labelledby="offcanvasBottomLabel"
      >
        <div className="offcanvas-header">
          <h5 className="offcanvas-title" id="offcanvasBottomLabel">
            {targetName}
          </h5>
          <button
            type="button"
            className="btn-close"
            data-bs-dismiss="offcanvas"
            aria-label="Close"
            onClick={() => handleDeletePrivateCHat()}
          ></button>
        </div>
        <div className="offcanvas-body small">
          <div className="messageHistory">
            {messageHistory.map((singleMessageHistory, ind) => (
              <div key={ind}>
                <ul>
                  {singleMessageHistory.source_id == userId ? (
                    <li style={{ color: "red" }}>
                      {singleMessageHistory.massage_content}
                    </li>
                  ) : (
                    <li style={{ color: "blue" }}>
                      {singleMessageHistory.massage_content}
                    </li>
                  )}
                </ul>
              </div>
            ))}
            {lastSentMessage.map((singleLastSentMessage, ind) => (
              <ul key={ind}>
                <li style={{ color: "red" }}>{singleLastSentMessage.data}</li>
              </ul>
            ))}
          </div>
          <div className="messageInput">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            ></input>
            <button
              onClick={() => {
                handleSendHttpMessage();
                handleSendMessage();
              }}
            >
              send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Friends;
