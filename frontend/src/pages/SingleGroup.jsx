import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { SERVER_URL } from "../utils/serverUtil";

const SingleGroup = () => {
  const { libraryId } = useParams();
  const [groupData, setGroupData] = useState("");
  const [groupCreator, setGroupCreator] = useState("");
  const [isGroupUpdated, setIsGroupUpdated] = useState(false);
  const [groupMembersId, setGroupMembersIds] = useState([]);
  const [groupMembersData, setGroupMembersData] = useState([]);

  useEffect(() => {
    setIsGroupUpdated(false);
    const server_data = async () => {
      const response = await axios(SERVER_URL + "/groups/" + libraryId, {
        Accept: "application/json",
        "Content-Type": "application/json",
      });
      setGroupData(response.data.data);
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
          Accept: "application/json",
          "Content-Type": "application/json",
        }
      );
      setGroupCreator(response.data.data);
    };
    group_creator_handler();
    group_members_id_handler();
  }, [groupData]);

  useEffect(() => {
    setIsGroupUpdated(false);
    const group_member_data_handler = async () => {
      const result = [];
      for (let i = 0; i < groupMembersId.length; i++) {
        result.push(
          (await axios(SERVER_URL + "/users/" + groupMembersId[i].user_id)).data
            .data
        );
      }
      setGroupMembersData(result);
    };
    group_member_data_handler();
  }, [groupData]);

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
    </div>
  );
};

export default SingleGroup;
