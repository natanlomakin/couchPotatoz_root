import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import useWebSocket, { ReadyState } from "react-use-websocket";
import axios from "axios";
import { SERVER_URL, WS_SERVER_URL } from "../utils/serverUtil";
import { parseJwt } from "../utils/tokenDecodeUtil";
import { getCookie } from "../utils/cookieUtil";

const SingleGroup = () => {
  const { libraryId } = useParams();
  const [groupData, setGroupData] = useState("");
  const [groupCreator, setGroupCreator] = useState("");
  const [isGroupUpdated, setIsGroupUpdated] = useState(false);
  const [groupMembersId, setGroupMembersIds] = useState([]);
  const [groupMembersData, setGroupMembersData] = useState([]);
  const [groupChatId, setGroupChatId] = useState("");
  const [lastSentMessage, setLastSentMessage] = useState([]);
  const [message, setMessage] = useState("");
  const [userId, setUserId] = useState("");
  const [groupChatHistory, setGroupChatHistory] = useState([]);
  const [userName, setUserName] = useState("");

  const { sendMessage, lastMessage, sendJsonMessage } = useWebSocket(
    WS_SERVER_URL + "/group/messages/ws/" + groupChatId
  );

  useEffect(() => {
    setUserId(parseJwt(getCookie("access_token")).sub);
    if (lastMessage !== null) {
      console.log(lastMessage);
      const parsedMessage = JSON.parse(JSON.parse(lastMessage.data));
      console.log("parsed message", parsedMessage);
      setLastSentMessage((prev) => prev.concat(parsedMessage));
      console.log(lastSentMessage);
    }
  }, [lastMessage, setLastSentMessage]);

  const handleSendMessage = () => {
    if (message.trim() !== "") {
      console.log(lastSentMessage);
      sendJsonMessage({ userName: userName, message: message });
      /* sendMessage(message, false); */
      setMessage("");
    }
  };

  const handleSendHttpMessage = async () => {
    const response = await axios.post(
      SERVER_URL + "/group/messages/",
      {
        group_id: libraryId,
        user_id: userId,
        user_name: userName,
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

  const getGroupChatHistory = async () => {
    const response = await axios(SERVER_URL + "/group/messages/" + libraryId, {
      headers: {
        authorization: "Bearer " + getCookie("access_token"),
      },
      Accept: "application/json",
      "Content-Type": "application/json",
    });
    setGroupChatHistory(response.data.data);
  };

  useEffect(() => {
    setIsGroupUpdated(false);
    const server_data = async () => {
      const response = await axios(SERVER_URL + "/groups/" + libraryId, {
        Accept: "application/json",
        "Content-Type": "application/json",
      });
      setGroupData(response.data.data);
      setGroupChatId(response.data.data.chatId);
    };
    server_data();
  }, [isGroupUpdated]);

  useEffect(() => {
    setIsGroupUpdated(false);

    const group_members_id_handler = async () => {
      const result = await axios(SERVER_URL + "/group/members/" + libraryId, {
        Accept: "application/json",
        "Content-Type": "application/json",
      });
      setGroupMembersIds(result.data.data);
    };

    const group_creator_handler = async () => {
      const response = await axios(
        SERVER_URL + "/users/" + groupData.createdBy_id,
        {
          headers: {
            authorization: "Bearer " + getCookie("access_token"),
          },
          Accept: "application/json",
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        }
      );
      setGroupCreator(response.data.data);
    };
    group_creator_handler();
    group_members_id_handler();
  }, [groupData, isGroupUpdated]);

  useEffect(() => {
    setIsGroupUpdated(false);
    const group_member_data_handler = async () => {
      const result = [];
      for (let i = 0; i < groupMembersId.length; i++) {
        result.push(
          (
            await axios(SERVER_URL + "/users/" + groupMembersId[i].user_id, {
              headers: {
                authorization: "Bearer " + getCookie("access_token"),
              },
              Accept: "application/json",
              "Content-Type": "application/json",
            })
          ).data.data
        );
      }
      setGroupMembersData(result);
      setUserName(() => {
        for (let i = 0; i < result.length; i++) {
          if (result[i].id === userId) {
            return result[i].userName;
          }
        }
      });
    };
    group_member_data_handler();
  }, [groupData, isGroupUpdated]);

  const addUserToGroup = async () => {
    const response = await axios.post(
      SERVER_URL + "/group/members/",
      {
        role: "user",
        status: "active",
        user_id: userId,
        group_id: libraryId,
      },
      {
        headers: {
          authorization: "Bearer " + getCookie("access_token"),
        },
        Accept: "application/json",
        "Content-Type": "application/json",
      }
    );
    setIsGroupUpdated(true);
  };

  const removeUserFromGroup = async () => {
    console.log(groupMembersData);
    const response = await axios.delete(
      SERVER_URL + "/group/members/" + libraryId + "/" + userId,
      {
        headers: {
          authorization: "Bearer " + getCookie("access_token"),
        },
        Accept: "application/json",
        "Content-Type": "application/json",
      }
    );
    setIsGroupUpdated(true);
  };

  return (
    <div>
      <div className="mainContainer">
        <div>
          <h1>{groupData.title}</h1>
          <h4>Created By: {groupCreator.userName}</h4>
          <p>{groupData.summery}</p>
        </div>
        <div>
          <h2>Members</h2>
          {groupMembersData.map((member, ind) => (
            <div key={ind}>
              <h3>{member.userName}</h3>
            </div>
          ))}
        </div>
      </div>
      {groupMembersData.find((member) => {
        return member.id === userId;
      }) ? (
        <div>
          <div>
            <button
              class="btn btn-danger"
              type="button"
              onClick={removeUserFromGroup}
            >
              Leave group
            </button>
          </div>
          <div>
            <button
              class="btn btn-primary"
              type="button"
              data-bs-toggle="offcanvas"
              data-bs-target="#offcanvasRight"
              aria-controls="offcanvasRight"
              /* data-bs-target="#staticBackdrop" */
              onClick={getGroupChatHistory}
            >
              Send Group Message
            </button>
          </div>
        </div>
      ) : (
        <div>
          <button
            class="btn btn-primary"
            type="button"
            data-bs-toggle="offcanvas"
            data-bs-target="#offcanvasRight"
            aria-controls="offcanvasRight"
            disabled
          >
            Send Group Message
          </button>
          <br></br>
          <span>Please enter the group to send messages.</span>
          <br></br>
          <button class="btn btn-info" type="button" onClick={addUserToGroup}>
            Enter group
          </button>
        </div>
      )}

      <div
        className="offcanvas offcanvas-end"
        tabIndex="-1"
        data-bs-backdrop="static"
        id="offcanvasRight"
        aria-labelledby="offcanvasRightLabel"
      >
        <div className="offcanvas-header">
          <h5 className="offcanvas-title" id="offcanvasRightLabel">
            {groupData.title} Chat
          </h5>
          <button
            type="button"
            className="btn-close"
            data-bs-dismiss="offcanvas"
            aria-label="Close"
          ></button>
        </div>
        <div className="offcanvas-body">
          <div className="groupChatHistory">
            {groupChatHistory &&
              groupChatHistory.map((singleGroupMessage, ind) => (
                <div key={ind} className="groupChatHistory-single">
                  {singleGroupMessage.user_name}:<br></br>
                  {singleGroupMessage.massage_content}
                </div>
              ))}
            <br></br>
            {lastSentMessage.map((singleLastSentMessage, ind) => (
              <ul key={ind}>
                <h5>{singleLastSentMessage.userName}</h5>
                <li style={{ color: "red" }}>
                  <h6>{singleLastSentMessage.message}</h6>
                </li>
              </ul>
            ))}
          </div>
          <div className="groupMessageInput">
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

export default SingleGroup;
